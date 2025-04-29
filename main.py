import os
import cv2
from tkinter import messagebox
from tkinter import*
from tkinter import filedialog as fd

#Default settings
root_folder = ""
default_fps = 15
video_name = "New animation"
Font1 = ("Arial",13)
Font2 = ("Arial",10)
Font3 = ("Arial",8)
#Main window
c= Tk()
c.geometry("300x300")
c.resizable(False, False)
c.title("Images to video")

Name_from_directory_checkbox_checking_variable = IntVar()

def select_directory():
    global root_folder
    filename = fd.askdirectory()
    root_folder = filename
    Selected_folder_text.delete("1.0","end-1c")
    Selected_folder_text.insert("1.0",root_folder)

def Name_from_directory_checking():
    global video_name
    if Name_from_directory_checkbox_checking_variable.get()==1:
       Name_insert.config(bg="gray",state=DISABLED)
    else:
        Name_insert.config(bg="white",state=NORMAL)
        default_video_name = Name_insert.get("1.0","end-1c")
        video_name = default_video_name
    c.after(100, Name_from_directory_checking) 

def Manage_folders():
    Manage_folders_window= Tk()
    Manage_folders_window.geometry("600x500")
    Manage_folders_window.resizable(False, False)
    Manage_folders_window.title("Images to video")
    Manage_folders_window.mainloop()

#Add elements
Title_text_Video_settings = Label(c,text="Images to video tool",font=Font1)
Title_text_Video_settings.place(x=70,y=0)

Selected_folder_text = Text(c, height=2,width=35)
Selected_folder_text.place(x=7,y=25)

Directory_text = Label(c, text="Directory",font=Font2)
Directory_text.place(x=10,y=66)

Directory_btn = Button(c,text="Open folder",command=select_directory)
Directory_btn.place(x=90,y=63)

Manage_folders_btn = Button(c,text="Manage Folders",command=Manage_folders)
Manage_folders_btn.place(x=170,y=63)

Number_of_repeats_text = Label(c,text="Number of Repeats",font=Font2)
Number_of_repeats_text.place(x=0,y=165)

Number_of_repeats_insert = Text(c, height=1,width=4)
Number_of_repeats_insert.place(x=155,y=165)
Number_of_repeats_insert.insert("1.0","1")

Frames_text = Label(c, text="FPS",font=Font2)
Frames_text.place(x=0,y=190)

Frames_insert = Text(c, height=1,width=4)
Frames_insert.insert("1.0","15")
Frames_insert.place(x=155,y=190)

Name_text = Label(c, text="Name",font=Font2)
Name_text.place(x=0,y=215)

Name_insert = Text(c, height=2,width=15,)
Name_insert.insert("1.0","New animation")
Name_insert.place(x=70,y=215)

Name_from_directory_checkbox_text = Label(c,text="Get name \nfrom \ndirectory",font=Font3)
Name_from_directory_checkbox_text.place(x=200,y=205)

Name_from_directory_checkbox = Checkbutton(c,variable=Name_from_directory_checkbox_checking_variable)
Name_from_directory_checkbox.place(x=260,y=215)

def process_images_in_folder(folder_path, output_video_name=video_name + ".mp4", fps=float(Frames_insert.get("1.0","end-1c"))):
    current_path = root
    #Naming video after directory
    if Name_from_directory_checkbox_checking_variable.get()==1:
        def get_relative_path(target_path, start_path):
            return os.path.relpath(target_path, start_path)
        os.chdir(root_folder)
        relative_path = get_relative_path(current_path, root_folder)
        output_video_name = relative_path.replace("\\","") + ".mp4"
    else:
        output_video_name = Name_insert.get("1.0","end-1c") + ".mp4"
    #Processing images
    images = [img for img in os.listdir(folder_path) 
        if img.endswith((".jpg", ".png", ".jpeg"))]
    print(Frames_insert.get("1.0","end-1c"))
    if not images:
        return
    
    images.sort()

    first_image = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, _ = first_image.shape
    

    video = cv2.VideoWriter(
        os.path.join(folder_path, output_video_name),
        cv2.VideoWriter_fourcc(*'mp4v'),
        float(Frames_insert.get("1.0","end-1c")),
        (width, height)
    )
    for i in range(int(Number_of_repeats_insert.get("1.0","end-1c"))):
     for image_name in images:
        img_path = os.path.join(folder_path, image_name)
        frame = cv2.imread(img_path)
        video.write(frame)
    video.release()
    print(f"Video saved in: {os.path.join(folder_path, output_video_name)}")

#Folder walking
def process_all_folders(root_folder):
    global root
    for root, dirs, files in os.walk(root_folder):
        has_images = any(file.endswith((".jpg", ".png", ".jpeg")) for file in files)
        
        if has_images:
            process_images_in_folder(root)
    
    messagebox.showinfo("Process ended","Process has succesfully ended")

def Render():
    process_all_folders(root_folder)

Render_btn = Button(c, text="Render",command=Render)
Render_btn.place(x=250,y=270)

Cancel_btn = Button(c, text="Exit", command=c.destroy)
Cancel_btn.place(x=5,y=270)

Name_from_directory_checking()

c.mainloop()
