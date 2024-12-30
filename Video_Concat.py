"""
Concatenates a sequence of videos.
Concatenates video in ascending alphanumerical order.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _Utils_DateTime


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None
_Command_FFMpeg = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Folder_Data_Name = None
File_Concat_Name = None
Video_Output_Name = None
Arguments_Overridden = False
Videos_Input_Name = None


def _Context_Create():
    global Folder_Data_Name
    global File_Concat_Name
    global Video_Output_Name

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name = \
            _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if File_Concat_Name is None:
        File_Concat_Name = \
            _os_path.join(Folder_Data_Name, f"Concat_{timestamp}.txt")
        # end statement

    if Video_Output_Name is None:
        Video_Output_Name = \
            _os_path.join(Folder_Data_Name, f"Output_{timestamp}.mp4")
        # end statement


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Videos_Input_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage=\
            f"python {_Script_basename} [--help]"
            + f" <{_nameof(Videos_Input_Name)}>",

        description=\
            "Concatenates a sequence of videos."
            + " Concatenates video in ascending alphanumerical order.",

        epilog=\
            "Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Videos_Input_Name)}",
        type=str,
        help="Name of the video sequence folder.",
        metavar=f"{_nameof(Videos_Input_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Videos_Input_Name is None:
            Videos_Input_Name = _Arguments.Videos_Input_Name

        Videos_Input_Name = _os_path.abspath(Videos_Input_Name)


def _ConcatDemuxer_Generate():
    Videos_isdir = _os_path.isdir(Videos_Input_Name)
    Video_Input_Names = []

    if Videos_isdir:
        Video_Input_Names = _os.listdir(Videos_Input_Name)
        Video_Input_Names.sort()

    for Index, File_Name in enumerate(Video_Input_Names):
        Video_Input_Names[Index] = _os_path.join(Videos_Input_Name, File_Name)

    Video_Input_Names_New = []

    for File_Name in Video_Input_Names:
        Video_isfile = _os_path.isfile(File_Name)
        Video_basename = _os_path.basename(File_Name)
        _, Video_Ext = _os_path.splitext(Video_basename)
        Video_Ext_Matched = Video_Ext.lower() == ".mp4"

        if Video_isfile and Video_Ext_Matched:
            Video_Input_Names_New.append(File_Name)
        # end if
    # end if

    Video_Input_Names = Video_Input_Names_New
    Concat_Lines = []

    for File_Name in Video_Input_Names:
        Concat_Lines.append(f"file '{File_Name}'")

    Concat_str = "\n".join(Concat_Lines)

    with open(File_Concat_Name, mode="w", encoding="utf-8") as File_Concat:
        File_Concat.write(Concat_str)
    # end with
# end def


def _Video_Concat():
    global _Command_FFMpeg

    _Command_FFMpeg =\
        f"ffmpeg"\
        + f"  -f concat"\
        + f"  -safe 0"\
        + f"  -i \"{File_Concat_Name}\""\
        + f"  -filter:v fps=30"\
        + f"  -pix_fmt yuvj420p"\
        + f"  -movflags +faststart"\
        + f"  -c:v h264"\
        + f"  -profile:v high"\
        + f"  \"{Video_Output_Name}\""

    print(f"{_Command_FFMpeg = }")
    _os.system(_Command_FFMpeg)


def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _ConcatDemuxer_Generate()
    _Video_Concat()

    print(
        f"{Videos_Input_Name = :s}\n"
        + f"{File_Concat_Name = :s}\n"
        + f"{Video_Output_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
