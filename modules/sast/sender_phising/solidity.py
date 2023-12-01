from printib import *
from module import Module
from lib.contract_solidity import Solidity_Contract
from lib.vulnerabilities.sender_phising import Sender_Phising
from modules.utils import count_till_line, get_solidity_contract


class CustomModule(Module):
    """
    Module to detect the vulnerability: Sender phising control
    See lib.vulnerabilities.sender_phising for more info
    """

    def __init__(self):
        information = {"Name": "Sender Phising Solidity check",
                       "Description": Sender_Phising.info, "Author": "@chgara"}

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
        Check the contract in search of tx.origin
        :param contract: The solidity smart contract
        """
        phising_vuln = Sender_Phising()
        print(phising_vuln)
        for statement in contract.code:
            if "tx.origin" in statement:
                line_num = count_till_line(statement, contract)
                phising_vuln.add_description(
                    f"    found in line {line_num} of contract {contract.name}"
                )
                phising_vuln.add_code(f"    {statement}")
                phising_vuln.print_vulnerability()
                return
        print_ok("✅ tx.origin phising not found, all ok")

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
