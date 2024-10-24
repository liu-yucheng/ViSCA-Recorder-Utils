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

## [`Data_FromRecorder_Process.py`](./Data_FromRecorder_Process.py)

- Processes a data folder (from ViSCA Recorder).
---
- Step 1-1. Uses `Batch_Video_FromRecorderImages_Convert.py`. Converts all captured nested image folders into video clips.
- Step 1-2. Uses `Video_Concat.py`. Concatenates all video clips (from step 1-1) into 1 video.
- Step 1-3. Uses `JSON_FromRecorder_Concat.py`. Concatenates all recorded JSON files into 1 JSON file.
---
- Step 2-1. Uses `Batch_Video_FromRecorderImages_WithSickness_Convert.py`. Converts all captured nested image folders into video clips (including clips with sickness only).
- Step 2-2. Uses `Video_Concat.py`. Concatenates all video clips (from step 2-1) into 1 video.
- Step 2-3. Uses `JSON_FromRecorder_Concat.py`. Concatenates all recorded JSON files into 1 JSON file (including items with sickness only).
---
- `python Data_FromRecorder_Process.py [--help] <Folder_Data_FromRecorder_Name>`

## [`Batch_Video_FromRecorderImages_Convert.py`](./Batch_Video_FromRecorderImages_Convert.py)

- Performs a batch of `Batch_Video_FromRecorderImages_Convert.py` operations.
- `python Batch_Video_FromRecorderImages_Convert.py [--help] <Folder_NestedImages_Name>`

## [`Batch_Video_FromRecorderImages_WithSickness_Convert.py`](./Batch_Video_FromRecorderImages_WithSickness_Convert.py)

- Performs a batch of `Video_FromRecorderImages_WithSickness_Convert.py` operations.
- `python Batch_Video_FromRecorderImages_WithSickness_Convert.py [--help] <Folder_NestedImages_Name>`

## [`Video_FromRecorderImages_Convert.py`](./Video_FromRecorderImages_Convert.py)

- Converts an image sequence (from ViSCA Recorder) to a video.
- Image name `C printf` formats.
  - `time_%06.6f_sickness_%01.1f.png`.
  - or `time_%06.6f_sickness_%01.1f.jpg`.
- Image sequence time unit: seconds.
- `python Video_FromRecorderImages_Convert.py [--help] <Folder_Images_Name>`

## [`Video_FromRecorderImages_WithSickness_Convert.py`](./Video_FromRecorderImages_WithSickness_Convert.py)

- Converts an image sequence (from ViSCA Recorder) to a video (includes clips with sickness only).
- Image name `C printf` formats.
  - `time_%06.6f_sickness_%01.1f.png`.
  - or `time_%06.6f_sickness_%01.1f.jpg`.
- Image sequence time unit: seconds.
- `python Video_FromRecorderImages_WithSickness_Convert.py [--help] <Folder_Images_Name>`

## [`JSON_FromRecorder_Concat.py`](./JSON_FromRecorder_Concat.py)

- Concatenates a sequence of JSON (from ViSCA Recorder) files.
- Concatenates JSONs in ascending alphanumerical order.
- `python JSON_FromRecorder_Concat.py [--help] <Folder_JSONs_Input_Name>`

## [`JSON_FromRecorder_WithSickness_Concat.py`](./JSON_FromRecorder_WithSickness_Concat.py)

- Concatenates a sequence of JSON (from ViSCA Recorder) files (includes items with sickness only).
- Concatenates JSONs in ascending alphanumerical order.
- `python JSON_FromRecorder_WithSickness_Concat.py [--help] <Folder_JSONs_Input_Name>`

## [`Video_Concat.py`](./Video_Concat.py)

- Concatenates a sequence of videos.
- Concatenates video in ascending alphanumerical order.
- `python Video_Concat.py [--help] <Videos_Input_Name>`

## ~~[`Video_Blend.py`](./Video_Blend.py)~~ (Deprecated)

- Blends 2 videos into 1 video.
- Uses the 2nd video as an overlay on the 1st video.
- `python Video_Blend.py [--help] <Video_Input1_Name> <Video_Input2_Name>`

# Copyright

```
Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
GNU AGPL 3.0 License available at: https://www.gnu.org/licenses/agpl-3.0.txt
```
