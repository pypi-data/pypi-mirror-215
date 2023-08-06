import os

from jinja2 import Environment
from jinja2.ext import Extension


def create_extension(method: str):
    class PathExtension(Extension):
        def __init__(self, environment: Environment):
            super().__init__(environment)

            environment.filters[method] = getattr(os.path, method)

    return PathExtension


dirname = create_extension('dirname')
basename = create_extension('basename')
