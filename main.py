import os
import cv2
from tkinter import messagebox
from tkinter import*
from tkinter import filedialog as fd
from tkinter.ttk import Progressbar

#Default settings
root_folder = ""
default_fps = 15
video_name = "New animation"

Manage_folders_variable = {}

Font1 = ("Arial",13)
Font2 = ("Arial",10)
Font3 = ("Arial",8)

#Main window
c= Tk()
c.geometry("425x400")
c.resizable(False, False)
c.title("Images to video")

Name_from_directory_checkbox_checking_variable = IntVar()
Save_directory_checkbox_checking_variable = IntVar(value=1)

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
    else:
        Name_insert.config(state=NORMAL, bg="white")

    c.after(100, Name_from_directory_checking)

def Save_directory_checkbox_checking():
    Selected_saving_directory_text.delete("1.0", "end")

    if Save_directory_checkbox_checking_variable.get() == 1:
        Directory_saving_btn.config(state=DISABLED, bg="gray")
        if root_folder:
            Selected_saving_directory_text.insert("1.0", root_folder)
        else:
            Selected_saving_directory_text.insert("1.0", "Not selected")
    else:
        Directory_saving_btn.config(state=NORMAL, bg="SystemButtonFace")
        try:
            Selected_saving_directory_text.insert("1.0", save_folder_directory)
        except:
            Selected_saving_directory_text.insert("1.0", "Not selected")

    c.after(100, Save_directory_checkbox_checking)

def Confirm_folders():
    selected = [folder for folder, var in Manage_folders_variable.items() if var.get() == 1]
    if selected:
        print("Selected folders:")
        for folder in selected:
            print(f"{folder}")
    else:
        print("No folders selected.")

def Manage_folders():
    global Manage_folders_variable

    Manage_folders_win = Toplevel()
    Manage_folders_win.title("Manage folders")
    Manage_folders_win.geometry("400x400")

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
                Manage_folders_variable[folder] = IntVar(value=1)  # auto checked

            var = Manage_folders_variable[folder]

            row = Frame(scrollable_frame)
            row.pack(anchor="w", padx=20)
            Checkbutton(row, variable=var).pack(side=LEFT)
            Label(row, text=folder).pack(side=LEFT)

    except Exception as e:
        Label(scrollable_frame, text="Directory is not selected").pack()

    Checkbutton(scrollable_frame, variable=select_all_var, command=toggle_select_all).place(x=0, y=30)
    Label(scrollable_frame, text="Select all").place(x=20, y=30)

    Frame(scrollable_frame, height=20).pack()

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
                Lenght_displayer.config(text="Video length: N/A")
                c.after(1000, update_video_length_display)
                return

        total_images = 0
        repeats = int(Number_of_repeats_insert.get("1.0", "end-1c")) or 1
        speed = Speed_insert.get() or 1  # avoid zero

        for folder in selected_folders:
            if os.path.isdir(folder):
                for _, _, files in os.walk(folder):
                    images = [f for f in files if f.lower().endswith((".jpg", ".png", ".jpeg"))]
                    total_images += len(images)

        total_frames = total_images * repeats
        total_seconds = total_frames / speed if speed else 0

        Lenght_displayer.config(text=f"Video length: {total_seconds:.2f} sec")

    except Exception as e:
        Lenght_displayer.config(text="Error calculating length")

    # Repeat every 1 second
    c.after(1000, update_video_length_display)


#Add elements
Title_text_Video_settings = Label(c,text="Images to video tool",font=Font1)
Title_text_Video_settings.place(x=130,y=0)

Selected_folder_text = Text(c, height=2,width=51)
Selected_folder_text.place(x=7,y=25)

Directory_text = Label(c, text="Directory",font=Font2)
Directory_text.place(x=0,y=66)

Directory_btn = Button(c,text="Open folder",command=select_directory)
Directory_btn.place(x=90,y=63)

Manage_folders_btn = Button(c,text="Manage Folders",command=Manage_folders)
Manage_folders_btn.place(x=170,y=63)

Number_of_repeats_text = Label(c,text="Number of Repeats",font=Font2)
Number_of_repeats_text.place(x=0,y=165)

