"""
Blends 2 MP4 videos into 1 MP4 video.
Uses the 2nd MP4 videos as an overlay on the 1st MP4 video.
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import _date_time_utils


_os_path = _os.path
_data_folder_name = None
_mp4_out_file_name = None
_parser = None
_arguments = None
_override_arguments = False
_mp4_in1_file_name = None
_mp4_in2_file_name = None


def _create_context():
    global _data_folder_name
    global _mp4_out_file_name

    if _data_folder_name is None:
        _data_folder_name = _os_path.dirname(__file__)
        _data_folder_name = _os_path.join(_data_folder_name, ".blend_2_mp4s_data")

    print(f"{_data_folder_name = }")
    _os.makedirs(_data_folder_name, exist_ok=True)
    timestamp = _date_time_utils.find_now_custom_date_time_string()

    if _mp4_out_file_name is None:
        _mp4_out_file_name = _os_path.join(_data_folder_name, f"output-{timestamp}.mp4")

    print(f"{_mp4_out_file_name = }")


def _parse_arguments():
    global _parser
    global _arguments
    global _mp4_in1_file_name
    global _mp4_in2_file_name

    _parser = _ArgumentParser(
        prog="blend_2_mp4s.py",
        usage="python blend_2_mp4s.py <mp4-in1-file-name> <mp4-in2-file-name>",
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

    if not _override_arguments:
        _arguments = _parser.parse_args()

        if _mp4_in1_file_name is None:
            _mp4_in1_file_name = _arguments.mp4_in1_file_name

        if _mp4_in2_file_name is None:
            _mp4_in2_file_name = _arguments.mp4_in2_file_name

        _mp4_in1_file_name = _os_path.abspath(_mp4_in1_file_name)
        _mp4_in2_file_name = _os_path.abspath(_mp4_in2_file_name)

    print(f"{_mp4_in1_file_name = }")
    print(f"{_mp4_in2_file_name = }")


def _blend_2_mp4s():
    in1 = _mp4_in1_file_name
    in2 = _mp4_in2_file_name
    out1 = _mp4_out_file_name

    command =\
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

    print(f"{command = }")
    _os.system(command)


def main():
    """
    Starts the main procedure.
    """
    print("begin Blend 2 MP4s")
    _create_context()
    _parse_arguments()
    _blend_2_mp4s()
    print("end Blend 2 MP4s")


if __name__ == "__main__":
    main()
