import os
import cv2
from tkinter import*
from tkinter import messagebox, PhotoImage, ttk, filedialog as fd
from tkinter.ttk import Progressbar

#Default settings
root_folder = ""
default_fps = 15
video_name = "New animation"

Manage_folders_variable = {}
Folder_custom_settings = {}

#Define fonts
Font1 = ("Arial",18)
Font2 = ("Arial",10)
Font3 = ("Arial",8)
Font_lenght = ("Arial",22)

#Main window
c= Tk()
c.attributes("-fullscreen", False)
c.title("Images to video")
c.iconbitmap("ico.ico")
c.state("zoomed")
scrn_width, scrn_height = c.winfo_screenwidth(), c.winfo_screenheight()
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
        Lenght_displayer.config(bg=Bottom_panel["bg"])
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
        same_directory_save = Save_directory_same_as_material_checkbox_CUSTOM_variable.get()
        
        save_path = custom_save_path if 'custom_save_path' in locals() else Folder_custom_settings.get(folder, {}).get('save', "")
        
        Folder_custom_settings[folder] = {
            "repeat": repeat,
            "fps": fps,
            "directory_name": directory_name,
            "name": name,
            "save": save_path,
            "same_as_directory_save": same_directory_save
        }
        settings_win.destroy()

    def on_closing():
        if Save_directory_same_as_material_checkbox_CUSTOM_variable.get() == 0:
            current_save_path = custom_save_path if 'custom_save_path' in locals() else Folder_custom_settings.get(folder, {}).get('save', "")
            if not current_save_path:
                response = messagebox.askyesno(
                    "Unsaved changes",
                    "Are you sure you want to continue\nwithout saving?",
                    icon='warning'
                )
                
                if response is None:
                    settings_win.lift()
                    settings_win.focus_force()
                    return
                elif not response:
                    settings_win.lift()
                    settings_win.focus_force()
                    return
        
        settings_win.destroy()

    def select_custom_save_directory():
        nonlocal custom_save_path
        custom_save_path = fd.askdirectory()
        if custom_save_path:
            Custom_saving_folder_displayer.delete("1.0", "end")
            Custom_saving_folder_displayer.insert("1.0", custom_save_path)

    def Get_name_from_directory_CUSTOM_checking():
        if Get_custom_name_from_directory_variable.get() == 1:
            Custom_name_insert.config(state=DISABLED, bg="gray")
        else:
            Custom_name_insert.config(state=NORMAL, bg="white")
        settings_win.after(300, Get_name_from_directory_CUSTOM_checking)

    # Check if window already exists for this folder
    for window in c.winfo_children():
        if isinstance(window, Toplevel) and window.title() == f"Settings for {folder}":
            window.lift()
            window.focus_force()
            return

    settings_win = Toplevel()
    settings_win.title(f"Settings for {folder}")
    settings_win.geometry("400x400")
    settings_win.iconbitmap("ico.ico")
    settings_win.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Bring window to front and focus
    settings_win.lift()
    settings_win.focus_force()

    folder_settings = Folder_custom_settings.get(folder, {})
    custom_save_path = folder_settings.get("save", "")

    Label(settings_win, text=f"Settings for: {folder}", font=Font1).pack(pady=5)

    Label(settings_win, text="Repeats: ",font=Font2).place(x=10,y=50)
    Custom_repeat_insert = Text(settings_win,width=3,height=1)
    Custom_repeat_insert.insert("1.0", folder_settings.get("repeat", 1))
    Custom_repeat_insert.place(x=100,y=50)

    # Custom speed
    Label(settings_win, text="Speed (FPS):",font=Font2).place(x=10,y=85)
    Custom_fps_scale = Scale(settings_win, from_=1, to=100, orient=HORIZONTAL)
    Custom_fps_scale.set(folder_settings.get("fps", default_fps))
    Custom_fps_scale.place(x=100,y=68)

    # Custom name
    Label(settings_win, text="Name: ",font=Font2).place(x=10,y=120)
    Custom_name_insert = Text(settings_win,width=20,height=1,bg="white")
    Custom_name_insert.insert("1.0", folder_settings.get("name", ""))
    Custom_name_insert.place(x=100,y=120)
    
    # Get name from directory CUSTOM
    Label(settings_win,text="Get name\nfrom\ndirectory",font=Font3).place(x=270,y=105)
    Get_custom_name_from_directory = Checkbutton(settings_win,variable=Get_custom_name_from_directory_variable)
    Get_custom_name_from_directory.place(x=335,y=115)
    Get_custom_name_from_directory_variable.set(folder_settings.get("directory_name", 0))

    # Custom_saving_directory
    Label(settings_win,text="Save directory: ",font=Font2).place(x=10,y=255)
    
    # Same as material checkbox
    Label(settings_win,text="Same as\nsource folder",font=Font3).place(x=100,y=250)
    Save_directory_same_as_material_checkbox_CUSTOM = Checkbutton(settings_win,
                                                                variable=Save_directory_same_as_material_checkbox_CUSTOM_variable)
    Save_directory_same_as_material_checkbox_CUSTOM.place(x=200,y=255)
    Save_directory_same_as_material_checkbox_CUSTOM_variable.set(folder_settings.get("same_as_directory_save", 0))

    Button(settings_win, text="Select Folder", command=select_custom_save_directory).place(x=250,y=250)

    Custom_saving_folder_displayer = Text(settings_win,width=47,height=2)
    Custom_saving_folder_displayer.place(x=10,y=320)
    if custom_save_path:
        Custom_saving_folder_displayer.insert("1.0", custom_save_path)
    else:
        Custom_saving_folder_displayer.insert("1.0", "Saving directory is not selected")

    Button(settings_win, text="Save", command=save_settings).place(x=180,y=360)

    Get_name_from_directory_CUSTOM_checking()
    
    # Keep the window on top
    settings_win.attributes('-topmost', True)
    settings_win.after(100, lambda: settings_win.attributes('-topmost', False))
    
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

