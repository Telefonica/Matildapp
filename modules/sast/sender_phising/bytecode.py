from printib import *
from module import Module
from lib.bytecode_contract import ByteCode_Contract
from modules.utils import count_till_line, get_bytecode_from_path
from lib.vulnerabilities.sender_phising import Sender_Phising


class CustomModule(Module):
    """
    Module to detect the vulnerability: Sender phising control
    See lib.vulnerabilities.sender_phising for more info
    """

    def __init__(self):
        information = {"Name": "Sender Phising Bytecode check",
                       "Description": Sender_Phising.info,
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
        phising_vuln = Sender_Phising()
        for instruction in contract.opcodes:
            if "ORIGIN" in instruction:
                position = count_till_line(instruction, contract)
                phising_vuln.add_code(
                    f"Found ORIGIN opcode in position {position}")
                phising_vuln.print_vulnerability()
                return

        print_ok("✅ tx.origin phising not found, all ok")

    def run_module(self) -> None:
        contract = get_bytecode_from_path(self.args)
        return self.check_contract(contract) if contract else None
