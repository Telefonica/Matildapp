import time
from console import print_ok, print_error
from lib.bytecode_contract import ByteCode_Contract
from module import Module
from utils import get_bytecode_from_path, find_function_selectors, resolve_function_selector


class CustomModule(Module):
    """
    Module to resolve functions selectors in the bytecode (or from a list of function selectors)
    """

    def __init__(self):
        information = {
            "Name": "Resolve Function Selectors",
            "Description": """Once you have identified the function selectors in the bytecode of a contract,
     you can resolve them to human-readable function signatures. For this purpose, you can use the
     4bytes.directory API, which provides a database of function selectors and their corresponding
     function signatures. This module resolves function selectors to human-readable function signatures.
            """,
            "Author": "@jalvarezz13",
        }

        # -----------name-----default_value--description--required?
        options = {
            "bytecode": [None, "Bytecode, alias of the contract in the datastore or path to .txt containing the bytecode", True],
            "show_not_found": [
                None,
                "Show not found function selectors ('set show_not_found true' to enable. 'unset show_not_found' by default)",
                False,
            ],
        }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def run_module(self) -> None:
        function_selectors = []
        if isinstance(self.args["bytecode"], str):
            bytecode: ByteCode_Contract | None = get_bytecode_from_path(self.args)
            function_selectors = find_function_selectors(bytecode.bytecode)
        elif isinstance(self.args["bytecode"], list):
            function_selectors = self.args["bytecode"]
        else:
            print_error("❌ Not expected input")

        if len(function_selectors) == 0:
            print_error("❌ No function selectors found...")
        elif len(function_selectors) >= 1:
            print_ok("⚠️ Function selectors found. Resolving...")
            for selector in function_selectors:
                response = resolve_function_selector(selector)
                time.sleep(0.25)
                if len(response) == 1 and response[0] == "Not found" and self.args["show_not_found"]:
                    print_error(f"❌ Function selector {selector} not found")
                if len(response) >= 1 and response[0] != "Not found":
                    print_ok(f"✅ Function selector {selector} found")
                    for result in response:
                        print("\t-> ", result)
