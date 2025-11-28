"""
Blends 2 videos into 1 video.
Uses the 2nd video as an overlay on the 1st video.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _utils__date_time


_os_path = _os.path
_nameof = _varname.core.nameof
_baesname = _os_path.basename(__file__)
_parser = None
_args = None
_command_ffmpeg = None

name_no_ext: str
"""Name of this file without extension."""
name_no_ext, _ = _os_path.splitext(_baesname)
folder_name__data: str = None
"""Folder name of script data."""
file_name__video_output: str = None
"""File name of output video."""
args__overridden: bool = False
"""Whether the arguments are overridden."""
file_name__video_input_1: str = None
"""File name of 1st input video."""
file_name__video_input_2: str = None
"""File name of 2nd input video."""


def _context__create():
    global folder_name__data
    global file_name__video_output

    if folder_name__data is None:
        folder_name__data = _os_path.dirname(__file__)
        folder_name__data = _os_path.join(folder_name__data, f".{name_no_ext}__data")
    # end if

    _os.makedirs(folder_name__data, exist_ok=True)
    timestamp = _utils__date_time.date_time_str_custom__find_for_now()

    if file_name__video_output is None:
        file_name__video_output = _os_path.join(folder_name__data, f"output__{timestamp}.mp4")
    # end if
# end def


def _args_parse():
    global _parser
    global _args
    global file_name__video_input_1
    global file_name__video_input_2

    _parser = _ArgumentParser(
        prog=_baesname,
        usage=\
            f"python {_baesname} [--help]"
            + f" <{_nameof(file_name__video_input_1)}> <{_nameof(file_name__video_input_2)}>"
        ,
        description=\
            "Blends 2 videos into 1 video."
            + " Uses the 2nd video as an overlay on the 1st video."
        ,
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.",
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(file_name__video_input_1)}",
        type=str,
        help="Name of the 1st video.",
        metavar=f"{_nameof(file_name__video_input_1)}"
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(file_name__video_input_2)}",
        type=str,
        help="Name of the 2nd video.",
        metavar=f"{_nameof(file_name__video_input_2)}"
    )
    # end statement

    if not args__overridden:
        _args = _parser.parse_args()

        if file_name__video_input_1 is None:
            file_name__video_input_1 = getattr(_args, _nameof(file_name__video_input_1))
        # end if

        if file_name__video_input_2 is None:
            file_name__video_input_2 = getattr(_args, _nameof(file_name__video_input_2))
        # end if

        file_name__video_input_1 = _os_path.abspath(file_name__video_input_1)
        file_name__video_input_2 = _os_path.abspath(file_name__video_input_2)
    # end if
# end def


def _Video_Blend():
    global _command_ffmpeg
    input_1 = file_name__video_input_1
    input_2 = file_name__video_input_2
    output_1 = file_name__video_output

    _command_ffmpeg = \
        f"ffmpeg" \
        + f" -i \"{input_1}\"" \
        + f" -i \"{input_2}\"" \
        + f" -filter_complex \"" \
        + f"  [0]format=yuvj420p,colorchannelmixer=ar=0:ag=0:ab=0:aa=1[v1];" \
        + f"  [1]format=yuvj420p,colorchannelmixer=ar=2:ag=2:ab=2:aa=0[v2];" \
        + f"  [v2][v1]scale2ref[v2][v1];" \
        + f"  [v1][v2]blend=all_mode=\"addition\":all_opacity=0.65" \
        + f" \"" \
        + f" -pix_fmt yuvj420p" \
        + f" -movflags +faststart" \
        + f" -c:v h264" \
        + f" -profile:v high" \
        + f" \"{output_1}\""
    # end statement

    print(f"{_command_ffmpeg = }")
    _os.system(_command_ffmpeg)
# end def


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_baesname}")
    _context__create()
    _args_parse()
    _Video_Blend()

    print(
        f"{file_name__video_input_1 = :s}\n"
            + f"{file_name__video_input_2 = :s}\n"
            + f"{file_name__video_output = :s}"
        ,
    )
    # end statement

    print(f"end {_baesname}")
# end def


if __name__ == "__main__":
    main()
# end if
