"""
Timed images to MP4.
Converts a sequence of timed images to an MP4 video.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import re as _re
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
images_folder_name = None


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
    global images_folder_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} [--help] <images-folder-name>",
        description="Converts a sequence of timed images to an MP4 video.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _parser.add_argument(
        "images_folder_name",
        type=str,
        help="The folder name of the timed image sequence.",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if images_folder_name is None:
            images_folder_name = _arguments.images_folder_name

        images_folder_name = _os_path.abspath(images_folder_name)


def _generate_concat_demuxer():
    images_isdir = _os_path.isdir(images_folder_name)
    image_file_names = []

    if images_isdir:
        image_file_names = _os.listdir(images_folder_name)
        image_file_names.sort()

    for index, file_name in enumerate(image_file_names):
        image_file_names[index] = _os_path.join(images_folder_name, file_name)

    new_image_file_names = []

    for file_name in image_file_names:
        image_isfile = _os_path.isfile(file_name)
        image_basename = _os_path.basename(file_name)
        _, image_ext = _os_path.splitext(file_name)
        image_ext_matched = image_ext.lower() == ".png"
        image_ext_matched = image_ext_matched or image_ext.lower() == ".jpg"

        if image_isfile and image_ext_matched:
            new_image_file_names.append(file_name)
        # end if
    # end if

    image_file_names = new_image_file_names
    prev_time = float(0)
    curr_time = float(0)
    concat_lines = []

    for index, file_name in enumerate(image_file_names):
        image_basename = _os_path.basename(file_name)
        image_no_ext, _ = _os_path.splitext(image_basename)
        split_groups = _re.split("_+", image_no_ext)

        if \
            len(split_groups) >= 4 \
            and split_groups[0] == "time" \
            and split_groups[2] == "sickness" \
        :
            concat_lines.append(f"file '{file_name}'")
            curr_time = float(split_groups[1])
            duration = curr_time - prev_time
            concat_lines.append(f"duration {duration:6f}")
            prev_time = curr_time
        # end if
    # end for

    concat_str = "\n".join(concat_lines)

    with open(concat_file_name, mode="w", encoding="utf-8") as concat_file:
        concat_file.write(concat_str)
    # end with
# end def


def _convert_images_to_mp4():
    global _ffmpeg_command

    _ffmpeg_command =\
        f"ffmpeg"\
        + f"  -f concat"\
        + f"  -safe 0"\
        + f"  -i \"{concat_file_name}\""\
        + f"  -filter:v fps=30"\
        + f"  -pix_fmt yuvj420p"\
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
    _convert_images_to_mp4()

    print(
        f"{images_folder_name = :s}\n"
        + f"{concat_file_name = :s}\n"
        + f"{mp4_file_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
