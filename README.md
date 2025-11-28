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

## [./data_from_recorder__batch_process.py](./data_from_recorder__batch_process.py)

- Performs a batch of `./data_from_recorder__process.py` operations.
- Operates on every subfolder in the specified folder.
- `python ./data_from_recorder__batch_process.py [--help] <folder_name__batch_data_from_recorder>`

## [./data_from_recorder__process.py](./data_from_recorder__process.py)

- Processes a data folder (from ViSCA Recorder).
---
- Step 1-1.
Uses `./video_from_recorder__batch_convert.py`.
Converts all captured nested image folders into video clips.
- Step 1-2.
Uses `./video__concat.py`.
Concatenates all video clips (from step 1-1) into 1 video.
- Step 1-3.
Uses `./json_from_recorder__concat.py`.
Concatenates all recorded JSON files into 1 JSON file.
---
- Step 2-1.
Uses `./video_from_recorder_with_sickness__batch_convert.py`. 
Converts all captured nested image folders into video clips (including clips with sickness only).
- Step 2-2.
Uses `./video__concat.py`.
Concatenates all video clips (from step 2-1) into 1 video.
- Step 2-3.
Uses `./json_from_recorder_with_sickness__concat.py`.
Concatenates all recorded JSON files into 1 JSON file (including items with sickness only).
---
- `python ./data_from_recorder__process.py [--help] <folder_name__data_from_recorder>`

## [./video_from_recorder__batch_convert.py](./video_from_recorder__batch_convert.py)

- Performs a batch of `./video_from_recorder__convert.py` operations.
- `python ./video_from_recorder__batch_convert.py [--help] <folder_name__images_nested>`

## [./video_from_recorder_with_sickness__batch_convert.py](./video_from_recorder_with_sickness__batch_convert.py)

- Performs a batch of `./video_from_recorder_with_sickness__convert.py` operations.
- `python ./video_from_recorder_with_sickness__batch_convert.py [--help] <folder_name__images_nested>`

## [./video_from_recorder__convert.py](./video_from_recorder__convert.py)

- Converts an image sequence (from ViSCA Recorder) to a video.
- Supported image file name `C printf` formats.
  - `time_%06.6f_sickness_%01.1f.png`.
  - `time_%06.6f_sickness_%01.1f.jpg`.
- Image sequence time format and unit: float, seconds.
- `python ./video_from_recorder__convert.py [--help] <folder_name__images>`

## [./video_from_recorder_with_sickness__convert.py](./video_from_recorder_with_sickness__convert.py)

- Converts an image sequence (from ViSCA Recorder) to a video (includes clips with sickness only).
- Supported image file name `C printf` formats.
  - `time_%06.6f_sickness_%01.1f.png`.
  - `time_%06.6f_sickness_%01.1f.jpg`.
- Image sequence time format and unit: float, seconds.
- `python ./video_from_recorder_with_sickness__convert.py [--help] <folder_name__images>`

## [./json_from_recorder__concat.py](./json_from_recorder__concat.py)

- Concatenates a sequence of JSON (from ViSCA Recorder) files.
- Concatenates JSONs in ascending alphanumerical order.
- Creates a copy of concatenated JSONs in which the `items` get flattened into `items__flattened`.
- `python ./json_from_recorder__concat.py [--help] <folder_name__jsons_input>`

## [./json_from_recorder_with_sickness__concat.py](./json_from_recorder_with_sickness__concat.py)

- Concatenates a sequence of JSON (from ViSCA Recorder) files (includes items with sickness only).
- Concatenates JSONs in ascending alphanumerical order.
- Creates a copy of concatenated JSONs in which the `items` get flattened into `items__flattened`.
- `python ./json_from_recorder_with_sickness__concat.py [--help] <folder_name__jsons_input>`

## [./video__concat.py](./video__concat.py)

- Concatenates a sequence of videos.
- Concatenates video in ascending alphanumerical order.
- `python ./video__concat.py [--help] <folder_name__videos_input>`

## ~~[./video__blend.py](./video__blend.py)~~ (Deprecated)

- Blends 2 videos into 1 video.
- Uses the 2nd video as a semi-transparent overlay on the 1st video.
- `python ./video__blend.py [--help] <file_name__video_1> <file_name__video_2>`

# Copyright

```
Copyright (C) 2024-2025 Yucheng Liu. Under the GNU AGPL 3.0 License.
GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .
```
