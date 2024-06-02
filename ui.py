import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

def create_env_file():
    """Creates a .env file with user-provided credentials."""
    try:
        rh_email = rh_email_entry.get()
        rh_pass = rh_pass_entry.get()
        rh_access_token = rh_access_token_entry.get()
        fb_email = fb_email_entry.get()
        fb_pass = fb_pass_entry.get()
        dc_email = dc_email_entry.get()
        dc_pass = dc_pass_entry.get()

        # Debugging: Print the values to the console
        # print(f"RH_EMAIL={rh_email}")
        # print(f"RH_PASS={rh_pass}")
        # print(f"FB_EMAIL={fb_email}")
        # print(f"FB_PASS={fb_pass}")
        # print(f"DC_EMAIL={dc_email}")
        # print(f"DC_PASS={dc_pass}")

        with open(".env", "w") as env_file:
            env_file.write(f"RH_EMAIL='{rh_email}'\n")
            env_file.write(f"RH_PASS='{rh_pass}'\n")
            env_file.write(f"RH_ACCESS_TOKEN='{rh_access_token}'\n")
            env_file.write(f"FB_EMAIL='{fb_email}'\n")
            env_file.write(f"FB_PASS='{fb_pass}'\n")  # Corrected key name
            env_file.write(f"DC_EMAIL='{dc_email}'\n")
            env_file.write(f"DC_PASS='{dc_pass}'\n")
        messagebox.showinfo("Success", ".env file created successfully!")
        root.destroy()  # Close the UI window
        subprocess.run(["python", "main.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_ui():
    """Creates and runs the UI for credential input."""
    global root, rh_email_entry, rh_pass_entry, rh_access_token_entry, fb_email_entry, fb_pass_entry, dc_email_entry, dc_pass_entry
    root = tk.Tk()
    root.title("Enter Credentials")
    root.configure(bg='#1a1a1a')

    # Set window size and prevent fullscreen
    root.geometry("500x400")
    root.resizable(False, False)  # Disable resizing

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', background='#1a1a1a', foreground='#ff6600')
    style.configure('TEntry', fieldbackground='#333333', foreground='#ffffff')
    style.configure('TButton', background='#ff6600', foreground='#ffffff')

    # Create a frame to hold the input fields and labels
    input_frame = tk.Frame(root, bg='#1a1a1a')
    input_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Rabbit Hole Credentials
    rh_email_label = ttk.Label(input_frame, text="Rabbit Hole Email:")
    rh_email_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    rh_email_entry = ttk.Entry(input_frame)
    rh_email_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    rh_pass_label = ttk.Label(input_frame, text="Rabbit Hole Password:")
    rh_pass_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    rh_pass_entry = ttk.Entry(input_frame, show="*")
    rh_pass_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    rh_access_token_label = ttk.Label(input_frame, text="Rabbit Hole Access Token:")
    rh_access_token_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    rh_access_token_entry = ttk.Entry(input_frame, show="*")
    rh_access_token_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    # Facebook Credentials
    fb_email_label = ttk.Label(input_frame, text="Facebook Email:")
    fb_email_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    fb_email_entry = ttk.Entry(input_frame)
    fb_email_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

    fb_pass_label = ttk.Label(input_frame, text="Facebook Password:")
    fb_pass_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    fb_pass_entry = ttk.Entry(input_frame, show="*")
    fb_pass_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    # Discord Credentials
    dc_email_label = ttk.Label(input_frame, text="Discord Email:")
    dc_email_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    dc_email_entry = ttk.Entry(input_frame)
    dc_email_entry.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

    dc_pass_label = ttk.Label(input_frame, text="Discord Password:")
    dc_pass_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')
    dc_pass_entry = ttk.Entry(input_frame, show="*")
    dc_pass_entry.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

    # Submit Button
    submit_button = ttk.Button(root, text="Submit", command=create_env_file)
    submit_button.pack(pady=10)

    # Make input fields expand to fill the width
    for i in range(7):
        input_frame.grid_rowconfigure(i, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()  # Run the UI

# Run the UI
# create_ui()