def update_manage_folders_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    Label(scrollable_frame, text="Manage folders", font=('Arial', 14)).pack(pady=10, padx=130)

    header_frame = Frame(scrollable_frame)
    header_frame.pack(fill=X, pady=5)

    def toggle_select_all():
        value = select_all_var.get()
        for var in Manage_folders_variable.values():
            var.set(value)

    Checkbutton(scrollable_frame, variable=select_all_var, command=toggle_select_all).place(x=0, y=30)
    Label(scrollable_frame, text="Select all").place(x=20, y=30)
    Frame(scrollable_frame, height=20).pack()

    Manage_folders_variable.clear()
    try:
        for folder in os.listdir(root_folder):
            full_path = os.path.join(root_folder, folder)
            if not os.path.isdir(full_path):
                continue

            Manage_folders_variable[folder] = IntVar(value=1)
            var = Manage_folders_variable[folder]

            row = Frame(scrollable_frame)
            row.pack(anchor="w", padx=20)
            Checkbutton(row, variable=var).pack(side=LEFT)
            Button(row, image=customize_img, command=lambda f=folder: Folder_settings(f)).pack(side=LEFT)
            Label(row, text=folder).pack(side=LEFT)

    except Exception as e:
        Label(scrollable_frame, text="Directory is not selected").pack()

def update_image_and_video_counts():
    try:
        if not root_folder:
            Video_count_text.config(text="0")
            Image_count_text.config(text="0")
            c.after(1000, update_image_and_video_counts)
            return
            
        selected_folders = [
            os.path.join(root_folder, folder)
            for folder, var in Manage_folders_variable.items()
            if var.get() == 1
        ]
        
        if not selected_folders and root_folder:
            selected_folders = [root_folder]
        
        final_folders = []
        total_images = 0
        
        for folder in selected_folders:
            if os.path.isdir(folder):
                for root, dirs, files in os.walk(folder):
                    if not dirs:
                        final_folders.append(root)
                        images = [
                            f for f in files
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
                        ]
                        total_images += len(images)
        
        Video_count_text.config(text=str(len(final_folders)))
        Image_count_text.config(text=str(total_images))
        
    except Exception as e:
        print(f"Error updating counts: {e}")
        Video_count_text.config(text="Error")
        Image_count_text.config(text="Error")
    
    c.after(1000, update_image_and_video_counts)
