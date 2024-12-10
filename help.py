from rich.markup import escape

from console import console

commands = [
    {"command": "load <module>", "description": "Load a specific module"},
    {"command": "back", "description": "Unload a module"},
    {"command": "show", "description": "Show module info and options"},
    {"command": "set <option> <value>", "description": "Assign value to an option"},
    {"command": "unset <option>", "description": "Set null an option"},
    {
        "command": "global <option> <value>",
        "description": "Assign value to a global option",
    },
    {"command": "run", "description": "Start the module"},
    {"command": "jobs", "description": "Show jobs in background"},
    {
        "command": "networks",
        "description": "Manage and interact with network configurations (add, remove, show, alias)",
    },
    {
        "command": "wallets",
        "description": "Manage and interact with wallet configurations (add, remove, show, alias)",
    },
    {"command": "help", "description": "Show this text"},
    {
        "command": "# system_command",
        "description": "Executes a command on the local system",
    },
    {"command": "quit", "description": "Bye bye matildapp!"},
]


def show_help():
    for command in commands:
        console.print(escape(command["command"]), style="yellow")
        console.print(f"{'-' * len(command['command'])}")
        console.print(f'|_ {command["description"]}')
        console.print()
