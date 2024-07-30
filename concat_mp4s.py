"""
Concatenate MP4s.
Converts a sequence of MP4 videos to an MP4 video by concatenating them.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import _datetime_utils


_os_path = _os.path
_script_basename = _os_path.basename(__file__)
_parser = None
_arguments = None
_ffmpeg_command = None

data_folder_name = None
concat_file_name = None
mp4_out_file_name = None
arguments_overridden = False
mp4s_in_folder_name = None


def _create_context():
    global data_folder_name
    global concat_file_name
    global mp4_out_file_name

    script_no_ext, _ = _os_path.splitext(_script_basename)

    if data_folder_name is None:
        data_folder_name = _os_path.dirname(__file__)
        data_folder_name = _os_path.join(data_folder_name, f".{script_no_ext}_data")

    _os.makedirs(data_folder_name, exist_ok=True)
    timestamp = _datetime_utils.find_now_custom_date_time_string()

    if concat_file_name is None:
        concat_file_name = _os_path.join(data_folder_name, f"concat-{timestamp}.txt")

    if mp4_out_file_name is None:
        mp4_out_file_name = _os_path.join(data_folder_name, f"output-{timestamp}.mp4")


def _parse_arguments():
    global _parser
    global _arguments
    global mp4s_in_folder_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} [--help] <mp4s-in-folder-name>",
        description="Converts a sequence of MP4 videos to an MP4 video by concatenating them.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _parser.add_argument(
        "mp4s_in_folder_name",
        type=str,
        help="The folder name of the MP4 video sequence.",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if mp4s_in_folder_name is None:
            mp4s_in_folder_name = _arguments.mp4s_in_folder_name

        mp4s_in_folder_name = _os_path.abspath(mp4s_in_folder_name)


def _generate_concat_demuxer():
    mp4s_isdir = _os_path.isdir(mp4s_in_folder_name)
    mp4_in_file_names = []

    if mp4s_isdir:
        mp4_in_file_names = _os.listdir(mp4s_in_folder_name)
        mp4_in_file_names.sort()

    for index, file_name in enumerate(mp4_in_file_names):
        mp4_in_file_names[index] = _os_path.join(mp4s_in_folder_name, file_name)

    new_mp4_file_names = []

    for file_name in mp4_in_file_names:
        mp4_isfile = _os_path.isfile(file_name)
        mp4_basename = _os_path.basename(file_name)
        _, mp4_ext = _os_path.splitext(mp4_basename)
        mp4_ext_matched = mp4_ext.lower() == ".mp4"

        if mp4_isfile and mp4_ext_matched:
            new_mp4_file_names.append(file_name)
        # end if
    # end if

    mp4_in_file_names = new_mp4_file_names
    concat_lines = []

    for file_name in mp4_in_file_names:
        concat_lines.append(f"file '{file_name}'")

    concat_str = "\n".join(concat_lines)

    with open(concat_file_name, mode="w", encoding="utf-8") as concat_file:
        concat_file.write(concat_str)
    # end with
# end def


def _concat_mp4s():
    global _ffmpeg_command

    _ffmpeg_command =\
        f"ffmpeg"\
        + f"  -f concat"\
        + f"  -safe 0"\
        + f"  -i \"{concat_file_name}\""\
        + f"  -filter:v fps=30"\
        + f"  -pix_fmt yuv420p"\
        + f"  -movflags +faststart"\
        + f"  -c:v h264"\
        + f"  -profile:v high"\
        + f"  \"{mp4_out_file_name}\""

    print(f"{_ffmpeg_command = }")
    _os.system(_ffmpeg_command)


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_script_basename}")
    _create_context()
    _parse_arguments()
    _generate_concat_demuxer()
    _concat_mp4s()

    print(
        f"{mp4s_in_folder_name = :s}\n"
        + f"{concat_file_name = :s}\n"
        + f"{mp4_out_file_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
