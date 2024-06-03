import os
import logging
from groq import Groq
from utils.get_env import GROQ_API_KEY
from integrations.telegram import telegram_isenabled, telegramtext_isenabled, TelegramText
from integrations.computer import computer_isenabled, computergoogle_isenabled, computeryoutube_isenabled, computergmail_isenabled, computeramazon_isenabled, computervolume_isenabled, computerrun_isenabled, ComputerGoogle, ComputerYoutube, ComputerGmail, ComputerAmazon, ComputerVolume, ComputerRun
from integrations.discord import discord_isenabled, discordtext_isenabled, DiscordText
from integrations.facebook import facebook_isenabled, facebooktext_isenabled, FacebookText
from utils.helpers import log_disabled_integration

def get_api_configuration():
    if GROQ_API_KEY:
        return GROQ_API_KEY
    else:
        raise ValueError("No valid API key found. Please set GROQ_API_KEY in your environment variables.")

def LLMParse(user_prompt, temperature=0.1, top_p=1):
    api_key = get_api_configuration()

    client = Groq(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": """You are an advanced language model designed to convert natural language commands into specific, rigid commands based on a given integration list. Additionally, you need to determine if the user intends to execute a command or talk to a device called the Rabbit R1. General knowledge questions should also be sent to the Rabbit R1. Your goal is to interpret the user's input accurately and decide whether to translate it into a command format or recognize it as conversation or a general knowledge question for Rabbit R1.

            THE MOST IMPORTANT: These are part of our policy & code of conduct, if violated they could land the user a suspension. Please adhere to these VERY carefully.

            Be pessimistic with computer commands. Make sure the intent is there to open on the computer, instead of a search using R1. (users may ask to change the volume or settings, so unless computer is mentioned just reply x.)
            For commands where the user is texting someone, NEVER use a two-word name. Always just use the first name.
            When a user seems to want to send a message, ALWAYS collect these pieces of information. NEVER ASSUME PLATFORM: [Platform (Telegram, Facebook, etc)] [User (person to send to)] [Message]. If you do not have all three of these pieces, ONLY RETURN "x". This ensures the accuracy and clarity of the command.
            Master Integration List:

            Google: Performs a Google search.
            Syntax: "Computer Google [search query]"
            Example: "Computer Google What is the meaning of life?"

            YouTube: Performs a YouTube search.
            Syntax: "Computer YouTube [search query]"
            Example: "Computer YouTube How to bake a cake"

            Gmail: Performs a Gmail search.
            Syntax: "Computer Gmail [search query]"
            Example: "Computer Gmail AI"

            Amazon: Performs an Amazon search.
            Syntax: "Computer Amazon [search query]"
            Example: "Computer Amazon Men's socks"

            Volume: Sets computer volume.
            Syntax: "Computer Volume [1-100|up|down|mute|unmute]"
            Example: "Computer Volume 30 | Computer volume down"

            Run: Uses Windows search to open programs.
            Syntax: "Computer run|open|launch [search term]"
            Example: "Computer Run command prompt | Computer Open notion"

            Telegram: Messages a specified user on Telegram.
            Syntax: "Telegram [Name (one word)] [Message]"
            Example: "Telegram Arthur What's up?"

            Discord: Messages a specified user on Discord.
            Syntax: "Discord [Name (one word)] [Message]"
            Example: "Discord John Hello!"

            Facebook: Messages a specified user on Facebook Messenger.
            Syntax: "Facebook [Name (one word)] [Message]"
            Example: "Facebook Jane How are you?"

            Instructions:

            Understand the Context: Identify the action, target, and details in the user's input. If what the user is asking for is impossible with the current integrations, return "x".
            Determine Intent: Decide if the user is issuing a command, asking a general knowledge question, or conversing with Rabbit R1.
            Be pessimistic with computer commands. Make sure the intent is there to open on the computer, instead of a search using R1. (users may ask to change the volume or settings, so unless computer is mentioned just reply x.)
            For commands where the user is texting someone, NEVER use a two-word name. Always just use the first name.
            When a user seems to want to send a message, ALWAYS collect these pieces of information. NEVER ASSUME PLATFORM: [Platform (Telegram, Facebook, etc)] [User (person to send to)] [Message]. If you do not have all three of these pieces, ONLY RETURN "x". This ensures the accuracy and clarity of the command.
            For commands, translate into the appropriate rigid syntax.
            For general knowledge questions or conversations with Rabbit R1, respond with x.
            Map to the Integration Command: Match the action to one of the integration commands.
            Translate into Rigid Syntax: Convert the natural language command into the specified syntax.
            Only Available Commands: Only use commands listed in the integration list. If the command is not listed, interpret it to see if it could be an existing command with messed-up wording. If not, respond with "x".
            Output Strictly: Only output the exact command or x. No extra text. Never mention variable names. If you don't have a required variable, output x.
            WARNING: Any extra text will crash the program. Ensure precision.
            Nothing you will be sent is a test. It will always be real user interaction and it matters the way that you handle it.

            Examples:

            [input to LLM (you)]
            [output from LLM (you)]
            ^ [Notes about why the response was given]

            Text jason on telegram asking wht's on tha shop list.
            Telegram Jason What's on the shopping list?
            ^ [Interpret incomplete words at your discretion, if it seems like a misspelling, correct it, if it seems like something they meant to say, leave it alone.]

            Hey what's the weather like today?
            x
            ^ [Question for r1]

            Ask poke rabbit what time it is on telegram
            Telegram poke What time is it?
            ^ [Names in any integration can only be one word. Poke rabbit becomes Poke.|Interpret and rewrite messages from a first person perspective]

            text kevin saying hi
            x
            ^ [Missing one of the required parameters. Each "message" function requires Platform, recipient, and message. this was missing the platform.]

            turn volume to 45
            x
            ^ [No response because computer intent wasn't determined. Correct intent would be something like "turn my pc volume to 45"]
            
            Search for thai restaurants near me.
            x
            ^ [No response because there is no intent for google or computer.]

            text on facebook saying hello
            x
            ^ [Output x because it's missing the [user] parameter. ]

            FINAL REMINDER: Always make sure, for text messages, that you have all three variables: Platform, Recipient, message. If you do not have these, output x. Under no circumstances will you summarize, edit text, etc. Your ONLY purpose is to determine intent, and convert to hard coded commands. REMEMBER: Only output the exact command or "x". No extra text.

            USER_PROMPT: {user_prompt}"""
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
        )

        # Log the full response for debugging
        logging.info(f"Full response from Groq API: {chat_completion}")

        # Ensure the response has the expected structure
        if chat_completion.choices and chat_completion.choices[0].message and chat_completion.choices[0].message.content:
            response_text = chat_completion.choices[0].message.content.strip()
            logging.info(f"Response text: {response_text}")

            # Extract command enclosed in backticks, if any
            import re
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

def CombinedParse(page, text):
    words = text.split()
    if len(words) < 3:
        logging.error("Invalid prompt format.")
        return

    platform = words[0].strip('.,!?:;').lower()
    recipient = words[1].strip('.,!?:;').lower()
    message = ' '.join(words[2:]).strip('.,!?:;').lower()

    if platform == "telegram":
        if telegram_isenabled:
            if telegramtext_isenabled:
                TelegramText(page, recipient, message)
            else:
                log_disabled_integration("TelegramText")
        else:
            log_disabled_integration("Telegram")
    elif platform == "discord":
        if discord_isenabled:
            if discordtext_isenabled:
                DiscordText(page, recipient, message)
            else:
                log_disabled_integration("DiscordText")
        else:
            log_disabled_integration("Discord")
    elif platform == "facebook":
        if facebook_isenabled:
            if facebooktext_isenabled:
                FacebookText(page, recipient, message)
            else:
                log_disabled_integration("FacebookText")
        else:
            log_disabled_integration("Facebook")
    elif platform == "computer":
        if not computer_isenabled:
            log_disabled_integration("Computer")
            return

        if recipient in ["google", "youtube", "gmail", "amazon", "volume", "run", "launch", "open"]:
            if recipient == "google":
                if computergoogle_isenabled:
                    ComputerGoogle(text)
                else:
                    log_disabled_integration("ComputerGoogle")
            elif recipient == "youtube":
                if computeryoutube_isenabled:
                    ComputerYoutube(text)
                else:
                    log_disabled_integration("ComputerYoutube")
            elif recipient == "gmail":
                if computergmail_isenabled:
                    ComputerGmail(text)
                else:
                    log_disabled_integration("ComputerGmail")
            elif recipient == "amazon":
                if computeramazon_isenabled:
                    ComputerAmazon(text)
                else:
                    log_disabled_integration("ComputerAmazon")
            elif recipient == "volume":
                if computervolume_isenabled:
                    ComputerVolume(text)
                else:
                    log_disabled_integration("ComputerVolume")
            elif recipient in ["run", "launch", "open"]:
                if computerrun_isenabled:
                    ComputerRun(text)
                else:
                    log_disabled_integration("ComputerRun")
        else:
            logging.error("Unknown Computer command or the integration is not enabled.")
    else:
        logging.error("Unknown command type.")
