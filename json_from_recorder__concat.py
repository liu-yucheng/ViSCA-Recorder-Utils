"""
Concatenates a sequence of JSON (from ViSCA Recorder) files.
Concatenates JSONs in ascending alphanumerical order.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import json as _json
import pandas as _pandas
import varname as _varname
import _utils__date_time


_os_path = _os.path
_nameof = _varname.core.nameof
_basename = _os_path.basename(__file__)
_parser = None
_args = None
_file_names__jsons_input = None
_record_concat = None
_record_concat_flattened = None

name_no_ext: str
"""The name of this file without extension."""
name_no_ext, _ = _os_path.splitext(_basename)
folder_name__data: str = None
"""The folder name of script data."""
file_name__json_output: str = None
"""The file name of output JSON."""
file_name__json_output_flattened: str = None
"""The file name of output flattened JSON."""
args__overridden: bool = False
"""Whether the arguments are overridden."""
folder_name__jsons_input: str = None
"""The folder name of the ViSCA Recorder JSON file sequence."""


def _context__create():
    global folder_name__data
    global file_name__json_output
    global file_name__json_output_flattened

    if folder_name__data is None:
        folder_name__data = _os_path.dirname(__file__)
        folder_name__data = _os_path.join(folder_name__data, f".{name_no_ext}__data")
    # end if

    _os.makedirs(folder_name__data, exist_ok=True)
    timestamp = _utils__date_time.date_time_str_custom__find_for_now()

    if file_name__json_output is None:
        file_name__json_output = _os_path.join(folder_name__data, f"output__{timestamp}.json")
    # end if

    if file_name__json_output_flattened is None:
        file_name__json_output_flattened = _os_path.join(folder_name__data, f"output_flattened__{timestamp}.json")
    # end if
# end def

def _args__parse():
    global _parser
    global _args
    global folder_name__jsons_input

    _parser = _ArgumentParser(
        prog=_basename,
        usage=f"python {_basename} [--help] <{_nameof(folder_name__jsons_input)}>",
        description=\
            "Concatenates a sequence of JSON (from ViSCA Recorder) files."
            + " Concatenates JSONs in ascending alphanumerical order."
        ,
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.",
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(folder_name__jsons_input)}",
        type=str,
        help="The folder name of the ViSCA Recorder JSON file sequence.",
        metavar=f"{_nameof(folder_name__jsons_input)}"
    )
    # end statement

    if not args__overridden:
        _args = _parser.parse_args()

        if folder_name__jsons_input is None:
            folder_name__jsons_input = getattr(_args, _nameof(folder_name__jsons_input))
        # end if

        folder_name__jsons_input = _os_path.abspath(folder_name__jsons_input)
    # end if
# end def

def _jsons__probe():
    global _file_names__jsons_input

    isdir__jsons_input = _os_path.isdir(folder_name__jsons_input)
    _file_names__jsons_input = []

    if isdir__jsons_input:
        _file_names__jsons_input = _os.listdir(folder_name__jsons_input)
        _file_names__jsons_input.sort()
    # end if

    for index, file_name in enumerate(_file_names__jsons_input):
        _file_names__jsons_input[index] = _os_path.join(folder_name__jsons_input, file_name)
    # end for

    new_file_names__jsons_input = []

    for file_name in _file_names__jsons_input:
        isfile = _os_path.isfile(file_name)
        basename = _os_path.basename(file_name)
        _, ext = _os_path.splitext(basename)
        ext__matched = ext.lower() == ".json"

        if isfile and ext__matched:
            new_file_names__jsons_input.append(file_name)
        # end if
    # end for

    _file_names__jsons_input = new_file_names__jsons_input
# end def


def _jsons__concat():
    global _record_concat

    print(f"begin {_nameof(_jsons__concat)}")

    _record_concat = {
        "visca_recorder_utils": {
            "files_concat": [],
            "json_flatten_enabled": False
        },
        "items": [],
    }
    # end statement

    for index, file_name in enumerate(_file_names__jsons_input):
        basename__json_input = _os_path.basename(file_name)
        print(f"begin Concatenating {index + 1} / {len(_file_names__jsons_input)} {basename__json_input}")
        record = {}

        with open(file_name, "r", encoding="utf-8") as file__json_input:
            record = _json.load(file__json_input)
            record = dict(record)
        # end with

        if "items" in record:
            items = record["items"]
            items = list(items)
            _record_concat["items"] += items
        # end if

        _record_concat["visca_recorder_utils"]["files_concat"].append(basename__json_input)
        print(f"end Concatenating {index + 1} / {len(_file_names__jsons_input)} {basename__json_input}")
    # end for

    print(f"{len(_record_concat["items"]) = }")

    with open(file_name__json_output, "w", encoding="utf-8") as file__json_output:
        _json.dump(_record_concat, file__json_output, indent=4)
    # end with

    print(f"end {_nameof(_jsons__concat)}")
# end def

def _jsons_flattened__concat():
    global _record_concat_flattened
    print(f"begin {_nameof(_jsons_flattened__concat)}")

    _record_concat_flattened = {
        "visca_recorder_utils": dict(_record_concat["visca_recorder_utils"]),
        "items_flattened": [],
    }
    # end statement

    _record_concat_flattened["visca_recorder_utils"]["json_flatten_enabled"]= True
    items = _record_concat["items"]
    items_dataframe = _pandas.json_normalize(items, sep=".")
    items_flattened = items_dataframe.to_dict(orient="records")
    _record_concat_flattened["items_flattened"] = items_flattened
    print(f"{len(_record_concat_flattened["items_flattened"]) = }")

    with open(file_name__json_output_flattened, "w", encoding="utf-8") as file__json_output_flattened:
        _json.dump(_record_concat_flattened, file__json_output_flattened, indent=4)
    # end with

    print(f"end {_nameof(_jsons_flattened__concat)}")
# end def

def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_basename}")
    _context__create()
    _args__parse()
    _jsons__probe()
    _jsons__concat()
    _jsons_flattened__concat()

    print(
        f"{folder_name__jsons_input = :s}\n"
            + f"{file_name__json_output = :s}\n"
            + f"{file_name__json_output_flattened = :s}"
        ,
    )
    # end statement

    print(f"end {_basename}")
# end def


if __name__ == "__main__":
    main()
# end if
