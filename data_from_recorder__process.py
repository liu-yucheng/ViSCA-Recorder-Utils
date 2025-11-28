"""
Processes a data folder (from ViSCA Recorder).
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _utils__date_time
import video_from_recorder__batch_convert as _video_from_recorder__batch_convert
import video__concat as _video__concat
import json_from_recorder__concat as _json_from_recorder__concat
import video_from_recorder_with_sickness__batch_convert as _video_from_recorder_with_sickness__batch_convert
import json_from_recorder_with_sickness__concat as _json_from_recorder_with_sickness__concat


_os_path = _os.path
_nameof = _varname.core.nameof
_basename = _os_path.basename(__file__)
_parser = None
_args = None

name_no_ext: str
"""Name of this file without extension."""
name_no_ext, _ = _os_path.splitext(_basename)
folder_name__data: str = None
"""Name of the script data folder."""
folder_name__outputs: str = None
"""Name of the outputs folder."""
folder_name__video_from_recorder__batch_convert: str = None
"""Name of the batch video from recorder images convert folder."""
folder_name__video__concat: str = None
"""Name of the video concat folder."""
folder_name__json_from_recorder__concat: str = None
"""Name of the json from recorder concat folder."""
folder_name__video_from_recorder_with_sickness__batch_convert: str = None
"""Name of the batch video from recorder images with sickness convert folder."""
folder_name__video_with_sickness__concat: str = None
"""Name of the video with sickness concat folder."""
folder_name__json_from_recorder_with_sickness__concat: str = None
"""Name of the json from recorder with sickness concat folder."""
args_overridden: str = False
"""Whether the arguments have been overridden externally."""
folder_name__data_from_recorder: str = None
"""Name of the data folder from recorder."""


def _context__create():
    global folder_name__data
    global folder_name__outputs
    global folder_name__video_from_recorder__batch_convert
    global folder_name__video__concat
    global folder_name__json_from_recorder__concat
    global folder_name__video_from_recorder_with_sickness__batch_convert
    global folder_name__video_with_sickness__concat
    global folder_name__json_from_recorder_with_sickness__concat

    if folder_name__data is None:
        folder_name__data = _os_path.dirname(__file__)
        folder_name__data = _os_path.join(folder_name__data, f".{name_no_ext}__data")
    # end if

    _os.makedirs(folder_name__data, exist_ok=True)
    timestamp = _utils__date_time.date_time_str_custom__find_for_now()

    if folder_name__outputs is None:
        folder_name__outputs = _os_path.join(folder_name__data, f"outputs__{timestamp}")
    # end if

    _os.makedirs(folder_name__outputs, exist_ok=True)

    if folder_name__video_from_recorder__batch_convert is None:
        folder_name__video_from_recorder__batch_convert \
        = _os_path.join(
            folder_name__outputs,
            f".{_video_from_recorder__batch_convert.name_no_ext}__data",
        )
        # end statement
    # end if

    _os.makedirs(folder_name__video_from_recorder__batch_convert, exist_ok=True)

    if folder_name__video__concat is None:
        folder_name__video__concat = \
        _os_path.join(folder_name__outputs, f".{_video__concat.name_no_ext}__data")
        # end statement
    # end if

    _os.makedirs(folder_name__video__concat, exist_ok=True)

    if folder_name__json_from_recorder__concat is None:
        folder_name__json_from_recorder__concat \
        = _os_path.join(folder_name__outputs, f".{_json_from_recorder__concat.name_no_ext}__data")
        # end statement
    # end if

    _os.makedirs(folder_name__json_from_recorder__concat, exist_ok=True)

    if folder_name__video_from_recorder_with_sickness__batch_convert is None:
        folder_name__video_from_recorder_with_sickness__batch_convert \
        = _os_path.join(
            folder_name__outputs,
            f".{_video_from_recorder_with_sickness__batch_convert.name_no_ext}__data",
        )
        # end statement
    # end if

    _os.makedirs(folder_name__video_from_recorder_with_sickness__batch_convert, exist_ok=True)

    if folder_name__video_with_sickness__concat is None:
        folder_name__video_with_sickness__concat \
        = _os_path.join(folder_name__outputs, f".{_video__concat.name_no_ext}__with_sickness__data")
        # end statement
    # end if

    _os.makedirs(folder_name__video_with_sickness__concat, exist_ok=True)

    if folder_name__json_from_recorder_with_sickness__concat is None:
        folder_name__json_from_recorder_with_sickness__concat \
        = _os_path.join(
            folder_name__outputs,
            f".{_json_from_recorder_with_sickness__concat.name_no_ext}__data"
        )
        # end statement
    # end if

    _os.makedirs(folder_name__json_from_recorder_with_sickness__concat, exist_ok=True)
# end def


def _args__parse():
    global _parser
    global _args
    global folder_name__data_from_recorder

    _parser = _ArgumentParser(
        prog=_basename,
        usage=f"python {_basename} [--help] <{_nameof(folder_name__data_from_recorder)}>",
        description="Processes a data folder (from ViSCA Recorder).",
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(folder_name__data_from_recorder)}",
        type=str,
        help="The name of a data folder from ViSCA Recorder.",
        metavar=f"{_nameof(folder_name__data_from_recorder)}"
    )
    # end statement

    if not args_overridden:
        _args = _parser.parse_args()

        if folder_name__data_from_recorder is None:
            folder_name__data_from_recorder = getattr(_args, _nameof(folder_name__data_from_recorder))
        # end if

        folder_name__data_from_recorder = _os_path.abspath(folder_name__data_from_recorder)
    # end if
# end def


def _video_from_recorder__batch_convert__perform():
    _video_from_recorder__batch_convert.folder_name__data = folder_name__video_from_recorder__batch_convert
    _video_from_recorder__batch_convert.folder_name__outputs = folder_name__video_from_recorder__batch_convert
    _video_from_recorder__batch_convert.args__overridden = True
    _video_from_recorder__batch_convert.folder_name__images_nested = folder_name__data_from_recorder
    _video_from_recorder__batch_convert.main()
# end def


def _video__concat__perform():
    file_names__videos_input = _os.listdir(folder_name__video_from_recorder__batch_convert)
    file_names__videos_input.sort()

    for index, file_name in enumerate(file_names__videos_input):
        file_names__videos_input[index] = _os_path.join(folder_name__video_from_recorder__batch_convert, file_name)
    # end for

    new_file_names__videos_input = []

    for file_name in file_names__videos_input:
        basename = _os_path.basename(file_name)
        _, ext = _os_path.splitext(basename)
        ext__matched = ext.lower() == ".mp4"

        if ext__matched:
            new_file_names__videos_input.append(file_name)
        # end if
    # end for

    file_names__videos_input = new_file_names__videos_input

    if len(file_names__videos_input) >= 1:
        basename__video_input_1 = _os_path.basename(file_names__videos_input[0])
    else:
        basename__video_input_1 = "video__empty.mp4"
    # end if

    name_no_ext__video_input_1, _ = _os_path.splitext(basename__video_input_1)
    _video__concat.folder_name__data = folder_name__video__concat

    _video__concat.file_name__concat \
    = _os_path.join(folder_name__video__concat, f"concat__{name_no_ext__video_input_1}.txt")
    # end statement

    _video__concat.file_name__video_output \
    = _os_path.join(folder_name__outputs, f"concat__{name_no_ext__video_input_1}.mp4")
    # end statement

    _video__concat.args__overridden = True
    _video__concat.folder_name__videos_input = folder_name__video_from_recorder__batch_convert
    _video__concat.main()
# end def


def _json_from_recorder__concat__perform():
    file_names__jsons_input = _os.listdir(folder_name__data_from_recorder)
    file_names__jsons_input.sort()

    for index, file_name in enumerate(file_names__jsons_input):
        file_names__jsons_input[index] = _os_path.join(folder_name__data_from_recorder, file_name)
    # end for

    new_file_names__jsons_input = []

    for file_name in file_names__jsons_input:
        basename = _os_path.basename(file_name)
        _, ext = _os_path.splitext(basename)
        ext__matched = ext.lower() == ".json"

        if ext__matched:
            new_file_names__jsons_input.append(file_name)
        # end if
    # end for

    file_names__jsons_input = new_file_names__jsons_input
    basename__json_input_1 = _os_path.basename(file_names__jsons_input[0])
    name_no_ext__json_input_1, _ = _os_path.splitext(basename__json_input_1)

    _json_from_recorder__concat.folder_name__data = folder_name__json_from_recorder__concat

    _json_from_recorder__concat.file_name__json_output \
    = _os_path.join(folder_name__outputs, f"concat__{name_no_ext__json_input_1}.json")
    # end statement

    _json_from_recorder__concat.file_name__json_output_flattened \
    = _os_path.join(folder_name__outputs, f"concat_flattened__{name_no_ext__json_input_1}.json")
    # end statement

    _json_from_recorder__concat.args__overridden = True
    _json_from_recorder__concat.folder_name__jsons_input = folder_name__data_from_recorder
    _json_from_recorder__concat.main()
# end def


def _video_from_recorder_with_sickness__batch_convert__perform(
    time_s__before_sickness: float,
    time_s__after_sickness: float,
) -> None:
    print(
        f"begin {_nameof(_video_from_recorder_with_sickness__batch_convert__perform)}\n"
            + f"{time_s__before_sickness = :.3f}\n"
            + f"{time_s__after_sickness = :.3f}"
        ,
    )
    # end statement

    _video_from_recorder_with_sickness__batch_convert.folder_name__data \
    = folder_name__video_from_recorder_with_sickness__batch_convert
    # end statement

    _video_from_recorder_with_sickness__batch_convert.folder_name__outputs \
    = folder_name__video_from_recorder_with_sickness__batch_convert
    # end statement

    _video_from_recorder_with_sickness__batch_convert.time_s__before_sickness = time_s__before_sickness
    _video_from_recorder_with_sickness__batch_convert.time_s__after_sickness = time_s__after_sickness
    _video_from_recorder_with_sickness__batch_convert.args__overridden = True
    _video_from_recorder_with_sickness__batch_convert.folder_name__images_nested = folder_name__data_from_recorder
    _video_from_recorder_with_sickness__batch_convert.main()
    print(f"end {_nameof(_video_from_recorder_with_sickness__batch_convert__perform)}")
# end def


def _video__concat__with_sickness__perform(
    time_s__before_sickness: float,
    time_s__after_sickness: float,
) -> None:
    print(
        f"begin {_nameof(_video__concat__with_sickness__perform)}\n"
            + f"{time_s__before_sickness = :.3f}\n"
            + f"{time_s__after_sickness = :.3f}"
        ,
    )
    # end statement

    file_names__videos_input = _os.listdir(folder_name__video_from_recorder_with_sickness__batch_convert)
    file_names__videos_input.sort()

    for index, file_name in enumerate(file_names__videos_input):
        file_names__videos_input[index] \
        = _os_path.join(folder_name__video_from_recorder_with_sickness__batch_convert, file_name)
        # end statement
    # end for

    new_file_names__videos_input = []

    for file_name in file_names__videos_input:
        basename = _os_path.basename(file_name)
        _, ext = _os_path.splitext(basename)
        ext__matched = ext.lower() == ".mp4"

        if ext__matched:
            new_file_names__videos_input.append(file_name)
        # end if
    # end for

    file_names__videos_input = new_file_names__videos_input

    if len(file_names__videos_input) >= 1:
        basename__video_input_1 = _os_path.basename(file_names__videos_input[0])
    else:
        basename__video_input_1 = "video__empty.mp4"
    # end if

    name_no_ext__video_input_1, _ = _os_path.splitext(basename__video_input_1)
    _video__concat.folder_name__data = folder_name__video_with_sickness__concat

    _video__concat.file_name__concat \
    = _os_path.join(
        folder_name__video_with_sickness__concat,

        f"concat_with_sickness"
            + f"_before_{time_s__before_sickness:.3f}s"
            + f"_after_{time_s__after_sickness:.3f}s"
            + f"__{name_no_ext__video_input_1}.txt"
        ,
    )
    # end statement

    _video__concat.file_name__video_output \
    = _os_path.join(
        folder_name__outputs,

        f"concat_with_sickness"
            + f"_before_{time_s__before_sickness:.3f}s"
            + f"_after_{time_s__after_sickness:.3f}s"
            + f"__{name_no_ext__video_input_1}.mp4"
        ,
    )
    # end statement

    _video__concat.args__overridden = True
    _video__concat.folder_name__videos_input = folder_name__video_from_recorder_with_sickness__batch_convert
    _video__concat.main()
    print(f"end {_nameof(_video__concat__with_sickness__perform)}")
# end def


def _json_from_recorder_with_sickness__concat__perform(
    time_s__before_sickness: float,
    time_s__after_sickness: float,
) -> None:
    print(
        f"begin {_nameof(_json_from_recorder_with_sickness__concat__perform)}\n"
            + f"{time_s__before_sickness = :.3f}\n"
            + f"{time_s__after_sickness = :.3f}"
        ,
    )
    # end statement

    file_names__jsons_input = _os.listdir(folder_name__data_from_recorder)
    file_names__jsons_input.sort()

    for index, file_name in enumerate(file_names__jsons_input):
        file_names__jsons_input[index] = _os_path.join(folder_name__data_from_recorder, file_name)
    # end for

    new_file_names__jsons_input = []

    for file_name in file_names__jsons_input:
        basename = _os_path.basename(file_name)
        _, ext = _os_path.splitext(basename)
        ext__matched = ext.lower() == ".json"

        if ext__matched:
            new_file_names__jsons_input.append(file_name)
        # end if
    # end for

    file_names__jsons_input = new_file_names__jsons_input
    basename__json_input_1 = _os_path.basename(file_names__jsons_input[0])
    name_no_ext__json_input_1, _ = _os_path.splitext(basename__json_input_1)

    _json_from_recorder_with_sickness__concat.time_s__before_sickness = time_s__before_sickness
    _json_from_recorder_with_sickness__concat.time_s__after_sickness = time_s__after_sickness
    _json_from_recorder_with_sickness__concat.folder_name__data = folder_name__json_from_recorder__concat

    _json_from_recorder_with_sickness__concat.file_name__json_output \
    = _os_path.join(
        folder_name__outputs,

        f"concat_with_sickness"
            + f"_before_{time_s__before_sickness:.3f}s"
            + f"_after_{time_s__after_sickness:.3f}s"
            + f"__{name_no_ext__json_input_1}.json"
        ,
    )
    # end statement

    _json_from_recorder_with_sickness__concat.file_name__json_output_flattened \
    = _os_path.join(
        folder_name__outputs,

        f"concat_flattened_with_sickness"
            + f"_before_{time_s__before_sickness:.3f}s"
            + f"_after_{time_s__after_sickness:.3f}s"
            + f"__{name_no_ext__json_input_1}.json"
        ,
    )
    # end statement

    _json_from_recorder_with_sickness__concat.args__overridden = True
    _json_from_recorder_with_sickness__concat.folder_name__jsons_input = folder_name__data_from_recorder
    _json_from_recorder_with_sickness__concat.main()
    print(f"end {_nameof(_json_from_recorder_with_sickness__concat__perform)}")
# end def


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_basename}")
    _context__create()
    _args__parse()
    _video_from_recorder__batch_convert__perform()
    _video__concat__perform()
    _json_from_recorder__concat__perform()
    _video_from_recorder_with_sickness__batch_convert__perform(3.0, 3.0)
    _video__concat__with_sickness__perform(3.0, 3.0)
    _json_from_recorder_with_sickness__concat__perform(0.5, 0.5)
    _json_from_recorder_with_sickness__concat__perform(3.0, 3.0)

    print(
        f"{folder_name__data_from_recorder = :s}\n"
            + f"{folder_name__outputs = :s}"
        ,
    )
    # end statement

    print(f"end {_basename}")
# end def


if __name__ == "__main__":
    main()
# end if
