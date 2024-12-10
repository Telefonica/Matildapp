import io
import os
import re
import json
from pathlib import Path
from packaging.specifiers import SpecifierSet

import solcx
from rich import print
from rich.tree import Tree
from solidity_parser import parser
from pyevmasm import disassemble_hex

from console import print_error, print_info, print_ok
from module import Module

PLUS_SIGN = "[[bold green]+[/bold green]]"
EXCL_SIGN = "[[bold red]![/bold red]]"


class CustomModule(Module):
    def __init__(self):
        information = {
            "Name": "Get information about a contract",
            "Description": "This module get information about a contract (solidity).",
            "Author": "@toolsprods",
        }

        # -----------name-----default_value--description--required?
        options = {
            "contract": [None, "Contract path in order to get info", True],
            "show_code": ["true", "Show code", True],
            "show_abi": ["false", "Show ABI value", True],
            "show_bytecode": ["false", "Show bytecode value", True],
            "show_opcodes": ["false", "Show opcodes value", True],
        }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # This module must be always implemented, it is called by the run option

    def validate_options(self):
        contract_path = Path(self.args["contract"])

        if not os.path.isfile(contract_path):
            print_error(f'Error: File {self.args["contract"]} does not exist')
            return False

        if not os.path.basename(contract_path).endswith(".sol"):
            print_error(f'Error: File {self.args["contract"]} is not a Solidity file')
            return False

        return True

    def version_installed(self, version):
        versions = solcx.get_installed_solc_versions()
        for v in versions:
            if version == str(v):
                return True
        return False

    def get_compiler_version(self, sourceUnitObject):
        pragmas = []
        for pragma in sourceUnitObject.pragmas:
            pragmas.append(pragma.value)
        return pragmas

    def get_contracts_name(self, sourceUnitObject):
        return sourceUnitObject.contracts.keys()

    def get_contract_functions(self, sourceUnitObject, contractName):
        return sourceUnitObject.contracts[contractName].functions.keys()

    # def get_info(self, contract, code=False, abi=False, bytecode=False, opcodes=False):
    #     info = {}

    #     info[contract.get_name()] = {
    #         "pragma": contract.get_pragma(),
    #     }

    #     functions = contract.get_functions().keys()
    #     if functions:
    #         info[contract.get_name()]["functions"] = {}

    #         for function in functions:
    #             info[contract.get_name()]["functions"][function] = {
    #                 "visibility": contract.get_visibility(function),
    #             }

    #             modifiers = contract.get_modifiers(function)
    #             if modifiers:
    #                 info[contract.get_name()]["functions"][function]["modifiers"] = []
    #                 for modifier in modifiers:
    #                     info[contract.get_name()]["functions"][function]["modifiers"].append(modifier.name)

    #     if code:
    #         try:
    #             info[contract.get_name()]["code"] = contract.get_original()
    #         except Exception as e:
    #             info[contract.get_name()]["code"] = None

    #     if abi:
    #         try:
    #             info[contract.get_name()]["abi"] = contract.get_abi()
    #         except Exception as e:
    #             info[contract.get_name()]["abi"] = None

    #     if bytecode:
    #         try:
    #             info[contract.get_name()]["bytecode"] = contract.get_bytecode()
    #         except Exception as e:
    #             info[contract.get_name()]["bytecode"] = None

    #     if opcodes:
    #         try:
    #             info[contract.get_name()]["opcodes"] = contract.get_opcodes()
    #         except Exception as e:
    #             info[contract.get_name()]["opcodes"] = None

    #     return info

    # TODO: Move this function to a utils file
    def get_content_between_positions(self, contract, positions, file=True):
        start_line = positions["start"]["line"]
        start_column = positions["start"]["column"]
        end_line = positions["end"]["line"]
        end_column = positions["end"]["column"]

        if file:
            with open(contract, "r") as file:
                lines = file.readlines()
        else:
            buf = io.StringIO(contract)
            lines = buf.readlines()

        content = ""
        for line_number, line in enumerate(lines, 1):
            if start_line <= line_number <= end_line:
                if line_number == start_line:
                    content += line[start_column:]
                elif line_number == end_line:
                    content += line[: end_column + 1]
                else:
                    content += line

        return content, start_line

    # TODO: Move this function to a utils file
    # Adapted from py-solc-x/solcx/install.py
    def select_pragma_version(self, pragma_string: str, version_list):
        """
        Get a matching version from the given pragma string and a version list.

        Args:
            pragma_string (str): A pragma str.
            version_list (List[Version]): A list of valid versions.

        Returns:
            Optional[Version]: A selected version from the given list.
        """

        comparator_set_range = pragma_string.replace(" ", "").split("||")
        comparator_regex = re.compile(r"(([<>]?=?|\^)\d+\.\d+\.\d+)")
        version = None

        def _as_spec(item: str) -> str:
            ret = item.replace("^", "~=")

            if ret and ret[0].isnumeric():
                return f"=={ret}"

            elif ret and len(ret) >= 2 and ret[0] == "=" and ret[1] != "=":
                return f"={ret}"

            return ret

        for comparator_set in comparator_set_range:
            specs = ",".join([_as_spec(i[0]) for i in comparator_regex.findall(comparator_set)])
            spec = SpecifierSet(specs)
            matching = sorted(list(spec.filter(version_list)), reverse=True)
            selected = matching[0] if matching else None
            if selected and (not version or version < selected):
                version = selected

        return version

    def run_module(self):
        if self.args["show_code"] in ["true", "false"] and self.args["show_code"] == "true":
            show_code = True
        elif self.args["show_code"] in ["true", "false"] and self.args["show_code"] == "false":
            show_code = False
        else:
            print_error("The value in show_code is not correct (by default set to true)")
            show_code = True

        if self.args["show_abi"] in ["true", "false"] and self.args["show_abi"] == "true":
            show_abi = True
        elif self.args["show_abi"] in ["true", "false"] and self.args["show_abi"] == "false":
            show_abi = False
        else:
            print_error("The value in show_abi is not correct (by default set to true)")
            show_abi = True

        if self.args["show_bytecode"] in ["true", "false"] and self.args["show_bytecode"] == "true":
            show_bytecode = True
        elif self.args["show_bytecode"] in ["true", "false"] and self.args["show_bytecode"] == "false":
            show_bytecode = False
        else:
            print_error("The value in show_bytecode is not correct (by default set to true)")
            show_bytecode = True

        if self.args["show_opcodes"] in ["true", "false"] and self.args["show_opcodes"] == "true":
            show_opcodes = True
        elif self.args["show_opcodes"] in ["true", "false"] and self.args["show_opcodes"] == "false":
            show_opcodes = False
        else:
            print_error("The value in show_opcode is not correct (by default set to true)")
            show_opcodes = True

        if not self.validate_options():
            return

        contracts = []

        print_ok("Solidity file detected")

        try:
            sourceUnit = parser.parse_file(self.args["contract"], loc=True)
        except Exception as e:
            print_error(e)
            print_error("Error parsing sourceUnit")
            return

        sourceUnitObject = parser.objectify(sourceUnit)

        pragmas = self.get_compiler_version(sourceUnitObject)[0]
        contracts_name = self.get_contracts_name(sourceUnitObject)
        compiled_source = None

        try:
            all_versions = solcx.get_installable_solc_versions()
            ver = str(self.select_pragma_version(pragmas, all_versions))
            print_info(f"{ver} compiler version detected from pragma: {pragmas}")
        except Exception as e:
            print_error(f"Error getting version from pragma: {pragmas}")

        if self.version_installed(ver):
            print_ok(f"Version {ver} is installed!")
        else:
            print_error(f"Version {ver} is not installed...")
            print_info(f"Installing version {ver}")
            solcx.install_solc(version=ver, show_progress=True, solcx_binary_path=None)

        try:
            print_info("Compiling contract...")
            compiled_source = solcx.compile_files(
                [self.args["contract"]],
                output_values=["abi", "bin-runtime"],
                solc_version=ver,
                import_remappings=[
                    f'@openzeppelin/contracts/={os.path.join(Path().resolve(), "lib/openzeppelin/contracts/")}'
                ],
            )
            print_ok("Compiled done!")
        except Exception as e:
            print(e)
            print_error("Error compiling source")
        finally:
            print("")
        # END COMPILE CONTRACT

        # PARSE CONTRACT
        for contract in contracts_name:
            raw_code = self.get_content_between_positions(
                self.args["contract"], sourceUnitObject.contracts[contract]._node.loc, file=True
            )[0]
            functions = sourceUnitObject.contracts[contract].functions
            if compiled_source:
                abi = compiled_source[f'{self.args["contract"]}:{contract}']["abi"]
                bytecode = compiled_source[f'{self.args["contract"]}:{contract}']["bin-runtime"]
            else:
                abi = None
                bytecode = None
            contracts.append(
                {
                    "contract": contract,
                    "pragmas": pragmas,
                    "code": raw_code,
                    "abi": abi,
                    "bytecode": bytecode,
                    "functions": functions,
                }
            )
        # END PARSE CONTRACT

        try:
            tree = Tree("[bold]Information about contracts[/bold]")
            for contract in contracts:
                contract_tree = tree.add(f'{PLUS_SIGN} [bold]Contract:[/bold] {contract.get("contract")}')
                contract_tree.add(f'{PLUS_SIGN} [bold]Pragma:[/bold] {contract.get("pragmas")}')
                functions_tree = contract_tree.add(f"{PLUS_SIGN} [bold]Functions:[/bold]")
                for function, fdata in contract.get("functions").items():
                    function_tree = functions_tree.add(f"{PLUS_SIGN} [bold]{function}[/bold]")
                    function_tree.add(f"{PLUS_SIGN} Visibility: {fdata.visibility}")
                    try:
                        for modifier in fdata.modifiers:
                            function_tree.add(f"{PLUS_SIGN} Modifier: {modifier}")
                    except Exception as e:
                        pass
                if show_code:
                    contract_tree.add(f'{PLUS_SIGN} [bold]Code:[/bold]\n{contract.get("code")}')
                if show_abi:
                    contract_tree.add(f'{PLUS_SIGN} [bold]ABI:[/bold]\n{json.dumps(contract.get("abi"), indent=2)}')
                if show_bytecode:
                    contract_tree.add(f'{PLUS_SIGN} [bold]Bytecode:[/bold]\n{contract.get("bytecode")}')
                if show_opcodes:
                    contract_tree.add(f'{PLUS_SIGN} [bold]Opcodes:[/bold]\n{disassemble_hex(contract.get("bytecode"))}')

                print(tree)
        except Exception as e:
            print(e)
            print(f"{EXCL_SIGN} Error getting contract info")

    # super(CustomModule, self).run(t=thread1)
