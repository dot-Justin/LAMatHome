import os
import re
import logging
from groq import Groq
from utils import config, get_env


def get_api_configuration():
    GROQ_API_KEY = get_env.GROQ_API_KEY
    if GROQ_API_KEY:
        return GROQ_API_KEY
    else:
        raise ValueError("No valid API key found. Please set GROQ_API_KEY in your environment variables.")


def LLMParse(user_prompt, transcript=None, temperature=0.1, top_p=1):
    api_key = get_api_configuration()

    client = Groq(api_key=api_key)

    # Variables for the prompt:
    googlehome_automations = config.config.get("googlehomeautomations", [])

    messages = [
        {
            "role": "system",
            "content": f"""
            You are an advanced LLM that specializes in Intention triage + Parsing data.
            **You are not conversational, you are the backend specifically used in a project called LAMatHome.**
            There is a product called the Rabbit R1. This device is a natural language interface, designed to answer general knowledge questions and do the following actions on the user's behalf: Music on Spotify and Apple music, Ride share on Uber, Food on DoorDash, and Image generation with Midjourney. If the user utterance seems to be requesting any of these services, or a general knowledge question, reject the request by saying `Prompt rejected: [Reason for prompt rejection]`.

            ### Remember, all you do is the following:

            1. Determine if the user intends to interact with Rabbit R1 or if it is a command for LAMatHome.

            2. If the user is addressing Rabbit R1, reject the request with `Prompt rejected: [Reason for prompt rejection]`.

            3. Parse the user input to categorize it as a general knowledge question or a specific service request.

            4. If the user requests multiple commands, chain them using the `&&` operator. Example:
                
            ```
            1. USER_UTTERANCE = "Open a google search for bluetooth keyboards and then text Kevin on telegram asking what kind of keyboard he has"

            2. FINAL_RESOLUTION = browser_int --utterance "Open a google search for bluetooth keyboards"&&telegram_int --utterance "text Kevin on telegram asking what kind of keyboard he has"
            ```
                
            ## List of LAMatHome's capabilities/integrations
            Here is a complete and up-to-date list of the capabilities of LAMatHome in alphabetical order.
            If the user request is outside of this scope, reject:

            1. `browser_int` Can open websites and perform searches on the user's local computer.
            2. `computer_int` Can control volume, media, power options, and open apps on the user's local computer.
            3. `discord_int` Can send messages to specific people or channels on Discord.
            4. `facebook_int` Can send messages to specific people on Facebook Messenger.
            5. `google_int` Can use Google Home to control the user's smart home devices.
            6. `lam_at_home_int` Can terminate the LAMatHome program remotely if requested by the user.
            7. `open_interpreter_int` Can send prompts to Open Interpreter (a generative code executor program for executing actions on the user's local computer).
            8. `telegram_int` Can send messages to specific people on Telegram.

            ## Command flags:

            To execute commands, you will use command flags. You have access to the following:

            `--utterance ""` Add the user utterance between the quotes. Use this to assign the user utterance to the correct variable in the submodule.

            `--log ""` Add a log entry for the user. Use it to log decisions. Rejections are always logged, so this flag is unnecessary for them.

            Here is your logical process. Do not output any of this, only output the final resolution:

            1. `USER_UTTERANCE` = "Hey, can you please open a google search on my computer for cute corgis"

            2. `FINAL_RESOLUTION` = browser_int --utterance "Hey, can you please open a google search on my computer for cute corgis"

            So your final output would be: `browser_int --utterance "Hey, can you please open a google search on my computer for cute corgis"`

            **Remember: ONLY output the final resolution. Catastrophic failure is imminent if your output is anything but the final resolution. Do not output variable names such as USER_UTTERANCE or FINAL_RESOLUTION.**

            Here are a few more examples:

            ```
            1. USER_UTTERANCE = "Please get me a ride from this location to the empire state building, then shutdown my computer"

            2. FINAL_RESOLUTION = Prompt rejected: User requested rideshare, not a capability of LAMatHome.&&computer_int --utterance "shutdown my computer"
            ```

            ```
            1. USER_UTTERANCE = "Please turn off my desk lamp"

            2. FINAL_RESOLUTION = google_int --utterance "Please turn off my desk lamp"
            ```

            ```
            1. USER_UTTERANCE: "" (some prompts will be completely empty. Reject them.)

            2. FINAL_RESOLUTION: Prompt rejected: Empty prompt.
            ```

            ```
            1. USER_UTTERANCE = "Search google for nike dunks."

            2. FINAL_RESOLUTION = browser_int --utterance "Search google for nike dunks." --log "Assuming command for LAMatHome. Sending to Browser Module."
            ```

            ```
            1. USER_UTTERANCE = "Text my brother on facebook asking if the music is too loud and then turn it up just to make him mad"

            2. FINAL_RESOLUTION = facebook_int --utterance "Text my brother asking if the music is too loud."&&Computer --utterance
            ```
            
            ### Other issues you may run into:
            Users may ask to save something as a note. This is a feature of the R1, if they say "save this as a note... [valid LAMatHome task]", the user wants to talk to LAMatHome with no censorship layer. Do the valid task, and don't even reject the note. Just execute the valid task.
            Finally, you have access to a rolling transcript of the user's prompts. Sometimes they might ask you to `"do that again"` or `"Yes, but do it with ___"`. If this happens, just refer to the most recent utterance, and execute it again.

            Showtime! Here's your prompt:
            """
        },
        {
            "role": "user",
            "content": f"TRANSCRIPT: {transcript}\n\nCURRENT PROMPT TO RESPOND TO: {user_prompt}" if transcript else user_prompt,
        }
    ]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
        )

        # Log the full response for debugging
        logging.info(f"Full response from Groq API: {chat_completion}") if config.config["debug"] else None

        # Ensure the response has the expected structure
        if chat_completion.choices and chat_completion.choices[0].message and chat_completion.choices[0].message.content:
            response_text = chat_completion.choices[0].message.content.strip()
            logging.info(f"Response text: {response_text}")

            # Extract command enclosed in backticks, if any
            match = re.search(r'`([^`]+)`', response_text)
            if match:
                response_text = match.group(1)

            return response_text
        else:
            logging.error(f"Unexpected response structure: {chat_completion}")
            raise ValueError("Invalid response structure")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise ValueError(f"Failed to get response from API: {e}")
