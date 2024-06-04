import coloredlogs
import logging

# Define the splash text
splash_text = """
"I'm sorry, as an AI assistant, I can't..."
NOW YOU CAN:
   __    ___    __  ___  ___   __    __ __                   |    (\  /)
  / /   / _ |  /  |/  / / _ | / /_  / // /___   __ _  ___    |
 / /__ / __ | / /|_/ / / __ |/ __/ / _  // _ \ /  ' \/ -_)   |   (◠ + ◠ )
/____//_/ |_|/_/  /_/ /_/ |_|\__/ /_//_/ \___//_/_/_/\__/    |      ►◄
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
    colored_text = ""

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            factor = (i * len(line) + j) / (len(line) * len(lines))
            interpolated_color = tuple(
                int(interpolate_color(start_rgb[k], end_rgb[k], factor))
                for k in range(3)
            )
            colored_text += f"{color_to_ansi(*interpolated_color)}{char}"
        colored_text += '\033[0m\n'  # Reset color at end of each line

    return colored_text

# Apply gradient to splash text
start_color = '#dac60e'
end_color = '#ff4d00'
colored_splash = apply_gradient(splash_text, start_color, end_color)

splash_text_goodbye = """
LAMatHome is exiting... Goodbye!
   __    ___    __  ___  ___   __    __ __                   |    (\  /)
  / /   / _ |  /  |/  / / _ | / /_  / // /___   __ _  ___    |
 / /__ / __ | / /|_/ / / __ |/ __/ / _  // _ \ /  ' \/ -_)   |   (◠ + ◠ )
/____//_/ |_|/_/  /_/ /_/ |_|\__/ /_//_/ \___//_/_/_/\__/    |      ►◄
"""
colored_splash_goodbye = apply_gradient(splash_text_goodbye, start_color, end_color)
