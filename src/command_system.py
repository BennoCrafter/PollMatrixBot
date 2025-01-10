import importlib.util
import sys
from pathlib import Path
from typing import Optional
from src.utils.logging_config import setup_logger
from src.commands.command import Command


logger = setup_logger(__name__)

def register_command_from_path(path: Path, trigger_names: list[str]) -> Optional[Command]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None:
        logger.error(f"Could not import {path}")
        return

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module

    if spec.loader is None:
        logger.error(f"Could not load loader for {path}")
        return

    spec.loader.exec_module(module)

    for name, obj in module.__dict__.items():
        if not isinstance(obj, type):
            continue

        if issubclass(obj, Command) and obj.__bases__[0] == Command:
            logger.info(f"Registered command {name}")
            command = obj(trigger_names=trigger_names)
            return command
