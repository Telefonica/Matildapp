import os
import json
import signal
import argparse
import threading
from time import sleep
from subprocess import Popen, PIPE

from rich import print
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree
from pynput.keyboard import Controller
from web3 import Web3

import banner
from complete import Completer
from connect import Connect
from console import print_error, print_info, print_ok, print_table
from datastore import datastore
from datastore.contract_info import ContractInfo
from datastore.network import Network
from datastore.wallet import Wallet
from help import show_help
from session import Session
from setglobal import Global
from web3_connection import BlockchainConnection


try:
    import readline
    import rlcompleter

    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except:
    pass

# TODO: Refactor this into a separate module
PLUS_SIGN = "[[bold green]+[/bold green]]"
EXCL_SIGN = "[[bold red]![/bold red]]"


class Console:
    def console(self):
        signal.signal(signal.SIGINT, self.keyboard_interrupt_handler)

        # Configuring the commpleter
        self.comp = Completer(
            [
                "load",
                "set",
                "unset",
                "global",
                "show",
                "run",
                "interact",
                # "jobs",
                "contracts",
                "networks",
                "wallets",
                "back",
                "quit",
                "help",
                "connect",
                "disconnect",
            ]
        )
        readline.set_completer_delims(" \t\n;")
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.comp.complete)

        # commands & functions
        self.switcher = {
            "load": self.load,
            "set": self.set,
            "unset": self.unset,
            "global": self.setglobal,
            "show": self.show,
            "run": self.run,
            "interact": self.interact,
            # "jobs": self.jobs,
            "contracts": self.contracts,
            "networks": self.networks,
            "wallets": self.wallets,
            "back": self.back,
            "quit": self.quit,
            "exit": self.quit,
            "help": self.help,
            "connect": self.connect,
            "disconnect": self.disconnect,
        }

        banner.print_banner()
        print(" [yellow][+][/yellow] Starting the console...")
        print(" [green][*][/green] Console ready!\n")

        self.session = None

        while True:
            try:
                if self.session is None:
                    # /* Definitions available for use by readline clients. */
                    # define RL_PROMPT_START_IGNORE  '\001'
                    # define RL_PROMPT_END_IGNORE    '\002'
                    user_input = input(
                        "\001\033[1;32m\002matildapp $ > \001\033[0m\002"
                    ).strip()
                    # from console import console

                    # user_input = console.input(
                    #     "[bold green]matildapp $ > [/bold green]"
                    # )
                    # user_input = Prompt.ask("[bold green]matildapp $ > [/bold green]")
                else:
                    user_input = input(
                        "matildapp $ >["
                        + "\001\033[1;32m\002"
                        + self.session.header()
                        + "\001\033[0m\002"
                        + "]> "
                    ).strip()

                if user_input == "":
                    continue
                else:
                    self.switch(user_input)
            except Exception as e:
                print_error(e)

    def keyboard_interrupt_handler(self, signal, frame):
        print_error("Closing matildapp, wait...")
        self.quit()

    # Switcher
    def switch(self, u_input):
        try:
            if u_input.startswith("#"):
                self.execute_command(u_input[1:])
            else:
                u_input = u_input.split()
                if len(u_input) >= 2:
                    self.switcher.get(u_input[0], self._command_error)(u_input[1:])
                else:
                    self.switcher.get(u_input[0], self._command_error)()
        except Exception as e:
            print_error(e)

    # Functions to check errors begin
    def _command_error(self):
        raise Exception("Command not found")

    def _raise_exception_specify(self, option):
        raise Exception("Specify %s" % (option))

    def _check_load_module(self):
        if not self.session:
            raise Exception("Please, load a module")

    def _check_set(self, user_input, op=2):
        self._check_load_module()
        throw = False
        if op == 1:
            if not user_input:
                throw = True
        else:
            if not (len(user_input) >= 2):
                throw = True
        if throw:
            self._raise_exception_specify("value")

    # Functions to check errors end

    # Command functionality begin
    def execute_command(self, command):
        try:
            data = Popen(command, shell=True, stdout=PIPE).stdout.read()
            print("")
            for line in data.decode().split("\n"):
                print_info(line)
        except Exception as e:
            raise Exception(str(e))

    def load(self, user_input=None):
        if not user_input:
            self._raise_exception_specify("module")
        self.session = Session(user_input[0])
        # The module is incorrect
        if not (self.session.correct_module()):
            print_error("Invalid module")
            self.session = None
        else:
            self.comp.set_commands_to_set(self.session.get_options_name())

    """def jobs(self, user_input=None):
        if not user_input:
            Jobs.get_instance().show_jobs()
        elif len(user_input) > 0 and  user_input[0] == "-k":
            if len(user_input) == 2:
                id = user_input[1]
                if Jobs.get_instance().is_id_job(id):
                    print_info("ID job found")
                    Jobs.get_instance().kill_jobs(id)
                else:
                    print_error("ID job not found")
            else:
                print_error("ID job with multiple parameters")
        elif len(user_input) > 0 and  user_input[0] == "-K":
            Jobs.get_instance().kill_all_jobs()"""

    def set(self, user_input=[]):
        self._check_set(user_input)
        value = " ".join([str(x) for x in user_input[1:]])
        self.session.set(user_input[0], value)

    def unset(self, user_input=[]):
        self._check_set(user_input, op=1)
        self.session.unset(user_input[0])

    def setglobal(self, user_input=[]):
        self._check_set(user_input)
        try:
            value = " ".join([str(x) for x in user_input[1:]])
            self.session.set(user_input[0], value)
            Global.get_instance().add_value(user_input[0], value)
        except:
            print_error("Option not found for your configuration, use show")

    def show(self, user_input=[]):
        self._check_load_module()
        self.session.show()

    def run(self, user_input=[]):
        self._check_load_module()
        self.session.run()

    def back(self, user_input=[]):
        self.session = None

    def quit(self, user_input=[]):
        """if Jobs.get_instance().hasjobs():
        Jobs.get_instance().kill_all_jobs()"""
        print_info("bye!")
        exit(0)

    def help(self, user_input=[]):
        show_help()
        # Command functionality end

    def connect(self, user_input=[]):
        """Connect to a blockchain using a provider URI or a datastore alias."""
        if not user_input or len(user_input) != 1:
            return print_info(
                "Usage: connect <provider_endpoint_uri or datastore_alias>"
            )

        provider_input = user_input[0]

        # Check if it's an alias and get the corresponding RPC URL from datastore
        rpc = None
        for key, network in datastore.networks.items():
            if network.alias == provider_input:
                rpc = network.rpc
                print_info(f"Using RPC from alias '{provider_input}': {rpc}")
                break

        # If not found, treat it as a direct URI
        if not rpc:
            rpc = provider_input

            # Validate the RPC URL before proceeding
            if not Network.validate_url(rpc):
                return print_error(f"Invalid RPC URL: {rpc}")

            # If valid, inform the user
            print_info(f"Using direct RPC: {rpc}")

        # Create connection instance and connect
        connection = BlockchainConnection()
        connection.connect(rpc)

    def disconnect(self, user_input=[]):
        """
        Disconnect from the current blockchain connection.

        Usage:
            disconnect

        If there's an active connection, it will be terminated. If no connection exists,
        an informational message will be displayed.
        """
        # Retrieve the singleton instance of BlockchainConnection
        connection = BlockchainConnection.get_instance()

        # Check if there's an active connection
        if connection.web3 and connection.web3.is_connected():
            connection.disconnect()
            print_ok("Disconnected from blockchain successfully!")
        else:
            print_info("No active blockchain connection found.")

    def interact(self, user_input=[]):
        """Interact with a contract on the blockchain."""
        if not user_input:
            return print_info("Usage: interact <contract_address>")

        contract_address = user_input[0]
        connection = BlockchainConnection.get_instance()

        # Create a contract instance
        try:
            contract = connection.contract_interact(contract_address)
            print_info(
                f"Successfully connected to contract at address: {contract_address}"
            )

            # Add to datastore
            datastore.add_contract(
                contract.address,
                bytecode=Web3.to_hex(contract.bytecode),
                network=connection.web3.provider.endpoint_uri,
            )
            # print_ok(f"address: {contract.address}")
            # print_ok(f"bytecode: {Web3.to_hex(contract.bytecode)}")
            return contract
        except Exception as e:
            print_error(e)
            # print_error(f"Failed to interact with contract at address: {contract_address}")

    def contracts(self, user_input=[]):
        help_text = "Use show [--tree], add, remove, alias"

        def show(args):
            """
            Display contracts in a table or tree format based on arguments.

            Args:
                args (list): List of arguments passed to the 'show' command.
                            Use '--tree' to display contracts as a tree.
            """
            if not datastore.contracts:
                print_info("No contracts found.")
                return

            if "--tree" in args:
                try:
                    # Root node of the tree
                    tree = Tree("[bold green]Contracts Information[/bold green]")

                    # Loop through each contract in the datastore
                    for address, contract in datastore.contracts.items():
                        contract_tree = tree.add(f"[bold]Address:[/bold] {address}")

                        # Alias
                        contract_tree.add(
                            f"{PLUS_SIGN} [bold]Alias:[/bold] {contract.alias}"
                        )

                        # Network
                        if contract.network:
                            contract_tree.add(
                                f"{PLUS_SIGN} [bold]Network:[/bold] {contract.network}"
                            )
                        else:
                            contract_tree.add(
                                f"{PLUS_SIGN} [bold]Network:[/bold] Unknown"
                            )

                        # Source
                        if contract.source:
                            contract_tree.add(
                                f"{PLUS_SIGN} [bold]Source:[/bold]\n{contract.source}"
                            )

                        # ABI
                        if contract.abi:
                            contract_tree.add(
                                f"{PLUS_SIGN} [bold]ABI:[/bold]\n{json.dumps(contract.abi, indent=2)}"
                            )

                        # Bytecode
                        if contract.bytecode:
                            contract_tree.add(
                                f"{PLUS_SIGN} [bold]Bytecode:[/bold]\n{contract.bytecode}"
                            )

                        # Selectors
                        if contract.selectors:
                            selectors_tree = contract_tree.add(
                                f"{PLUS_SIGN} [bold]Function Selectors:[/bold]"
                            )
                            for selector in contract.selectors:
                                selectors_tree.add(f"{PLUS_SIGN} {selector}")

                    # Print the tree
                    print(tree)
                except Exception as e:
                    print_error(f"Error displaying contracts: {e}")
            else:
                # Display contracts as a table
                table = Table(title="Contracts")

                table.add_column("Address", style="cyan", no_wrap=True)
                table.add_column("Alias", style="green")
                table.add_column("Network", style="magenta")
                table.add_column("Source", style="yellow")

                for contract in datastore.contracts.values():
                    table.add_row(
                        contract.address,
                        contract.alias or "",
                        contract.network or "",
                        contract.source or "",
                    )

                print_table(table)
                print_info(f"Total contracts: {len(datastore.contracts)}")
                print_info("Use 'show --tree' to display more details.")

        def add(args):
            add_help = "Use add <address> [contract_file_path] [alias <alias>] [network <network>] [source <source>] [bytecode <bytecode>]"

            # Check if at least a contract address or a contract file path was provided
            if not args or len(args) < 1:
                return print_info(add_help)

            # Initialize the values
            address = None
            contract_file_path = None
            alias = None
            network = None
            source = None
            bytecode = None
            abi = None

            # The first argument should be the contract address or the contract file path
            first_arg = args[0]

            # Check if it's a contract address or a file path
            if first_arg.startswith(
                "0x"
            ):  # Assume it's a contract address if it starts with "0x"
                address = first_arg
                contract_file_path = args[1] if len(args) > 1 else None
            else:
                contract_file_path = first_arg
                address = None  # If it's a file, there shouldn't be an address

            # Parse optional parameters
            for i in range(2 if contract_file_path else 1, len(args), 2):
                key = args[i]
                value = args[i + 1] if i + 1 < len(args) else None

                if key == "alias":
                    alias = value
                elif key == "network":
                    network = value
                elif key == "source":
                    source = value
                elif key == "bytecode":
                    bytecode = value
                else:
                    return print_info(add_help)

            # Check if either the address or the file path is valid
            if not address and not contract_file_path:
                return print_error(
                    "You must specify either a contract address or a contract file path."
                )

            # Check if the contract already exists
            if address and address in datastore.contracts:
                return print_error(f"Contract with address '{address}' already exists.")

            # TODO: If a contract file path is provided, attempt to load the contract
            if contract_file_path:
                if contract_file_path.endswith(".json"):
                    try:
                        with open(contract_file_path, "r") as abi_file:
                            abi = json.load(abi_file)
                    except FileNotFoundError:
                        return print_error(
                            f"Contract ABI file not found: {contract_file_path}"
                        )
                    except json.JSONDecodeError:
                        return print_error(
                            f"Error decoding JSON in ABI file: {contract_file_path}"
                        )
                else:
                    source = contract_file_path  # Assume it's the source file
                    print_info(f"Using contract source file: {source}")

            # Add the contract to the datastore
            try:
                datastore.add_contract(
                    address=address,
                    abi=abi,
                    alias=alias,
                    network=network,
                    source=source,
                    bytecode=bytecode,
                )
                print_info(
                    f"Contract added successfully: {address if address else contract_file_path}"
                )
            except Exception as e:
                print_info(f"Error adding contract: {e}")

        def remove(args):
            remove_help = "Use remove <address_or_alias>"

            if not args or len(args) < 1:
                return print_info(remove_help)

            value = args[0]

            try:
                # Check by address
                if value in datastore.contracts:
                    datastore.remove_contract(address=value)
                    print_info(f"Contract removed successfully: {value}")
                    return

                # Check by alias
                address_to_remove = next(
                    (
                        contract.address
                        for contract in datastore.contracts.values()
                        if contract.alias == value
                    ),
                    None,
                )

                if address_to_remove:
                    datastore.remove_contract(address=address_to_remove)
                    print_info(
                        f"Contract with alias '{value}' removed successfully (Address: {address_to_remove})"
                    )
                else:
                    print_error(f"No contract found with address or alias: {value}")

            except Exception as e:
                print_error(f"Error removing contract: {e}")

        def alias(args):
            alias_help = "Use alias <current_address_or_alias> <new_alias>"

            if not args or len(args) < 2:
                return print_info(alias_help)

            try:
                current_identifier = args[0]
                new_alias = args[1]

                address = None
                if current_identifier in datastore.contracts:
                    address = current_identifier
                else:
                    address = next(
                        (
                            key
                            for key, contract in datastore.contracts.items()
                            if contract.alias == current_identifier
                        ),
                        None,
                    )

                if not address:
                    return print_error(
                        f"No contract found with address or alias: {current_identifier}"
                    )

                datastore.update_contract_alias(address=address, new_alias=new_alias)
                print_info(
                    f"Alias updated successfully for contract {address}: {new_alias}"
                )

            except ValueError as ve:
                print_error(str(ve))
            except Exception as e:
                print_error(f"Error updating alias: {e}")

        command_map = {
            "show": show,
            "add": add,
            "remove": remove,
            "alias": alias,
        }

        if not user_input:
            return print_info(help_text)

        command = user_input[0]
        handler = command_map.get(command, lambda args: print_info(help_text))
        handler(user_input[1:])

    def networks(self, user_input=[]):
        help_text = "Use add, remove, show, alias"

        def show(args):
            if not datastore.networks:
                print_info("No networks found")
                return

            table = Table(title="Networks")

            table.add_column("RPC", style="cyan", no_wrap=True)
            table.add_column("Chain ID", style="magenta")
            table.add_column("Alias", style="green")
            table.add_column("Symbol", style="yellow")

            for rpc, network in datastore.networks.items():
                # If alis is same as RPC, then it show "-"
                if network.alias == rpc:
                    network.alias = "-"
                table.add_row(rpc, str(network.chain_id), network.alias, network.symbol)

            print_table(table)

        def add(args):
            add_help = "Use add rpc chain_id [alias] [symbol] [block_explorer]"

            # Minimum argument validation
            if len(args) < 2:
                return print_info(add_help)

            # Argument assignment
            rpc = args[0]  # First argument as RPC
            chain_id = args[1]  # Second argument as Chain ID
            alias = args[2] if len(args) > 2 else None  # Optional
            symbol = args[3] if len(args) > 3 else None  # Optional
            block_explorer = args[4] if len(args) > 4 else None  # Optional

            # Call to add_network method
            try:
                datastore.add_network(
                    rpc=rpc,
                    chain_id=int(chain_id),
                    alias=alias,
                    symbol=symbol,
                    block_explorer=block_explorer,
                )
                print_info(
                    f"Network added successfully: RPC={rpc}, Chain ID={chain_id}"
                )
            except Exception as e:
                print_info(f"Error adding network: {e}")

        def remove(args):
            remove_help = "Use remove <rpc_or_alias>"

            # Validate minimum arguments
            if not args or len(args) < 1:
                return print_info(remove_help)

            # Extract the provided value (could be RPC or alias)
            value = args[0]

            try:
                # Attempt to find the network using the RPC
                if value in datastore.networks:
                    datastore.remove_network(rpc=value)
                    print_info(f"Network removed successfully: {value}")
                    return

                # Attempt to find the network using the alias
                rpc_to_remove = next(
                    (
                        rpc
                        for rpc, network in datastore.networks.items()
                        if network.alias == value
                    ),
                    None,
                )

                if rpc_to_remove:
                    datastore.remove_network(rpc=rpc_to_remove)
                    print_info(
                        f"Network with alias '{value}' removed successfully (RPC: {rpc_to_remove})"
                    )
                else:
                    print_error(f"No network found with RPC or alias: {value}")

            except Exception as e:
                print_error(f"Error removing network: {e}")

        def alias(args):
            alias_help = "Use networks alias <current_rpc_or_alias> <new_alias>"

            # Validate minimum arguments
            if not args or len(args) < 2:
                return print_info(alias_help)

            try:
                # Extract arguments
                current_identifier = args[0]
                new_alias = args[1]

                # Check if the identifier is an RPC or an alias
                rpc = None
                if current_identifier in datastore.networks:
                    rpc = current_identifier  # It's an RPC
                else:
                    # Search for the alias in the networks dictionary
                    rpc = next(
                        (
                            key
                            for key, network in datastore.networks.items()
                            if network.alias == current_identifier
                        ),
                        None,
                    )

                if not rpc:
                    return print_error(
                        f"No network found with RPC or alias: {current_identifier}"
                    )

                # Update the alias using the resolved RPC
                datastore.update_network_alias(rpc=rpc, new_alias=new_alias)
                print_info(f"Alias updated successfully for network {rpc}: {new_alias}")

            except ValueError as ve:
                print_error(str(ve))
            except Exception as e:
                print_error(f"Error updating alias: {e}")

        command_map = {
            "show": show,
            "add": add,
            "remove": remove,
            "alias": alias,
        }

        if not user_input:
            return print_info(help_text)

        command = user_input[0]
        handler = command_map.get(command, lambda args: print_info(help_text))
        handler(user_input[1:])

    def wallets(self, user_input=[]):
        help_text = "Use add, remove, show, alias"

        def show(args):
            if not datastore.wallets:
                print_info("No wallets found")
                return

            table = Table(title="Wallets")

            table.add_column("Address", style="cyan", no_wrap=True)
            table.add_column("Alias", style="green")
            table.add_column("Private key", style="red")

            for address, wallet in datastore.wallets.items():
                # Check if the wallet has a private key and display '*' in red if so
                private_key = "*" if wallet.private_key else ""
                table.add_row(address, wallet.alias, private_key)

            print_table(table)

        def add(args):
            add_help = "Use add wallet private_key <key> or add wallet address <address> [alias <alias>]"

            # Validate minimum arguments
            if not args or len(args) < 2:
                return print_info(add_help)

            # Initialize parameters
            private_key = None
            address = None
            alias = None

            # Parse arguments
            try:
                for i in range(0, len(args), 2):
                    key = args[i]
                    value = args[i + 1] if i + 1 < len(args) else None

                    if key == "private_key":
                        private_key = value
                    elif key == "address":
                        address = value
                    elif key == "alias":
                        alias = value
                    else:
                        return print_info(add_help)

                # Ensure valid arguments
                if not private_key and not address:
                    return print_error(
                        "You must specify either a private_key or an address."
                    )

                if private_key and address:
                    return print_error("Specify only one: private_key or address.")

                if address and address in datastore.wallets:
                    return print_error(f"Address '{address}' already exists.")
                elif private_key:
                    generated_address = Wallet.generate_address(private_key)

                    if generated_address in datastore.wallets:
                        if datastore.wallets[generated_address].private_key:
                            return print_error(
                                f"Public address with private key '{private_key}' already exists."
                            )

                # Call the add_wallet function
                datastore.add_wallet(
                    private_key=private_key, address=address, alias=alias
                )
                print_info(
                    f"Wallet added successfully: {address or 'Private Key Wallet'}"
                )
            except IndexError:
                print_info(add_help)
            except Exception as e:
                print_error(f"Error adding wallet: {e}")

        def remove(args):
            remove_help = "Use remove <address_or_alias>"

            # Validate minimum arguments
            if not args or len(args) < 1:
                return print_info(remove_help)

            # Extract the provided value (could be address or alias)
            value = args[0]

            try:
                # Attempt to find the wallet using the address
                if value in datastore.wallets:
                    datastore.remove_wallet(address=value)
                    print_info(f"Wallet removed successfully: {value}")
                    return

                # Attempt to find the wallet using the alias
                address_to_remove = next(
                    (
                        wallet.address
                        for wallet in datastore.wallets.values()
                        if wallet.alias == value
                    ),
                    None,
                )

                if address_to_remove:
                    datastore.remove_wallet(address=address_to_remove)
                    print_info(
                        f"Wallet with alias '{value}' removed successfully (Address: {address_to_remove})"
                    )
                else:
                    print_error(f"No wallet found with address or alias: {value}")

            except Exception as e:
                print_error(f"Error removing wallet: {e}")

        def alias(args):
            alias_help = "Use wallets alias <current_address_or_alias> <new_alias>"

            # Validate minimum arguments
            if not args or len(args) < 2:
                return print_info(alias_help)

            try:
                # Extract arguments
                current_identifier = args[0]
                new_alias = args[1]

                # Check if the identifier is an address or an alias
                address = None
                if current_identifier in datastore.wallets:
                    address = current_identifier  # It's an address
                else:
                    # Search for the alias in the wallets dictionary
                    address = next(
                        (
                            key
                            for key, wallet in datastore.wallets.items()
                            if wallet.alias == current_identifier
                        ),
                        None,
                    )

                if not address:
                    return print_error(
                        f"No wallet found with address or alias: {current_identifier}"
                    )

                # Update the alias using the resolved address
                datastore.update_wallet_alias(address=address, new_alias=new_alias)
                print_info(
                    f"Alias updated successfully for wallet {address}: {new_alias}"
                )

            except ValueError as ve:
                print_error(str(ve))
            except Exception as e:
                print_error(f"Error updating alias: {e}")

        command_map = {
            "show": show,
            "add": add,
            "remove": remove,
            "alias": alias,
        }

        if not user_input:
            return print_info(help_text)

        command = user_input[0]
        handler = command_map.get(command, lambda args: print_info(help_text))
        handler(user_input[1:])


def load_instructions(f):
    keyboard = Controller()
    sleep(1)
    data_file = open(f)
    for line in data_file.readlines():
        keyboard.type(line + "\n")
        sleep(0.2)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="File with instructions, one per line...")
    args = parser.parse_args()
    if args.file:
        th = threading.Thread(target=load_instructions, args=(args.file,))
        th.start()
    Console().console()
