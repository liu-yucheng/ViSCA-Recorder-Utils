"""
Performs a batch of "./video_from_recorder_with_sickness__convert.py" operations.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import video_from_recorder_with_sickness__convert as _video_from_recorder_with_sickness__convert
import _utils__date_time


_os_path = _os.path
_nameof = _varname.core.nameof
_basename = _os_path.basename(__file__)
_parser = None
_args = None
_folder_names__images = None

name_no_ext: str
"""Name of this file without extension."""
name_no_ext, _ = _os_path.splitext(_basename)
folder_name__data: str = None
"""Folder name of script data."""
folder_name__outputs: str = None
"""Folder name of script outputs."""
time_s__before_sickness: float = None
"""Time in seconds before sickness clips."""
time_s__after_sickness: float = None
"""Time in seconds after sickness clips."""
args__overridden: bool = False
"""Whether the arguments are overridden."""
folder_name__images_nested: str = None
"""Folder name of nested images."""


def _context__create():
    global folder_name__data
    global folder_name__outputs
    global time_s__before_sickness
    global time_s__after_sickness

    if folder_name__data is None:
        folder_name__data = _os_path.dirname(__file__)
        folder_name__data = _os_path.join(folder_name__data, f".{name_no_ext}__data")
    # end if

    _os.makedirs(folder_name__data, exist_ok=True)
    timestamp = _utils__date_time.date_time_str_custom__find_for_now()

    if folder_name__outputs is None:
        folder_name__outputs = _os_path.join(folder_name__data, f"output__{timestamp}")
    # end if

    _os.makedirs(folder_name__outputs, exist_ok=True)

    if time_s__before_sickness is None:
        time_s__before_sickness = 3.0
    # end if

    if time_s__after_sickness is None:
        time_s__after_sickness = 3.0
    # end if
# end def


def _args__parse():
    global _parser
    global _args
    global folder_name__images_nested

    _parser = _ArgumentParser(
        prog=_basename,
        usage=f"python {_basename} [--help] <{_nameof(folder_name__images_nested)}>",
        description="Performs a batch of \"./video_from_recorder_with_sickness__convert.py\" operations.",
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.",
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(folder_name__images_nested)}",
        type=str,
        help="Name of the folder that contains multiple image folders.",
        metavar=f"{_nameof(folder_name__images_nested)}"
    )
    # end statement

    if not args__overridden:
        _args = _parser.parse_args()

        if folder_name__images_nested is None:
            folder_name__images_nested = getattr(_args, _nameof(folder_name__images_nested))
        # end if

        folder_name__images_nested = _os_path.abspath(folder_name__images_nested)
    # end if
# end def


def _image_folders__probe():
    global _folder_names__images

    _folder_names__images = []
    isdir__images_nested = _os_path.isdir(folder_name__images_nested)

    if isdir__images_nested:
        _folder_names__images = _os.listdir(folder_name__images_nested)
        _folder_names__images.sort()
    # end if

    for index, folder_name in enumerate(_folder_names__images):
        _folder_names__images[index] = _os_path.join(folder_name__images_nested, folder_name)
    # end for

    new_folder_names__images = []

    for folder_name in _folder_names__images:
        isdir = _os_path.isdir(folder_name)

        if isdir:
            new_folder_names__images.append(folder_name)
        # end if
    # end for

    _folder_names__images = new_folder_names__images
# end def


def _batch_ops__perform():
    print(f"begin {_nameof(_batch_ops__perform)}")

    for index, folder_name in enumerate(_folder_names__images):
        print(f"begin Operation {index + 1} / {len(_folder_names__images)}")
        basename = _os_path.basename(folder_name)
        _video_from_recorder_with_sickness__convert.time_s__before_sickness = time_s__before_sickness
        _video_from_recorder_with_sickness__convert.time_s__after_sickness = time_s__after_sickness
        _video_from_recorder_with_sickness__convert.max_time_s__between_clips = 3.0
        _video_from_recorder_with_sickness__convert.folder_name__data = folder_name__outputs

        _video_from_recorder_with_sickness__convert.file_name__concat \
        = _os_path.join(folder_name__outputs, f"{basename}.txt")
        # end statement

        _video_from_recorder_with_sickness__convert.file_name__video \
        = _os_path.join(folder_name__outputs, f"{basename}.mp4")
        # end statement

        _video_from_recorder_with_sickness__convert.args__overridden = True
        _video_from_recorder_with_sickness__convert.folder_name__images = folder_name
        _video_from_recorder_with_sickness__convert.main()
        print(f"end Operation {index + 1} / {len(_folder_names__images)}")
    # end for

    print(f"end {_nameof(_batch_ops__perform)}")
# end def


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_basename}")
    _context__create()
    _args__parse()
    _image_folders__probe()
    _batch_ops__perform()

    print(
        f"{folder_name__images_nested = :s}\n"
            + f"{folder_name__outputs = :s}\n"
            + f"{time_s__before_sickness = :.3f}\n"
            + f"{time_s__after_sickness = :.3f}\n"
        ,
    )
    # end statement

    print(f"end {_basename}")


if __name__ == "__main__":
    main()
