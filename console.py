from rich.console import Console

console = Console(highlight=False)


def print_error(text):
    console.print(f"[red][!][/red] {text}")


def print_info(text):
    console.print(text, style="yellow")


def print_ok(text):
    console.print(f"[green][+][/green] {text}")


def print_table(data):
    console.print(data)
