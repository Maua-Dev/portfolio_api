import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIRECTORY = PROJECT_ROOT / "iac" / "build"
PYTHON_TOP_LEVEL_DIR = BUILD_DIRECTORY / "python"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements-app.txt"
SHARED_CODE_SOURCE = PROJECT_ROOT / "src" / "shared"


def adjust_layer_directory():
    """Empacota a Layer para Lambda Python 3.13/Linux/x86_64."""
    if BUILD_DIRECTORY.exists():
        shutil.rmtree(BUILD_DIRECTORY)

    shared_parent = PYTHON_TOP_LEVEL_DIR / "src"
    shared_parent.mkdir(parents=True)

    # Pacote explícito para permitir imports de src.shared na Lambda.
    shutil.copy2(PROJECT_ROOT / "src" / "__init__.py", shared_parent)
    shutil.copytree(
        SHARED_CODE_SOURCE,
        shared_parent / "shared",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "-r", str(REQUIREMENTS_FILE),
        "--target", str(PYTHON_TOP_LEVEL_DIR),
        "--platform", "manylinux2014_x86_64",
        "--implementation", "cp",
        "--python-version", "3.13",
        "--abi", "cp313",
        "--only-binary=:all:",
        "--no-compile",
        "--upgrade",
    ])


if __name__ == "__main__":
    adjust_layer_directory()