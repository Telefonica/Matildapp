from printib import *
from module import Module
from lib.contract_solidity import Solidity_Contract
from modules.utils import count_till_line, get_solidity_contract
from lib.vulnerabilities.rigth_to_left_override_character import Right_To_Left_Override_Character


class CustomModule(Module):
    """
    Module to detect the scam: Right to left override character
    For more info about the vulnerability/scam you can see in the file:
          lib.vulnerabilities.rigth_to_left_override_character
    """
    # TODO

    def __init__(self):
        information = {"Name": "Rigth to left override Solidity check",
                       "Description": Right_To_Left_Override_Character.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"contract": [
            None, "Contract path, should be a solidity file", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: Solidity_Contract) -> None:
        """
        Check the contract
        :param contract: The solidity smart contract
        Detection cases: (Solidity only)
            1. The contract has present the (U+202E) character
            Final conlusion: 1
        """
        vulnerability = Right_To_Left_Override_Character()
        for line in contract.code:
            if "\u202E" in line:
                line_number = count_till_line(line, contract)
                vulnerability.add_code(f"Line {line_number}: {line}")
                vulnerability.print_vulnerability()
        print_ok("✅ Not vulnerable to Right to left override character")

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
