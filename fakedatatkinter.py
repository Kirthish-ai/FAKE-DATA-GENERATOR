import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from faker import Faker
import json
import pyperclip
import qrcode
from PIL import ImageTk, Image
from io import BytesIO
import tkinter.font as font

fake = Faker()

def generate_fake_data(num_entries=1):
    data = []
    for _ in range(num_entries):
        entry = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
        }
        data.append(entry)
    return data

def generate_data():
    try:
        num = int(num_entry.get())
        fake_data_global = generate_fake_data(num)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "***** Generated Data *****\n")
        output_text.insert(tk.END, json.dumps(fake_data_global, indent=4))
        output_text.insert(tk.END, "\n***** End of Data *****")
        window.fake_data = fake_data_global
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a number.")

def surprise_me():
    random_name = fake.name()
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Random Name: {random_name}")
    window.random_name = random_name

def copy_to_clipboard():
    text_to_copy = output_text.get(1.0, tk.END)
    pyperclip.copy(text_to_copy)
    messagebox.showinfo("Copied", "Data copied to clipboard!")

def export_to_json():
    if hasattr(window, "fake_data"):
        data_to_export = window.fake_data
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w") as f:
                json.dump(data_to_export, f, indent=4)
            messagebox.showinfo("Exported", f"Data exported to {filename}")
    elif hasattr(window, "random_name"):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                f.write(window.random_name)
            messagebox.showinfo("Exported", f"Name exported to {filename}")
    else:
        messagebox.showerror("Error", "No data to export.")

def generate_qr():
    if hasattr(window, "fake_data"):
        json_data = json.dumps(window.fake_data)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((500, 500)) 
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        pil_img = Image.open(img_buffer)
        tk_img = ImageTk.PhotoImage(pil_img)
        qr_window = tk.Toplevel(window)
        qr_window.title("QR Code")
        qr_label = tk.Label(qr_window, image=tk_img)
        qr_label.image = tk_img
        qr_label.pack()
    else:
        messagebox.showerror("Error", "No data generated to create QR code.")

def change_theme():
    global current_theme
    if current_theme == "tech_blue":
        apply_paper_theme()
        current_theme = "paper"
    else:
        apply_tech_blue_theme()
        current_theme = "tech_blue"

def apply_tech_blue_theme():
    window.config(bg="#000033")
    num_label.config(bg="#000033", fg="#ADD8E6")
    generate_button.config(bg="#000066", fg="black")
    copy_button.config(bg="#000066", fg="black")
    export_button.config(bg="#000066", fg="black")
    surprise_button.config(bg="#000066", fg="black")
    qr_button.config(bg="#000066", fg="black")
    output_text.config(bg="#000066", fg="#ADD8E6")
    num_entry.config(bg="white", fg="black")
    output_text.config(font=("TkFixedFont", 12))

def apply_paper_theme():
    window.config(bg="#F5F5DC")
    num_label.config(bg="#F5F5DC", fg="black")
    generate_button.config(bg="#E9E4D4", fg="black")
    copy_button.config(bg="#E9E4D4", fg="black")
    export_button.config(bg="#E9E4D4", fg="black")
    surprise_button.config(bg="#E9E4D4", fg="black")
    qr_button.config(bg="#E9E4D4", fg="black")
    output_text.config(bg="#E9E4D4", fg="black")
    num_entry.config(bg="white", fg="black")
    output_text.config(font=("Courier New", 12))

window = tk.Tk()
window.title("Fake Data Generator")
window.geometry("800x800")

current_theme = "tech_blue" 

home_frame = tk.Frame(window, bg="#000033")
home_frame.pack(fill=tk.BOTH, expand=True)

num_label = tk.Label(home_frame, text="Number of Entries:", fg="#ADD8E6", bg="#000033")
num_label.grid(row=0, column=0, padx=3, pady=3)
num_entry = tk.Entry(home_frame, bg="white", fg="black")
num_entry.grid(row=0, column=1, padx=0, pady=5)

generate_button = tk.Button(home_frame, text="Generate Data", command=generate_data, bg="#000066", fg="black")
generate_button.grid(row=1, column=0, padx=3, pady=3)

copy_button = tk.Button(home_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="#000066", fg="black")
copy_button.grid(row=1, column=1, padx=3, pady=3)

export_button = tk.Button(home_frame, text="Export to JSON", command=export_to_json, bg="#000066", fg="black")
export_button.grid(row=1, column=2, padx=3, pady=3)

surprise_button = tk.Button(home_frame, text="Surprise Me!", command=surprise_me, bg="#000066", fg="black")
surprise_button.grid(row=1, column=3, padx=3, pady=3)

qr_button = tk.Button(home_frame, text="Generate QR", command=generate_qr, bg="#000066", fg="black")
qr_button.grid(row=0, column=4, padx=3, pady=3)

theme_button = tk.Button(home_frame, text="Change Theme", command=change_theme, bg="#000066", fg="black")
theme_button.grid(row=1, column=4, padx=3, pady=3)

output_text = scrolledtext.ScrolledText(home_frame, width=190, height=150, bg="#000066", fg="#ADD8E6")
output_text.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

window.mainloop()