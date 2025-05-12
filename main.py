import os
import cv2
from tkinter import*
from tkinter import messagebox, PhotoImage, filedialog as fd
from tkinter.ttk import Progressbar

#Default settings
root_folder = ""
default_fps = 15
video_name = "New animation"

Manage_folders_variable = {}
Folder_custom_settings = {}

#Define fonts
Font1 = ("Arial",13)
Font2 = ("Arial",10)
Font3 = ("Arial",8)

#Main window
c= Tk()
c.geometry("475x400")
c.resizable(False, False)
c.title("Images to video")
c.iconbitmap("ico.ico")

customize_img = PhotoImage(file="icons/customize.png")

Name_from_directory_checkbox_checking_variable = IntVar()
Save_directory_checkbox_checking_variable = IntVar()
set_all_enabled_var = IntVar()

#Master checkboxes variables
Master_repeats_checkbox_variable = IntVar(value=1)
Master_speed_checkbox_variable = IntVar(value=1)
Master_name_checkbox_variable = IntVar(value=1)
Master_save_checkbox_variable = IntVar(value=1)

#variables for checkoboxes in folder settings
Get_custom_name_from_directory_variable = IntVar()
Save_directory_same_as_material_checkbox_CUSTOM_variable = IntVar()

#Master checking
def Master_repeats_checking():
    if Master_repeats_checkbox_variable.get() == 1:
        Number_of_repeats_insert.config(state=NORMAL,bg="white")
        Main_repeats = True
    else:
        Number_of_repeats_insert.config(state=DISABLED,bg="gray")
        Main_repeats = False
    c.after(500, Master_repeats_checking)

def Master_speed_checking():
    if Master_speed_checkbox_variable.get() == 1:
        Speed_insert.config(state=NORMAL,bg="white")
        Lenght_displayer.config(bg="white")
    else:
        Speed_insert.config(state=DISABLED,bg="gray")
        Lenght_displayer.config(bg="gray")
    c.after(500, Master_speed_checking)

def Master_name_checking():
    global Name_from_directory_checkbox_checking_variable
    if Master_name_checkbox_variable.get() == 1:
        Name_from_directory_checkbox.config(state=NORMAL,bg="white")
        if Name_from_directory_checkbox_checking_variable.get()==0:
            Name_insert.config(state=NORMAL,bg="white")
        Main_name = True
    else:
        Name_from_directory_checkbox.config(state=DISABLED,bg="darkgray")
        Name_insert.config(state=DISABLED,bg="gray")
        Main_name = False
    c.after(500, Master_name_checking)

def Master_save_checking():
    if Master_save_checkbox_variable.get() == 1:
        Save_directory_same_as_material_checkbox.config(state=NORMAL,bg="white")
        if Save_directory_checkbox_checking_variable.get() == 0:
            Directory_saving_btn.config(state=NORMAL,bg="white")
        Main_saving = True
    else:
        Save_directory_same_as_material_checkbox.config(state=DISABLED,bg="gray")
        Directory_saving_btn.config(state=DISABLED,bg="gray")
        Main_saving = False
    c.after(500,Master_save_checking)

#Other processes
def Confirm_folders():
    selected = [folder for folder, var in Manage_folders_variable.items() if var.get() == 1]
    if selected:
        print("Selected folders:")
        for folder in selected:
            print(f"{folder}")
    else:
        print("No folders selected.")

