"""
Blends 2 MP4 videos into 1 MP4 video.
Uses the 2nd MP4 videos as an overlay on the 1st MP4 video.
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
mp4_out_file_name = None
arguments_overridden = False
mp4_in1_file_name = None
mp4_in2_file_name = None


def _create_context():
    global data_folder_name
    global mp4_out_file_name

    script_no_ext, _ = _os_path.splitext(_script_basename)

    if data_folder_name is None:
        data_folder_name = _os_path.dirname(__file__)
        data_folder_name = _os_path.join(data_folder_name, f".{script_no_ext}_data")

    _os.makedirs(data_folder_name, exist_ok=True)
    timestamp = _datetime_utils.find_now_custom_date_time_string()

    if mp4_out_file_name is None:
        mp4_out_file_name = _os_path.join(data_folder_name, f"output-{timestamp}.mp4")


def _parse_arguments():
    global _parser
    global _arguments
    global mp4_in1_file_name
    global mp4_in2_file_name

    _parser = _ArgumentParser(
        prog=_script_basename,
        usage=f"python {_script_basename} <mp4-in1-file-name> <mp4-in2-file-name>",
        description="Blends 2 MP4 videos into 1 MP4 video.",
        epilog="Copyright (C) 2024 Yucheng Liu. Under the GNU GPL3/3+ License."
    )

    _parser.add_argument(
        "mp4_in1_file_name",
        type=str,
        help="The 1st MP4 file name.",
        metavar="string"
    )

    _parser.add_argument(
        "mp4_in2_file_name",
        type=str,
        help="The 2nd MP4 file name.",
        metavar="string"
    )

    if not arguments_overridden:
        _arguments = _parser.parse_args()

        if mp4_in1_file_name is None:
            mp4_in1_file_name = _arguments.mp4_in1_file_name

        if mp4_in2_file_name is None:
            mp4_in2_file_name = _arguments.mp4_in2_file_name

        mp4_in1_file_name = _os_path.abspath(mp4_in1_file_name)
        mp4_in2_file_name = _os_path.abspath(mp4_in2_file_name)


def _blend_2_mp4s():
    global _ffmpeg_command

    in1 = mp4_in1_file_name
    in2 = mp4_in2_file_name
    out1 = mp4_out_file_name

    _ffmpeg_command =\
        f"ffmpeg"\
        + f"  -i \"{in1}\""\
        + f"  -i \"{in2}\""\
        + f"  -filter_complex \""\
        + f"    [0]format=yuva420p,colorchannelmixer=ar=0:ag=0:ab=0:aa=1[v1];"\
        + f"    [1]format=yuva420p,colorchannelmixer=ar=2:ag=2:ab=2:aa=0[v2];"\
        + f"    [v2][v1]scale2ref[v2][v1];"\
        + f"    [v1][v2]blend=all_mode=\"addition\":all_opacity=0.65"\
        + f"  \""\
        + f"  -pix_fmt yuv420p"\
        + f"  -movflags +faststart"\
        + f"  -c:v h264"\
        + f"  -profile:v high"\
        + f"  \"{out1}\""

    print(f"{_ffmpeg_command = }")
    _os.system(_ffmpeg_command)


def main():
    """
    Starts the main procedure.
    """
    print(f"begin {_script_basename}")
    _create_context()
    _parse_arguments()
    _blend_2_mp4s()

    print(
        f"{mp4_in1_file_name = :s}\n"
        + f"{mp4_in2_file_name = :s}\n"
        + f"{mp4_out_file_name = :s}"
    )

    print(f"end {_script_basename}")


if __name__ == "__main__":
    main()
