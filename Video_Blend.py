"""
Blends 2 videos into 1 video.
Uses the 2nd video as an overlay on the 1st video.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


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
Video_Output_Name = None
Arguments_Overridden = False
Video_Input1_Name = None
Video_Input2_Name = None


def _Context_Create():
    global Folder_Data_Name
    global Video_Output_Name

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name = \
            _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if Video_Output_Name is None:
        Video_Output_Name = \
            _os_path.join(Folder_Data_Name, f"Output_{timestamp}.mp4")
        # end statement


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Video_Input1_Name
    global Video_Input2_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage=\
            f"python {_Script_basename} [--help] <{_nameof(Video_Input1_Name)}>"
            + f" <{_nameof(Video_Input2_Name)}>",

        description=\
            "Blends 2 videos into 1 video."
            + " Uses the 2nd video as an overlay on the 1st video.",

        epilog=\
            "Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Video_Input1_Name)}",
        type=str,
        help="Name of the 1st video.",
        metavar=f"{_nameof(Video_Input1_Name)}"
    )

    _Parser.add_argument(
        f"{_nameof(Video_Input2_Name)}",
        type=str,
        help="Name of the 2nd video.",
        metavar=f"{_nameof(Video_Input2_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Video_Input1_Name is None:
            Video_Input1_Name = _Arguments.Video_Input1_Name

        if Video_Input2_Name is None:
            Video_Input2_Name = _Arguments.Video_Input2_Name

        Video_Input1_Name = _os_path.abspath(Video_Input1_Name)
        Video_Input2_Name = _os_path.abspath(Video_Input2_Name)


def _Video_Blend():
    global _Command_FFMpeg

    Input1 = Video_Input1_Name
    Input2 = Video_Input2_Name
    Output1 = Video_Output_Name

    _Command_FFMpeg =\
        f"ffmpeg"\
        + f"  -i \"{Input1}\""\
        + f"  -i \"{Input2}\""\
        + f"  -filter_complex \""\
        + f"    [0]format=yuvj420p,colorchannelmixer=ar=0:ag=0:ab=0:aa=1[v1];"\
        + f"    [1]format=yuvj420p,colorchannelmixer=ar=2:ag=2:ab=2:aa=0[v2];"\
        + f"    [v2][v1]scale2ref[v2][v1];"\
        + f"    [v1][v2]blend=all_mode=\"addition\":all_opacity=0.65"\
        + f"  \""\
        + f"  -pix_fmt yuvj420p"\
        + f"  -movflags +faststart"\
        + f"  -c:v h264"\
        + f"  -profile:v high"\
        + f"  \"{Output1}\""

    print(f"{_Command_FFMpeg = }")
    _os.system(_Command_FFMpeg)


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _Video_Blend()

    print(
        f"{Video_Input1_Name = :s}\n"
        + f"{Video_Input2_Name = :s}\n"
        + f"{Video_Output_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    main()
