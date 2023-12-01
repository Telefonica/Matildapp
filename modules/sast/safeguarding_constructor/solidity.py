from printib import *
from module import Module
from modules.utils import get_solidity_contract
from lib.contract_solidity import Solidity_Contract
from lib.vulnerabilities.safeguarding_constructor import Safeguading_Constructor


class CustomModule(Module):
    """
    Module to detect the vulnerability: Constructor safeguarding
    See lib.vulnerabilities.safeguarding_constructor for more info
    """

    def __init__(self):
        information = {"Name": "Constructor Safeguarding vulnerability check",
                       "Description": Safeguading_Constructor.info,

                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"contract": [None, "Contract path", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: Solidity_Contract) -> None:
        """
        Check the contract depending on the pragma version
        :param contract: Solidity_Contract object
        """
        pragma_version = contract.pragma_version
        safeguarding_vuln = Safeguading_Constructor()
        if ([int(x) for x in pragma_version] > [0, 4, 22]):
            for f in contract.functions:
                if contract.name == f.selector:
                    safeguarding_vuln.print_vulnerability()
                    break

    def run_module(self):
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
