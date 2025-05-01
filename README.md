# Images-to-video

This tool can make videos from your images.

<img width="226" alt="ImageToVideo_JnlyYzx0gY" src="https://github.com/user-attachments/assets/383d1f62-d67f-4ad6-82a7-1587c890e9d0" />
<img width="150" src="https://github.com/user-attachments/assets/470cad39-d420-41c7-b017-e43e8feb7d79" />

 *Version 0.1.1-alpha*
  
## How it works?
- Image to video tool uses [OpenCV](https://opencv.org/) libary for process Images to videos and [Tkinter](https://docs.python.org/3/library/tkinter.html) for simple GUI.
This program uses the os.walk() function from the os library to recursively traverse the directory structure, starting from the specified root folder. Its task is to automatically search all subfolders and identify image files with .jpg, .jpeg and .png extensions. When it finds at least one such file in one of the folders, it assembles a video in .mp4 format from all the images in that folder. The resolution of the resulting video is automatically taken from the first image found, and the order of the images corresponds to the alphabetical order of the file names.
- A separate video is created for each folder containing suitable image files. The output video can be named either by a user-selected name or automatically according to the path from the main folder to the folder containing the relevant materials. The program thus enables efficient and structured processing of large sets of images into clear video files.

## Future enhancements
1. Add Progress bar
3. Different settings for diferent folders
4. Change lenght of video
5. Speed settings
6. Resolution settings
7. Rebuild to [.NET](https://dotnet.microsoft.com/en-us/)

## Used third party apps
+ Visual Studio Code ([visualstudio.com](https://code.visualstudio.com/))
+ paint.net ([getpaint.net](https://www.getpaint.net/))
+ ShareX ([getsharex.net](https://getsharex.com/t))
