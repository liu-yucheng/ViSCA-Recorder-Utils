"""
Performs a batch of "Data_FromRecorder_Process.py" operations.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _Utils_DateTime
import Data_FromRecorder_Process as _Data_FromRecorder_Process


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None
_Folder_Data_FromRecorder_Names = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Folder_Data_Name = None
Folder_Outputs_Name = None
Arguments_Overridden = False
Folder_Batch_Data_FromRecorder_Name = None


def _Context_Create():
    global Folder_Data_Name
    global Folder_Outputs_Name

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name \
        = _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    Timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if Folder_Outputs_Name is None:
        Folder_Outputs_Name \
        = _os_path.join(Folder_Data_Name, f"Outputs_{Timestamp}")

    _os.makedirs(Folder_Outputs_Name, exist_ok=True)


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Folder_Batch_Data_FromRecorder_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage\
        = f"python {_Script_basename} [--help]" \
            + f" <{_nameof(Folder_Batch_Data_FromRecorder_Name)}>",

        description\
        ="Performs a batch of \"Data_FromRecorder_Process.py\" operations.",

        epilog\
        ="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Folder_Batch_Data_FromRecorder_Name)}",
        type=str,
        help="Name of the folder that contains multiple ViSCA Recorder data folders.",
        metavar=f"{_nameof(Folder_Batch_Data_FromRecorder_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Folder_Batch_Data_FromRecorder_Name is None:
            Folder_Batch_Data_FromRecorder_Name \
            = _Arguments.Folder_Batch_Data_FromRecorder_Name

        Folder_Batch_Data_FromRecorder_Name \
        = _os_path.abspath(Folder_Batch_Data_FromRecorder_Name)


def _Folders_Data_FromRecorder_Probe():
    global _Folder_Data_FromRecorder_Names

    _Folder_Data_FromRecorder_Names = []
    NestedData_isdir = _os_path.isdir(Folder_Batch_Data_FromRecorder_Name)

    if NestedData_isdir:
        _Folder_Data_FromRecorder_Names = _os.listdir(Folder_Batch_Data_FromRecorder_Name)
        _Folder_Data_FromRecorder_Names.sort()

    for Index, Folder_Name in enumerate(_Folder_Data_FromRecorder_Names):
        _Folder_Data_FromRecorder_Names[Index] \
        = _os_path.join(Folder_Batch_Data_FromRecorder_Name, Folder_Name)

    Names_Folder_Images_New = []

    for Folder_Name in _Folder_Data_FromRecorder_Names:
        Folder_isdir = _os_path.isdir(Folder_Name)

        if Folder_isdir:
            Names_Folder_Images_New.append(Folder_Name)
        # end if
    # end for

    _Folder_Data_FromRecorder_Names = Names_Folder_Images_New


def _Batch_Operations_Perform():
    print("begin _Batch_Operations_Perform")

    for Index, Folder_Name in enumerate(_Folder_Data_FromRecorder_Names):
        print(f"begin Operation {Index + 1} / {len(_Folder_Data_FromRecorder_Names)}")
        Folder_basename = _os_path.basename(Folder_Name)

        _Data_FromRecorder_Process.Folder_Data_Name \
        = f".{_Data_FromRecorder_Process.Script_NoExt}_{Folder_basename}_Data"

        _Data_FromRecorder_Process.Folder_Data_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            _Data_FromRecorder_Process.Folder_Data_Name
        )

        _Data_FromRecorder_Process.Folder_Outputs_Name \
        = f"visca-recorder-utils_{Folder_basename}"

        _Data_FromRecorder_Process.Folder_Outputs_Name \
        = _os_path.join(
            Folder_Outputs_Name,
            _Data_FromRecorder_Process.Folder_Outputs_Name
        )

        _Data_FromRecorder_Process.Folder_Batch_Video_FromRecorderImages_Convert_Name \
        = _os_path.join(
            _Data_FromRecorder_Process.Folder_Data_Name,
            ".Batch_Video_FromRecorderImages_Convert_Data"
        )

        _Data_FromRecorder_Process.Folder_Video_Concat_Name \
        = _os_path.join(
            _Data_FromRecorder_Process.Folder_Data_Name,
            ".Video_Concat_Data"
        )

        _Data_FromRecorder_Process.Folder_JSON_FromRecorder_Concat_Name \
        = _os_path.join(
            _Data_FromRecorder_Process.Folder_Data_Name,
            ".JSON_FromRecorder_Concat_Data"
        )

        _Data_FromRecorder_Process.Folder_Batch_Video_FromRecorderImages_WithSickness_Convert_Name \
        = _os_path.join(
            _Data_FromRecorder_Process.Folder_Data_Name,
            ".Batch_Video_FromRecorderImages_WithSickness_Convert_Data"
        )

        _Data_FromRecorder_Process.Folder_Video_Concat_WithSickness_Name \
        = _os_path.join(
            _Data_FromRecorder_Process.Folder_Data_Name,
            ".Video_Concat_WithSickness_Data"
        )

        _Data_FromRecorder_Process.Folder_JSON_FromRecorder_WithSickness_Concat_Name \
        = _os_path.join(
            _Data_FromRecorder_Process.Folder_Data_Name,
            ".JSON_FromRecorder_WithSickness_Concat_Data"
        )

        _Data_FromRecorder_Process.Arguments_Overridden = True
        _Data_FromRecorder_Process.Folder_Data_FromRecorder_Name = Folder_Name
        _Data_FromRecorder_Process.Main()
        print(f"end Operation {Index + 1} / {len(_Folder_Data_FromRecorder_Names)}")

    print("end _Batch_Operations_Perform")


def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _Folders_Data_FromRecorder_Probe()
    _Batch_Operations_Perform()

    print(
        f"{Folder_Batch_Data_FromRecorder_Name = :s}\n"
        + f"{Folder_Outputs_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