def select_directory():
    global root_folder
    filename = fd.askdirectory()
    root_folder = filename

    Selected_folder_text.delete("1.0", "end")
    if root_folder:
        Selected_folder_text.insert("1.0", root_folder)
        update_manage_folders_list()
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

def process_all_folders():
    selected_folders = [
        os.path.join(root_folder, folder)
        for folder, var in Manage_folders_variable.items()
        if var.get() == 1
    ]
    
    if not selected_folders:
        selected_folders = [root_folder]
        print(f"[DEBUG] No folders selected, using root: {root_folder}")

    print(f"[DEBUG] Folders to process: {selected_folders}")
    
    final_folders = []
    for folder in selected_folders:
        for root, dirs, files in os.walk(folder):
            if not dirs:
                final_folders.append(root)
    
    if not final_folders:
        messagebox.showerror("Error", "No final folders found (folders without subfolders)")
        return
    
    print(f"[DEBUG] Found {len(final_folders)} final folders to process")
    
    total_frames = 0
    for folder in final_folders:
        images = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        total_frames += len(images) * (int(Number_of_repeats_insert.get("1.0", "end-1c")) or 1)
    
    if total_frames == 0:
        messagebox.showerror("Error", "No images found in any final folder")
        return
    
    frame_tracker = [0]
    success_count = 0
    
    for folder in final_folders:
        try:
            result_path = process_single_folder(folder, total_frames, frame_tracker)
            if result_path:
                success_count += 1
                print(f"[SUCCESS] Created video: {result_path}")
        except Exception as e:
            print(f"[ERROR] Failed to process {folder}: {str(e)}")
    
    messagebox.showinfo("Process complete", 
                      f"Successfully created {success_count} videos.")
    progress_bar['value'] = 0

def process_single_folder(folder_path, total_frames, frame_tracker):
    custom_settings = get_effective_custom_settings(folder_path)
    
    images = [f for f in os.listdir(folder_path) 
              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not images:
        print(f"[WARNING] No images in final folder: {folder_path}")
        return None

    images.sort()
    print(f"[DEBUG] Processing {len(images)} images in final folder: {folder_path}")

    repeats = int(custom_settings.get("repeat", Number_of_repeats_insert.get("1.0", "end-1c"))) if Master_repeats_checkbox_variable.get() != 1 else int(Number_of_repeats_insert.get("1.0", "end-1c"))
    fps = custom_settings.get("fps", Speed_insert.get()) if Master_speed_checkbox_variable.get() != 1 else Speed_insert.get()

    relative_path = os.path.relpath(folder_path, root_folder)
    clean_name = relative_path.replace("\\", "").replace("/", "").replace(" ", "_")
    
    if Master_name_checkbox_variable.get() == 1:
        video_name = (clean_name + ".mp4" if Name_from_directory_checkbox_checking_variable.get() == 1 
                     else Name_insert.get("1.0", "end-1c").strip() + ".mp4")
    else:
        video_name = (clean_name + ".mp4" if custom_settings.get("directory_name", 0) == 1 
                     else custom_settings.get("name", "output") + ".mp4")

    if Master_save_checkbox_variable.get() == 1:
        save_path = folder_path if Save_directory_checkbox_checking_variable.get() == 1 else save_folder_directory
    else:
        save_path = folder_path if custom_settings.get("same_as_directory_save", 0) == 1 else custom_settings.get("save", folder_path)

    os.makedirs(save_path, exist_ok=True)

    first_img = cv2.imread(os.path.join(folder_path, images[0]))
    if first_img is None:
        print(f"[ERROR] Cannot read first image: {images[0]}")
        return None
        
    height, width = first_img.shape[:2]

    base_name, ext = os.path.splitext(video_name)
    counter = 1
    output_path = os.path.join(save_path, video_name)
    while os.path.exists(output_path):
        output_path = os.path.join(save_path, f"{base_name}_{counter}{ext}")
        counter += 1

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, float(fps), (width, height))
    
    if not video.isOpened():
        print(f"[ERROR] Cannot create video file: {output_path}")
        return None

    for _ in range(repeats):
        for img_name in images:
            img_path = os.path.join(folder_path, img_name)
            frame = cv2.imread(img_path)
            if frame is not None:
                video.write(frame)
                frame_tracker[0] += 1
                progress_bar['value'] = (frame_tracker[0] / total_frames) * 100
                c.update_idletasks()
            else:
                print(f"[WARNING] Cannot read image: {img_path}")

    video.release()
    return output_path

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
                Lenght_displayer.config(text="N/A")
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

        Lenght_displayer.config(text=f"{total_seconds:.2f} sec")

    except Exception as e:
        Lenght_displayer.config(text="Error calculating length")

    c.after(500, update_video_length_display)

