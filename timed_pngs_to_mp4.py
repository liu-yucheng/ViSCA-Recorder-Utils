"""
Timed PNGs to MP4.
Converts a sequence of timed PNG images to an MP4 video.
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
mp4_file_name = None
arguments_overridden = False
pngs_folder_name = None


def _create_context():
    global data_folder_name
    global concat_file_name
    global mp4_file_name

    script_no_ext, _ = _os_path.splitext(_script_basename)

    if data_folder_name is None:
        data_folder_name = _os_path.dirname(__file__)
        data_folder_name = _os_path.join(data_folder_name, f".{script_no_ext}_data")

    _os.makedirs(data_folder_name, exist_ok=True)
    timestamp = _datetime_utils.find_now_custom_date_time_string()

    if concat_file_name is None:
        concat_file_name = _os_path.join(data_folder_name, f"concat-{timestamp}.txt")

    if mp4_file_name is None:
        mp4_file_name = _os_path.join(data_folder_name, f"output-{timestamp}.mp4")


def _parse_arguments():
    global _parser
    global _arguments
    global pngs_folder_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} <pngs-folder-name>",
        description="Converts a sequence of timed PNG images to an MP4 video.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU GPL3/3+ License."
    )

    _parser.add_argument(
        "pngs_folder_name",
        type=str,
        help="The folder name of the PNG timed image sequence",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if pngs_folder_name is None:
            pngs_folder_name = _arguments.pngs_folder_name

        pngs_folder_name = _os_path.abspath(pngs_folder_name)


def _generate_concat_demuxer():
    pngs_isdir = _os_path.isdir(pngs_folder_name)
    png_file_names = []

    if pngs_isdir:
        png_file_names = _os.listdir(pngs_folder_name)
        png_file_names.sort()

    for index, file_name in enumerate(png_file_names):
        png_file_names[index] = _os_path.join(pngs_folder_name, file_name)

    new_png_file_names = []

    for file_name in png_file_names:
        png_isfile = _os_path.isfile(file_name)
        png_basename = _os_path.basename(file_name)
        _, png_ext = _os_path.splitext(file_name)
        png_ext_matched = png_ext.lower() == ".png"

        if png_isfile and png_ext_matched:
            new_png_file_names.append(file_name)
        # end if
    # end if

    png_file_names = new_png_file_names
    prev_ms = 0
    curr_ms = 0
    concat_lines = []

    for file_name in png_file_names:
        concat_lines.append(f"file '{file_name}'")
        png_basename = _os_path.basename(file_name)
        png_no_ext, _ = _os_path.splitext(png_basename)
        curr_ms = int(png_no_ext)
        dur_ms = curr_ms - prev_ms
        dur_secs = dur_ms / 1000
        prev_ms = curr_ms
        concat_lines.append(f"duration {dur_secs:3f}")

    concat_str = "\n".join(concat_lines)

    with open(concat_file_name, mode="w", encoding="utf-8") as concat_file:
        concat_file.write(concat_str)
    # end with
# end def


def _convert_pngs_to_mp4():
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
        + f"  \"{mp4_file_name}\""

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
    _convert_pngs_to_mp4()

    print(
        f"{pngs_folder_name = :s}\n"
        + f"{concat_file_name = :s}\n"
        + f"{mp4_file_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
