from web3 import Web3
from rich.table import Table

from module import Module
from console import print_table, print_error


class CustomModule(Module):
    """
    Module to read the storage of a contract
    """

    def __init__(self):
        information = {
            "Name": "Read contract storage",
            "Description": """This module allows you to visualize the storage of a contract.
   To extract the storage, the contract address and the network alias are required.
   The information is displayed in a table with the index, value in hex, value as a number and value as a text.
            """,
            "Author": "@jalvarezz13",
        }

        # -----------name-----default_value--description--required?
        options = {
            "contract": [None, "Contract address or contract alias in the datastore", True],
            "network": [None, "Network alias to use", True],
        }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class attributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def run_module(self) -> None:
        contract_address = self.args["contract"]
        network_rpc = self.args["network"]

        web3 = Web3(Web3.HTTPProvider(network_rpc))

        # Get the contract storage
        storage = {}
        for i in range(0, 10):
            try:
                value = web3.eth.get_storage_at(contract_address, i)
                if not value:
                    continue
                storage[i] = value
            except Exception as e:
                print_error(f"Error getting storage position {i}: {e}")
                break

        if storage:
            table = Table(title="Contract storage")

            table.add_column("Index", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")
            table.add_column("Possible number", style="magenta")
            table.add_column("Possible text", style="yellow")

            for postion, value in storage.items():
                table.add_row(str(postion), str(Web3.to_hex(value)), str(Web3.to_int(value)), str(Web3.to_text(value)))

            print_table(table)
        else:
            print_error("Oops, the storage is empty...")
