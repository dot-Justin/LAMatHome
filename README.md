# 🐇 LAM At Home
<img src="assets/LAMAtHome.png" alt="LAMAtHome" width="400"/>

#### *Work in progress - Feel free to fork and submit a pull request if you make something cool!*

## ❓ What does LAM At Home do?
This program locally runs Playwright to constantly refresh hole.rabbit.tech, looking for new entries. If a new entry begins with a keyword, it will carry out an action. Essentially, this adds functionality to your Rabbit r1 by allowing integrations currently unsupported by the Rabbit team.

## 🌐 Integrations

### 💻 Computer
**Syntax**: `"Computer [Function] [Query]"`

| Function   | Description                                      | Syntax                          | Example                                                   |
|------------|--------------------------------------------------|---------------------------------|-----------------------------------------------------------|
| **Google** | Performs a Google search for the provided query. | `"Computer Google [search query]"` | `"Computer Google What is the meaning of life?"`          |
| **YouTube**| Performs a YouTube search for the provided query.| `"Computer YouTube [search query]"`| `"Computer YouTube How to bake a cake"`                    |

**Setup**: 
- No setup required!

### 💬 Telegram
**Syntax**: `"Telegram [User] [Message content]"` (Working on more telegram functionality)

| Function    | Description                           | Syntax                             | Example                         |
|-------------|---------------------------------------|-------------------------------------|---------------------------------|
| **Telegram**| Messages a specified user on Telegram.| `"Telegram [Name (one word)] [Message]"` | `"Telegram Arthur What's up?"` |

**Setup**:
1. If a Telegram prompt is detected, Playwright will open up a Telegram window with a QR code.
    - Head to the Telegram app on your phone, tap the hamburger menu at the top left, tap `Settings` > `Devices` > `Link Desktop Device`, and scan the QR code.
    - If you get an error like "Expired", manually refresh the Telegram QR page. Your session will be saved so it will be rare that you need to do this.

**Tips**:
- There is a chance that you will be sending messages to random people. This is a result of the way Telegram search works.
- The first word of your prompt needs to be "Telegram" for this to work.
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

LAMAtHome runs off groups of functions, called Integrations. By default, every integration is enabled, however each integration, as well as its child functions, can be disabled. Follow these steps to do so:
- Disable entire Integrations (Computer, Telegram, etc.)
    1. Open `main.py`
    2. Scroll to the Integration you want to disable (marked by a wall of comments, including the name. Or, search for the function name.)
    3. Find the line where it says `integrationname_isenabled=True` and change to `integrationname_isenabled=False`

- Disable only certain functions (ComputerGoogle, TelegramText, etc)
    1. Find the function you want to disable
    2. Follow the same steps as above.

## 🔥 Acknowledgements
- Thanks to poke for the original idea [rabbitWrighter](https://github.com/glovergaytan-fs/rabbitWrighter/tree/main)
- Obligatory "There's no way you're that young" [rabbitt](https://github.com/GikitSRC/rabbitt)

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
