import yaml
from pathlib import Path

default_config_path = Path("assets/default_config.yaml")


def load_config(config_path: Path):
    if not config_path.exists():
        # create config based on default config path
        default_config_content = read_file(default_config_path)
        with open(config_path, "w") as f:
            f.write(default_config_content)

    return read_yaml_file(config_path)


def read_file(file_path: Path) -> str:
    if not file_path.exists():
        return ""

    with open(file_path, "r") as f:
        file_data = f.read()
    return file_data


def read_yaml_file(file_path: Path) -> dict:
    if not file_path.exists():
        return {}

    with open(file_path, "r") as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data
