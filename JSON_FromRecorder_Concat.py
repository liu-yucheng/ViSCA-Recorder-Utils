"""
Concatenates a sequence of JSON (from ViSCA Recorder) files.
Concatenates JSONs in ascending alphanumerical order.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import json as _json
import _Utils_DateTime


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None
_JSON_Input_Names = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Folder_Data_Name = None
JSON_Output_Name = None
Arguments_Overridden = False
Folder_JSONs_Input_Name = None


def _Context_Create():
    global Folder_Data_Name
    global JSON_Output_Name

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name = \
            _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if JSON_Output_Name is None:
        JSON_Output_Name = \
            _os_path.join(Folder_Data_Name, f"Output_{timestamp}.json")
        # end statement


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Folder_JSONs_Input_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage=
            f"python {_Script_basename} [--help]"
            + f" <{_nameof(Folder_JSONs_Input_Name)}>",

        description=\
            "Concatenates a sequence of JSON (from ViSCA Recorder) files."
            + " Concatenates JSONs in ascending alphanumerical order.",

        epilog=\
            "Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Folder_JSONs_Input_Name)}",
        type=str,
        help="The folder name of the ViSCA Recorder JSON file sequence.",
        metavar=f"{_nameof(Folder_JSONs_Input_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Folder_JSONs_Input_Name is None:
            Folder_JSONs_Input_Name = _Arguments.Folder_JSONs_Input_Name

        Folder_JSONs_Input_Name = _os_path.abspath(Folder_JSONs_Input_Name)


def _JSONs_Probe():
    global _JSON_Input_Names

    JSONs_isdir = _os_path.isdir(Folder_JSONs_Input_Name)
    _JSON_Input_Names = []

    if JSONs_isdir:
        _JSON_Input_Names = _os.listdir(Folder_JSONs_Input_Name)
        _JSON_Input_Names.sort()

    for Index, File_Name in enumerate(_JSON_Input_Names):
        _JSON_Input_Names[Index] = \
            _os_path.join(Folder_JSONs_Input_Name, File_Name)
        # end statement

    JSON_Names_New = []

    for File_Name in _JSON_Input_Names:
        JSON_isfile = _os_path.isfile(File_Name)
        JSON_basename = _os_path.basename(File_Name)
        _, JSON_Ext = _os_path.splitext(JSON_basename)
        JSON_Ext_Matched = JSON_Ext.lower() == ".json"

        if JSON_isfile and JSON_Ext_Matched:
            JSON_Names_New.append(File_Name)
        # end if
    # end if

    _JSON_Input_Names = JSON_Names_New


def _JSONs_Concat():
    print("begin _JSONs_Concat")

    Record_Concat = {
        "items": [],
        "concatenated_files": []
    }

    for Index, File_Name in enumerate(_JSON_Input_Names):
        JSON_Input_basename = _os_path.basename(File_Name)

        print(
            f"begin Concatenating {Index + 1} / {len(_JSON_Input_Names)}"
            + f" {JSON_Input_basename}"
        )

        Record = {}

        with open(File_Name, "r", encoding="utf-8") as JSON_Input:
            Record = _json.load(JSON_Input)
            Record = dict(Record)

        if "items" in Record:
            Record_Items = Record["items"]
            Record_Items = list(Record_Items)
            Record_Concat["items"] += Record_Items

        Record_Concat["concatenated_files"].append(JSON_Input_basename)

        print(
            f"end Concatenating {Index + 1} / {len(_JSON_Input_Names)}"
            + f" {JSON_Input_basename}"
        )

    with open(JSON_Output_Name, "w", encoding="utf-8") as JSON_Output:
        _json.dump(Record_Concat, JSON_Output, indent=4)

    print("end _JSONs_Concat")


def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _JSONs_Probe()
    _JSONs_Concat()

    print(
        f"{Folder_JSONs_Input_Name = :s}\n"
        + f"{JSON_Output_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
