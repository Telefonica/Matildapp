from printib import *
from module import Module
from modules.utils import get_bytecode_from_path
from lib.bytecode_contract import ByteCode_Contract
from lib.vulnerabilities.timestamp_dependence import Timestamp_Dependence


class CustomModule(Module):
    """
    Module to detect the vulnerability: Timestamp Dependence on bytecode
    See lib.vulnerabilities.timestamp_dependence for more info
    """

    def __init__(self):
        information = {"Name": "Timestamp manipulation Bytecode Check",
                       "Description": Timestamp_Dependence.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"bytecode": [
            None, "Bytecode or path to .txt containing the bytecode", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: ByteCode_Contract) -> None:
        """
        Check the contract
        :param contract: The bytecode smart contract
        """
        timestamp_vulnerability = Timestamp_Dependence()
        for instruction in contract.opcodes:
            if "TIMESTAMP" in instruction:
                timestamp_vulnerability.print_vulnerability()
                return
        print_ok("✅ Not vulnerable to 15sec timestamp manipulation, al ok")

    def run_module(self) -> None:
        contract = get_bytecode_from_path(self.args)
        return self.check_contract(contract) if contract else None
