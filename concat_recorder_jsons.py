"""
Concatenate recorder JSONs.
Converts a sequence of ViSCA Recorder JSON files to a JSON file by concatenating them.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import json as _json
import _datetime_utils


_os_path = _os.path
_script_basename = _os_path.basename(__file__)
_parser = None
_arguments = None
_json_in_file_names = None

data_folder_name = None
json_out_file_name = None
arguments_overridden = False
jsons_in_folder_name = None


def _create_context():
    global data_folder_name
    global json_out_file_name

    script_no_ext, _ = _os_path.splitext(_script_basename)

    if data_folder_name is None:
        data_folder_name = _os_path.dirname(__file__)
        data_folder_name = _os_path.join(data_folder_name, f".{script_no_ext}_data")

    _os.makedirs(data_folder_name, exist_ok=True)
    timestamp = _datetime_utils.find_now_custom_date_time_string()

    if json_out_file_name is None:
        json_out_file_name = _os_path.join(data_folder_name, f"output-{timestamp}.json")


def _parse_arguments():
    global _parser
    global _arguments
    global jsons_in_folder_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} [--help] <jsons-in-folder-name>",
        description="Converts a sequence of ViSCA Recorder JSON files to a JSON file by concatenating them.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _parser.add_argument(
        "jsons_in_folder_name",
        type=str,
        help="The folder name of the ViSCA Recorder JSON file sequence.",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if jsons_in_folder_name is None:
            jsons_in_folder_name = _arguments.jsons_in_folder_name

        jsons_in_folder_name = _os_path.abspath(jsons_in_folder_name)


def _probe_json_files():
    global _json_in_file_names

    jsons_isdir = _os_path.isdir(jsons_in_folder_name)
    _json_in_file_names = []

    if jsons_isdir:
        _json_in_file_names = _os.listdir(jsons_in_folder_name)
        _json_in_file_names.sort()

    for index, file_name in enumerate(_json_in_file_names):
        _json_in_file_names[index] = _os_path.join(jsons_in_folder_name, file_name)

    new_json_file_names = []

    for file_name in _json_in_file_names:
        json_isfile = _os_path.isfile(file_name)
        json_basename = _os_path.basename(file_name)
        _, json_ext = _os_path.splitext(json_basename)
        json_ext_matched = json_ext.lower() == ".json"

        if json_isfile and json_ext_matched:
            new_json_file_names.append(file_name)
        # end if
    # end if

    _json_in_file_names = new_json_file_names


def _concat_jsons():
    print("begin Concatenating JSONs")

    concat_record = {
        "items": [],
        "concatenated_files": []
    }

    for index, file_name in enumerate(_json_in_file_names):
        json_in_basename = _os_path.basename(file_name)
        print(f"begin Concatenating {index + 1} / {len(_json_in_file_names)} {json_in_basename}")
        record = {}

        with open(file_name, "r", encoding="utf-8") as json_in_file:
            record = _json.load(json_in_file)
            record = dict(record)

        if "items" in record:
            record_items = record["items"]
            record_items = list(record_items)
            concat_record["items"] += record_items

        concat_record["concatenated_files"].append(json_in_basename)
        print(f"end Concatenating {index + 1} / {len(_json_in_file_names)} {json_in_basename}")

    with open(json_out_file_name, "w", encoding="utf-8") as json_out_file:
        _json.dump(concat_record, json_out_file, indent=4)

    print("end Concatenating JSONs")


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_script_basename}")
    _create_context()
    _parse_arguments()
    _probe_json_files()
    _concat_jsons()

    print(
        f"{jsons_in_folder_name = :s}\n"
        + f"{json_out_file_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