#Menu_bar
menu_bar = Menu(c)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open folder", command=select_directory)
file_menu.add_command(label="Render", command=process_all_folders)

Program_menu = Menu(file_menu, tearoff=0)
Program_menu.add_command(label="Exit", command=c.destroy)

Windows_menu = Menu(menu_bar, tearoff=0)
Windows_menu.add_command(label="Open Manage folders as window",command=Manage_folders)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Program",menu=Program_menu)
menu_bar.add_cascade(label="Windows", menu=Windows_menu)

c.config(menu=menu_bar,bg="#c3c3c3")

#Add elements
Title_text_Video_settings = Label(c,text="Images to video tool",font=Font1,bg="#c3c3c3")
Title_text_Video_settings.pack(pady=scrn_height*0.02)

Selected_folder_text = Text(c, height=2,width=57)
Selected_folder_text.place(x=scrn_width*0.02,y=scrn_height*0.02)

progress_bar = Progressbar(c, orient="horizontal", length=375, mode="determinate")
progress_bar.place(x=scrn_width*0.65,y=scrn_height*0.029)

#Main window frame
Main_window_frame = Frame(c)
Main_window_frame.pack(side=TOP, fill=BOTH, expand=True) 

stats_frame = Frame(c, bg="white")
stats_frame.place(relx=0, rely=0.095, relwidth=0.3, relheight=0.9)
stats_frame.grid_columnconfigure(2, weight=1)
stats_frame.grid_columnconfigure(1, weight=1)

Manage_folders_frame = Frame(c)
Manage_folders_frame.place(x=scrn_width*0.7, y=scrn_height*0.085, relwidth=0.3, relheight=0.9)

Bottom_panel = Frame(c,bg="#b0b0b0")
Bottom_panel.place(x=0, y=scrn_height*0.8, relwidth=1, relheight=0.1)

#Separator
separator_header = ttk.Separator(c, orient='horizontal')
separator_header.place(x=0,y=scrn_height*0.08,relwidth=1, relx=0.0)

separator_stats = ttk.Separator(c,orient="vertical")
separator_stats.place(x=scrn_width*0.3,y=scrn_height*0.085,relwidth=0.002,relheight=0.9)

separator_Manage_folders = ttk.Separator(c, orient='vertical')
separator_Manage_folders.place(x=scrn_width*0.7, y=scrn_height*0.085, relwidth=0.002, relheight=0.9)

separator_footer = ttk.Separator(c, orient='horizontal')
separator_footer.place(x=0,y=scrn_height*0.8,relwidth=1, relx=0.0)

#Master checkboxes
Use_master_settings_text = Label(c,text="Use main settings")
Use_master_settings_text.place(x=scrn_width*0.61,y=scrn_height*0.1)

Master_repeats_checkbox = Checkbutton(c,variable=Master_repeats_checkbox_variable)
Master_repeats_checkbox.place(x=scrn_width*0.65,y=scrn_height*0.15)

