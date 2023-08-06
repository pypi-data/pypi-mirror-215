import os
import typing
import inspect

from jinja2 import Environment
from jinja2.ext import Extension


class PathExtension(Extension):
    filters: typing.List[str] = ["dirname", "basename", "abspath", "join", "exists", "split", "splitext",
                                 "isabs", "islink", "isfile", "isdir"]

    def __init__(self, environment: Environment):
        super().__init__(environment)

        for name, func in inspect.getmembers(os.path, inspect.isfunction):
            environment.filters[name] = func
