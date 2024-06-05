<p align="center">
  <img src="assets/LAH_splash.gif" alt="LAMatHome" width="800"/>
</p>

<p align="center">
  <i>LAMatHome helps you expand the functionality of your rabbit r1. Here's how it works: </i>
</p>

## Overview:

### Grabbing journal entries:
By using your `hole.rabbit.tech` account token, we can directly fetch journal entries from the API. By doing this, we can efficiently grab your latest journal entry.

### Intention routing and command parsing:
By providing the user's utterance to `llama3-70b-8192` via the [Groq API](https://console.Groq.com) we can determine:

1. If the user is talking to r1, or if it is a command meant for LAMatHome
2. Which integration to call, and what parameters to give it

By doing this, we avoid the user having to learn every command for every integration, and enables natural language commands. It also enables creativity for the LLM to craft texts for you, if you're into automating social interaction.

**Examples:**

|User utterance in journal entry|LLM "rigid command" Output|
|-----------------------|----------|
|"Can you text my roommate Justin on telegram, yelling in all caps, that his music is too loud? Add a few extra exclamation points."|`Telegram Justin YOUR MUSIC IS TOO LOUD!!!`|
|"Can you turn the volume on my computer up to 100 to spite my roommate?"|`Computer Volume 100`|
|"What time does the moon come out today?"|`x`*|

*\*`x` is the output when the LLM decides your intention was to talk to r1, or, that it didn't have enough information. e.g. Name of recipient, platform to send on, etc.*

Then, `llm_parse.py` takes your neatly formatted command, and executes it based on which integration is called, and the parameters.

### Integrations
Below is a list of our current integrations. This list is kept up-to-date.

