"""
Batch timed PNGs to MP4.
Performs a batch of "timed PNGs to MP4" operations.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import timed_pngs_to_mp4 as _timed_pngs_to_mp4
import _date_time_utils


_os_path = _os.path
_data_folder_name = None
_output_folder_name = None
_parser = None
_arguments = None
_override_arguments = False
_nested_pngs_folder_name = None
_pngs_folder_names = None


def _create_context():
    global _data_folder_name
    global _output_folder_name

    if _data_folder_name is None:
        _data_folder_name = _os_path.dirname(__file__)
        _data_folder_name = _os_path.join(_data_folder_name, ".batch_timed_pngs_to_mp4_data")

    print(f"{_data_folder_name = }")
    # _os.makedirs(_data_folder_name, exist_ok=True)
    timestamp = _date_time_utils.find_now_custom_date_time_string()

    if _output_folder_name is None:
        _output_folder_name = _os_path.join(_data_folder_name, f"output-{timestamp}")

    print(f"{_output_folder_name = }")
    _os.makedirs(_output_folder_name, exist_ok=True)


def _parse_arguments():
    global _parser
    global _arguments
    global _nested_pngs_folder_name

    _parser = _ArgumentParser(
        prog="batch_timed_pngs_to_mp4.py",
        usage="python batch_timed_pngs_to_mp4.py <nested-pngs-folder-name>",
        description="Performs a batch of \"timed PNGs to MP4\" operations.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU GPL3/3+ License."
    )

    _parser.add_argument(
        "nested_pngs_folder_name",
        type=str,
        help="The name of the folder that contains multiple PNG timed image folders.",
        metavar="string"
    )

    if not _override_arguments:
        _arguments = _parser.parse_args()

        if _nested_pngs_folder_name is None:
            _nested_pngs_folder_name = _arguments.nested_pngs_folder_name

        _nested_pngs_folder_name = _os_path.abspath(_nested_pngs_folder_name)

    print(f"{_nested_pngs_folder_name = }")


def _probe_timed_png_folders():
    global _pngs_folder_names

    nested_exist = _os_path.exists(_nested_pngs_folder_name)
    nested_isdir = _os_path.isdir(_nested_pngs_folder_name)
    subfolder_names = []

    if nested_exist and nested_isdir:
        subfolder_names = _os.listdir(_nested_pngs_folder_name)

    if _pngs_folder_names is None:
        _pngs_folder_names = []

    if isinstance(_pngs_folder_names, list):
        _pngs_folder_names.clear()

    for subfolder_name in subfolder_names:
        subfolder_name = _os_path.join(_nested_pngs_folder_name, subfolder_name)
        subfolder_isdir = _os_path.isdir(subfolder_name)

        if subfolder_isdir:
            _pngs_folder_names.append(subfolder_name)
        # end if
    # end for

    print(f"{_pngs_folder_names = }")


def _perform_batch_operations():
    print(f"begin Batch operations")

    for index, pngs_folder_name in enumerate(_pngs_folder_names):
        print(f"begin Operation {index + 1}/{len(_pngs_folder_names)}")
        pngs_folder_base_name = _os_path.basename(pngs_folder_name)
        _timed_pngs_to_mp4._data_folder_name = _output_folder_name
        _timed_pngs_to_mp4._concat_file_name = _os_path.join(_output_folder_name, f"{pngs_folder_base_name}.txt")
        _timed_pngs_to_mp4._mp4_file_name = _os_path.join(_output_folder_name, f"{pngs_folder_base_name}.mp4")
        _timed_pngs_to_mp4._override_arguments = True
        _timed_pngs_to_mp4._pngs_folder_name = pngs_folder_name
        _timed_pngs_to_mp4.main()
        print(f"end Operation {index + 1}/{len(_pngs_folder_names)}")

    print(f"end Batch operations")


def main():
    """
    Starts the main procedure.
    """
    print("begin Batch timed PNGs to MP4")
    _create_context()
    _parse_arguments()
    _probe_timed_png_folders()
    _perform_batch_operations()
    print("end Batch timed PNGs to MP4")


if __name__ == "__main__":
    main()
