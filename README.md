# Images-to-video

This tool can make videos from your images.

<img width="150" src="https://github.com/user-attachments/assets/470cad39-d420-41c7-b017-e43e8feb7d79" />
  
## How it works?
- Image to video tool uses [OpenCV](https://opencv.org/) libary for process Images to videos and [Tkinter](https://docs.python.org/3/library/tkinter.html) for simple GUI.
This program uses the os.walk() function from the os library to recursively traverse the directory structure, starting from the specified root folder. Its task is to automatically search all subfolders and identify image files with .jpg, .jpeg and .png extensions. When it finds at least one such file in one of the folders, it assembles a video in .mp4 format from all the images in that folder. The resolution of the resulting video is automatically taken from the first image found, and the order of the images corresponds to the alphabetical order of the file names.
- A separate video is created for each selected folder that contains suitable image files. The output video can either use a custom name defined by the user or be automatically named based on the folder's path relative to the main directory. With the ability to manage which folders are processed, the program offers efficient and organized conversion of large image collections into clearly structured video files.

## Future enhancements
1. Add Progress bar
2. Different settings for diferent folders
3. Change lenght of video
4. Speed settings
5. Resolution settings 
6. Rebuild to C

## Used third party apps
+ Visual Studio Code ([visualstudio.com](https://code.visualstudio.com/))
+ paint.net ([getpaint.net](https://www.getpaint.net/))
+ ShareX ([getsharex.net](https://getsharex.com/t))
