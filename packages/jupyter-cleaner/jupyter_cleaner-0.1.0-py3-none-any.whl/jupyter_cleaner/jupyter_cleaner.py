import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

import black  # type: ignore
from reorder_python_imports import _validate_replace_import  # type: ignore
from reorder_python_imports import fix_file_contents  # type: ignore
from reorder_python_imports import import_obj_from_str  # type: ignore
from reorder_python_imports import REMOVALS  # type: ignore
from reorder_python_imports import Replacements  # type: ignore
from reorder_python_imports import REPLACES  # type: ignore

if sys.version_info >= (3, 11):
    try:
        import tomllib
    except ImportError:
        # Help users on older alphas
        if not TYPE_CHECKING:
            import tomli as tomllib
else:
    import tomli as tomllib


def run(
    files: Sequence[Path],
    execution_count: int = 0,
    remove_code_output: bool = True,
    format: bool = True,
    reorder_imports: bool = True,
    black_config: Optional[Dict[str, str]] = None,
) -> None:
    """Format Jupyter lab files.

    :param Union[str, Path, Sequence[Union[str, Path]]] files: file(s) to be formatted
    :param int execution_count: sets execution count, defaults to 0
    :param bool remove_code_output: remove output from code cells, defaults to True
    :param bool format: format cells using black, defaults to True
    :param bool reorder_imports: reorder imports using reoder-python-imports, defaults to True
    :param Optional[Dict[str, str]] black_config: configuration from black formatting, defaults to None
    :raises TypeError: when file input is unrecognised
    """
    if black_config is None:
        black_config = {}

    for file in files:
        if not file.is_file() and not file.exists() and file.suffix != ".ipynb":
            continue

        with open(file) as f:
            data = json.load(f)
            python_version = data["metadata"]["language_info"]["version"]
            min_python_version = tuple(map(int, re.findall(r"(\d+)", python_version)))
            if len(min_python_version) > 2:
                min_python_version = min_python_version[:2]

            for cell in data["cells"]:
                if "execution_count" in cell.keys() and cell["cell_type"] == "code":
                    cell["execution_count"] = execution_count
                    if remove_code_output:
                        cell["outputs"] = []

                    if format:
                        try:
                            mode = black.Mode(is_ipynb=True, **black_config)  # type: ignore
                            str_cell_content = black.format_cell(
                                "".join(cell["source"]), mode=mode, fast=False
                            )
                            cell_content = [
                                f"{c}\n" for c in str_cell_content.split("\n")
                            ]
                            cell_content[-1] = cell_content[-1][
                                :-1
                            ]  # remove last newline
                            cell["source"] = cell_content
                        except black.NothingChanged:
                            pass

                    if reorder_imports:
                        to_remove = {
                            import_obj_from_str(s).key
                            for k, v in REMOVALS.items()
                            if min_python_version >= k
                            for s in v
                        }
                        replace_import: List[str] = []
                        for k, v in REPLACES.items():
                            if min_python_version >= k:
                                replace_import.extend(
                                    _validate_replace_import(replace_s)
                                    for replace_s in v
                                )
                        to_replace = Replacements.make(replace_import)
                        str_cell_content = fix_file_contents(
                            "".join(cell["source"]),
                            to_replace=to_replace,
                            to_remove=to_remove,
                        )[:-1]
                        cell_content = [f"{c}\n" for c in str_cell_content.split("\n")]
                        cell_content[-1] = cell_content[-1][:-1]
                        cell["source"] = cell_content

        with open(file, "w") as f:
            json.dump(data, f)


