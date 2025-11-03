import tkinter as tk
import os
import sys
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import datetime

SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "RamblingCactus", "notes")
os.makedirs(SAVE_FOLDER, exist_ok=True) #create a directory if it doesn't already exist

#setting up the root
root = tk.Tk()
root.title("Rambling Cactus")
root.configure(bg="#3d5200")

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#setting up the background image
image_path = resource_path("assets/Cactus.jpg")
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()

#icon
icon_path = resource_path("assets/cactus_icon.ico")
root.iconbitmap(icon_path)

#text widget
text = tk.Text(root, bg="#9bbba5", fg="black", font=("Consolas", 11))
text.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")

current_file = None

#function to list notes in a save directory, so we can edit them
def list_notes():
    listbox.delete(0, tk.END) #make sure we are not duplicating in the widget on reload
    for file in os.listdir(SAVE_FOLDER):
        if file.endswith(".txt"):
            listbox.insert(tk.END, file)

#function to save a note into a file
def save_note():
    global current_file
    if current_file: #check if we want to save already existing file -> no naming dialog needed
        path = os.path.join(SAVE_FOLDER, current_file)
    else:
        #name the file
        filename = simpledialog.askstring("Save", "Enter filename (without extension):")
        #make sure we are not saving with no name
        if not filename:
            return
        current_file = f"{filename.strip()}.txt" #update the file status to already existing
        path = os.path.join(SAVE_FOLDER, current_file) #set the path

    try:
        note = text.get("1.0", "end-1c") #select the text in text widget as note
        #write text into a txt file
        with open(path, "w") as f:
            f.write(note)
            #make a date stamp
            current_date = datetime.date.today()
            f.write(f"\ncreation date: {str(current_date)}")
        messagebox.showinfo("Saved", f"Note saved as: {path}") #inform abt saving
        list_notes() #reload the list so it shows without having to close
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save note: {e}")

#function to make sure that the selected file appears in the text widget
def load_selected_note(event):
    global current_file #has to be global, as we use it across multiple functions
    selection = listbox.curselection()
    if selection:
        selected_index = selection[0]
        filename = listbox.get(selected_index)
        current_file = filename
        path = os.path.join(SAVE_FOLDER, filename)
        try:
            #open the file selected
            with open(path, 'r') as f:
                content = f.read()
                text.delete("1.0", tk.END) #deletes the textbox
                text.insert(tk.END, content) #writes read info from file
        except Exception as e:
            messagebox.showerror("error" f"couldn't load note: {e}")

#create a new file, basically just clears the text widget
def new_note():
    global current_file
    text.delete("1.0", tk.END)
    current_file = None

#function for file deletion inside the app
def delete_note():
    global current_file
    selection = listbox.curselection()
    if selection:
        selected_index = selection[0]
        filename = listbox.get(selected_index)
        current_file = filename
        path = os.path.join(SAVE_FOLDER, filename)
        os.remove(path)
        messagebox.showinfo("Deleted", f"Note {filename} deleted")
        new_note()
    list_notes()

#buttons
save_button = tk.Button(root, text='Save', command=save_note, bg="#9bbba5")
save_button.grid(column=1, row=0, sticky="e", padx=30, pady=5)

new_button = tk.Button(root, text=' New ', command=new_note, bg="#9bbba5")
new_button.grid(column=1, row=0, sticky="e", padx=80, pady=5)

delete_button = tk.Button(root, text='Delete', command=delete_note, bg="#9bbba5")
delete_button.grid(column=1, row=0, sticky="e", padx=134, pady=5)

#list of notes in folder
listbox = tk.Listbox(root, height=10, bg="#9bbba5")
listbox.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
listbox.bind("<<ListboxSelect>>", load_selected_note)

#scrollbar
text_scrollbar = tk.Scrollbar(root, orient='vertical', command=text.yview, bg='#9bbba5')
text.configure(yscrollcommand=text_scrollbar.set)
text_scrollbar.grid(column=2, row=1, sticky='nsew', pady=10, padx=5)

#Making sure the widgets grow
root.grid_columnconfigure(0, weight=1)  # For Listbox
root.grid_columnconfigure(1, weight=4)  # For Text widget
root.grid_rowconfigure(1, weight=1)     # Make row 1 grow

list_notes() #updating the list of notes on start
root.mainloop()