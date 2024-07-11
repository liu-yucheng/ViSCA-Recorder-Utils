"""
Timed PNGs to MP4.
Converts a sequence of timed PNG images to an MP4 video.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import _date_time_utils


_os_path = _os.path
_data_folder_name = None
_concat_file_name = None
_mp4_file_name = None
_parser = None
_arguments = None
_override_arguments = False
_pngs_folder_name = None


def _create_context():
    global _data_folder_name
    global _concat_file_name
    global _mp4_file_name

    if _data_folder_name is None:
        _data_folder_name = _os_path.dirname(__file__)
        _data_folder_name = _os_path.join(_data_folder_name, ".timed_pngs_to_mp4_data")

    print(f"{_data_folder_name = }")
    _os.makedirs(_data_folder_name, exist_ok=True)
    timestamp = _date_time_utils.find_now_custom_date_time_string()

    if _concat_file_name is None:
        _concat_file_name = _os_path.join(_data_folder_name, f"concat-{timestamp}.txt")

    print(f"{_concat_file_name = }")

    if _mp4_file_name is None:
        _mp4_file_name = _os_path.join(_data_folder_name, f"output-{timestamp}.mp4")

    print(f"{_mp4_file_name = }")


def _parse_arguments():
    global _parser
    global _arguments
    global _pngs_folder_name

    _parser = _ArgumentParser(
        prog="timed_pngs_to_mp4.py",
        usage="python timed_pngs_to_mp4.py <pngs-folder-name>",
        description="Converts a sequence of timed PNG images to an MP4 video.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU GPL3/3+ License."
    )

    _parser.add_argument(
        "pngs_folder_name",
        type=str,
        help="The folder name of the PNG timed image sequence",
        metavar="string"
    )

    if not _override_arguments:
        _arguments = _parser.parse_args()

        if _pngs_folder_name is None:
            _pngs_folder_name = _arguments.pngs_folder_name

        _pngs_folder_name = _os_path.abspath(_pngs_folder_name)

    print(f"{_pngs_folder_name = }")


def _generate_concat_demuxer():
    pngs_exists = _os_path.exists(_pngs_folder_name)
    pngs_isdir = _os_path.isdir(_pngs_folder_name)
    png_file_names = []

    if pngs_exists and pngs_isdir:
        png_file_names = _os.listdir(_pngs_folder_name)

    for index, png_file_name in enumerate(png_file_names):
        png_file_names[index] = _os_path.join(_pngs_folder_name, png_file_name)

    new_png_file_names = []

    for png_file_name in png_file_names:
        png_exists = _os_path.exists(png_file_name)
        png_isfile = _os_path.isfile(png_file_name)

        if png_exists and png_isfile:
            new_png_file_names.append(png_file_name)
        # end if
    # end if

    png_file_names = new_png_file_names
    prev_ms = 0
    curr_ms = 0
    concat_lines = []

    for png_file_name in png_file_names:
        concat_lines.append(f"file '{png_file_name}'")
        png_basename = _os_path.basename(png_file_name)
        png_basename_no_ext, _ = _os_path.splitext(png_basename)
        curr_ms = int(png_basename_no_ext)
        dur_ms = curr_ms - prev_ms
        dur_secs = dur_ms / 1000
        prev_ms = curr_ms
        concat_lines.append(f"duration {dur_secs:3f}")

    concat_str = "\n".join(concat_lines)

    with open(_concat_file_name, mode="w", encoding="utf-8") as concat_file:
        concat_file.write(concat_str)
    # end with


def _convert_pngs_to_mp4():
    command =\
        f"ffmpeg"\
        + f"  -f concat"\
        + f"  -safe 0"\
        + f"  -i \"{_concat_file_name}\""\
        + f"  -filter:v fps=30"\
        + f"  -pix_fmt yuv420p"\
        + f"  -movflags +faststart"\
        + f"  -c:v h264"\
        + f"  -profile:v high"\
        + f"  \"{_mp4_file_name}\""

    print(f"{command=}")
    _os.system(command)


def main():
    """
    Starts the main procedure.
    """
    print("begin Timed PNGs to MP4")
    _create_context()
    _parse_arguments()
    _generate_concat_demuxer()
    _convert_pngs_to_mp4()
    print("end Timed PNGs to MP4")


if __name__ == "__main__":
    main()
