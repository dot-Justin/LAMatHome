import os
import json
import logging
import coloredlogs
from datetime import datetime, timezone
import threading
from integrations import lam_at_home
from utils import config, get_env, rabbit_hole, splash_screen, new_ui, llm_parse, task_executor, journal
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from PIL import Image
import _tkinter
import customtkinter
from customtkinter import CTkImage

ui_window = None
main_thread = None
stop_event = threading.Event()

def toggle_ui():
    global ui_window
    logging.info("Toggling UI window")
    try:
        if ui_window is None or not ui_window.winfo_exists():
            logging.info("Creating new UI window")
            ui_window = new_ui.create_ui()
        else:
            if ui_window.state() == 'withdrawn':
                logging.info("Showing UI window")
                ui_window.deiconify()
            else:
                logging.info("Hiding UI window")
                ui_window.withdraw()
    except _tkinter.TclError as e:
        logging.error(f"Error toggling UI window: {e}")
        ui_window = None

def start_drag(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def do_drag(event):
    x = root.winfo_pointerx() - x_offset
    y = root.winfo_pointery() - y_offset
    root.geometry(f"+{x}+{y}")

def process_utterance(journal_entry, user_journal, playwright_context):
    if isinstance(journal_entry, str):
        utterance = journal_entry
    else:
        utterance = journal_entry['utterance']['prompt']
    logging.info(f"Prompt: {utterance}")

    entry, promptParsed = None, None
    try:
        if utterance:
            # split prompt into tasks
            promptParsed = llm_parse.LLMParse(utterance, journal.get_interactions())
            tasks = promptParsed.split("&&")

            # iterate through tasks and execute each sequentially
            for task in tasks:
                if task != "x":
                    logging.info(f"Task: {task}")
                    task_executor.execute_task(playwright_context, task)
        else:
            logging.info("No prompt found in entry, skipping LLM Parse and task execution.")

        # Append the completed interaction to the journal
        entry = journal.add_entry(journal_entry, llm_response=promptParsed)

        if config.config['lamathomesave_isenabled'] and entry.type in ["vision", "ai-generated-image"]:
            lam_at_home.save(entry)

    except PlaywrightTimeoutError:
        logging.error("Playwright timed out while waiting for response.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    try:
        print(splash_screen.colored_splash)
        logging.info("LAMatHome is starting...")

        # create cache directory if it doesn't exist
        if not os.path.exists(config.config['cache_dir']):
            os.makedirs(config.config['cache_dir'])

        # Ensure state.json exists and is valid
        state_file = os.path.join(config.config['cache_dir'], config.config['state_file'])
        if not os.path.exists(state_file) or os.stat(state_file).st_size == 0:
            with open(state_file, 'w') as f:
                json.dump({}, f)

        # Initialize journal for storing rolling transcript
        user_journal = journal.Journal(max_entries=config.config['rolling_transcript_size'])

        with sync_playwright() as p:
            # Use firefox for full headless
            browser = p.firefox.launch(headless=False)
            context = browser.new_context(storage_state=state_file)  # Use state to stay logged in

            user, assistant = None, None
            if get_env.RH_ACCESS_TOKEN:
                # fetch rabbit hole user profile
                profile = rabbit_hole.fetch_user_profile()
                user = profile.get('name')
                assistant = profile.get('assistantName')
            
            if config.config["mode"] == "rabbit":
                current_time_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                logging.info(f"Welcome {user}! LAMatHome is now listening for journal entries posted by {assistant}")
                for journal_entry in rabbit_hole.journal_entries_generator(current_time_iso):
                    if stop_event.is_set():
                        break
                    process_utterance(journal_entry, user_journal, context)
            
            elif config.config["mode"] == "cli":
                logging.info("Entering interactive mode...")
                while not stop_event.is_set():
                    user_input = input(f"{user}@LAMatHome> " if user else "LAMatHome> ")
                    process_utterance(user_input, user_journal, context)

            else:
                logging.error("Invalid mode specified in config.json")

    except KeyboardInterrupt:
        logging.info("Program terminated by user")
    finally:
        lam_at_home.terminate()

def run_main_in_thread():
    global main_thread
    stop_event.clear()
    main_thread = threading.Thread(target=main)
    main_thread.start()

def stop_main_thread():
    stop_event.set()
    print(splash_screen.colored_splash_goodbye)
    os.kill(os.getpid(), 2)  # Send SIGINT signal to simulate Ctrl+C

if __name__ == "__main__":
    # Configure logging and run LAMatHome
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    coloredlogs.install(
        level='INFO', 
        fmt='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S', 
        field_styles={'asctime': {'color': 'white'}}
    )
    
    root = customtkinter.CTk()
    root.title("LAMatHome Control")

    # Remove window decorations
    root.overrideredirect(True)

    # Set the window background to be transparent
    root.attributes('-transparentcolor', root['bg'])

    # Load the image
    image_path = "assets/LAH_splash.png"
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        logging.error(f"Image not found at {image_path}")
        root.destroy()
        exit()

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate maximum allowed dimensions (20% of screen size)
    max_width = int(screen_width * 0.25)
    max_height = int(screen_height * 0.25)

    # Resize the image if it exceeds the maximum allowed dimensions
    image_width, image_height = image.size
    if image_width > max_width or image_height > max_height:
        scaling_factor = min(max_width / image_width, max_height / image_height)
        new_width = int(image_width * scaling_factor)
        new_height = int(image_height * scaling_factor)
        image = image.resize((new_width, new_height), Image.LANCZOS)

    # Convert the image to a CTkImage
    ctk_image = CTkImage(light_image=image, dark_image=image, size=(new_width, new_height))

    # Create the button with the image and transparent background
    toggle_button = customtkinter.CTkButton(master=root, image=ctk_image, text="", command=toggle_ui, fg_color="#161B22", border_color="#ff4d06", border_width=1, hover_color="#ff4d06", corner_radius=8)
    toggle_button.pack(padx=0, pady=0)

    # Adjust the button size to match the image size
    toggle_button.configure(width=new_width, height=new_height)

    # Adjust the window size to match the button size
    root.geometry(f"{new_width}x{new_height + 80}")  # Adjust height to accommodate the start/stop buttons

    x = (screen_width) - (new_width // 2)
    y = (screen_height) - (new_height // 2)
    root.geometry(f"+{x}+{y}")

    # Bind mouse events to make the window draggable
    toggle_button.bind("<Button-1>", start_drag)
    toggle_button.bind("<B1-Motion>", do_drag)

    # Frame to hold start/stop buttons
    button_frame = customtkinter.CTkFrame(master=root, fg_color="#161B22")
    button_frame.pack(pady=(10, 0))

    # Add a start button to the UI
    start_button = customtkinter.CTkButton(master=button_frame, text="Start", command=run_main_in_thread, fg_color="#161B22", border_color="#ff4d06", border_width=1, hover_color="#ff4d06", corner_radius=8)
    start_button.pack(side="left", padx=(5, 5))

    # Add a stop button to the UI
    stop_button = customtkinter.CTkButton(master=button_frame, text="Stop", command=stop_main_thread, fg_color="#161B22", border_color="#ff4d06", border_width=1, hover_color="#ff4d06", corner_radius=8)
    stop_button.pack(side="left", padx=(5, 5))

    # Start the GUI event loop
    root.mainloop()
