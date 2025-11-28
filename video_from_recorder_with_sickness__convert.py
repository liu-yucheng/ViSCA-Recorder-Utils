"""
Converts an image sequence (from ViSCA Recorder) to a video (includes clips with sickness only).
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import re as _re
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
time_s__before_sickness: float = None
"""Time in seconds before sickness to include in the video."""
time_s__after_sickness: float = None
"""Time in seconds after sickness to include in the video."""
max_time_s__between_clips: float = None
"""Maximum time in seconds between clips."""
sickness_threshold: float = None
"""Sickness threshold to include in the video."""
folder_name__data: str = None
"""Folder name of script data."""
file_name__concat: str = None
"""File name of the concat demuxer file."""
file_name__video: str = None
"""File name of the output video."""
args__overridden: bool = False
"""Whether the arguments are overridden."""
folder_name__images: str = None
"""Folder name of the image sequence."""


def _context__create():
    global time_s__before_sickness
    global time_s__after_sickness
    global sickness_threshold
    global max_time_s__between_clips
    global folder_name__data
    global file_name__concat
    global file_name__video

    if time_s__before_sickness is None:
        time_s__before_sickness = 3.0
    # end if

    if time_s__after_sickness is None:
        time_s__after_sickness = 3.0
    # end if

    if sickness_threshold is None:
        sickness_threshold = 0.75
    # end if

    if max_time_s__between_clips is None:
        max_time_s__between_clips = 3.0
    # end if

    if folder_name__data is None:
        folder_name__data = _os_path.dirname(__file__)
        folder_name__data = _os_path.join(folder_name__data, f".{name_no_ext}__data")
    # end if

    _os.makedirs(folder_name__data, exist_ok=True)
    timestamp = _utils__date_time.date_time_str_custom__find_for_now()

    if file_name__concat is None:
        file_name__concat = _os_path.join(folder_name__data, f"concat__{timestamp}.txt")
    # end if

    if file_name__video is None:
        file_name__video = _os_path.join(folder_name__data, f"output__{timestamp}.mp4")
    # end if
# end def


def _args__parse():
    global _parser
    global _args
    global folder_name__images

    _parser = _ArgumentParser(
        prog=_basename,
        usage=f"python {_basename} [--help] <{_nameof(folder_name__images)}>",
        description=\
            "Converts an image sequence (from ViSCA Recorder) to a video"
            + " (includes clips with sickness only)."
        ,
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(folder_name__images)}",
        type=str,
        help="Name of the image sequence folder.",
        metavar=f"{_nameof(folder_name__images)}"
    )
    # end statement

    if not args__overridden:
        _args = _parser.parse_args()

        if folder_name__images is None:
            folder_name__images = getattr(_args, _nameof(folder_name__images))
        # end if

        folder_name__images = _os_path.abspath(folder_name__images)
    # end if
# end def


def _concat_demuxer__generate():
    isdir__images = _os_path.isdir(folder_name__images)
    file_names__images = []

    if isdir__images:
        file_names__images = _os.listdir(folder_name__images)
        file_names__images.sort()
    # end if

    for index, image_name in enumerate(file_names__images):
        file_names__images[index] = _os_path.join(folder_name__images, image_name)
    # end for

    new_file_names__images = []

    for image_name in file_names__images:
        isfile = _os_path.isfile(image_name)
        basename = _os_path.basename(image_name)
        _, ext = _os_path.splitext(image_name)
        ext__matched = ext.lower() == ".png" or ext.lower() == ".jpg"

        if isfile and ext__matched:
            new_file_names__images.append(image_name)
        # end if
    # end if

    file_names__images = new_file_names__images
    print("begin Recording image time and sickness")
    name_to_time__images = {}
    name_to_sickness__images = {}

    for index, image_name in enumerate(file_names__images):
        basename = _os_path.basename(image_name)
        name_no_ext, _ = _os_path.splitext(basename)
        basename_split = _re.split("_+", name_no_ext)

        basename__matched \
        = len(basename_split) >= 4 and basename_split[0] == "time" and basename_split[2] == "sickness"
        # end statement

        if basename__matched:
            time_ = float(basename_split[1])
            sickness = float(basename_split[3])
            name_to_time__images[image_name] = time_
            name_to_sickness__images[image_name] = sickness
        # end if
    # end for

    print("end Recording image time and sickness")
    print("begin Filtering on-sickness images")
    names_dict__images_on_sickness = {}
    name_to_time__images_on_sickness = {}

    for index, image_name in enumerate(file_names__images):
        time_ = name_to_time__images[image_name]
        sickness = name_to_sickness__images[image_name]

        if sickness >= sickness_threshold:
            if image_name not in names_dict__images_on_sickness:
                names_dict__images_on_sickness[image_name] = None
            # end if

            if image_name not in name_to_time__images_on_sickness:
                name_to_time__images_on_sickness[image_name] = time_
            # end if
        # end if
    # end for

    print("end Filtering on-sickness images")
    print("begin Filtering before-sickness images")
    names_dict__images_before_sickness = {}
    name_to_time__images_before_sickness = {}

    for index, image_name in enumerate(file_names__images):
        if image_name in names_dict__images_on_sickness:
            time_ = name_to_time__images[image_name]
            index_trace = index
            file_name_trace__image = image_name
            time_trace = time_

            while time_ - time_trace < time_s__before_sickness and index_trace >= 0:
                file_name_trace__image = file_names__images[index_trace]
                time_trace = name_to_time__images[file_name_trace__image]

                if file_name_trace__image not in names_dict__images_before_sickness:
                    names_dict__images_before_sickness[file_name_trace__image] = None
                # end if

                if file_name_trace__image not in name_to_time__images_before_sickness:
                    name_to_time__images_before_sickness[file_name_trace__image] = time_trace
                # end if

                index_trace -= 1
            # end while
        # end if
    # end for

    print("end Filtering before-sickness images")
    print("begin Filtering after-sickness images")
    names_dict__images_after_sickness = {}
    name_to_time__images_after_sickness = {}

    for index, image_name in enumerate(file_names__images):
        if image_name in names_dict__images_on_sickness:
            time_ = name_to_time__images[image_name]
            index_trace = index
            file_name_trace__image = image_name
            time_trace = time_

            while time_trace - time_ < time_s__after_sickness and index_trace < len(file_names__images):
                file_name_trace__image = file_names__images[index_trace]
                time_trace = name_to_time__images[file_name_trace__image]

                if file_name_trace__image not in names_dict__images_after_sickness:
                    names_dict__images_after_sickness[file_name_trace__image] = None
                # end if

                if file_name_trace__image not in name_to_time__images_after_sickness:
                    name_to_time__images_after_sickness[file_name_trace__image] = time_trace
                # end if

                index_trace += 1
            # end while
        # end if
    # end for

    print("end Filtering after-sickness images")
    print("begin Composing with-sickness images")

    file_names__images_with_sickness = list(names_dict__images_on_sickness.keys()) \
        + list(names_dict__images_before_sickness.keys()) \
        + list(names_dict__images_after_sickness.keys())
    # end statement

    file_names__images_with_sickness.sort()
    name_to_time__images_with_sickness = {}

    for key, item in name_to_time__images_on_sickness.items():
        name_to_time__images_with_sickness[key] = item
    # end for

    for key, item in name_to_time__images_before_sickness.items():
        name_to_time__images_with_sickness[key] = item
    # end for

    for key, item in name_to_time__images_after_sickness.items():
        name_to_time__images_with_sickness[key] = item
    # end for

    print("end Composing with-sickness images")
    time_s__curr = float(0)
    time_s__prev = float(0)
    lines__concat = []

    for index, image_name in enumerate(file_names__images_with_sickness):
        time_s__curr = name_to_time__images_with_sickness[image_name]

        if time_s__curr - time_s__prev > max_time_s__between_clips:
            time_s__prev = time_s__curr - max_time_s__between_clips
        # end if

        lines__concat.append(f"file '{image_name}'")
        time_s__between = time_s__curr - time_s__prev
        lines__concat.append(f"duration {time_s__between:6f}")
        time_s__prev = time_s__curr
    # end for

    str__concat = "\n".join(lines__concat)

    with open(file_name__concat, mode="w", encoding="utf-8") as file__concat:
        file__concat.write(str__concat)
    # end with
# end def


def _video__convert():
    global _command_ffmpeg

    _command_ffmpeg = \
        f"ffmpeg" \
        + f" -f concat" \
        + f" -safe 0" \
        + f" -i \"{file_name__concat}\"" \
        + f" -filter:v fps=30" \
        + f" -pix_fmt yuvj420p" \
        + f" -movflags +faststart" \
        + f" -c:v h264" \
        + f" -profile:v high" \
        + f" \"{file_name__video}\""
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
    _video__convert()

    print(
        f"{time_s__before_sickness = }\n"
            + f"{time_s__after_sickness = }\n"
            + f"{max_time_s__between_clips = }\n"
            + f"{folder_name__images = :s}\n"
            + f"{file_name__concat = :s}\n"
            + f"{file_name__video = :s}"
        ,
    )
    # end statement

    print(f"end {_basename}")
# end def


if __name__ == "__main__":
    main()
# end if
