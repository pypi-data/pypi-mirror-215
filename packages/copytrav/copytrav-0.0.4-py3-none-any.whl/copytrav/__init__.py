"""Copytrav provides the ability to create copies of python package data on disk."""
import importlib.resources
from importlib.resources.abc import Traversable
import os
from pathlib import Path
import tempfile
from typing import Union

def copy(module: str, pth: Path=None, dst: Path=None) -> Path:
    """Given a module in the form: 'module.sub_module', copy all items at the
    pth to the destination, dst. If no path given, the module from the root
    level is copied.

    Args:
        module: The path to (typically) the namespace module containing data
            in the example form "mymodule.data".
        dst: Where you want the items copied to. Top-level dir is copied. If no
            dst is given, a temporary directory will be created.
        pth: Path in the example form
            "item_at_module_root/level/directory_or_file".

    Returns:
        The path to the directory to which items were copied. If dst is given,
        this will simply be dst.
    """
    def copy_aux(current_level: Traversable, current_path: Path):
        new_path = os.path.join(current_path, current_level.name)
        if current_level.is_dir():
            os.mkdir(new_path)
            for item in current_level.iterdir():
                copy_aux(item, new_path)
        else:
            with open(new_path, "wb") as new_file:
                new_file.write(current_level.read_bytes())
    start = importlib.resources.files(module)
    if pth:
        for_split = pth.split(os.path.sep)
        for level in for_split:
            start = start.joinpath(level)
    if not dst:
        dst = tempfile.mkdtemp(prefix=module.replace(".", "_"))
    copy_aux(start, dst)

    return dst
