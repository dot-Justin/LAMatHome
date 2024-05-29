# 🐇 LAM At Home
<img src="assets/LAMAtHome.png" alt="LAMAtHome" width="400"/>

#### *Work in progress - Feel free to fork and submit a pull request if you make something cool!*

## ❓ What does LAM At Home do?
This program locally runs Playwright to constantly refresh hole.rabbit.tech, looking for new entries. If a new entry begins with a keyword, it will carry out an action. Essentially, this adds functionality to your Rabbit r1 by allowing integrations currently unsupported by the Rabbit team.

## 🌐 Integrations

### 💻 Computer

**Syntax**: `"Computer [Function] [Query]"`
|| Function | Description | Syntax | Example |
|-|-|-|-|-|
|🔎| **Google** | Performs a Google search for the provided query. | `"Computer Google [search query]"` | `"Computer Google What is the meaning of life?"`|
|🔎| **YouTube** | Performs a YouTube search for the provided query.| `"Computer YouTube [search query]"`| `"Computer YouTube How to bake a cake"`|
|🔎| **Gmail** | Performs a Gmail search for the provided query.| `"Computer Gmail [search query]"`| `"Computer Gmail AI"`|
|🔎| **Amazon** | Performs an Amazon search for the provided query.| `"Computer Amazon [search query]"`| `"Computer Amazon Men's socks"`|
|⚙️| **Volume** | Sets computer volume| `"Computer Volume [1-100\|up\|down\|mute\|unmute]"`| `"Computer Volume 30 \| Computer volume down"`|


**Setup**: 
- Set your default browser in Windows Settings > Apps > Default apps

### 💬 Telegram
**Syntax**: `"Telegram [User] [Message content]"` (Working on more telegram functionality)

|| Function | Description | Syntax | Example |
|-|-|-|-|-|
|💬| **Telegram** | Messages a specified user on Telegram. | `"Telegram [Name (one word)] [Message]"` | `"Telegram Arthur What's up?"`|

**Setup**:
1. For first time setup and login to telegram, you will need to run the program in headful mode.
    - This can be done in `main.py`, under the main function. Search for "headless=" and ensure that it's set to ""
2. If a Telegram prompt is detected, Playwright will open up a Telegram window with a QR code.
    - Head to the Telegram app on your phone, tap the hamburger menu at the top left, tap `Settings` > `Devices` > `Link Desktop Device`, and scan the QR code.
    - If you get an error like "Expired", manually refresh the Telegram QR page. Your session will be saved so it will be rare that you need to do this.

**Tips**:
- There is a chance that you will be sending messages to random people. This is a result of the way Telegram search works.
- If your entry decides to save as a note, this will not work, try to 5xptt and give your prompt again.

## 👨‍💻 Installation & Usage

1. Clone the repository:
    ```
    git clone https://github.com/dot-Justin/LAMAtHome
    ```

2. Install the required packages:
    ```
    pip install -r requirements.txt
    playwright install
    ```

3. Add your credentials to `.env` file.

4. Run the script:
    ```
    py main.py
    ```

## ⚙️ Configuration

LAMAtHome uses groups of functions called Integrations. By default, every integration and its functions are enabled. In the examples below, notice the difference in the way they are announced. Integrations have large blocks of comments, and functions have small ones. You can disable entire integrations or specific functions by following these steps:

### 🟦 Disable Entire Integrations (Computer, Telegram, etc.)
1. Go to the `/integrations/` directory and open the file for the integration you want to configure (e.g., `computer.py`, `telegram.py`).
2. At the top of the file, locate the line that says `integrationname_isenabled=True` and change it to `integrationname_isenabled=False`.

    - Note: Disabling an integration with the same name as the file will disable the entire integration.

Example:

```
#############################################################
#                                                           #
#                          Computer:                        #
#                                                           #
#############################################################

# (set to False to disable entire integration)
computer_isenabled = True
```

### ⏹️ Disable Specific Functions (ComputerGoogle, TelegramText, etc.)
1. Open the file for the integration under `/integrations/` where the function is defined.
2. Scroll to the function you want to disable (each function is marked by a block comment with its name, or you can search for the function name).
3. Locate the line that says `functionname_isenabled=True` and change it to `functionname_isenabled=False`.

Example:

```
############################
#      ComputerVolume      #
############################

# (set to False to disable)
computervolume_isenabled = True
```

By following these steps, you can easily customize which integrations and functions are enabled or disabled in LAMAtHome.

## 🔥 Acknowledgements
- Thanks to poke for the original idea [rabbitWrighter](https://github.com/glovergaytan-fs/rabbitWrighter/tree/main)
- Obligatory "There's no way you're that young" [rabbitt](https://github.com/GikitSRC/rabbitt)

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