Number_of_repeats_insert = Text(c, height=1,width=4)
Number_of_repeats_insert.place(x=160,y=165)
Number_of_repeats_insert.insert("1.0","1")

Speed_text = Label(c, text="Speed",font=Font2)
Speed_text.place(x=0,y=210)

Speed_insert = Scale(c, from_=0,to=100,orient=HORIZONTAL)
Speed_insert.place(x=100,y=190)

Lenght_displayer = Label(c, text="Video length: 0.00 sec")
Lenght_displayer.place(x=250, y=200)

Name_text = Label(c, text="Name",font=Font2)
Name_text.place(x=0,y=240)

Name_insert = Text(c, height    =2,width=15,)
Name_insert.insert("1.0","New animation")
Name_insert.place(x=70,y=240)

Name_from_directory_checkbox_text = Label(c,text="Get name \nfrom \ndirectory",font=Font3)
Name_from_directory_checkbox_text.place(x=200,y=230)

Name_from_directory_checkbox = Checkbutton(c,variable=Name_from_directory_checkbox_checking_variable)
Name_from_directory_checkbox.place(x=260,y=240)

Save_directory_text = Label(c,text="Save directory",font=Font2)
Save_directory_text.place(x=0,y=290)

Directory_saving_btn = Button(c,text="Select folder",command=select_save_folder)
Directory_saving_btn.place(x=90,y=290)

Save_directory_same_as_material_text = Label(c,text="Same as\nmaterial",font=Font3)
Save_directory_same_as_material_text.place(x=200,y=285)

Save_directory_same_as_material_checkbox = Checkbutton(c,variable=Save_directory_checkbox_checking_variable)
Save_directory_same_as_material_checkbox.place(x=260,y=290)

Selected_saving_directory_text = Text(c, height=2,width=51)
Selected_saving_directory_text.place(x=7,y=325)

def count_total_frames(folders):
    total = 0
    repeats = int(Number_of_repeats_insert.get("1.0", "end-1c"))
    for folder_path in folders:
        for root, _, files in os.walk(folder_path):
            images = [f for f in files if f.lower().endswith((".jpg", ".png", ".jpeg"))]
            total += len(images) * repeats
    return total

def process_images_in_folder(folder_path, total_frames, frame_tracker):
    if Name_from_directory_checkbox_checking_variable.get() == 1:
        relative_path = os.path.relpath(folder_path, root_folder)
        output_video_name = relative_path.replace("\\", "") + ".mp4"
    else:
        output_video_name = Name_insert.get("1.0", "end-1c") + ".mp4"

    if Save_directory_checkbox_checking_variable.get() == 1:
        save_path = folder_path
    else:
        try:
           save_path = save_folder_directory
        except:
            messagebox.showerror("No directory","You haven't selected saving directory")

    images = [img for img in os.listdir(folder_path) if img.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not images:
        return

    images.sort()
    first_image = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, _ = first_image.shape

    video = cv2.VideoWriter(
        os.path.join(save_path, output_video_name),
        cv2.VideoWriter_fourcc(*'mp4v'),
        float(Speed_insert.get()),
        (width, height)
    )

    for _ in range(int(Number_of_repeats_insert.get("1.0", "end-1c"))):
        for image_name in images:
            img_path = os.path.join(folder_path, image_name)
            frame = cv2.imread(img_path)
            video.write(frame)

            frame_tracker[0] += 1
            progress_bar['value'] = int((frame_tracker[0] / total_frames) * 100)
            c.update_idletasks()

    video.release()
    print(f"Video saved in: {os.path.join(save_path, output_video_name)}")

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
Render_btn.place(x=375,y=370)

Cancel_btn = Button(c, text="Exit", command=c.destroy)
Cancel_btn.place(x=5,y=370)

progress_bar = Progressbar(c, orient="horizontal", length=325, mode="determinate")
progress_bar.place(x=43,y=372)

Save_directory_checkbox_checking()
Name_from_directory_checking()
update_video_length_display()


Selected_folder_text.insert("1.0", "Not selected")
Selected_saving_directory_text.insert("1.0", "Not selected")

c.mainloop()
