import json
import os
from dotenv import load_dotenv, set_key, dotenv_values
import customtkinter
import tkinter as tk

# --- Colors ---
PRIMARY_COLOR = "#ff4d06"
SECONDARY_COLOR = "#000000"

CONFIG_FILE = "config.json"
CREDENTIALS_FILE = ".env"

# --- Config File Handling ---
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return False

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# --- Credentials File Handling ---
def load_env():
    try:
        return dotenv_values(CREDENTIALS_FILE)
    except FileNotFoundError:
        return False

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "w") as f:
            f.write("")  # Create an empty .env file if it doesn't exist
    return load_env()

def save_credentials(credentials):
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "w") as f:
            f.write("")  # Create an empty .env file if it doesn't exist
    for key, value in credentials.items():
        set_key(dotenv_path=CREDENTIALS_FILE, key_to_set=key, value_to_set=value)

# --- Load Initial Data ---
config = load_config()
credentials = load_credentials()

# --- UI Functions ---
def update_config(key, value):
    config[key] = value
    save_config(config)

def update_credentials(key, value):
    credentials[key] = value
    save_credentials(credentials)
    
# --- Tooltip Class ---
class ToolTip:
    current_tooltip = None  # Class variable to keep track of the current tooltip

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Hide the current tooltip if there is one
        if ToolTip.current_tooltip:
            ToolTip.current_tooltip.hide_tooltip(None)

        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = customtkinter.CTkToplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = customtkinter.CTkLabel(self.tooltip, pady=10, padx=10, text=self.text, bg_color=PRIMARY_COLOR, text_color="black")
        label.pack()

        # Set this tooltip as the current tooltip
        ToolTip.current_tooltip = self

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            # Clear the current tooltip if it is this one
            if ToolTip.current_tooltip == self:
                ToolTip.current_tooltip = None

def create_integration_frame(parent_tab, title):
    frame = customtkinter.CTkFrame(master=parent_tab)
    frame.pack(pady=10, padx=10, fill="both", expand=True)
    label = customtkinter.CTkLabel(master=frame, text=title, font=("Power Grotesk", 22))
    label.pack(pady=(0, 5))
    return frame

def create_toggle(parent, key, text, tooltip_text=None):
    toggle = customtkinter.CTkSwitch(master=parent, text=text, command=lambda: update_config(key, toggle.get() == 1))
    toggle.pack(pady=2, anchor="w")
    if config.get(key, False):
        toggle.select()
    else:
        toggle.deselect()
    if tooltip_text:
        ToolTip(toggle, tooltip_text)

def create_mode_toggle(parent, key, text, tooltip_text=None):
    def toggle_mode():
        current_value = config.get(key, 'rabbit')
        new_value = 'cli' if current_value == 'rabbit' else 'rabbit'
        update_config(key, new_value)
        toggle.select() if new_value == 'rabbit' else toggle.deselect()

    toggle = customtkinter.CTkSwitch(master=parent, text=text, command=toggle_mode)
    toggle.pack(pady=2, anchor="w")
    if config.get(key, 'rabbit') == 'rabbit':
        toggle.select()
    else:
        toggle.deselect()
    if tooltip_text:
        ToolTip(toggle, tooltip_text)

def create_input(parent, key, placeholder, tooltip_text=None):
    entry = customtkinter.CTkEntry(master=parent, placeholder_text=placeholder)
    entry.pack(pady=2, fill="x")
    entry.insert(0, config.get(key, ""))  # Set initial value from config

    def update_entry(event=None):
        update_config(key, entry.get())

    entry.bind("<FocusOut>", update_entry)
    if tooltip_text:
        ToolTip(entry, tooltip_text)
        
def create_credential_input(parent, key, placeholder, tooltip_text=None):
    frame = customtkinter.CTkFrame(master=parent)
    frame.pack(pady=2, fill="x")

    entry = customtkinter.CTkEntry(master=frame, placeholder_text=placeholder, show="*")
    entry.pack(side="left", fill="x", expand=True)
    entry.insert(0, credentials.get(key, ""))  # Set initial value from credentials

    def update_entry(event=None):
        update_credentials(key, entry.get())

    entry.bind("<FocusOut>", update_entry)
    entry.bind("<Return>", update_entry)

    if tooltip_text:
        ToolTip(entry, tooltip_text)

    def toggle_visibility():
        if entry.cget("show") == "*":
            entry.configure(show="")
        else:
            entry.configure(show="*")

    visibility_toggle = customtkinter.CTkSwitch(master=frame, text="Show", command=toggle_visibility)
    visibility_toggle.pack(side="right")
    
def create_slider(parent, key, from_, to_, text, tooltip_text=None):
    label = customtkinter.CTkLabel(master=parent, text=text)
    label.pack(pady=(5, 0), anchor="w")

    def update_slider(value):
        update_config(key, float(value))

    slider = customtkinter.CTkSlider(master=parent, from_=from_, to=to_, command=update_slider)
    slider.pack(pady=2, fill="x")
    slider.set(config.get(key, 0.1))  # Set initial value from config
    if tooltip_text:
        ToolTip(slider, tooltip_text)

# --- UI Setup ---

ui_instance = None

def on_closing():
    global ui_instance
    ui_instance.destroy()
    ui_instance = None