def Folder_settings(folder):
    def save_settings():
        repeat = Custom_repeat_insert.get("1.0","end-1c")
        fps = Custom_fps_scale.get()
        directory_name = Get_custom_name_from_directory_variable.get()
        name = Custom_name_insert.get("1.0","end-1c")
        if Save_directory_same_as_material_checkbox_CUSTOM_variable.get() == 0:
            save = fd.askdirectory()
        else:
            save = ""
            
        same_directory_save = Save_directory_same_as_material_checkbox_CUSTOM_variable.get()
        Folder_custom_settings[folder] = {
            "repeat": repeat,
            "fps": fps,
            "directory_name": directory_name,
            "name": name,
            "save": save,
            "same_as_directory_save": same_directory_save
        }
        settings_win.destroy()

    def Get_name_from_directory_CUSTOM_checking():
        if Get_custom_name_from_directory_variable.get() == 1:
         Custom_name_insert.config(state=DISABLED, bg="gray")
        else:
          Custom_name_insert.config(state=NORMAL, bg="white")
        settings_win.after(300, Get_name_from_directory_CUSTOM_checking)

    settings_win = Toplevel()
    settings_win.title(f"Settings for {folder}")
    settings_win.geometry("400x400")
    settings_win.iconbitmap("ico.ico")

    Label(settings_win, text=f"Settings for: {folder}", font=Font1).pack(pady=5)

    #Custom repeats
    Label(settings_win, text="Repeats: ",font=Font2).place(x=10,y=50)
    Custom_repeat_insert = Text(settings_win,width=3,height=1)
    Custom_repeat_insert.insert("1.0",Folder_custom_settings.get(folder, {}).get("repeat", 1))
    Custom_repeat_insert.place(x=100,y=50)

    #Custom speed
    Label(settings_win, text="Speed (FPS):",font=Font2).place(x=10,y=85)
    Custom_fps_scale = Scale(settings_win, from_=1, to=100, orient=HORIZONTAL)
    Custom_fps_scale.set(Folder_custom_settings.get(folder, {}).get("fps", default_fps))
    Custom_fps_scale.place(x=100,y=68)

    #Custom name
    Label(settings_win, text="Name: ",font=Font2).place(x=10,y=120)
    Custom_name_insert = Text(settings_win,width=20,height=1,bg="white")
    Custom_name_insert.place(x=100,y=120)
    #Get name from directory CUSTOM
    Label(settings_win,text="Get name\nfrom\ndirectory",font=Font3).place(x=270,y=105)
    Get_custom_name_from_directory = Checkbutton(settings_win,variable=Get_custom_name_from_directory_variable)
    Get_custom_name_from_directory.place(x=335,y=115)

    #Custom_saving_directory
    Label(settings_win,text="Save directory: ",font=Font2).place(x=10,y=255)
    #Same as material
    Label(settings_win,text="Same as\nsource folder",font=Font3).place(x=100,y=250)
    Save_directory_same_as_material_checkbox_CUSTOM = Checkbutton(settings_win,variable=Save_directory_same_as_material_checkbox_CUSTOM_variable)
    Save_directory_same_as_material_checkbox_CUSTOM.place(x=200,y=255)

    #Saving folder displayer
    Custom_saving_folder_displayer = Text(settings_win,width=47,height=2)
    Custom_saving_folder_displayer.place(x=10,y=320)

    Button(settings_win, text="Save", command=save_settings).place(x=180,y=360)

    #Checking
    Get_name_from_directory_CUSTOM_checking()

    Custom_saving_folder_displayer.insert("1.0","Saving directory is not selected")

    settings_win.mainloop()