@lru_cache
def find_project_root(
    srcs: Sequence[str], stdin_filename: Optional[str] = None
) -> Path:
    """Modified version of black's find_project_root():

    Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.

    Returns a two-tuple with the first element as the project root path and
    the second element as a string describing the method by which the
    project root was discovered.
    """
    if stdin_filename is not None:
        srcs = tuple(stdin_filename if s == "-" else s for s in srcs)
    if not srcs:
        srcs = [str(Path.cwd().resolve())]

    path_srcs = [Path(Path.cwd(), src).resolve() for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (
            (directory / "pyproject.toml").is_file()
            or (directory / ".hg").is_dir()
            or (directory / ".git").exists()
        ):
            return directory

    return directory


def parse_pyproject() -> (
    Tuple[
        Union[List[str], str, None],
        Union[int, None],
        Union[bool, None],
        Union[bool, None],
        Union[bool, None],
    ]
):
    """Parse inputs from pyproject.toml

    :return Tuple[ Union[List[str], None], Union[int, None], Union[bool, None], Union[bool, None], Union[bool, None], ]: returns parsed pyproject information
    """
    project_root = find_project_root((str(Path.cwd().resolve()),))
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return (
            None,
            None,
            None,
            None,
            None,
        )

    with open(pyproject_path, "rb") as f:
        pyproject_toml = tomllib.load(f)

    config: Dict[str, Any] = pyproject_toml.get("tool", {}).get("jupyter_cleaner", {})

    files = config["files"] if "files" in config else None
    execution_count = config["execution_count"] if "execution_count" in config else None
    remove_code_output = (
        config["remove_code_output"] if "remove_code_output" in config else None
    )
    format = config["format"] if "format" in config else None
    reorder_imports = config["reorder_imports"] if "reorder_imports" in config else None
    return (
        files,
        execution_count,
        remove_code_output,
        format,
        reorder_imports,
    )


def parse_args():
    parser = argparse.ArgumentParser(description="jupyter_cleaner")
    parser.add_argument(
        "files_or_dir",
        type=str,
        nargs="*",
        help="Jupyter lab files to format or directories to search for lab files",
    )
    parser.add_argument(
        "--execution_count",
        type=int,
        default=0,
        help="Number to set for the execution count of every cell",
    )
    parser.add_argument(
        "--remove_code_output",
        action="store_false",
        help="Number to set for the execution count of every cell",
    )
    parser.add_argument(
        "--format",
        action="store_false",
        help="Format code of every cell (uses black)",
    )
    parser.add_argument(
        "--reorder_imports",
        action="store_false",
        help="Reorder imports of every cell (uses reorder-python-imports)",
    )
    args = parser.parse_args()
    return (
        args.files_or_dir,
        args.execution_count,
        args.remove_code_output,
        args.format,
        args.reorder_imports,
    )


def get_lab_files(files_or_dirs: List[Path]) -> List[Path]:
    files = []
    for file_or_dir in files_or_dirs:
        if file_or_dir.is_dir():
            files.extend([p for p in file_or_dir.rglob("*") if p.suffix == ".ipynb"])
        elif file_or_dir.is_file() and file_or_dir.suffix == ".ipynb":
            files.append(file_or_dir)
        else:
            raise ValueError("Files or directories do not exist or could not be found")
    return files


def process_inputs(
    args_files_or_dirs: List[str],
    args_execution_count: int,
    args_remove_code_output: bool,
    args_format: bool,
    args_reorder_imports: bool,
    project_files_or_dirs: Union[List[str], str, None],
    project_execution_count: Union[int, None],
    project_remove_code_output: Union[bool, None],
    project_format: Union[bool, None],
    project_reorder_imports: Union[bool, None],
) -> Tuple[List[Path], int, bool, bool, bool]:
    """Creates inputs of the right format and prioritises pyproject inputs over argparse inputs, outside of files and directories where all inputs are combined.

    :param List[str] args_files_or_dirs: files or directories from argparse
    :param int args_execution_count: execution count from argparse
    :param bool args_remove_code_output: remove code output from argparse
    :param bool args_format: apply formatting from argparse
    :param bool args_reorder_imports: reorder imports from argparse
    :param Union[List[str], str, None] project_files_or_dirs: files or directories from pyproject
    :param Union[int, None] project_execution_count: execution count from pyproject
    :param Union[bool, None] project_remove_code_output: remove code output from pyproject
    :param Union[bool, None] project_format: apply formatting from pyproject
    :param Union[bool, None] project_reorder_imports: reorder imports from pyproject
    :return Tuple[ Union[List[str], str, None], Union[int, None], Union[bool, None], Union[bool, None], Union[bool, None], ]: inputs to run()
    """
    if args_files_or_dirs is None:
        args_files_or_dirs = [Path.cwd().resolve()]
    if project_files_or_dirs is None:
        project_files_or_dirs = []
    elif isinstance(project_files_or_dirs, str):
        project_files_or_dirs = [project_files_or_dirs]
    files_or_dirs = [Path(f) for f in project_files_or_dirs + args_files_or_dirs]
    execution_count = (
        project_execution_count
        if project_execution_count is not None
        else args_execution_count
    )
    remove_code_output = (
        project_remove_code_output
        if project_remove_code_output is not None
        else args_remove_code_output
    )
    format = project_format if project_format is not None else args_format
    reorder_imports = (
        project_reorder_imports
        if project_reorder_imports is not None
        else args_reorder_imports
    )

    return (
        files_or_dirs,
        execution_count,
        remove_code_output,
        format,
        reorder_imports,
    )


def main():
    (
        args_files_or_dirs,
        args_execution_count,
        args_remove_code_output,
        args_format,
        args_reorder_imports,
    ) = parse_args()

    (
        project_files_or_dirs,
        project_execution_count,
        project_remove_code_output,
        project_format,
        project_reorder_imports,
    ) = parse_pyproject()

    (
        files_or_dirs,
        execution_count,
        remove_code_output,
        format,
        reorder_imports,
    ) = process_inputs(
        args_files_or_dirs,
        args_execution_count,
        args_remove_code_output,
        args_format,
        args_reorder_imports,
        project_files_or_dirs,
        project_execution_count,
        project_remove_code_output,
        project_format,
        project_reorder_imports,
    )

    files = get_lab_files(files_or_dirs)

    run(
        files,
        execution_count,
        remove_code_output,
        format,
        reorder_imports,
    )
