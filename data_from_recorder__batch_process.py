"""
Performs a batch of "./data_from_recorder__process.py" operations.
"""

# Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import _utils__date_time
import data_from_recorder__process as _data_from_recorder__process


_os_path = _os.path
_nameof = _varname.core.nameof
_basename = _os_path.basename(__file__)
_parser = None
_args = None
_folder_names__data_from_recorder = None

name_no_ext: str
"""Name of this file without extension."""
name_no_ext, _ = _os_path.splitext(_basename)
folder_name__data: str = None
"""Name of the script data folder."""
folder_name__outputs: str = None
"""Name of the outputs folder."""
args_overridden: bool = False
"""Whether the arguments have been overridden externally."""
folder_name__batch_data_from_recorder: str = None
"""Name of the batch recorder data folder."""


def _context__create():
    global folder_name__data
    global folder_name__outputs

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
# end def


def _args_parse():
    global _parser
    global _args
    global folder_name__batch_data_from_recorder

    _parser = _ArgumentParser(
        prog=_basename,
        usage=f"python {_basename} [--help] <{_nameof(folder_name__batch_data_from_recorder)}>",
        description="Performs a batch of \"./data_from_recorder__process.py\" operations.",
        epilog="Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.",
    )
    # end statement

    _parser.add_argument(
        f"{_nameof(folder_name__batch_data_from_recorder)}",
        type=str,
        help="Name of the folder that contains multiple ViSCA Recorder data folders.",
        metavar=f"{_nameof(folder_name__batch_data_from_recorder)}"
    )
    # end statement

    if not args_overridden:
        _args = _parser.parse_args()

        if folder_name__batch_data_from_recorder is None:
            folder_name__batch_data_from_recorder \
            = getattr(_args, _nameof(folder_name__batch_data_from_recorder))
            # end statement
        # end if

        folder_name__batch_data_from_recorder = _os_path.abspath(folder_name__batch_data_from_recorder)
    # end if
# end def


def _folder_names__data_from_recorder__probe():
    global _folder_names__data_from_recorder
    _folder_names__data_from_recorder = []
    isdir__batch_data = _os_path.isdir(folder_name__batch_data_from_recorder)

    if isdir__batch_data:
        _folder_names__data_from_recorder = _os.listdir(folder_name__batch_data_from_recorder)
        _folder_names__data_from_recorder.sort()
    # end if

    for index, folder_name in enumerate(_folder_names__data_from_recorder):
        _folder_names__data_from_recorder[index] \
        = _os_path.join(folder_name__batch_data_from_recorder, folder_name)
        # end statement
    # end for

    new_folder_names__data_from_recorder = []

    for folder_name in _folder_names__data_from_recorder:
        isdir__folder = _os_path.isdir(folder_name)

        if isdir__folder:
            new_folder_names__data_from_recorder.append(folder_name)
        # end if
    # end for

    _folder_names__data_from_recorder = new_folder_names__data_from_recorder
# end def


def _batch_ops__perform():
    print(f"begin {_nameof(_batch_ops__perform)}")

    for index, folder_name in enumerate(_folder_names__data_from_recorder):
        print(f"begin Operation {index + 1} / {len(_folder_names__data_from_recorder)}")
        basename__folder = _os_path.basename(folder_name)

        _data_from_recorder__process.folder_name__data \
        = f".{_data_from_recorder__process.name_no_ext}__{basename__folder}__data"
        # end statement

        _data_from_recorder__process.folder_name__data \
        = _os_path.join(folder_name__outputs, _data_from_recorder__process.folder_name__data)
        # end statement

        _data_from_recorder__process.folder_name__outputs = f"visca_recorder_utils__{basename__folder}"

        _data_from_recorder__process.folder_name__outputs \
        = _os_path.join(folder_name__outputs, _data_from_recorder__process.folder_name__outputs)
        # end statement

        _data_from_recorder__process.folder_name__video_from_recorder__batch_convert \
        = _os_path.join(_data_from_recorder__process.folder_name__data,".video_from_recorder__batch_convert__data")
        # end statement

        _data_from_recorder__process.folder_name__video__concat \
        = _os_path.join(_data_from_recorder__process.folder_name__data, ".video__concat__data")
        # end statement

        _data_from_recorder__process.folder_name__json_from_recorder__concat \
        = _os_path.join(_data_from_recorder__process.folder_name__data, ".json_from_recorder__concat__data")
        # end statement

        _data_from_recorder__process.folder_name__video_from_recorder_with_sickness__batch_convert \
        = _os_path.join(
            _data_from_recorder__process.folder_name__data,
            ".video_from_recorder_with_sickness__batch_convert__data",
        )
        # end statement

        _data_from_recorder__process.folder_name__video_with_sickness__concat \
        = _os_path.join(_data_from_recorder__process.folder_name__data, ".video_with_sickness__concat__data")
        # end statement

        _data_from_recorder__process.folder_name__json_from_recorder_with_sickness__concat \
        = _os_path.join(
            _data_from_recorder__process.folder_name__data,
            ".json_from_recorder_with_sickness__concat__data",
        )
        # end statement

        _data_from_recorder__process.args_overridden = True
        _data_from_recorder__process.folder_name__data_from_recorder = folder_name
        _data_from_recorder__process.main()
        print(f"end Operation {index + 1} / {len(_folder_names__data_from_recorder)}")
    # end for

    print(f"end {_nameof(_batch_ops__perform)}")
# end def


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_basename}")
    _context__create()
    _args_parse()
    _folder_names__data_from_recorder__probe()
    _batch_ops__perform()

    print(
        f"{folder_name__batch_data_from_recorder = :s}\n"
            + f"{folder_name__outputs = :s}"
        ,
    )
    # end statement

    print(f"end {_basename}")
# end def


if __name__ == "__main__":
    main()
# end if
