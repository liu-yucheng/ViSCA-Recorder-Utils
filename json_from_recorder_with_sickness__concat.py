"""
Concatenates a sequence of JSON (from ViSCA Recorder) files (includes items with sickness only).
Concatenates JSONs in ascending alphanumerical order.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import sys as _sys
import json as _json
import numpy as _numpy
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
time_s__before_sickness = None
time_s__after_sickness = None
sickness_threshold = None
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
    global time_s__before_sickness
    global time_s__after_sickness
    global sickness_threshold
    global folder_name__data
    global file_name__json_output
    global file_name__json_output_flattened

    if time_s__before_sickness is None:
        time_s__before_sickness = 0.5
    # end if

    if time_s__after_sickness is None:
        time_s__after_sickness = 0.5
    # end if

    if sickness_threshold is None:
        sickness_threshold = 0.75
    # end if

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
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
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
    # end if

    _file_names__jsons_input = new_file_names__jsons_input
# end def

def _jsons__concat():
    global _record_concat
    print(f"begin {_nameof(_jsons__concat)}")

    _record_concat = {
        "visca_recorder_utils": {
            "files_concat": [],
            "json_flatten_enabled": False,
            "filter_with_sickness": {
                "time_s__before_sickness": time_s__before_sickness,
                "time_s__after_sickness": time_s__after_sickness,
                "sickness_threshold": sickness_threshold,
            },
            "sickness_stats": {
                "time_s__on_sickness": 0.0,
                "time_s__total": 0.0,
                "proportion_on_sickness": 0.0,
            },
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

    print("begin With-sickness filtering")
    print("begin Finding on-sickness indexes")
    items = list(_record_concat["items"])
    indexes_on_sickness = []
    indexes_on_sickness__dict = {}
    time_s__on_sickness = 0.0
    time_s__total = 0.0
    time_s__prev = 0.0
    time_s__curr = 0.0

    for index, item in enumerate(items):
        if "sickness" in item and "reported" in item["sickness"]:
            sickness = float(item["sickness"]["reported"])
        else:
            sickness = float(0)
        # end if

        if "timestamp" in item and "game_time_seconds" in item["timestamp"]:
            time_s__curr = float(item["timestamp"]["game_time_seconds"])
        else:
            time_s__curr = time_s__prev
        # end if

        time_s__between = time_s__curr - time_s__prev
        time_s__between = _numpy.clip(time_s__between, 0.0, 3.0)

        if sickness >= sickness_threshold:
            indexes_on_sickness__dict[index] = None
            time_s__on_sickness += time_s__between
        # end if

        time_s__total += time_s__between
        time_s__prev = time_s__curr
    # end for

    proportion_on_sickness = time_s__on_sickness / time_s__total
    _record_concat["visca_recorder_utils"]["sickness_stats"]["time_s__on_sickness"] = time_s__on_sickness
    _record_concat["visca_recorder_utils"]["sickness_stats"]["time_s__total"] = time_s__total
    _record_concat["visca_recorder_utils"]["sickness_stats"]["proportion_on_sickness"] = proportion_on_sickness
    indexes_on_sickness = list(indexes_on_sickness__dict.keys())
    indexes_on_sickness.sort()
    print("end Finding on-sickness indexes")
    print("begin Finding before-sickness indexes")
    indexes_before_sickness__dict = {}

    for index in indexes_on_sickness:
        item = items[index]
        time_ = _sys.float_info.max

        if "timestamp" in item and "game_time_seconds" in item["timestamp"]:
            time_ = float(item["timestamp"]["game_time_seconds"])
        # end if

        index__trace = index
        time__trace = time_

        while time_ - time__trace < time_s__before_sickness and index__trace >= 0:
            item_trace = items[index__trace]
            time__trace = _sys.float_info.min

            if "timestamp" in item_trace and "game_time_seconds" in item_trace["timestamp"]:
                time__trace = float(item_trace["timestamp"]["game_time_seconds"])
            # end if

            if index__trace not in indexes_before_sickness__dict:
                indexes_before_sickness__dict[index__trace] = None
            # end if

            index__trace -= 1
        # end while
    # end for

    print("end Finding before-sickness indexes")
    print("begin Finding after-sickness indexes")
    indexes_after_sickness__dict = {}

    for index in indexes_on_sickness:
        item = items[index]
        time_ = _sys.float_info.min

        if "timestamp" in item and "game_time_seconds" in item["timestamp"]:
            time_ = float(item["timestamp"]["game_time_seconds"])
        # end if

        index__trace = index
        time__trace = time_

        while time__trace - time_ < time_s__after_sickness and index__trace < len(items):
            item_trace = items[index__trace]
            time__trace = _sys.float_info.max

            if "timestamp" in item_trace and "game_time_seconds" in item_trace["timestamp"]:
                time__trace = float(item_trace["timestamp"]["game_time_seconds"])
            # end if

            if index__trace not in indexes_after_sickness__dict:
                indexes_after_sickness__dict[index__trace] = None
            # end if

            index__trace += 1
        # end while
    # end for

    print("end Finding after-sickness indexes")
    print("begin Composing with-sickness indexes")
    indexes_with_sickness__dict = {}

    for key, item in indexes_on_sickness__dict.items():
        indexes_with_sickness__dict[key] = item
    # end for

    for key, item in indexes_before_sickness__dict.items():
        indexes_with_sickness__dict[key] = item
    # end for

    for key, item in indexes_after_sickness__dict.items():
        indexes_with_sickness__dict[key] = item
    # end for

    items_with_sickness = []

    for index, item in enumerate(items):
        if index in indexes_with_sickness__dict:
            items_with_sickness.append(item)
        # end if
    # end for

    _record_concat["items"] = items_with_sickness
    print("end With-sickness filtering")
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

    _record_concat_flattened["visca_recorder_utils"]["json__flattening_enabled"]= True
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
        f"{time_s__before_sickness = }\n"
            + f"{time_s__after_sickness = }\n"
            + f"{folder_name__jsons_input = :s}\n"
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
