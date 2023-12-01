from printib import *
from module import Module
from modules.utils import get_solidity_contract
from lib.contract_solidity import Solidity_Contract
from lib.vulnerabilities.timestamp_dependence import Timestamp_Dependence


class CustomModule(Module):
    """
    Module to detect the vulnerability: Timestamp Dependence
    See lib.vulnerabilities.timestamp_dependence for more info
    """

    def __init__(self):
        information = {"Name": "Timestamp Manipulation Solidity check",
                       "Description": Timestamp_Dependence.info,
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
        """
        timestamp_vulnerability = Timestamp_Dependence()
        for statement in contract.code:
            if "block.timestamp" in statement:
                timestamp_vulnerability.print_vulnerability()
                return
        print_ok("✅ Not vulnerable to 15sec timestamp manipulation, al ok")

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
