from printib import *
from module import Module
from modules.utils import get_bytecode_from_address, get_bytecode_from_path
from lib.bytecode_contract import ByteCode_Contract
from lib.vulnerabilities.unprotected_selfdestruct import Unprotected_Selfdestruct


class CustomModule(Module):
    """
    Module to detect the vulnerability: Unprotected Selfdestruct
    See lib.vulnerabilities.unprotected_selfdestruct for more info
    """

    def __init__(self):
        information = {"Name": "Unprotected Selfdestruct Solidity check",
                       "Description": Unprotected_Selfdestruct.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"address": [
            None, "Address of the deployed Smart Contract", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: ByteCode_Contract) -> None:
        """
        Check the contract
        :param contract: The solidity smart contract
        """
        vuln = Unprotected_Selfdestruct("potentially")
        # TODO: add more control to this
        for instruction in contract.opcodes:
            if "SELFDESTRUCT" in instruction:
                vuln.print_vulnerability()
                return
        print_ok("✅ Not vulnerable to selfdestruct, al ok")

    def run_module(self) -> None:
        contract = get_bytecode_from_address(self.args)
        return self.check_contract(contract) if contract else None
