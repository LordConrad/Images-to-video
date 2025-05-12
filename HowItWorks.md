# Image to Video Tool

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Enabled-lightgrey)](https://opencv.org/)
[![GUI](https://img.shields.io/badge/Tkinter-GUI-yellow)](https://docs.python.org/3/library/tkinter.html)

This tool is designed to convert folders of images into video files. It is built using [OpenCV](https://opencv.org/) for image processing and [Tkinter](https://docs.python.org/3/library/tkinter.html) for the graphical user interface (GUI).

## Overview

The program recursively traverses a directory structure starting from a user-selected root folder. It searches all subfolders for image files with the `.jpg`, `.jpeg`, or `.png` extensions. If it finds at least one such file in a folder, it compiles all the images in that folder into a video in `.mp4` format.

## Features

-  **Automatic Image Detection**: Identifies folders with valid images automatically.
-  **Custom Settings per Folder**: Define FPS, output name, and save location for each folder.
-  **Main Settings Override**: Set global preferences to override individual folder options.
-  **Image Sorting**: Alphabetical sorting before compiling the video.
-  **Resolution Detection**: Uses the first image to determine output resolution.
-  **Naming Options**:
  - Custom name
  - Derived from folder name
-  **Save Path Options**:
  - Save next to the image folder
  - Save to a global folder
-  **Repeat & Speed Control**: Control video length with FPS and frame repeats.
-  **Video Length Estimator**: Preview expected video duration.
-  **Folder Manager**: Pick specific folders to include/exclude.

## Dependencies

- Python 3.x
- OpenCV (`cv2`)
- Tkinter (included with standard Python installations)

## Usage

1. **Run the application.**
2. **Select a root folder** that contains subfolders with image files.
3. **Use the Folder Manager** to choose which subfolders to include or exclude and configure settings individually if desired.
4. **Set Global Preferences** (optional):
    - FPS
    - Output name pattern
    - Save path
    - Frame repeat count
5. **Review Estimated Duration** for each video.
6. **Start Processing** — the tool will generate `.mp4` videos for all selected folders.

## Output

Each processed folder will result in one `.mp4` video saved based on the chosen naming and saving settings. Videos are built by sequencing images and optionally repeating them, using the selected FPS for timing.
