"""
Converts an image sequence (from ViSCA Recorder) to a video
  (includes clips with sickness only).
"""

# Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License.
# GNU AGPL 3.0 License: https://www.gnu.org/licenses/agpl-3.0.txt .


from argparse import ArgumentParser as _ArgumentParser
import os as _os
import varname as _varname
import re as _re
import _Utils_DateTime


_os_path = _os.path
_nameof = _varname.core.nameof
_Script_basename = _os_path.basename(__file__)
_Parser = None
_Arguments = None
_Command_FFMpeg = None

Script_NoExt, _ = _os_path.splitext(_Script_basename)
Clips_WithSickness_TimeBefore_Seconds = None
Clips_WithSickness_TimeAfter_Seconds = None
Clips_WithSickness_TimeBetween_Max_Seconds = None
Clips_WithSickness_Sickness_SicknessThreshold = float(0.75)
Folder_Data_Name = None
File_Concat_Name = None
Video_Name = None
Arguments_Overridden = False
Folder_Images_Name = None


def _Context_Create():
    global Clips_WithSickness_TimeBefore_Seconds
    global Clips_WithSickness_TimeAfter_Seconds
    global Clips_WithSickness_TimeBetween_Max_Seconds
    global Folder_Data_Name
    global File_Concat_Name
    global Video_Name

    if Clips_WithSickness_TimeBefore_Seconds is None:
        Clips_WithSickness_TimeBefore_Seconds = 0.5

    if Clips_WithSickness_TimeAfter_Seconds is None:
        Clips_WithSickness_TimeAfter_Seconds = 0.5

    if Clips_WithSickness_TimeBetween_Max_Seconds is None:
        Clips_WithSickness_TimeBetween_Max_Seconds = 3

    if Folder_Data_Name is None:
        Folder_Data_Name = _os_path.dirname(__file__)

        Folder_Data_Name \
        = _os_path.join(Folder_Data_Name, f".{Script_NoExt}_Data")
        # end statement
    # end if

    _os.makedirs(Folder_Data_Name, exist_ok=True)
    timestamp = _Utils_DateTime.DateTime_Custom_FindStringFor_Now()

    if File_Concat_Name is None:
        File_Concat_Name \
        = _os_path.join(Folder_Data_Name, f"Concat_{timestamp}.txt")
        # end statement
    # end if

    if Video_Name is None:
        Video_Name = _os_path.join(Folder_Data_Name, f"Output_{timestamp}.mp4")
    # end if


def _Arguments_Parse():
    global _Parser
    global _Arguments
    global Folder_Images_Name

    _Parser = _ArgumentParser(
        prog=_Script_basename,

        usage\
        =f"python {_Script_basename} [--help]"
        + f" <{_nameof(Folder_Images_Name)}>",

        description\
        ="Converts an image sequence (from ViSCA Recorder) to a video"
        + " (includes clips with sickness only).",

        epilog\
        ="Copyright (C) 2024 Yucheng Liu. Under the GNU AGPL 3.0 License."
    )

    _Parser.add_argument(
        f"{_nameof(Folder_Images_Name)}",
        type=str,
        help="Name of the image sequence folder.",
        metavar=f"{_nameof(Folder_Images_Name)}"
    )

    if not Arguments_Overridden:
        _Arguments = _Parser.parse_args()

        if Folder_Images_Name is None:
            Folder_Images_Name = _Arguments.Folder_Images_Name

        Folder_Images_Name = _os_path.abspath(Folder_Images_Name)
    # end if


