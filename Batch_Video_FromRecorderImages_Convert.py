"""
Performs a batch of "Video_FromRecorderImages_Convert.py" operations.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import Video_FromRecorderImages_Convert as _Video_FromRecorderImages_WithSickness_Convert
import _Utils_DateTime


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None
_Folder_Images_Names = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Folder_Data_Name = None
Folder_Output_Name = None
Arguments_Overridden = False
Folder_NestedImages_Name = None


def _Context_Create():
    global Folder_Data_Name
    global Folder_Output_Name

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name = \
            _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    Timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if Folder_Output_Name is None:
        Folder_Output_Name = \
            _os_path.join(Folder_Data_Name, f"Output_{Timestamp}")
        # end statement

    _os.makedirs(Folder_Output_Name, exist_ok=True)


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Folder_NestedImages_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage=\
            f"python {_Script_basename} [--help]"
            + f" <{_nameof(Folder_NestedImages_Name)}>",

        description=\
            "Performs a batch of \"Video_FromRecorderImages_Convert.py\""
            + " operations.",

        epilog=\
            "Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Folder_NestedImages_Name)}",
        type=str,
        help="Name of the folder that contains multiple image folders.",
        metavar=f"{_nameof(Folder_NestedImages_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Folder_NestedImages_Name is None:
            Folder_NestedImages_Name = _Arguments.Folder_NestedImages_Name

        Folder_NestedImages_Name = _os_path.abspath(Folder_NestedImages_Name)


def _Folders_Image_Probe():
    global _Folder_Images_Names

    _Folder_Images_Names = []
    NestedImages_isdir = _os_path.isdir(Folder_NestedImages_Name)

    if NestedImages_isdir:
        _Folder_Images_Names = _os.listdir(Folder_NestedImages_Name)
        _Folder_Images_Names.sort()

    for Index, Folder_Name in enumerate(_Folder_Images_Names):
        _Folder_Images_Names[Index] = \
            _os_path.join(Folder_NestedImages_Name, Folder_Name)

    Names_Folder_Images_New = []

    for Folder_Name in _Folder_Images_Names:
        Folder_isdir = _os_path.isdir(Folder_Name)

        if Folder_isdir:
            Names_Folder_Images_New.append(Folder_Name)
        # end if
    # end for

    _Folder_Images_Names = Names_Folder_Images_New


def _Batch_Operations_Perform():
    print("begin _Batch_Operations_Perform")

    for Index, Folder_Name in enumerate(_Folder_Images_Names):
        print(f"begin Operation {Index + 1} / {len(_Folder_Images_Names)}")
        Folder_basename = _os_path.basename(Folder_Name)
        _Video_FromRecorderImages_WithSickness_Convert.Folder_Data_Name = Folder_Output_Name

        _Video_FromRecorderImages_WithSickness_Convert.File_Concat_Name = \
            _os_path.join(Folder_Output_Name, f"{Folder_basename}.txt")

        _Video_FromRecorderImages_WithSickness_Convert.Video_Name = \
            _os_path.join(Folder_Output_Name, f"{Folder_basename}.mp4")

        _Video_FromRecorderImages_WithSickness_Convert.Arguments_Overridden = True
        _Video_FromRecorderImages_WithSickness_Convert.Folder_Images_Name = Folder_Name
        _Video_FromRecorderImages_WithSickness_Convert.Main()
        print(f"end Operation {Index + 1} / {len(_Folder_Images_Names)}")

    print("end _Batch_Operations_Perform")


def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _Folders_Image_Probe()
    _Batch_Operations_Perform()

    print(
        f"{Folder_NestedImages_Name = :s}\n"
        + f"{Folder_Output_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
