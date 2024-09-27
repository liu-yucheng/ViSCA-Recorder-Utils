"""
Batch timed images to MP4.
Performs a batch of "timed images to MP4" operations.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import timed_images_to_mp4 as _timed_images_to_mp4
import _datetime_utils


_os_path = _os.path
_script_basename = _os_path.basename(__file__)
_parser = None
_arguments = None
_images_folder_names = None

data_folder_name = None
output_folder_name = None
arguments_overridden = False
nested_images_folder_name = None


def _create_context():
    global data_folder_name
    global output_folder_name

    script_no_ext, _ = _os_path.splitext(_script_basename)

    if data_folder_name is None:
        data_folder_name = _os_path.dirname(__file__)
        data_folder_name = _os_path.join(data_folder_name, f".{script_no_ext}_data")

    _os.makedirs(data_folder_name, exist_ok=True)
    timestamp = _datetime_utils.find_now_custom_date_time_string()

    if output_folder_name is None:
        output_folder_name = _os_path.join(data_folder_name, f"output-{timestamp}")

    _os.makedirs(output_folder_name, exist_ok=True)


def _parse_arguments():
    global _parser
    global _arguments
    global nested_images_folder_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} [--help] <nested-images-folder-name>",
        description="Performs a batch of \"timed images to MP4\" operations.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _parser.add_argument(
        "nested_images_folder_name",
        type=str,
        help="The name of the folder that contains multiple timed image folders.",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if nested_images_folder_name is None:
            nested_images_folder_name = _arguments.nested_images_folder_name

        nested_images_folder_name = _os_path.abspath(nested_images_folder_name)


def _probe_timed_image_folders():
    global _images_folder_names

    _images_folder_names = []
    nested_isdir = _os_path.isdir(nested_images_folder_name)

    if nested_isdir:
        _images_folder_names = _os.listdir(nested_images_folder_name)
        _images_folder_names.sort()

    for index, folder_name in enumerate(_images_folder_names):
        _images_folder_names[index] = _os_path.join(nested_images_folder_name, folder_name)

    new_images_folder_names = []

    for folder_name in _images_folder_names:
        folder_isdir = _os_path.isdir(folder_name)

        if folder_isdir:
            new_images_folder_names.append(folder_name)
        # end if
    # end for

    _images_folder_names = new_images_folder_names


def _perform_batch_operations():
    print("begin Batch operations")

    for index, folder_name in enumerate(_images_folder_names):
        print(f"begin Operation {index + 1} / {len(_images_folder_names)}")
        folder_basename = _os_path.basename(folder_name)
        _timed_images_to_mp4.data_folder_name = output_folder_name
        _timed_images_to_mp4.concat_file_name = _os_path.join(output_folder_name, f"{folder_basename}.txt")
        _timed_images_to_mp4.mp4_file_name = _os_path.join(output_folder_name, f"{folder_basename}.mp4")
        _timed_images_to_mp4.arguments_overridden = True
        _timed_images_to_mp4.images_folder_name = folder_name
        _timed_images_to_mp4.main()
        print(f"end Operation {index + 1} / {len(_images_folder_names)}")

    print("end Batch operations")


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_script_basename}")
    _create_context()
    _parse_arguments()
    _probe_timed_image_folders()
    _perform_batch_operations()

    print(
        f"{nested_images_folder_name = :s}\n"
        + f"{output_folder_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