||Name|Category|Description|Example prompt|
|-|-|-|-|-|
||[Google](https://google.com)|Search|Searches Google|`Search google on my computer for ______`|
||[YouTube](https://youtube.com)|Search|Searches YouTube|`Open a YouTube search for ______ on my computer`|
||[Gmail](https://gmail.com)|Search|Searches Gmail|`Search my emails on my computer for ______`|
||[Amazon](https://amazon.com)|Search|Searches Amazon|`Search amazon on computer: ______`|
||Volume|Local Actions|Sets volume, turns up/down, and mutes/unmutes.|`Change the volume on my pc to 50`|
||Run|Local Actions|Presses Windows key, searches for an app, and runs.|`Open up the chat app for gamers on my computer`|
||LAMatHome|Local Actions|Only integration currently is "terminate", which closes LAH.|`That's enough from you. Close LAM at home.`|
|⚠️|[Discord](https://discord.com)|Messaging|Sends a message on Discord to a specified person/channel|`Text poke on discord asking when he's going to be back online. Wait, no ask him on telegram. Actually no, discord is good.`|
|⚠️|[FB Messenger](https://messenger.com)|Messaging|Sends a message on FB Messenger to a specified person|`Ask Justin what he thinks of my new sunglasses. Oh, send that on facebook.`|
|⚠️|[Telegram](https://web.telegram.org/)|Messaging|Sends a message on Telegram to a specified person|`Message Kevin on telegram asking him when he's gonna PR his new feature`|

> [!NOTE]
>
> *Integrations marked with a ⚠️ are experimental and may send to the incorrect person/channel based on the way the user utterance is transcribed. This is a limitation of the r1, not LLM Parsing.*

## Quick start guide:

**1. Clone the repository and CD into it**

```
git clone https://github.com/dot-justin/LAMatHome
cd LAMatHome
```
**2. Install dependencies**
```
pip install -r requirements.txt
playwright install
```
**3. Obtaining your user token from [the rabbithole](https://hole.rabbit.tech/journal/details):**
   1. Log into the rabbit hole from the link above
   2. Press F12 to bring up the developer console. If this doesn't work, right-click the page, and click inspect. 
   3. Expand the developer console for better viewing
   4. Click the `Network` tab in the top navigation bar.
   5. Press Ctrl + R to reload the page.
   6. Near the bottom of the middle pane, find and select `fetchUserJournal`.
   7. In the new pane that opened, select `Payload` in the top navigation bar.
   8. Select everything inside the quotes after `accessToken`. This is your user token.
   Note: Your token will expire 24 hours after you log in. This is out of our control but we are working on a better way.

**4. Obtaining an API key from Groq:**
  1. Go to [console.groq.com/login](https://console.groq.com/login)
  2. Create an account.
  3. Once logged in, go to [console.groq.com/keys](https://console.groq.com/keys)
  4. Click `Create API Key`
  5. Create a name for your API key. This can be anything you want. Click `Submit`.
  6. Now, a window will pop up containing your API key. Click on `Copy`. After this point, you will not be able to access this key again from the Groq website. (Don't worry too much, you can create and delete keys at any time.)
  7. Back in the ui that popped up earlier, enter your API key in the field for `Groq API Key:`

>[!WARNING]
>
>  NEVER share your user tokens or API keys. They will be stored locally in the program and will only be used to authenticate with official API's.

```
py main.py
```
**5. Running LAMatHome and entering your credentials:**
The first time you run LAMatHome, it will bring up a ui to enter your credentials.
For any service that you want to use, enter your credentials. The only required values here are:
- Rabbit Hole Access Token
- GROQ API Key

After you enter these, and hit submit, you should be all set up and ready to go! Remember, you can edit your credentials any time by editing the `.env` file inside the root directory of the project.

### Usage guide:
When you want to run LAMatHome, do the following:

Run `main.py` from the root directory

`py main.py`

This will start the LAMatHome program, and (as long as your token is valid) you can start giving prompts to r1.

### Stopping LAMatHome
To stop LAMatHome, you have two options.
1. Via r1 voice prompt (If you can't get this to work, try method 2)
   - Say `Please close/quit/terminate LAMatHome`.

2. Manually
   - Find the command prompt where it's currently running from.
   - Press `Ctrl + C` to exit the program. You may see some errors, this is expected and will not mess up your installation.

### Disabling integrations
If you don't want to use specific integration, no worries! It's simple:
1. Open the `integrations/` folder in the your LAMatHome directory.
2. Open the `.py` file for the integration you'd like to disable (Use your favorite IDE. A good free one is [notepad++](https://notepad-plus-plus.org/downloads/))
3. Hit `Ctrl + F`, and search for `_isenabled`.
4. The first instance of this in each file will disable the integration altogether. (e.g. `computer_isenabled=False`)
5. If you want more granular control (i.e. disabling google searches but allowing everything else), you would find the line that says `(integrationname)(functionname)_isenabled`. For example, `computergoogle_isenabled`.
   - `=True` for enabled, `=False` for disabled.

We plan to make this easier to adjust in the future.

## Other information:
### Errors you may run into:
|Error|Meaning/Fix|
|-|-|
|`500 Server Error: Internal Server Error for url: https://hole.rabbit.tech/APIs/fetchUserJournal`|This means that for some reason, the request to the rabbit API failed. More often than not, this means that your token has expired. While this *can* happen if your token is valid, it is very rare. [Instructions to obtain user token](https://github.com/dot-Justin/LAMatHome#quick-start-guide)|
|`playwright._impl._errors.TimeoutError: Page.click: Timeout 30000ms exceeded.`|This means that, in waiting for a certain object on the website to load, it never loaded, and Playwright timed out. If this ever happens, please open a [bug issue](https://github.com/dot-Justin/LAMatHome/issues/new?assignees=&labels=bug&projects=&template=bug_report.md).|

### Prompts:
|Use case|Prompt|
|-|-|
|Get r1 to just say "ok" in response to commands:|`From now on, whenever I give you a command and you think that you can't do it, just reply with okay. Don't reply with any other acknowledgment or any other warning or message, just reply with okay if you cannot do the command. Say "ok" if you understand.`|

## Contributors:
[![LAMatHome's Contributors](https://stats.deeptrain.net/contributor/dot-justin/LAMatHome/?theme=dark)](https://github.com/dot-justin/LAMatHome/contributors)

## Acknowledgements:
- Thanks to poke for the original idea [https://github.com/glovergaytan-fs](rabbitWrighter)
- Obligatory "There's no way you're that young" [https://github.com/GikitSRC/rabbitt](rabbitt)

## License:
[MIT](https://choosealicense.com/licenses/mit/)