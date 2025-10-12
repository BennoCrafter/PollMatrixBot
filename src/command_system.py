import importlib.util
import sys
from pathlib import Path
from typing import Optional
from src.utils.logging_config import setup_logger
from src.commands.command import Command


command_descriptions: dict[str, str] = {}

logger = setup_logger(__name__)


def register_command_from_path(
    path: Path, trigger_names: list[str]
) -> Optional[Command]:
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
            command_descriptions[name] = obj.__doc__ or "Not provided"
            command = obj(trigger_names=trigger_names)
            return command


def get_all_extensions(for_path: Path) -> list[Path]:
    """Get all extensions for a folder path"""
    paths: list[Path] = []

    for path in for_path.iterdir():
        if path.is_dir() and path.stem not in ["__pycache__"]:
            paths += get_all_extensions(path)
            continue

        if (
            path.suffix != ".py"
            or path.name.startswith("_")
            or path.stem in ["command"]
        ):
            continue

        paths.append(path)
    return paths


def load_commands(for_path: Path, config: dict) -> list[Command]:
    """Load all commands from a folder path"""
    commands: list[Command] = []

    for path in get_all_extensions(for_path):
        tn: list[str] = config["commands"].get(path.stem, [])

        c = register_command_from_path(path, tn)
        if c is not None:
            commands.append(c)
    for c in commands:
        c.load()

    return commands
