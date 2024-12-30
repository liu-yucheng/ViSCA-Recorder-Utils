"""
Concatenates a sequence of JSON (from ViSCA Recorder) files
    (includes items with sickness only).

Concatenates JSONs in ascending alphanumerical order.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import sys as _sys
import json as _json
import pandas as _pandas
import varname as _varname
import _Utils_DateTime


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None
_Input_JSON_Names = None
_Record_Concat = None
_Record_Concat_Flattened = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Items_WithSickness_TimeBefore_Seconds = None
Items_WithSickness_TimeAfter_Seconds = None
Items_WithSickness_SicknessThreshold = float(0.75)
Folder_Data_Name = None
Output_JSON_Name = None
Output_JSON_Flattened_Name = None
Arguments_Overridden = False
Input_Folder_JSONs_Name = None


def _Context_Create():
    global Items_WithSickness_TimeBefore_Seconds
    global Items_WithSickness_TimeAfter_Seconds
    global Folder_Data_Name
    global Output_JSON_Name
    global Output_JSON_Flattened_Name

    if Items_WithSickness_TimeBefore_Seconds is None:
        Items_WithSickness_TimeBefore_Seconds = 0.5

    if Items_WithSickness_TimeAfter_Seconds is None:
        Items_WithSickness_TimeAfter_Seconds = 0.5

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name \
        = _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement
    # end if

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if Output_JSON_Name is None:
        Output_JSON_Name \
        = _os_path.join(Folder_Data_Name, f"Output_{timestamp}.json")
        # end statement

    if Output_JSON_Flattened_Name is None:
        Output_JSON_Flattened_Name \
        = _os_path.join(Folder_Data_Name, f"Output_Flattened_{timestamp}.json")
        # end statement
    # end if
# end def

def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Input_Folder_JSONs_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage\
        =f"python {_Script_basename} [--help]"
            + f" <{_nameof(Input_Folder_JSONs_Name)}>",

        description\
        ="Concatenates a sequence of JSON (from ViSCA Recorder) files."
            + " Concatenates JSONs in ascending alphanumerical order.",

        epilog\
        ="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Input_Folder_JSONs_Name)}",
        type=str,
        help="The folder name of the ViSCA Recorder JSON file sequence.",
        metavar=f"{_nameof(Input_Folder_JSONs_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Input_Folder_JSONs_Name is None:
            Input_Folder_JSONs_Name = _Arguments.Input_Folder_JSONs_Name

        Input_Folder_JSONs_Name = _os_path.abspath(Input_Folder_JSONs_Name)
    # end if
# end def

def _JSONs_Probe():
    global _Input_JSON_Names

    JSONs_isdir = _os_path.isdir(Input_Folder_JSONs_Name)
    _Input_JSON_Names = []

    if JSONs_isdir:
        _Input_JSON_Names = _os.listdir(Input_Folder_JSONs_Name)
        _Input_JSON_Names.sort()

    for Index, File_Name in enumerate(_Input_JSON_Names):
        _Input_JSON_Names[Index] \
        = _os_path.join(Input_Folder_JSONs_Name, File_Name)
        # end statement
    # end for

    JSON_Names_New = []

    for File_Name in _Input_JSON_Names:
        JSON_isfile = _os_path.isfile(File_Name)
        JSON_basename = _os_path.basename(File_Name)
        _, JSON_Ext = _os_path.splitext(JSON_basename)
        JSON_Ext_Matched = JSON_Ext.lower() == ".json"

        if JSON_isfile and JSON_Ext_Matched:
            JSON_Names_New.append(File_Name)
        # end if
    # end if

    _Input_JSON_Names = JSON_Names_New
# end def

def _JSONs_Concat():
    global _Record_Concat
    print("begin _JSONs_Concat")

    _Record_Concat = {
        "visca_recorder_utils": {
            "files__concatenated": [],
            "json__flattening_enabled": False,

            "filters__with_sickness": {
                "items__with_sickness__time_before": \
                    Items_WithSickness_TimeAfter_Seconds,

                "items__with_sickness__time_after": \
                    Items_WithSickness_TimeBefore_Seconds,

                "items__with_sickness__threshold": \
                    Items_WithSickness_SicknessThreshold
            },

            "sickness__statistics": {
                "time__with_sickness__seconds": float(0),
                "time__total__seconds": float(0),
                "time_proportion__with_sickness": float(0)
            }
        },

        "items": []
    }

    for Index, File_Name in enumerate(_Input_JSON_Names):
        Input_JSON_basename = _os_path.basename(File_Name)

        print(
            f"begin Concatenating {Index + 1} / {len(_Input_JSON_Names)}"
            + f" {Input_JSON_basename}"
        )

        Record = {}

        with open(File_Name, "r", encoding="utf-8") as JSON_Input:
            Record = _json.load(JSON_Input)
            Record = dict(Record)

        if "items" in Record:
            Record_Items = Record["items"]
            Record_Items = list(Record_Items)
            _Record_Concat["items"] += Record_Items

        _Record_Concat["visca_recorder_utils"]["files__concatenated"]\
            .append(Input_JSON_basename)

        print(
            f"end Concatenating {Index + 1} / {len(_Input_JSON_Names)}"
            + f" {Input_JSON_basename}"
        )

    print("begin Filtering (with sickness)")
    Indexes_WithSickness_Dict = {}
    Indexes_BeforeSickness_Dict = {}
    Indexes_AfterSickness_Dict = {}
    Items = list(_Record_Concat["items"])
    Time_WithSickness_Seconds = float(0)
    Time_Total_Seconds = float(0)
    Time_Item_Previous = float(0)
    Time_Item_Current = float(0)

    # Select items with sickness.
    for Index, Item in enumerate(Items):
        if "sickness" in Item and "reported" in Item["sickness"]:
            Sickness = float(Item["sickness"]["reported"])
        else:
            Sickness = float(0)

        if "timestamp" in Item and "game_time_seconds" in Item["timestamp"]:
            Time_Item_Current = float(Item["timestamp"]["game_time_seconds"])
        else:
            Time_Item_Current = Time_Item_Previous

        Time_BetweenItems_Duration = Time_Item_Current - Time_Item_Previous

        if Sickness >= Items_WithSickness_SicknessThreshold:
            Indexes_WithSickness_Dict[Index] = None
            Time_WithSickness_Seconds += Time_BetweenItems_Duration

        Time_Total_Seconds += Time_BetweenItems_Duration
        Time_Item_Previous = Time_Item_Current
    # end for

    TimeProportion_WithSickness = Time_WithSickness_Seconds / Time_Total_Seconds
    Indexes_WithSickness = list(Indexes_WithSickness_Dict.keys())
    Indexes_WithSickness.sort()

    # Select items before sickness.
    for Index in Indexes_WithSickness:
        Item = Items[Index]
        Time_ = _sys.float_info.max

        if "timestamp" in Item and "game_time_seconds" in Item["timestamp"]:
            Time_ = float(Item["timestamp"]["game_time_seconds"])

        Index_Trace = Index
        Time_Trace = Time_

        while \
            Time_ - Time_Trace < Items_WithSickness_TimeBefore_Seconds \
            and Index_Trace >= 0:
            Item_Trace = Items[Index_Trace]
            Time_Trace = _sys.float_info.min

            if \
                "timestamp" in Item_Trace \
                and "game_time_seconds" in Item_Trace["timestamp"]:
                Time_Trace \
                = float(Item_Trace["timestamp"]["game_time_seconds"])
                # end statement
            # end if

            if Index_Trace not in Indexes_BeforeSickness_Dict:
                Indexes_BeforeSickness_Dict[Index_Trace] = None

            Index_Trace -= 1
        # end while
    # end for

    # Select items after sickness.
    for Index in Indexes_WithSickness:
        Item = Items[Index]
        Time_ = _sys.float_info.min

        if "timestamp" in Item and "game_time_seconds" in Item["timestamp"]:
            Time_ = float(Item["timestamp"]["game_time_seconds"])

        Index_Trace = Index
        Time_Trace = Time_

        while \
            Time_Trace - Time_ < Items_WithSickness_TimeAfter_Seconds \
            and Index_Trace < len(Items):
            Item_Trace = Items[Index_Trace]
            Time_Trace = _sys.float_info.max

            if \
                "timestamp" in Item_Trace \
                and "game_time_seconds" in Item_Trace["timestamp"]:
                Time_Trace \
                = float(Item_Trace["timestamp"]["game_time_seconds"])
                # end statement
            # end if

            if Index_Trace not in Indexes_AfterSickness_Dict:
                Indexes_AfterSickness_Dict[Index_Trace] = None

            Index_Trace += 1
        # end while
    # end for

    for Key, Item in Indexes_BeforeSickness_Dict.items():
        Indexes_WithSickness_Dict[Key] = Item

    for Key, Item in Indexes_AfterSickness_Dict.items():
        Indexes_WithSickness_Dict[Key] = Item

    Items_WithSickness = []

    for Index, Item in enumerate(Items):
        if Index in Indexes_WithSickness_Dict:
            Items_WithSickness.append(Item)
        # end if
    # end for

    _Record_Concat["items"] = Items_WithSickness

    _Record_Concat\
        ["visca_recorder_utils"]\
        ["sickness__statistics"]\
        ["time__with_sickness__seconds"] \
    = Time_WithSickness_Seconds

    _Record_Concat\
        ["visca_recorder_utils"]\
        ["sickness__statistics"]\
        ["time__total__seconds"] \
    = Time_Total_Seconds

    _Record_Concat\
        ["visca_recorder_utils"]\
        ["sickness__statistics"]\
        ["time_proportion__with_sickness"] \
    = TimeProportion_WithSickness

    print("end Filtering (with sickness)")
    print(f"{len(_Record_Concat["items"]) = }")

    with open(Output_JSON_Name, "w", encoding="utf-8") as Output_JSON:
        _json.dump(_Record_Concat, Output_JSON, indent=4)

    print("end _JSONs_Concat")
# end def

def _JSONs_Flattened_Concat():
    global _Record_Concat_Flattened
    print("begin _JSONs_Flattened_Concat")

    _Record_Concat_Flattened = {
        "visca_recorder_utils": _Record_Concat["visca_recorder_utils"],
        "items__flattened": []
    }

    _Record_Concat_Flattened\
        ["visca_recorder_utils"]\
        ["json__flattening_enabled"]\
    = True

    Items = _Record_Concat["items"]
    Items_DataFrame = _pandas.json_normalize(Items, sep=".")
    Items_Flattened = Items_DataFrame.to_dict(orient="records")
    _Record_Concat_Flattened["items__flattened"] = Items_Flattened
    print(f"{len(_Record_Concat_Flattened["items__flattened"]) = }")

    with open(Output_JSON_Flattened_Name, "w", encoding="utf-8") \
    as Output_JSON_Flattened:
        _json.dump(_Record_Concat_Flattened, Output_JSON_Flattened, indent=4)

    print("end _JSONs_Flattened_Concat")
# end def

def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _JSONs_Probe()
    _JSONs_Concat()
    _JSONs_Flattened_Concat()

    print(
        f"{Items_WithSickness_TimeBefore_Seconds = }\n"
        + f"{Items_WithSickness_TimeAfter_Seconds = }\n"
        + f"{Input_Folder_JSONs_Name = :s}\n"
        + f"{Output_JSON_Name = :s}\n"
        + f"{Output_JSON_Flattened_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
