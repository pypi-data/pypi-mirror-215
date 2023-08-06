# main.py
import os
import logging as log
import typing
import uuid

import httpx
import json
import argparse
from typing import Dict, List, Tuple, Any
from tqdm import tqdm
from colorama import Fore, Style
from datetime import datetime
from dotenv import load_dotenv, set_key
from fnmatch import fnmatch
from pathlib import Path

import ast
import importlib.util
from lllml import LLLML

# Load environment variables
load_dotenv()

# Set up log
log.basicConfig(level=log.DEBUG)

# Set API Endpoint
# API_ENDPOINT = "http://api.MangoCheck.ai/prompt"
API_URL = "http://localhost:8080"
API_POST_PROMPTS = f"{API_URL}/api/post/prompts"
API_GET_PROMPTS = f"{API_URL}/api/get/prompts"
API_GET_TESTS = f"{API_URL}/api/get/tests"

# Load API key from environment variable
MANGOCHECK_API_KEY = os.getenv("MANGOCHECK_API_KEY")
# TODO: Delete this
MANGOCHECK_API_KEY = "920dbc4b071dd0c9bcf30027ec0cd86a6188332df17b36b1c6189d9c33115c24"
REQUEST_HEADERS = {"X-API-Key": f"{MANGOCHECK_API_KEY}"}
CACHE = Path(".mangocheck-cache")
RESULTS_HISTORY = CACHE / Path("results")


class Networking:
    @staticmethod
    def post(data: str, url: str = API_POST_PROMPTS) -> typing.Any:
        try:
            response = httpx.post(url, json=data, headers=REQUEST_HEADERS)
            if 300 > response.status_code >= 200:
                log.info("Data sent to API successfully.")
                return response.json()
            else:
                log.error(
                    f"There may have been errors sending data to the API: {response}"
                )
        except Exception as e:
            log.error(f"Exception occurred: {e}")

    @staticmethod
    def get(url: str) -> Any:
        try:
            response = httpx.get(url, headers=REQUEST_HEADERS)
            if 300 > response.status_code >= 200:
                log.info("Data sent to API successfully.")
            else:
                log.error(
                    f"There may have been errors sending data to the API: {response}"
                )
            return response.json()
        except Exception as e:
            log.error(f"Exception occurred: {e}")


class Print:
    @staticmethod
    def colored_result(data: Dict) -> None:
        if not dict:
            return
        test_result = data["LLM_Test_Result"]
        print(f"{Fore.YELLOW}Status: {test_result['status']}")
        print(
            f"Time Completed: {datetime.fromisoformat(test_result['time_completed'].replace('Z', '+00:00'))}"
        )
        for result in test_result["results"]:
            color = Fore.GREEN if result["status"] == "PASS" else Fore.RED
            print(
                f"{color}Test Name: {result['name']}\nStatus: {result['status']}\nScore: {result['score']}"
            )
            if "reason" in result:
                print(f"Reason: {result['reason']}")
        print(Style.RESET_ALL)

        file_location = "/tmp/mangotest/" + str(uuid.uuid4())
        print(f"Writing results to: {file_location}")
        with open(file_location, "w") as file:
            file.write(test_result)


class FileFinder:
    @staticmethod
    def getignored(dir: str) -> List[str]:
        ignored = []
        try:
            with open(os.path.join(dir, ".gitignore"), "r") as f:
                for line in f:
                    pattern = line.strip()
                    if pattern and not pattern.startswith("#"):
                        ignored.append(pattern)
        except:
            pass
        return ignored

    @staticmethod
    def findpy(dir: str):
        log.info("Trying to find python files. This might take a while")
        files = []
        ignored_patterns = FileFinder.getignored(dir)
        for root, _, filenames in os.walk(dir):
            for filename in filenames:
                path = os.path.join(root, filename)
                if not any(fnmatch(path, pattern) for pattern in ignored_patterns):
                    if path.endswith(".py"):  # Only consider Python files for parsing
                        files.append(path)
        return files

    @staticmethod
    def find_decorated(files: List[str], decoration: str) -> List[Tuple[str, str]]:
        functions = []

        for file in files:
            try:
                with open(file, "r") as f:
                    code = f.read()
            except:
                log.error(f"Some error occurred processing file {file}. Skipping")
                continue

            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        # For some reason, this is how AST handles custom functions
                        if hasattr(decorator, "id") and decorator.id == "staticmethod":
                            continue
                        if (
                            hasattr(decorator, "func")
                            and decorator.func.id == decoration
                        ):
                            functions.append((node.name, file))

        return functions


class MangoCheck:
    @staticmethod
    def authenticate():
        api_key = input("Please enter your API Key from mangocheck.ai: ")
        set_key(".env", "MANGOCHECK_API_KEY", api_key)
        print("API Key saved successfully.")

    @staticmethod
    def run_tests() -> None:
        root_folder = os.path.dirname(os.path.abspath(__file__))
        files = FileFinder.findpy(root_folder)
        functions = FileFinder.find_decorated(files, "MangoCheck")

        for func, file in functions:
            module_name = os.path.splitext(os.path.basename(file))[0]
            spec = importlib.util.spec_from_file_location(module_name, file)
            if not spec:
                log.error(f"Could not spec module {module_name}")
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, func):
                function = getattr(module, func)
                lllml = LLLML(function=function)
                lllml.add_metadata(filename=file)
                response = Networking.post(data=f"{lllml}")
                print(response)
                # Print.colored_result(response)
            else:
                log.fatal(f"Error on our end: {module} doesn't have {func}")
                exit(1)

    @staticmethod
    def view_last():
        """
        Checks .mangocheck-cache for the UUID of user's last run test; queries the database
        """
        if CACHE.exists() and CACHE.is_file():
            log.fatal(".mangocheck-cache is a file; it should be a directory")
            return
        if not CACHE.exists():
            CACHE.mkdir()
        if not RESULTS_HISTORY.exists():
            RESULTS_HISTORY.touch()

        with RESULTS_HISTORY.open() as f:
            data = json.load(f)
            for result in data:
                # TODO: Make this prettier
                print(result)

    @staticmethod
    def list_tests():
        """
        Lists the currently available tests for this API Key
        """
        tests = Networking.get(API_GET_TESTS)
        print(tests)

    @staticmethod
    def list_prompts():
        """
        Lists the given prompts that were run for this API key
        """
        result = Networking.get(API_GET_PROMPTS)
        print(result)


def main():
    parser = argparse.ArgumentParser(
        prog="mangocheck", description="MangoCheck Command Line Interface"
    )
    parser.add_argument(
        "command",
        help="Command to run",
        choices=[
            "run_tests",
            "authenticate",
            "list_tests",
            "list_prompts",
            "view_last",
        ],
    )

    args = parser.parse_args()

    if args.command == "run_tests":
        if not MANGOCHECK_API_KEY:
            log.error(
                "API Key not found. Please authenticate using 'mangocheck authenticate'"
            )
            exit(1)
        MangoCheck.run_tests()
    elif args.command == "authenticate":
        MangoCheck.authenticate()
    elif args.command == "list_prompts":
        MangoCheck.list_prompts()
    elif args.command == "list_tests":
        MangoCheck.list_tests()
    elif args.command == "view_last":
        MangoCheck.view_last()


if __name__ == "__main__":
    main()
