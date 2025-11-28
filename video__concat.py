"""
Concatenates a sequence of videos.
Concatenates video in ascending alphanumerical order.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _utils__date_time

_os_path = _os.path
_nameof = _varname.core.nameof
_basename = _os_path.basename(__file__)
_parser = None
_args = None
_command_ffmpeg = None

name_no_ext: str
"""Name of this file without extension."""
name_no_ext, _ = _os_path.splitext(_basename)
folder_name__data: str = None
"""Name of the data folder."""
file_name__concat: str = None
"""Name of the concat demuxer file."""
file_name__video_output: str = None
"""Name of the output video file."""
args__overridden: bool = False
"""Whether the arguments are overridden."""
folder_name__videos_input: str = None
"""Name of the video sequence folder."""


def _context__create():
    global folder_name__data
    global file_name__concat
    global file_name__video_output

    if folder_name__data is None:
        folder_name__data = _os_path.dirname(__file__)
        folder_name__data = _os_path.join(folder_name__data, f".{name_no_ext}__data")
    # end if

    _os.makedirs(folder_name__data, exist_ok=True)
    timestamp = _utils__date_time.date_time_str_custom__find_for_now()

    if file_name__concat is None:
        file_name__concat = _os_path.join(folder_name__data, f"concat__{timestamp}.txt")
    # end if

    if file_name__video_output is None:
        file_name__video_output = _os_path.join(folder_name__data, f"output__{timestamp}.mp4")
    # end if
# end def


def _args__parse():
    global _parser
    global _args
    global folder_name__videos_input

    _parser = _ArgumentParser(
        prog=_basename,
        usage=\
            f"python {_basename} [--help]"
            + f" <{_nameof(folder_name__videos_input)}>"
        ,
        description=\
            "Concatenates a sequence of videos."
            + " Concatenates video in ascending alphanumerical order."
        ,
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.",
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(folder_name__videos_input)}",
        type=str,
        help="Name of the video sequence folder.",
        metavar=f"{_nameof(folder_name__videos_input)}"
    )
    # end statement

    if not args__overridden:
        _args = _parser.parse_args()

        if folder_name__videos_input is None:
            folder_name__videos_input = getattr(_args, _nameof(folder_name__videos_input))
        # end if

        folder_name__videos_input = _os_path.abspath(folder_name__videos_input)
    # end if
# end def


def _concat_demuxer__generate():
    isdir__videos_input = _os_path.isdir(folder_name__videos_input)
    file_names__videos_input = []

    if isdir__videos_input:
        file_names__videos_input = _os.listdir(folder_name__videos_input)
        file_names__videos_input.sort()
    # end if

    for index, file_name in enumerate(file_names__videos_input):
        file_names__videos_input[index] = _os_path.join(folder_name__videos_input, file_name)
    # end for

    new_file_names__videos_input = []

    for file_name in file_names__videos_input:
        isfile = _os_path.isfile(file_name)
        basename = _os_path.basename(file_name)
        _, ext = _os_path.splitext(basename)
        ext__matched = ext.lower() == ".mp4"

        if isfile and ext__matched:
            new_file_names__videos_input.append(file_name)
        # end if
    # end if

    file_names__videos_input = new_file_names__videos_input
    lines__concat = []

    for file_name in file_names__videos_input:
        lines__concat.append(f"file '{file_name}'")
    # end for

    str__concat = "\n".join(lines__concat)

    with open(file_name__concat, mode="w", encoding="utf-8") as file__concat:
        file__concat.write(str__concat)
    # end with
# end def


def _video__concat():
    global _command_ffmpeg

    _command_ffmpeg = \
        f"ffmpeg"\
        + f" -f concat"\
        + f" -safe 0"\
        + f" -i \"{file_name__concat}\""\
        + f" -filter:v fps=30"\
        + f" -pix_fmt yuvj420p"\
        + f" -movflags +faststart"\
        + f" -c:v h264"\
        + f" -profile:v high"\
        + f" \"{file_name__video_output}\""
    # end statement

    print(f"{_command_ffmpeg = }")
    _os.system(_command_ffmpeg)
# end def


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_basename}")
    _context__create()
    _args__parse()
    _concat_demuxer__generate()
    _video__concat()

    print(
        f"{folder_name__videos_input = :s}\n"
            + f"{file_name__concat = :s}\n"
            + f"{file_name__video_output = :s}"
        ,
    )
    # end statement

    print(f"end {_basename}")
# end def


if __name__ == "__main__":
    main()
# end if