def Manage_folders():
    global Manage_folders_variable

    Manage_folders_win = Toplevel()
    Manage_folders_win.title("Manage folders")
    Manage_folders_win.geometry("400x400")
    Manage_folders_win.iconbitmap("ico.ico")

    canvas = Canvas(Manage_folders_win)
    scrollbar = Scrollbar(Manage_folders_win, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    Label(scrollable_frame, text="Manage folders", font=('Arial', 14)).pack(pady=10, padx=130)

    Button(scrollable_frame, text="Leave", command=Manage_folders_win.destroy).place(x=5, y=0)
    Button(scrollable_frame, text="Confirm", command=Confirm_folders).place(x=325, y=0)

    header_frame = Frame(scrollable_frame)
    header_frame.pack(fill=X, pady=5)

    select_all_var = IntVar(value=1)

    def toggle_select_all():
        value = select_all_var.get()
        for var in Manage_folders_variable.values():
            var.set(value)

    try:
        for folder in os.listdir(root_folder):
            full_path = os.path.join(root_folder, folder)
            if not os.path.isdir(full_path):
                continue

            if folder not in Manage_folders_variable:
                Manage_folders_variable[folder] = IntVar(value=1)

            var = Manage_folders_variable[folder]

            row = Frame(scrollable_frame)
            row.pack(anchor="w", padx=20)
            Checkbutton(row, variable=var).pack(side=LEFT)
            Button(row, image=customize_img, command=lambda f=folder: Folder_settings(f)).pack(side=LEFT)
            Label(row, text=folder).pack(side=LEFT)
    except Exception as e:
        Label(scrollable_frame, text="Directory is not selected").pack()

    Checkbutton(scrollable_frame, variable=select_all_var, command=toggle_select_all).place(x=0, y=30)
    Label(scrollable_frame, text="Select all").place(x=20, y=30)

    Frame(scrollable_frame, height=20).pack()

def select_directory():
    global root_folder
    filename = fd.askdirectory()
    root_folder = filename

    Selected_folder_text.delete("1.0", "end")
    if root_folder:
        Selected_folder_text.insert("1.0", root_folder)
    else:
        Selected_folder_text.insert("1.0", "Not selected")

def select_save_folder():
    global save_folder_directory
    save_folder_directory = fd.askdirectory()

def Name_from_directory_checking():      
    if Name_from_directory_checkbox_checking_variable.get() == 1:
        Name_insert.config(state=DISABLED, bg="gray")
    elif Name_from_directory_checkbox_checking_variable.get() == 0 and Master_name_checkbox_variable == 1:
        Name_insert.config(state=NORMAL, bg="white")

    c.after(100, Name_from_directory_checking)

def Save_directory_checkbox_checking():
    Selected_saving_directory_text.delete("1.0", "end")
    if Save_directory_checkbox_checking_variable.get() == 1:
        Directory_saving_btn.config(state=DISABLED, bg="gray")
        if root_folder:
            Selected_saving_directory_text.insert("1.0", root_folder)
        else:
            Selected_saving_directory_text.insert("1.0", "Saving directory is not selected")
    elif Save_directory_checkbox_checking_variable.get() == 0 and Master_save_checkbox_variable == 1:
        Directory_saving_btn.config(state=NORMAL, bg="SystemButtonFace")
        try:
            Selected_saving_directory_text.insert("1.0", save_folder_directory)
        except:
            Selected_saving_directory_text.insert("1.0", "Saving directory is not selected")
    else:
        try:
            Selected_saving_directory_text.insert("1.0", save_folder_directory)
        except:
            Selected_saving_directory_text.insert("1.0", "Saving directory is not selected")

    c.after(100, Save_directory_checkbox_checking)

#Video lenght checking
def update_video_length_display():
    try:
        selected_folders = [
            os.path.join(root_folder, folder)
            for folder, var in Manage_folders_variable.items()
            if var.get() == 1
        ]

        if not selected_folders:
            if root_folder:
                selected_folders = [root_folder]
            else:
                Lenght_displayer.config(text="Estimated\nvideo length: N/A")
                c.after(1000, update_video_length_display)
                return

        total_images = 0
        repeats = int(Number_of_repeats_insert.get("1.0", "end-1c")) or 1
        speed = Speed_insert.get() or 1

        for folder in selected_folders:
            if os.path.isdir(folder):
                for _, _, files in os.walk(folder):
                    images = [f for f in files if f.lower().endswith((".jpg", ".png", ".jpeg"))]
                    total_images += len(images)

        total_frames = total_images * repeats
        total_seconds = total_frames / speed if speed else 0

        Lenght_displayer.config(text=f"Estimated\nvideo length: {total_seconds:.2f} sec")

    except Exception as e:
        Lenght_displayer.config(text="Error calculating length")

    c.after(500, update_video_length_display)

#Add elements
Title_text_Video_settings = Label(c,text="Images to video tool",font=Font1)
Title_text_Video_settings.place(x=160,y=0)

#Folder settings
Selected_folder_text = Text(c, height=2,width=57)
Selected_folder_text.place(x=7,y=25)

Directory_text = Label(c, text="Directory",font=Font2)
Directory_text.place(x=0,y=66)

Directory_btn = Button(c,text="Open folder",command=select_directory)
Directory_btn.place(x=90,y=63)

Manage_folders_btn = Button(c,text="Manage Folders",command=Manage_folders)
Manage_folders_btn.place(x=170,y=63)

#Master checkboxes
Use_master_settings_text = Label(c,text="Use main settings")
Use_master_settings_text.place(x=360,y=100)

Master_repeats_checkbox = Checkbutton(c,variable=Master_repeats_checkbox_variable)
Master_repeats_checkbox.place(x=400,y=145)

Master_speed_checkbox = Checkbutton(c,variable=Master_speed_checkbox_variable)
Master_speed_checkbox.place(x=400,y=190)

Master_name_checkbox = Checkbutton(c,variable=Master_name_checkbox_variable)
Master_name_checkbox.place(x=400,y=240)

Master_save_checkbox = Checkbutton(c,variable=Master_save_checkbox_variable)
Master_save_checkbox.place(x=400,y=285)

#repeats
Number_of_repeats_text = Label(c,text="Number of Repeats",font=Font2)
Number_of_repeats_text.place(x=0,y=155)

Number_of_repeats_insert = Text(c, height=1,width=4,bg="white")
Number_of_repeats_insert.place(x=160,y=155)
Number_of_repeats_insert.insert("1.0","1")

#speed
Speed_text = Label(c, text="Speed",font=Font2)
Speed_text.place(x=0,y=200)

Speed_insert = Scale(c, from_=0,to=100,orient=HORIZONTAL,bg="white")
Speed_insert.place(x=90,y=180)

Lenght_displayer = Label(c, text="Estimated\nvideo length: 0.00 sec",font=Font3)
Lenght_displayer.place(x=200, y=190)

#name
Name_text = Label(c, text="Name",font=Font2)
Name_text.place(x=0,y=240)

Name_insert = Text(c, height=2,width=15,bg="white")
Name_insert.insert("1.0","New animation")
Name_insert.place(x=70,y=240)

Name_from_directory_checkbox_text = Label(c,text="Get name \nfrom \ndirectory",font=Font3)
Name_from_directory_checkbox_text.place(x=200,y=230)

Name_from_directory_checkbox = Checkbutton(c,variable=Name_from_directory_checkbox_checking_variable)
Name_from_directory_checkbox.place(x=260,y=240)

#Saving
Save_directory_text = Label(c,text="Save directory",font=Font2)
Save_directory_text.place(x=0,y=290)

Directory_saving_btn = Button(c,text="Select folder",command=select_save_folder)
Directory_saving_btn.place(x=90,y=290)

Save_directory_same_as_material_text = Label(c,text="Same as\nsource folder",font=Font3)
Save_directory_same_as_material_text.place(x=190,y=285)

Save_directory_same_as_material_checkbox = Checkbutton(c,variable=Save_directory_checkbox_checking_variable)
Save_directory_same_as_material_checkbox.place(x=260,y=290)

Selected_saving_directory_text = Text(c, height=2,width=57)
Selected_saving_directory_text.place(x=7,y=325)

def count_total_frames(folders):
    total = 0
    repeats = int(Number_of_repeats_insert.get("1.0", "end-1c"))
    for folder_path in folders:
        for root, _, files in os.walk(folder_path):
            images = [f for f in files if f.lower().endswith((".jpg", ".png", ".jpeg"))]
            total += len(images) * repeats
    return total

def get_effective_custom_settings(folder_path):
    current_path = folder_path
    while True:
        folder_name = os.path.basename(current_path)
        if folder_name in Folder_custom_settings:
            return Folder_custom_settings[folder_name]
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break
        current_path = parent_path
    return {}

def process_images_in_folder(folder_path, total_frames, frame_tracker):
    custom_settings = get_effective_custom_settings(folder_path)

    # Repeats
    if Master_repeats_checkbox_variable.get() == 1:
        repeats = int(Number_of_repeats_insert.get("1.0", "end-1c"))
    else:
        repeats = int(custom_settings.get("repeat", 1))

    # FPS
    if Master_speed_checkbox_variable.get() == 1:
        fps = Speed_insert.get()
    else:
        fps = custom_settings.get("fps", default_fps)

    # Video name
    if Master_name_checkbox_variable.get() == 1:
        if Name_from_directory_checkbox_checking_variable.get() == 1:
            relative_path = os.path.relpath(folder_path, root_folder)
            output_video_name = relative_path.replace("\\", "_").replace("/", "") + ".mp4"
        else:
            user_base_name = Name_insert.get("1.0", "end-1c").strip()
            folder_name = os.path.basename(folder_path)
            output_video_name = f"{user_base_name}.mp4"
    else:
        if custom_settings.get("directory_name",0)==1:
            relative_path = os.path.relpath(folder_path, root_folder)
            output_video_name = relative_path.replace("\\", "_").replace("/", "") + ".mp4"
        else:
            name = custom_settings.get("name", "output")
            output_video_name = f"{name}.mp4"

    # Save path
    if Master_save_checkbox_variable.get() == 1:
        if Save_directory_checkbox_checking_variable.get() == 1:
            save_path = folder_path
        else:
            try:
                save_path = save_folder_directory
            except:
                messagebox.showerror("No directory", "You haven't selected a saving directory")
                return
    else:
        if custom_settings.get("same_as_directory_save", 0)==1:
            save_path = folder_path
        else:
            save_path = custom_settings.get("save")

    images = [img for img in os.listdir(folder_path) if img.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not images:
        return

    images.sort()
    first_image = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, _ = first_image.shape

    base_name, extension = os.path.splitext(output_video_name)
    video_path = os.path.join(save_path, output_video_name)
    
    counter = 1
    while os.path.exists(video_path):
        output_video_name = f"{base_name}_{counter}{extension}"
        video_path = os.path.join(save_path, output_video_name)
        counter += 1

    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), float(fps), (width, height))

    for _ in range(repeats):
        for image_name in images:
            img_path = os.path.join(folder_path, image_name)
            frame = cv2.imread(img_path)
            video.write(frame)

            frame_tracker[0] += 1
            progress_bar['value'] = int((frame_tracker[0] / total_frames) * 100)
            c.update_idletasks()

    video.release()
    print(f"Video saved in: {video_path}")

