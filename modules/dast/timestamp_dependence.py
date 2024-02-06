from printib import *
from module import Module
from lib.bytecode_contract import ByteCode_Contract
from modules.utils import get_bytecode_from_address
from lib.vulnerabilities.timestamp_dependence import Timestamp_Dependence


class CustomModule(Module):
    """
    Module to detect the vulnerability: Timestamp Dependence on bytecode
    See lib.vulnerabilities.timestamp_dependence for more info
    """

    def __init__(self):
        information = {"Name": "Deployed contract timestamp manipulation check",
                       "Description": Timestamp_Dependence.info,
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
        Check the contract depending on the pragma version
        :param contract: The bytecode smart contract
        """
        timestamp_vulnerability = Timestamp_Dependence()
        for instruction in contract.opcodes:
            if "TIMESTAMP" in instruction:
                timestamp_vulnerability.print_vulnerability()
                return
        print_ok("✅ Not vulnerable to 15sec timestamp manipulation, al ok")

    def run_module(self) -> None:
        bytecode: (ByteCode_Contract | None) =\
            get_bytecode_from_address(self.args)
        return self.check_contract(bytecode) if bytecode else None