Master_speed_checkbox = Checkbutton(c,variable=Master_speed_checkbox_variable)
Master_speed_checkbox.place(x=scrn_width*0.65,y=scrn_height*0.25)

Master_name_checkbox = Checkbutton(c,variable=Master_name_checkbox_variable)
Master_name_checkbox.place(x=scrn_width*0.65,y=scrn_height*0.35)

Master_save_checkbox = Checkbutton(c,variable=Master_save_checkbox_variable)
Master_save_checkbox.place(x=scrn_width*0.65,y=scrn_height*0.45)

#repeats
Number_of_repeats_text = Label(c,text="Number of Repeats",font=Font2)
Number_of_repeats_text.place(x=scrn_height*0.55,y=scrn_height*0.15)

Number_of_repeats_insert = Text(c, height=1,width=4,bg="white")
Number_of_repeats_insert.place(x=scrn_width*0.42,y=scrn_height*0.15)
Number_of_repeats_insert.insert("1.0","1")

#speed
Speed_text = Label(c, text="Speed (FPS)",font=Font2)
Speed_text.place(x=scrn_width*0.34,y=scrn_height*0.25)

Speed_insert = Scale(c, from_=1,to=200,orient=HORIZONTAL,bg="white",length=scrn_width*0.2)
Speed_insert.place(x=scrn_width*0.42,y=scrn_height*0.23)

Lenght_displayer = Label(c, text="0.00 sec",font=Font_lenght)
Lenght_displayer.place(x=scrn_width*0.85, y=scrn_height*0.83)

Lenght_displayer_text = Label(c, text="Estimated video length",font=Font2,bg=Bottom_panel["bg"])
Lenght_displayer_text.place(x=scrn_width*0.85, y=scrn_height*0.80)

#name
Name_text = Label(c, text="Name",font=Font2)
Name_text.place(x=scrn_width*0.34,y=scrn_height*0.35)

Name_insert = Text(c, height=2,width=15,bg="white")
Name_insert.insert("1.0","New animation")
Name_insert.place(x=scrn_width*0.42,y=scrn_height*0.35)

Name_from_directory_checkbox_text = Label(c,text="Get name \nfrom \ndirectory",font=Font3)
Name_from_directory_checkbox_text.place(x=scrn_width*0.53,y=scrn_height*0.34)

Name_from_directory_checkbox = Checkbutton(c,variable=Name_from_directory_checkbox_checking_variable)
Name_from_directory_checkbox.place(x=scrn_width*0.58,y=scrn_height*0.35)