def process_all_folders(root_folder):
    selected_folders = [
        os.path.join(root_folder, folder)
        for folder, var in Manage_folders_variable.items()
        if var.get() == 1
    ]
    
    if not selected_folders:
        selected_folders = [os.path.join(root, "") for root, _, files in os.walk(root_folder)
                            if any(file.lower().endswith((".jpg", ".png", ".jpeg")) for file in files)]

    total_frames = count_total_frames(selected_folders)

    if total_frames == 0:
        messagebox.showerror("No images", "No image files found.")
        return

    frame_tracker = [0]
    for folder_path in selected_folders:
        for root, _, files in os.walk(folder_path):
            if any(file.lower().endswith((".jpg", ".png", ".jpeg")) for file in files):
                process_images_in_folder(root, total_frames, frame_tracker)

    progress_bar['value'] = 100
    messagebox.showinfo("Process ended", "Process has successfully ended")
    progress_bar['value'] = 0

def Render():
    process_all_folders(root_folder)

Render_btn = Button(c, text="Render",command=Render)
Render_btn.place(x=425,y=370)

Cancel_btn = Button(c, text="Exit", command=c.destroy)
Cancel_btn.place(x=5,y=370)

progress_bar = Progressbar(c, orient="horizontal", length=375, mode="determinate")
progress_bar.place(x=43,y=372)

Save_directory_checkbox_checking()
Name_from_directory_checking()
update_video_length_display()

Master_repeats_checking()
Master_speed_checking()
Master_name_checking()
Master_save_checking()

Selected_folder_text.insert("1.0", "Main folder is not selected")
Selected_saving_directory_text.insert("1.0", "Saving directory is not selected")
Speed_insert.set("15")

c.mainloop()
