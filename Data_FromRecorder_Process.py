"""
Processes a data folder (from ViSCA Recorder).
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _Utils_DateTime
import Batch_Video_FromRecorderImages_Convert as _Batch_Video_FromRecorderImages_Convert
import Video_Concat as _Video_Concat
import JSON_FromRecorder_Concat as _JSON_FromRecorder_Concat
import Batch_Video_FromRecorderImages_WithSickness_Convert as _Batch_Video_FromRecorderImages_WithSickness_Convert
import JSON_FromRecorder_WithSickness_Concat as _JSON_FromRecorder_WithSickness_Concat


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Folder_Data_Name = None
Folder_Outputs_Name = None
Folder_Batch_Video_FromRecorderImages_Convert_Name = None
Folder_Video_Concat_Name = None
Folder_JSON_FromRecorder_Concat_Name = None
Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name = None
Folder_Video_Concat_WithSickness_Name = None
Folder_JSON_FromRecorder_WithSickness_Concat_Name = None
Arguments_Overridden = False
Folder_Data_FromRecorder_Name = None


def _Context_Create():
    global Folder_Data_Name
    global Folder_Outputs_Name
    global Folder_Batch_Video_FromRecorderImages_Convert_Name
    global Folder_Video_Concat_Name
    global Folder_JSON_FromRecorder_Concat_Name
    global Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name
    global Folder_Video_Concat_WithSickness_Name
    global Folder_JSON_FromRecorder_WithSickness_Concat_Name

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name \
        = _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    Timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if Folder_Outputs_Name is None:
        Folder_Outputs_Name \
        = _os_path.join(Folder_Data_Name, f"Outputs_{Timestamp}")

    _os.makedirs(Folder_Outputs_Name, exist_ok=True)

    if Folder_Batch_Video_FromRecorderImages_Convert_Name is None:
        Folder_Batch_Video_FromRecorderImages_Convert_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            f".{_Batch_Video_FromRecorderImages_Convert.Script_NoExt}_Data"
        )
        # end statement
    # end if

    _os.makedirs(Folder_Batch_Video_FromRecorderImages_Convert_Name)

    if Folder_Video_Concat_Name is None:
        Folder_Video_Concat_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            f".{_Video_Concat.Script_NoExt}_Data"
        )
        # end statement
    # end if

    _os.makedirs(Folder_Video_Concat_Name)

    if Folder_JSON_FromRecorder_Concat_Name is None:
        Folder_JSON_FromRecorder_Concat_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            f".{_JSON_FromRecorder_Concat.Script_NoExt}_Data"
        )
        # end statement
    # end if

    _os.makedirs(Folder_JSON_FromRecorder_Concat_Name)

    if Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name is None:
        Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            f".{_Batch_Video_FromRecorderImages_WithSickness_Convert.Script_NoExt}_Data"
        )

    _os.makedirs(Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name)

    if Folder_Video_Concat_WithSickness_Name is None:
        Folder_Video_Concat_WithSickness_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            f".{_Video_Concat.Script_NoExt}_WithSickness_Data"
        )
        # end statement

    _os.makedirs(Folder_Video_Concat_WithSickness_Name)

    if Folder_JSON_FromRecorder_WithSickness_Concat_Name is None:
        Folder_JSON_FromRecorder_WithSickness_Concat_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            f".{_JSON_FromRecorder_WithSickness_Concat.Script_NoExt}_Data"
        )

    _os.makedirs(Folder_JSON_FromRecorder_WithSickness_Concat_Name)


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Folder_Data_FromRecorder_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage\
        =f"python {_Script_basename} [--help]"\
            + f" <{_nameof(Folder_Data_FromRecorder_Name)}>",

        description="Processes a data folder (from ViSCA Recorder).",

        epilog\
        ="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Folder_Data_FromRecorder_Name)}",
        type=str,
        help="The name of a data folder from ViSCA Recorder.",
        metavar=f"{_nameof(Folder_Data_FromRecorder_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Folder_Data_FromRecorder_Name is None:
            Folder_Data_FromRecorder_Name \
            = _Arguments.Folder_Data_FromRecorder_Name

        Folder_Data_FromRecorder_Name \
        = _os_path.abspath(Folder_Data_FromRecorder_Name)


def _Batch_Video_FromRecorderImages_Convert_Perform():
    _Batch_Video_FromRecorderImages_Convert.Folder_Data_Name \
    = Folder_Batch_Video_FromRecorderImages_Convert_Name

    _Batch_Video_FromRecorderImages_Convert.Folder_Output_Name \
    = Folder_Batch_Video_FromRecorderImages_Convert_Name

    _Batch_Video_FromRecorderImages_Convert.Arguments_Overridden = True

    _Batch_Video_FromRecorderImages_Convert.Folder_NestedImages_Name \
    = Folder_Data_FromRecorder_Name

    _Batch_Video_FromRecorderImages_Convert.Main()


def _Video_Concat_Perform():
    Video_Input_Names \
    = _os.listdir(Folder_Batch_Video_FromRecorderImages_Convert_Name)

    Video_Input_Names.sort()

    for Index, File_Name in enumerate(Video_Input_Names):
        Video_Input_Names[Index] \
        = _os_path.join(
            Folder_Batch_Video_FromRecorderImages_Convert_Name,
            File_Name
        )
        # end statement

    Video_Input_Names_New = []

    for File_Name in Video_Input_Names:
        Video_basename = _os_path.basename(File_Name)
        _, Video_Ext = _os_path.splitext(Video_basename)
        Video_Ext_Matched = Video_Ext.lower() == ".mp4"

        if Video_Ext_Matched:
            Video_Input_Names_New.append(File_Name)
        # end if
    # end for

    Video_Input_Names = Video_Input_Names_New
    Video_Input1_basename = _os_path.basename(Video_Input_Names[0])
    Video_Input1_NoExt, _ = _os_path.splitext(Video_Input1_basename)
    _Video_Concat.Folder_Data_Name = Folder_Video_Concat_Name

    _Video_Concat.File_Concat_Name \
    = _os_path.join(
        Folder_Video_Concat_Name,
        f"Concat_{Video_Input1_NoExt}.txt"
    )
    # end statement

    _Video_Concat.Video_Output_Name \
    = _os_path.join(Folder_Outputs_Name, f"Concat_{Video_Input1_NoExt}.mp4")

    _Video_Concat.Arguments_Overridden = True

    _Video_Concat.Videos_Input_Name \
    = Folder_Batch_Video_FromRecorderImages_Convert_Name

    _Video_Concat.Main()


def _JSON_FromRecorder_Concat_Perform():
    JSON_Input_Names = _os.listdir(Folder_Data_FromRecorder_Name)
    JSON_Input_Names.sort()

    for Index, File_Name in enumerate(JSON_Input_Names):
        JSON_Input_Names[Index] \
        = _os_path.join(Folder_Data_FromRecorder_Name, File_Name)
        # end statement

    JSON_Input_Names_New = []

    for File_Name in JSON_Input_Names:
        JSON_basename = _os_path.basename(File_Name)
        _, JSON_Ext = _os_path.splitext(JSON_basename)
        JSON_Ext_Matched = JSON_Ext.lower() == ".json"

        if JSON_Ext_Matched:
            JSON_Input_Names_New.append(File_Name)
        # end if
    # end for

    JSON_Input_Names = JSON_Input_Names_New
    JSON_Input1_basename = _os_path.basename(JSON_Input_Names[0])
    JSON_Input1_NoExt, _ = _os_path.splitext(JSON_Input1_basename)

    _JSON_FromRecorder_Concat.Folder_Data_Name \
    = Folder_JSON_FromRecorder_Concat_Name

    _JSON_FromRecorder_Concat.Output_JSON_Name \
    = _os_path.join(Folder_Outputs_Name, f"Concat_{JSON_Input1_NoExt}.json")

    _JSON_FromRecorder_Concat.Output_JSON_Flattened_Name \
    = _os_path.join(
        Folder_Outputs_Name,
        f"Concat_Flattened_{JSON_Input1_NoExt}.json"
    )

    _JSON_FromRecorder_Concat.Arguments_Overridden = True

    _JSON_FromRecorder_Concat.Input_Folder_JSONs_Name \
    = Folder_Data_FromRecorder_Name

    _JSON_FromRecorder_Concat.Main()


def _Batch_Video_FromRecorderImages_WithSickness_Convert_Perform():
    _Batch_Video_FromRecorderImages_WithSickness_Convert.Folder_Data_Name \
    = Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name

    _Batch_Video_FromRecorderImages_WithSickness_Convert.Folder_Output_Name \
    = Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name

    _Batch_Video_FromRecorderImages_WithSickness_Convert.Arguments_Overridden \
    = True

    _Batch_Video_FromRecorderImages_WithSickness_Convert.Folder_NestedImages_Name \
    = Folder_Data_FromRecorder_Name

    _Batch_Video_FromRecorderImages_WithSickness_Convert.Main()


def _Video_Concat_WithSickness_Perform():
    Video_Input_Names \
    = _os.listdir(
        Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name
    )
    # end statement

    Video_Input_Names.sort()

    for Index, File_Name in enumerate(Video_Input_Names):
        Video_Input_Names[Index] \
        = _os_path.join(
            Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name,
            File_Name
        )
        # end statement
    # end for

    Video_Input_Names_New = []

    for File_Name in Video_Input_Names:
        Video_basename = _os_path.basename(File_Name)
        _, Video_Ext = _os_path.splitext(Video_basename)
        Video_Ext_Matched = Video_Ext.lower() == ".mp4"

        if Video_Ext_Matched:
            Video_Input_Names_New.append(File_Name)
        # end if
    # end for

    Video_Input_Names = Video_Input_Names_New

    if len(Video_Input_Names) >= 1:
        Video_Input1_basename = _os_path.basename(Video_Input_Names[0])
    else:
        Video_Input1_basename = "empty-video.mp4"

    Video_Input1_NoExt, _ = _os_path.splitext(Video_Input1_basename)
    _Video_Concat.Folder_Data_Name = Folder_Video_Concat_WithSickness_Name

    _Video_Concat.File_Concat_Name \
    = _os_path.join(
        Folder_Video_Concat_WithSickness_Name,
        f"Concat_WithSickness_{Video_Input1_NoExt}.txt"
    )
    # end statement

    _Video_Concat.Video_Output_Name \
    = _os_path.join(
        Folder_Outputs_Name,
        f"Concat_WithSickness_{Video_Input1_NoExt}.mp4"
    )
    # end statement

    _Video_Concat.Arguments_Overridden = True

    _Video_Concat.Videos_Input_Name \
    = Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name

    _Video_Concat.Main()


def _JSON_FromRecorder_WithSickness_Concat_Perform():
    JSON_Input_Names = _os.listdir(Folder_Data_FromRecorder_Name)
    JSON_Input_Names.sort()

    for Index, File_Name in enumerate(JSON_Input_Names):
        JSON_Input_Names[Index] \
        = _os_path.join(Folder_Data_FromRecorder_Name, File_Name)
    # end for

    JSON_Input_Names_New = []

    for File_Name in JSON_Input_Names:
        JSON_basename = _os_path.basename(File_Name)
        _, JSON_Ext = _os_path.splitext(JSON_basename)
        JSON_Ext_Matched = JSON_Ext.lower() == ".json"

        if JSON_Ext_Matched:
            JSON_Input_Names_New.append(File_Name)
        # end if
    # end for

    JSON_Input_Names = JSON_Input_Names_New
    JSON_Input1_basename = _os_path.basename(JSON_Input_Names[0])
    JSON_Input1_NoExt, _ = _os_path.splitext(JSON_Input1_basename)

    _JSON_FromRecorder_WithSickness_Concat.Items_WithSickness_TimeBefore_Seconds \
    = 0.5

    _JSON_FromRecorder_WithSickness_Concat.Items_WithSickness_TimeAfter_Seconds \
    = 0.5

    _JSON_FromRecorder_WithSickness_Concat.Folder_Data_Name \
    = Folder_JSON_FromRecorder_Concat_Name

    _JSON_FromRecorder_WithSickness_Concat.Output_JSON_Name \
    = _os_path.join(
        Folder_Outputs_Name,
        f"Concat_WithSickness_{JSON_Input1_NoExt}.json"
    )

    _JSON_FromRecorder_WithSickness_Concat.Output_JSON_Flattened_Name \
    = _os_path.join(
        Folder_Outputs_Name,
        f"Concat_WithSickness_Flattened_{JSON_Input1_NoExt}.json"
    )

    _JSON_FromRecorder_WithSickness_Concat.Arguments_Overridden = True

    _JSON_FromRecorder_WithSickness_Concat.Input_Folder_JSONs_Name \
    = Folder_Data_FromRecorder_Name

    _JSON_FromRecorder_WithSickness_Concat.Main()


def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _Batch_Video_FromRecorderImages_Convert_Perform()
    _Video_Concat_Perform()
    _JSON_FromRecorder_Concat_Perform()
    _Batch_Video_FromRecorderImages_WithSickness_Convert_Perform()
    _Video_Concat_WithSickness_Perform()
    _JSON_FromRecorder_WithSickness_Concat_Perform()

    print(
        f"{Folder_Data_FromRecorder_Name = :s}\n"
        + f"{Folder_Outputs_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