#Folder settings
canvas = Canvas(Manage_folders_frame, bg="#c3c3c3")
scrollbar = Scrollbar(Manage_folders_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

Label(scrollable_frame, text="Manage folders", font=('Arial', 14)).pack(pady=10, padx=130,expand=True)

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


#Saving
Saving_master_text = Label(c,text="Saving",font=Font2)
Saving_master_text.place(x=scrn_width*0.34,y=scrn_height*0.44)

Save_directory_text = Label(c,text="Save directory",font=Font2,bg=Bottom_panel["bg"])
Save_directory_text.place(x=0,y=scrn_height*0.82)

Directory_saving_btn = Button(c,text="Select folder",command=select_save_folder)
Directory_saving_btn.place(x=scrn_width*0.08,y=scrn_height*0.82)

Save_directory_same_as_material_text = Label(c,text="Same as\nsource folder",font=Font3,bg=Bottom_panel["bg"])
Save_directory_same_as_material_text.place(x=scrn_width*0.15,y=scrn_height*0.81)

Save_directory_same_as_material_checkbox = Checkbutton(c,variable=Save_directory_checkbox_checking_variable,bg=Bottom_panel["bg"])
Save_directory_same_as_material_checkbox.place(x=scrn_width*0.22,y=scrn_height*0.82)

Selected_saving_directory_text = Text(c, height=2,width=57)
Selected_saving_directory_text.place(x=scrn_width*0.32,y=scrn_height*0.81)

#Stats frame
Label(stats_frame, text="Stats", font=('Arial', 14), bg="white").grid(row=0, column=1, columnspan=2, pady=10)
 
Label(stats_frame, text="Number of videos:", font=Font2, bg="white", anchor="e").grid(row=1, column=0, sticky="e", padx=5)
Video_count_text = Label(stats_frame, text="0", font=Font2, bg="white", width=8, anchor="e")
Video_count_text.grid(row=1, column=3, sticky="w", padx=5)

Label(stats_frame, text="Number of pictures:", font=Font2, bg="white", anchor="e").grid(row=2, column=0, sticky="e", padx=5)
Image_count_text = Label(stats_frame, text="0", font=Font2, bg="white", width=8, anchor="e")
Image_count_text.grid(row=2, column=3, sticky="w", padx=5)

#Video processing
def count_total_frames(folders):
    total = 0
    for folder in folders:
        for root, _, files in os.walk(folder):
            images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            total += len(images)
            print(f"[DEBUG] Folder: {root} | Images: {len(images)}")
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
    
    images = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(os.path.join(root, file))
    
    if not images:
        print(f"[ERROR] No images found in: {folder_path}")
        return

    print(f"[DEBUG] Found {len(images)} images in folder tree: {folder_path}")

    images.sort()
    
    repeats = int(custom_settings.get("repeat", Number_of_repeats_insert.get("1.0", "end-1c"))) if Master_repeats_checkbox_variable.get() != 1 else int(Number_of_repeats_insert.get("1.0", "end-1c"))
    fps = custom_settings.get("fps", Speed_insert.get()) if Master_speed_checkbox_variable.get() != 1 else Speed_insert.get()

    if Master_name_checkbox_variable.get() == 1:
        output_video_name = (os.path.basename(folder_path) + ".mp4" if Name_from_directory_checkbox_checking_variable.get() == 1 else Name_insert.get("1.0", "end-1c").strip() + ".mp4")
    else:
        output_video_name = (os.path.basename(folder_path) + ".mp4" if custom_settings.get("directory_name", 0) == 1 else custom_settings.get("name", "output") + ".mp4")

    if Master_save_checkbox_variable.get() == 1:
        save_path = folder_path if Save_directory_checkbox_checking_variable.get() == 1 else save_folder_directory
    else:
        save_path = folder_path if custom_settings.get("same_as_directory_save", 0) == 1 else custom_settings.get("save", folder_path)

    os.makedirs(save_path, exist_ok=True)

    first_image = cv2.imread(images[0])
    if first_image is None:
        print(f"[ERROR] Cannot read first image: {images[0]}")
        return
        
    height, width, _ = first_image.shape

    base_name, extension = os.path.splitext(output_video_name)
    video_path = os.path.join(save_path, output_video_name)
    
    counter = 1
    while os.path.exists(video_path):
        output_video_name = f"{base_name}_{counter}{extension}"
        video_path = os.path.join(save_path, output_video_name)
        counter += 1

    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_path, fourcc, float(fps), (width, height))
        
        if not video.isOpened():
            print(f"[ERROR] Cannot create video file: {video_path}")
            return

        for _ in range(repeats):
            for img_path in images:
                frame = cv2.imread(img_path)
                if frame is not None:
                    video.write(frame)
                    frame_tracker[0] += 1
                    progress = int((frame_tracker[0] / total_frames) * 100)
                    progress_bar['value'] = progress
                    c.update_idletasks()
                else:
                    print(f"[WARNING] Cannot read image: {img_path}")

        video.release()
        print(f"[SUCCESS] Video successfully saved to: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"[ERROR] Video creation failed: {str(e)}")
        return None

Save_directory_checkbox_checking()
Name_from_directory_checking()
update_video_length_display()
update_image_and_video_counts()

Master_repeats_checking()
Master_speed_checking()
Master_name_checking()
Master_save_checking()

Selected_folder_text.insert("1.0", "Main folder is not selected")
Selected_saving_directory_text.insert("1.0", "Saving directory is not selected")
Speed_insert.set("15")

c.mainloop()
