import argparse
from . import utils as utils
from .core import command as command
from .core.config import Config as Config
from .core.context import Context as Context, GroupResolver as GroupResolver
from .core.plugin import Plugin as Plugin, search_plugins as search_plugins
from _typeshed import Incomplete
from pathlib import Path
from typing import Mapping, Optional, Sequence, Tuple

parser: Incomplete
group: Incomplete
PROMPT: str

class PidFileType(argparse.FileType):
    def __call__(self, string): ...

context: Incomplete

def main(*config_files: str, args: Optional[argparse.Namespace] = ..., config_dirs: Sequence[Path] = ..., commands: Tuple[str, ...] = ..., config_dict: Optional[Mapping] = ...): ...
def process_iter(cfg, cpus=...): ...
def create_process(cfg): ...
def loop_run(conf: Incomplete | None = ..., future: Incomplete | None = ..., group_resolver: Incomplete | None = ..., ns: Incomplete | None = ..., cmds: Incomplete | None = ..., argv: Incomplete | None = ..., loop: Incomplete | None = ..., prompt: Incomplete | None = ..., process_name: Incomplete | None = ...): ...

class UriType(argparse.FileType):
    def __call__(self, string): ...

class ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string: Incomplete | None = ...) -> None: ...

class plugin(Plugin):
    def add_arguments(self, parser) -> None: ...

def main_with_conf(*args, **kwargs) -> None: ...
