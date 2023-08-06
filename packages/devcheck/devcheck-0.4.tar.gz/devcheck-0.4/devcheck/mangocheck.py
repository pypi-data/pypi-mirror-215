from typing import Dict
from main import Networking
import json as j
import sys


def MangoCheck(data: Dict | str | None = None):
    """
    You can either give this function a raw dictionary or a string containing the filepath (relative paths should be based on the directory that you run devcheck from)
    """

    def wrap(f):
        def wrapper(*args, **kwargs):
            # very monkey but :shrug:
            result = f(*args, **kwargs)
            if sys.argv[0] == "devcheck":
                json = {}
                if isinstance(data, Dict):
                    json["inputs"] = data
                elif isinstance(data, str):
                    with open(data) as file:
                        json["inputs"] = j.loads(file.read())
                else:
                    raise ValueError(f"{data} should not be done")
                json["lllml"] = result
                Networking.post(f"{json}")
            return result

        return wrapper

    return wrap
