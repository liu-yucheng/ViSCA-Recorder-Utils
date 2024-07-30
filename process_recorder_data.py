"""
Process recorder data.
Processes a folder of ViSCA Recorder data.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import _datetime_utils
import batch_timed_pngs_to_mp4 as _batch_timed_pngs_to_mp4
import concat_mp4s as _concat_mp4s
import concat_recorder_jsons as _concat_recorder_jsons


_os_path = _os.path
_script_basename = _os_path.basename(__file__)
_parser = None
_arguments = None

data_folder_name = None
outputs_folder_name = None
batch_timed_pngs_to_mp4_folder_name = None
concat_mp4s_folder_name = None
concat_recorder_jsons_folder_name = None
arguments_overridden = False
recorder_folder_name = None


def _create_context():
    global data_folder_name
    global outputs_folder_name
    global batch_timed_pngs_to_mp4_folder_name
    global concat_mp4s_folder_name
    global concat_recorder_jsons_folder_name

    script_no_ext, _ = _os_path.splitext(_script_basename)

    if data_folder_name is None:
        data_folder_name = _os_path.dirname(__file__)
        data_folder_name = _os_path.join(data_folder_name, f".{script_no_ext}_data")

    _os.makedirs(data_folder_name, exist_ok=True)
    timestamp = _datetime_utils.find_now_custom_date_time_string()

    if outputs_folder_name is None:
        outputs_folder_name = _os_path.join(data_folder_name, f"outputs-{timestamp}")

    _os.makedirs(outputs_folder_name, exist_ok=True)

    if batch_timed_pngs_to_mp4_folder_name is None:
        batch_timed_pngs_to_mp4_folder_name = _os_path.join(
            outputs_folder_name,
            ".batch_timed_pngs_to_mp4_data"
        )

    _os.makedirs(batch_timed_pngs_to_mp4_folder_name)

    if concat_mp4s_folder_name is None:
        concat_mp4s_folder_name = _os_path.join(outputs_folder_name, ".concat_mp4s_data")

    _os.makedirs(concat_mp4s_folder_name)

    if concat_recorder_jsons_folder_name is None:
        concat_recorder_jsons_folder_name = _os_path.join(
            outputs_folder_name,
            ".concat_recorder_jsons_data"
        )

    _os.makedirs(concat_recorder_jsons_folder_name)


def _parse_arguments():
    global _parser
    global _arguments
    global recorder_folder_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} [--help] <recorder-folder-name>",
        description="Processes a folder of ViSCA Recorder data.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _parser.add_argument(
        "recorder_folder_name",
        type=str,
        help="The name of the ViSCA Recorder data folder.",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if recorder_folder_name is None:
            recorder_folder_name = _arguments.recorder_folder_name

        recorder_folder_name = _os_path.abspath(recorder_folder_name)


def _perform_batch_timed_pngs_to_mp4():
    _batch_timed_pngs_to_mp4.data_folder_name = batch_timed_pngs_to_mp4_folder_name
    _batch_timed_pngs_to_mp4.output_folder_name = batch_timed_pngs_to_mp4_folder_name
    _batch_timed_pngs_to_mp4.arguments_overridden = True
    _batch_timed_pngs_to_mp4.nested_pngs_folder_name = recorder_folder_name
    _batch_timed_pngs_to_mp4.main()


def _perform_concat_mp4s():
    mp4_in_file_names = _os.listdir(batch_timed_pngs_to_mp4_folder_name)
    mp4_in_file_names.sort()

    for index, file_name in enumerate(mp4_in_file_names):
        mp4_in_file_names[index] = _os_path.join(batch_timed_pngs_to_mp4_folder_name, file_name)

    new_mp4_in_file_names = []

    for file_name in mp4_in_file_names:
        mp4_basename = _os_path.basename(file_name)
        _, mp4_ext = _os_path.splitext(mp4_basename)
        mp4_ext_matched = mp4_ext.lower() == ".mp4"

        if mp4_ext_matched:
            new_mp4_in_file_names.append(file_name)
        # end if
    # end for

    mp4_in_file_names = new_mp4_in_file_names
    mp4_in1_basename = _os_path.basename(mp4_in_file_names[0])
    mp4_in1_noext, _ = _os_path.splitext(mp4_in1_basename)
    _concat_mp4s.data_folder_name = concat_mp4s_folder_name
    _concat_mp4s.concat_file_name = _os_path.join(concat_mp4s_folder_name, f"concat-{mp4_in1_noext}.txt")
    _concat_mp4s.mp4_out_file_name = _os_path.join(outputs_folder_name, f"concat-{mp4_in1_noext}.mp4")
    _concat_mp4s.arguments_overridden = True
    _concat_mp4s.mp4s_in_folder_name = batch_timed_pngs_to_mp4_folder_name
    _concat_mp4s.main()


def _perform_concat_recorder_jsons():
    json_in_file_names = _os.listdir(recorder_folder_name)
    json_in_file_names.sort()

    for index, file_name in enumerate(json_in_file_names):
        json_in_file_names[index] = _os_path.join(recorder_folder_name, file_name)

    new_json_in_file_names = []

    for file_name in json_in_file_names:
        json_basename = _os_path.basename(file_name)
        _, json_ext = _os_path.splitext(json_basename)
        json_ext_matched = json_ext.lower() == ".json"

        if json_ext_matched:
            new_json_in_file_names.append(file_name)
        # end if
    # end for

    json_in_file_names = new_json_in_file_names
    json_in1_basename = _os_path.basename(json_in_file_names[0])
    json_in1_noext, _ = _os_path.splitext(json_in1_basename)
    _concat_recorder_jsons.data_folder_name = concat_recorder_jsons_folder_name
    _concat_recorder_jsons.json_out_file_name = _os_path.join(outputs_folder_name, f"concat-{json_in1_noext}.json")
    _concat_recorder_jsons.arguments_overridden = True
    _concat_recorder_jsons.jsons_in_folder_name = recorder_folder_name
    _concat_recorder_jsons.main()


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_script_basename}")
    _create_context()
    _parse_arguments()
    _perform_batch_timed_pngs_to_mp4()
    _perform_concat_mp4s()
    _perform_concat_recorder_jsons()

    print(
        f"{recorder_folder_name = :s}\n"
        + f"{outputs_folder_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
