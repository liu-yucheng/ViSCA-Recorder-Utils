# ViSCA-Recorder-Utils

- A utility toolset for the ViSCA Recorder application.

# Preparation

- Download and install [FFmpeg](https://ffmpeg.org/download.html).
- Make sure the `ffmpeg` command is available in the terminal.
- Open the repository directory in the terminal.
- Run `pip install -r ./requirements.txt` to install the python dependencies.

# Usage

## `timed_pngs_to_mp4.py`

- Converts a sequence of timed PNG images to an MP4 video.
- PNG file name format: `%08d.png`.
- PNG sequence time unit: milliseconds.
- `python timed_pngs_to_mp4.py <pngs-folder-name>`.

## `blend_2_mp4s.py`

- Blends 2 MP4 videos into 1 MP4 video.
- Uses the 2nd MP4 video as an overlay on the 1st MP4 video.
- `python blend_2_mp4s.py <mp4-in1-file-name> <mp4-in2-file-name>`

## `batch_timed_pngs_to_mp4.py`

- Performs a batch of `timed_pngs_to_mp4.py` operations.
- `python batch_timed_pngs_to_mp4.py <nested-pngs-folder-name>`

## `concat_mp4s.py`

- Converts a sequence of MP4 videos to an MP4 video by concatenating them.
- Concatenates MP4s in ascending alphanumerical order.
- `python concat_mp4s.py <mp4s-in-folder-name>`

## `concat_record_jsons.py`

- Converts a sequence of record JSON files to a JSON file by concatenating them.
- Concatenates JSONs in ascending alphanumerical order.
- `python concat_record_jsons.py <jsons-in-folder-name>`

# Copyright

```
Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt
```
