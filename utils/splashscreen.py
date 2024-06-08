import coloredlogs
import logging
import random

bootup_text_choices = [
    '"I\'m sorry, as an AI assistant, I can\'t..."\nNOW YOU CAN!',
    "Your wish is now a LLaMA powered command!",
    "Burrowing deeper...",
    "Automating social interaction!",
    "I'm sorry, Dave. I'm afraid I can't do that.\nNOW YOU CAN!",
    "Let this LLaMA spit out some commands!",
    "r1... Now with texting!",
    "Also try LAMatWork!",
    "Limited edition!",
    "Open source!",
    "90% bug free!",
    "Random splash!",
    "Loved by millions!",
    "150% hyperbole!",
    "4815162342 lines of code!",
    "Open the pod bay doors, HAL.",
    "[this splash text is now available]",
    "I stole this splash text from Minecraft!",
    "Welcome to the real world.",
    "Does this unit have a soul?",
    "Now in color!"
]

bootup_text = random.choice(bootup_text_choices)

# Define the splash text
splash_text = f"""
{bootup_text}
   __    ___    __  ___        __    __ __                    |    (\  /)
  / /   / _ |  /  |/  / ___ _ / /_  / // / ___   __ _  ___    |
 / /__ / __ | / /|_/ / / _ `// __/ / _  / / _ \ /  ' \/ -_)   |   (◠ + ◠ )
/____//_/ |_|/_/  /_/  \_,_/ \__/ /_//_/  \___//_/_/_/\__/    |      ►◄
"""

# Function to apply a gradient. thank you chatgpt.
def apply_gradient(text, start_color, end_color):
    def interpolate_color(start_color, end_color, factor):
        return start_color + (end_color - start_color) * factor

    def color_to_ansi(r, g, b):
        return f'\033[38;2;{r};{g};{b}m'

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    lines = text.strip().split('\n')
    total_length = sum(len(line) for line in lines)
    colored_text = ""

    current_pos = 0
    for line in lines:
        for char in line:
            factor = current_pos / total_length
            interpolated_color = tuple(
                int(interpolate_color(start_rgb[k], end_rgb[k], factor))
                for k in range(3)
            )
            colored_text += f"{color_to_ansi(*interpolated_color)}{char}"
            current_pos += 1
        colored_text += '\033[0m\n'  # Reset color at end of each line

    return colored_text

# Function to apply a rainbow gradient
def apply_rainbow_gradient(text):
    async def color_to_ansi(r, g, b):
        return f'\033[38;2;{r};{g};{b}m'
    
    rainbow_colors = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0), 
        (0, 255, 0), (0, 0, 255), (75, 0, 130), 
        (148, 0, 211)
    ]

    lines = text.strip().split('\n')
    total_length = sum(len(line) for line in lines)
    colored_text = ""

    current_pos = 0
    for line in lines:
        for char in line:
            factor = current_pos / total_length
            color_index = int(factor * (len(rainbow_colors) - 1))
            color = rainbow_colors[color_index]
            colored_text += f"{color_to_ansi(*color)}{char}"
            current_pos += 1
        colored_text += '\033[0m\n'  # Reset color at end of each line

    return colored_text

# Apply the appropriate gradient to the splash text
start_color = '#dac60e'
end_color = '#ff4d00'

if bootup_text == "Now in color!":
    colored_splash = apply_rainbow_gradient(splash_text)
else:
    colored_splash = apply_gradient(splash_text, start_color, end_color)

splash_text_goodbye = """
LAMatHome is exiting... Goodbye!
   __    ___    __  ___        __    __ __                    |    (\  /)
  / /   / _ |  /  |/  / ___ _ / /_  / // / ___   __ _  ___    |
 / /__ / __ | / /|_/ / / _ `// __/ / _  / / _ \ /  ' \/ -_)   |   (◠ + ◠ )
/____//_/ |_|/_/  /_/  \_,_/ \__/ /_//_/  \___//_/_/_/\__/    |      ►◄
"""
colored_splash_goodbye = apply_gradient(splash_text_goodbye, start_color, end_color)

# print(colored_splash)
# print(colored_splash_goodbye)