def create_ui():
    global ui_instance
    if ui_instance is None or not ui_instance.winfo_exists():
        ui_instance = customtkinter.CTk()
        
        screen_width = ui_instance.winfo_screenwidth()
        screen_height = ui_instance.winfo_screenheight()
        
        min_width = int(screen_width * 0.6)
        min_height = int(screen_height * 0.6)
        
        ui_instance.minsize(width=min_width, height=min_height)
        ui_instance.state('normal')  
        ui_instance.title("LAMatHOME")
        
        ui_instance.protocol("WM_DELETE_WINDOW", on_closing)

    # --- Style ---

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("utils/rabbit_color.json")

        # --- Tabs ---
        tabview = customtkinter.CTkTabview(master=ui_instance)
        tabview.pack(pady=10, padx=10, fill="both", expand=True)
        tabview.add("Configuration")
        tabview.add("Credentials")

        # --- Configuration Tab ---
        config_tab = tabview.tab("Configuration")

        # --- Scrollable Frame for Configuration Tab ---
        scrollable_frame = customtkinter.CTkScrollableFrame(master=config_tab)
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Mode Toggle ---
        mode_frame = create_integration_frame(scrollable_frame, "Mode Selection")
        create_mode_toggle(mode_frame, "mode", "Rabbit Mode", "Toggle between Rabbit mode and CLI mode")

        # --- Google Integration ---
        google_frame = create_integration_frame(scrollable_frame, "Google Integration")
        create_toggle(google_frame, "google_isenabled", "Enable Google Integration", "Enable or disable Google integration")
        create_toggle(google_frame, "googlehome_isenabled", "Enable Google Home", "Enable or disable Google Home integration")
        create_input(google_frame, "googlehomeautomations", "Google Home Automations (comma-separated)", "Comma-separated list of Google Home automations")

        # --- Lam at Home Integration ---
        lamathome_frame = create_integration_frame(scrollable_frame, "LamatHome Integration")
        create_toggle(lamathome_frame, "lamathome_isenabled", "Enable LamatHome", "Enable or disable LamatHome integration")
        create_toggle(lamathome_frame, "lamathometerminate_isenabled", "Enable LamatHome Termination", "Enable or disable LamatHome termination")

        # --- Open Interpreter Integration ---
        openinterpreter_frame = create_integration_frame(scrollable_frame, "Open Interpreter Integration")
        create_toggle(openinterpreter_frame, "openinterpreter_isenabled", "Enable Open Interpreter", "Enable or disable Open Interpreter integration")
        create_toggle(openinterpreter_frame, "openinterpreter_auto_run_isenabled", "Enable Auto Run", "Enable or disable auto run for Open Interpreter")
        create_toggle(openinterpreter_frame, "openinterpreter_verbose_mode_isenabled", "Enable Verbose Mode", "Enable or disable verbose mode for Open Interpreter")
        create_input(openinterpreter_frame, "openinterpreter_llm_api_base", "LLM API Base", "Base URL for the LLM API")
        create_input(openinterpreter_frame, "openinterpreter_llm_model", "LLM Model", "Model name for the LLM")
        create_slider(openinterpreter_frame, "openinterpreter_llm_temperature", 0.1, 1.0, "LLM Temperature", "Temperature setting for the LLM")

        # --- Telegram Integration ---
        telegram_frame = create_integration_frame(scrollable_frame, "Telegram Integration")
        create_toggle(telegram_frame, "telegram_isenabled", "Enable Telegram", "Enable or disable Telegram integration")
        create_toggle(telegram_frame, "telegramtext_isenabled", "Enable Telegram Text", "Enable or disable Telegram text integration")

        # --- Credentials Tab ---
        credentials_tab = tabview.tab("Credentials")

        # --- Scrollable Frame for Credentials Tab ---
        scrollable_frame_credentials = customtkinter.CTkScrollableFrame(master=credentials_tab)
        scrollable_frame_credentials.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Rabbithole Access Token ---
        rabbithole_frame = create_integration_frame(scrollable_frame_credentials, "Rabbithole Access Token")
        create_credential_input(rabbithole_frame, "RH_ACCESS_TOKEN", "Rabbithole Access Token", "Access token for Rabbithole journal")

        # --- API Keys ---
        api_frame = create_integration_frame(scrollable_frame_credentials, "API Keys")
        create_credential_input(api_frame, "GROQ_API_KEY", "Groq API Key", "API key for Groq")
        create_credential_input(api_frame, "OI_API_KEY", "Open Interpreter API Key", "API key for Open Interpreter")

        # --- Account Credentials ---
        account_frame = create_integration_frame(scrollable_frame_credentials, "Account Credentials")
        create_credential_input(account_frame, "DC_EMAIL", "Discord Email", "Email for Discord account")
        create_credential_input(account_frame, "DC_PASS", "Discord Password", "Password for Discord account")
        create_credential_input(account_frame, "FB_EMAIL", "Facebook Email", "Email for Facebook account")
        create_credential_input(account_frame, "FB_PASS", "Facebook Password", "Password for Facebook account")
        create_credential_input(account_frame, "G_HOME_EMAIL", "Google Home Email", "Email for Google Home account")
        create_credential_input(account_frame, "G_HOME_PASS", "Google Home Password", "Password for Google Home account")

        reminder_label = customtkinter.CTkLabel(master=scrollable_frame_credentials, text="Press Enter after inputing the last value to ensure you save it.")
        reminder_label.pack(pady=10, padx=11, anchor="w")

        return ui_instance