def _ConcatDemuxer_Generate():
    Images_isdir = _os_path.isdir(Folder_Images_Name)
    Image_Names = []

    if Images_isdir:
        Image_Names = _os.listdir(Folder_Images_Name)
        Image_Names.sort()

    for Index, Image_Name in enumerate(Image_Names):
        Image_Names[Index] = _os_path.join(Folder_Images_Name, Image_Name)

    Image_Names_New = []

    for Image_Name in Image_Names:
        Image_isfile = _os_path.isfile(Image_Name)
        Image_basename = _os_path.basename(Image_Name)
        _, Image_Ext = _os_path.splitext(Image_Name)

        Image_Ext_Matched \
        = Image_Ext.lower() == ".png" \
            or Image_Ext.lower() == ".jpg"
        # end statement

        if Image_isfile and Image_Ext_Matched:
            Image_Names_New.append(Image_Name)
        # end if
    # end if

    Image_Names = Image_Names_New
    Image_NameToTime = {}
    Image_NameToSickness = {}

    # Record image time and sickness.
    for Index, Image_Name in enumerate(Image_Names):
        Image_basename = _os_path.basename(Image_Name)
        Image_NoExt, _ = _os_path.splitext(Image_basename)
        Image_basename_Split = _re.split("_+", Image_NoExt)

        Image_basename_Matched \
        = len(Image_basename_Split) >= 4 \
            and Image_basename_Split[0] == "time" \
            and Image_basename_Split[2] == "sickness" \

        if Image_basename_Matched:
            Time_ = float(Image_basename_Split[1])
            Sickness = float(Image_basename_Split[3])
            Image_NameToTime[Image_Name] = Time_
            Image_NameToSickness[Image_Name] = Sickness
        # end if
    # end for

    Image_WithSickness_Names_Dict = {}
    Image_WithSickness_NameToTime = {}

    # Select images with sickness.
    for Index, Image_Name in enumerate(Image_Names):
        Time_ = Image_NameToTime[Image_Name]
        Sickness = Image_NameToSickness[Image_Name]

        if Sickness >= Clips_WithSickness_Sickness_SicknessThreshold:
            if Image_Name not in Image_WithSickness_Names_Dict:
                Image_WithSickness_Names_Dict[Image_Name] = None

            if Image_Name not in Image_WithSickness_NameToTime:
                Image_WithSickness_NameToTime[Image_Name] = Time_
            # end while
        # end if
    # end for

    Image_BeforeSickness_Names_Dict = {}
    Image_BeforeSickness_NameToTime = {}

    # Select images before sickness.
    for Index, Image_Name in enumerate(Image_Names):
        if Image_Name in Image_WithSickness_Names_Dict:
            Time_ = Image_NameToTime[Image_Name]
            Index_Trace = Index
            Image_Name_Trace = Image_Name
            Time_Trace = Time_

            while \
                Time_ - Time_Trace < Clips_WithSickness_TimeBefore_Seconds \
                and Index_Trace >= 0:
                Image_Name_Trace = Image_Names[Index_Trace]
                Time_Trace = Image_NameToTime[Image_Name_Trace]

                if Image_Name_Trace not in Image_BeforeSickness_Names_Dict:
                    Image_BeforeSickness_Names_Dict[Image_Name_Trace] = None
                    # end statement
                # end if

                if Image_Name_Trace not in Image_BeforeSickness_NameToTime:
                    Image_BeforeSickness_NameToTime[Image_Name_Trace] \
                    = Time_Trace
                    # end statement
                # end if

                Index_Trace -= 1
            # end while
        # end if
    # end for

    Image_AfterSickness_Names_Dict = {}
    Image_AfterSickness_NameToTime = {}

    # Select images after sickness.
    for Index, Image_Name in enumerate(Image_Names):
        if Image_Name in Image_WithSickness_Names_Dict:
            Time_ = Image_NameToTime[Image_Name]
            Index_Trace = Index
            Image_Name_Trace = Image_Name
            Time_Trace = Time_

            while \
                Time_Trace - Time_ < Clips_WithSickness_TimeAfter_Seconds \
                and Index_Trace < len(Image_Names):
                Image_Name_Trace = Image_Names[Index_Trace]
                Time_Trace = Image_NameToTime[Image_Name_Trace]

                if Image_Name_Trace not in Image_AfterSickness_Names_Dict:
                    Image_AfterSickness_Names_Dict[Image_Name_Trace] = None
                    # end if

                if Image_Name_Trace not in Image_AfterSickness_NameToTime:
                    Image_AfterSickness_NameToTime[Image_Name_Trace] \
                    = Time_Trace
                    # end statement
                # end if

                Index_Trace += 1
            # end while
        # end if
    # end for

    Image_WithSickness_Names \
    = list(Image_WithSickness_Names_Dict.keys()) \
        + list(Image_BeforeSickness_Names_Dict.keys()) \
        + list(Image_AfterSickness_Names_Dict.keys())

    Image_WithSickness_Names.sort()

    for Key, Item in Image_BeforeSickness_NameToTime.items():
        Image_WithSickness_NameToTime[Key] = Item

    for Key, Item in Image_AfterSickness_NameToTime.items():
        Image_WithSickness_NameToTime[Key] = Item

    Time_Current_Seconds = float(0)
    Time_Previous_Seconds = float(0)
    Concat_Lines = []

    for Index, Image_Name in enumerate(Image_WithSickness_Names):
        Time_Current_Seconds = Image_WithSickness_NameToTime[Image_Name]

        if \
            Time_Current_Seconds - Time_Previous_Seconds \
            > Clips_WithSickness_TimeBetween_Max_Seconds:
            Time_Previous_Seconds \
            = Time_Current_Seconds - Clips_WithSickness_TimeBetween_Max_Seconds
            # end statement
        # end if

        Concat_Lines.append(f"file '{Image_Name}'")
        Duration_Seconds = Time_Current_Seconds - Time_Previous_Seconds
        Concat_Lines.append(f"duration {Duration_Seconds:6f}")
        Time_Previous_Seconds = Time_Current_Seconds
        # end if
    # end for

    Concat_str = "\n".join(Concat_Lines)

    with open(File_Concat_Name, mode="w", encoding="utf-8") as Concat_File:
        Concat_File.write(Concat_str)
    # end with
# end def


def _Video_Convert():
    global _Command_FFMpeg

    _Command_FFMpeg =\
        f"ffmpeg"\
        + f"  -f concat"\
        + f"  -safe 0"\
        + f"  -i \"{File_Concat_Name}\""\
        + f"  -filter:v fps=30"\
        + f"  -pix_fmt yuvj420p"\
        + f"  -movflags +faststart"\
        + f"  -c:v h264"\
        + f"  -profile:v high"\
        + f"  \"{Video_Name}\""

    print(f"{_Command_FFMpeg = }")
    _os.system(_Command_FFMpeg)


def Main():
    """
    Starts the main procedure.
    """
    print(f"begin {_Script_basename}")
    _Context_Create()
    _Arguments_Parse()
    _ConcatDemuxer_Generate()
    _Video_Convert()

    print(
        f"{Clips_WithSickness_TimeBefore_Seconds = }\n"
        + f"{Clips_WithSickness_TimeAfter_Seconds = }\n"
        + f"{Clips_WithSickness_TimeBetween_Max_Seconds = }\n"
        + f"{Folder_Images_Name = :s}\n"
        + f"{File_Concat_Name = :s}\n"
        + f"{Video_Name = :s}"
    )

    print(f"end {_Script_basename}")


if __name__ == "__main__":
    Main()
