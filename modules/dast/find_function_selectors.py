from console import print_ok, print_error, print_info
from lib.bytecode_contract import ByteCode_Contract
from module import Module
from datastore import datastore
from utils import get_bytecode_from_path, find_function_selectors


class CustomModule(Module):
    """
    Module to find functions selectors in the bytecode
    """

    def __init__(self):
        information = {
            "Name": "Find Function Selectors",
            "Description": """Find function selectors in the bytecode of a contract.
   To identify function selectors within Ethereum smart contract bytecode. 
   Function selectors are derived from the first 4 bytes of the Keccak-256 hash
   of a function signature and are used in Ethereum's ABI encoding for method identification.
            """,
            "Author": "@pablogonzalezpe",
        }

        # -----------name-----default_value--description--required?
        options = {"bytecode": [None, "Bytecode, alias of the contract in the datastore or path to .txt containing the bytecode", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def run_module(self) -> None:
        bytecode: ByteCode_Contract | None = get_bytecode_from_path(self.args)
        selectors = find_function_selectors(bytecode.bytecode)

        if selectors and len(selectors) >= 0:
            print_ok("✅ Function selectors found:")
            for selector in selectors:
                print("\t-> ", selector)

            for _, contract in datastore.contracts.items():
                if contract.bytecode == bytecode.bytecode:
                    print_info("Updating contract in datastore...")
                    datastore.update_contract(contract.address, new_selectors=selectors)
        else:
            print_error("❌ No function selectors found")
