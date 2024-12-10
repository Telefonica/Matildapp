from random import choice

from pyfiglet import Figlet
from rich.text import Text

from console import console

ascii_fonts = ["graffiti", "doom", "basic"]
colors = ["red", "blue", "green", "yellow"]


def print_banner():
    banner = Figlet(font=choice(ascii_fonts))
    color = choice(colors)

    console.print(banner.renderText("Matildapp"), style=color)
    console.print("[-*-] matildapp: Multi Analysis Toolkit (by IdeasLocas) on DAPPs [-*-]", style="green")

    created = Text()
    created.append("[-*-]             Created by: ", style="blue")
    created.append("IdeasLocas", style="red")
    created.append("(", style="blue")
    created.append("With Love!", style="green")
    created.append(")             [-*-]", style="blue")

    console.print(created)
    console.print()
