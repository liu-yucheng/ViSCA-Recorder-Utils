# ViSCA-Recorder-Utils

- A utility toolset for the ViSCA Recorder application.

# Preparation

- Download and install [FFmpeg](https://ffmpeg.org/download.html).
- Make sure the `ffmpeg` command is available in the terminal.
- Install (Python)[https://www.python.org/downloads/]
- Make sure `python` and `pip` are available on your terminal command line.
- Open the repository directory in your terminal.
- Run `pip install -r ./requirements.txt` to install the python dependencies.

# Usage

## `timed_images_to_mp4.py`

- Converts a sequence of timed images to an MP4 video.
- Image file name format: `time_%.6f_sickness_%.1f.png` or `time_%.6f_sickness_%.1f.jpg`.
- Image sequence time unit: seconds.
- `python timed_images_to_mp4.py [--help] <images-folder-name>`

## `blend_2_mp4s.py`

- Blends 2 MP4 videos into 1 MP4 video.
- Uses the 2nd MP4 video as an overlay on the 1st MP4 video.
- `python blend_2_mp4s.py [--help] <mp4-in1-file-name> <mp4-in2-file-name>`

## `batch_timed_images_to_mp4.py`

- Performs a batch of `timed_images_to_mp4.py` operations.
- `python batch_timed_images_to_mp4.py [--help] <nested-images-folder-name>`

## `concat_mp4s.py`

- Converts a sequence of MP4 videos to an MP4 video by concatenating them.
- Concatenates MP4s in ascending alphanumerical order.
- `python concat_mp4s.py [--help] <mp4s-in-folder-name>`

## `concat_recorder_jsons.py`

- Converts a sequence of ViSCA Recorder JSON files to a JSON file by concatenating them.
- Concatenates JSONs in ascending alphanumerical order.
- `python concat_recorder_jsons.py [--help] <jsons-in-folder-name>`

## `process_recorder_data.py`

- Processes a folder of ViSCA Recorder data.
- Step 1. Uses `batch_timed_images_to_mp4.py` to convert all captured frames (in the form of nested timed image folders) into video clips (in the form of MP4 files).
- Step 2. Uses `concat_mp4s.py` to concatenate all converted video clips (the output of step 1) into 1 complete video file (in the form of an MP4 file).
- Step 3. Uses `concat_recorder_jsons.py` to concatenate all recorded textual data files (in the form of JSON files) into 1 complete textual data file (in the form of a JSON file).
- `python process_recorder_data.py [--help] <recorder-folder-name>`

# Copyright

```
Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt
```
