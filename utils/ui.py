import tkinter as tk
from tkinter import ttk, messagebox
from utils.contacts import contacts
from utils import config

def create_contacts_file(contacts):
    """Creates a contacts.py file with the provided contact data."""
    
    if contacts:
        with open(config.config['contacts_file'], "w") as contacts_file:
            contacts_file.write("contacts = " + str(contacts))
        messagebox.showinfo("Success", "contacts.py file created successfully!")
    else:
        messagebox.showinfo("Info", "contacts.py file already exists.")

def add_contact():
    """Adds a contact to the contacts dictionary."""
    platform = platform_var.get()
    name = name_entry.get()
    nicknames = nicknames_entry.get().split(',')

    if platform and name:
        if platform not in contacts:
            contacts[platform] = []
        contacts[platform].append({"name": name, "nicknames": nicknames})
        messagebox.showinfo("Success", f"Contact added to {platform}!")
    else:
        messagebox.showerror("Error", "Platform and Name are required fields.")

def create_contacts_list():
    """Creates and runs the UI for contact input."""
    global platform_var, name_entry, nicknames_entry, contacts
    contacts = {}

    contacts_window = tk.Toplevel(root)
    contacts_window.title("Enter Contacts")
    contacts_window.configure(bg='#1a1a1a')

    # Set window size and prevent fullscreen
    contacts_window.geometry("500x400")
    contacts_window.resizable(False, False)  # Disable resizing

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', background='#1a1a1a', foreground='#ff6600')
    style.configure('TEntry', fieldbackground='#333333', foreground='#ffffff')
    style.configure('TButton', background='#ff6600', foreground='#ffffff')

    # Create a frame to hold the input fields and labels
    input_frame = tk.Frame(contacts_window, bg='#1a1a1a')
    input_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Define the labels and entries in a list to reduce repetition
    fields = [
        ("Platform:", "platform_var", False),
        ("Name:", "name_entry", False),
        ("Nicknames (comma-separated):", "nicknames_entry", False)
    ]

    # Create and place the labels and entries dynamically
    for i, (label_text, var_name, is_password) in enumerate(fields):
        label = ttk.Label(input_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = ttk.Entry(input_frame, show="*" if is_password else "")
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        globals()[var_name] = entry

    # Add Contact Button
    add_contact_button = ttk.Button(contacts_window, text="Add Contact", command=add_contact)
    add_contact_button.pack(pady=10)

    # Create Contacts File Button
    create_file_button = ttk.Button(contacts_window, text="Create contacts.py", command=lambda: create_contacts_file(contacts))
    create_file_button.pack(pady=10)

    # Make input fields expand to fill the width
    for i in range(len(fields)):
        input_frame.grid_rowconfigure(i, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

def create_ui():
    """Creates and runs the main UI."""
    global root, rh_access_token_entry, groq_api_key_entry, dc_email_entry, dc_pass_entry, fb_email_entry, fb_pass_entry, gh_email_entry, gh_pass_entry
    root = tk.Tk()
    root.title("Main UI")
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

    # Define the labels and entries in a list to reduce repetition
    fields = [
        ("Rabbit Hole Access Token:", "rh_access_token_entry", True),
        ("GROQ API Key:", "groq_api_key_entry", True),
        ("Discord Email:", "dc_email_entry", False),
        ("Discord Password:", "dc_pass_entry", True),
        ("Facebook Email:", "fb_email_entry", False),
        ("Facebook Password:", "fb_pass_entry", True),
        ("Google Home Email:", "gh_email_entry", False),
        ("Google Home Password:", "gh_pass_entry", True)
    ]

    # Create and place the labels and entries dynamically
    for i, (label_text, var_name, is_password) in enumerate(fields):
        label = ttk.Label(input_frame, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = ttk.Entry(input_frame, show="*" if is_password else "")
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        globals()[var_name] = entry

    # Submit Button
    submit_button = ttk.Button(root, text="Submit", command=create_env_file)
    submit_button.pack(pady=10)

    # Create Contacts List Button
    create_contacts_button = ttk.Button(root, text="Create Contacts List", command=create_contacts_list)
    create_contacts_button.pack(pady=10)

    # Make input fields expand to fill the width
    for i in range(len(fields)):
        input_frame.grid_rowconfigure(i, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()  # Run the UI

def create_env_file():
    """Creates a .env file with user-provided credentials."""
    try:
        credentials = {
            "RH_ACCESS_TOKEN": rh_access_token_entry.get(),
            "GROQ_API_KEY": groq_api_key_entry.get(),
            "DC_EMAIL": dc_email_entry.get(),
            "DC_PASS": dc_pass_entry.get(),
            "FB_EMAIL": fb_email_entry.get(),
            "FB_PASS": fb_pass_entry.get(),
            "G_HOME_EMAIL": gh_email_entry.get(),
            "G_HOME_PASS": gh_pass_entry.get()
        }

        with open(".env", "w") as env_file:
            for key, value in credentials.items():
                env_file.write(f"{key}='{value}'\n")
        messagebox.showinfo("Success", ".env file created successfully!")
        root.destroy()  # Close the UI window
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


