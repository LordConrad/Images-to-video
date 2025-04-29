# Images-to-video

This tool can make videos from your images.

<img width="150" src="https://github.com/user-attachments/assets/470cad39-d420-41c7-b017-e43e8feb7d79" />

<br>

<img width="226" alt="python3 12_u4kRFWac6P" src="https://github.com/user-attachments/assets/977fd13e-5cd2-470d-b5e0-5aae2c880f87" />

## How it works?
- Image to video tool uses OpenCV libary for process Images to videos and Tkinter for simple GUI.
This program uses the os.walk() function from the os library to recursively traverse the directory structure, starting from the specified root folder. Its task is to automatically search all subfolders and identify image files with .jpg, .jpeg and .png extensions. When it finds at least one such file in one of the folders, it assembles a video in .mp4 format from all the images in that folder. The resolution of the resulting video is automatically taken from the first image found, and the order of the images corresponds to the alphabetical order of the file names.
- A separate video is created for each folder containing suitable image files. The output video can be named either by a user-selected name or automatically according to the path from the main folder to the folder containing the relevant materials. The program thus enables efficient and structured processing of large sets of images into clear video files.

## Used third party apps
+ Visual Studio Code
+ pain.net
+ ShareX

## Credit
+ HappyPeter (lot of useful tips thanks!)
