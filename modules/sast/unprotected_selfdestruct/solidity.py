from printib import *
from module import Module
from lib.contract import Contract_Parameter, evm_var_types
from lib.contract_solidity import Solidity_Contract, Solidity_Function
from modules.utils import count_till_line, get_solidity_contract
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
        # TODO: refactor this, and change how it works
        vuln = Unprotected_Selfdestruct()
        for f in contract.functions:
            if not "public" in f.access_modifiers and not "external" in f.access_modifiers:
                continue
            for statement in f.code:
                if not "selfdestruct(" in statement:
                    continue
                line_num = count_till_line(statement, contract)
                vuln.add_description(
                    f"Found in function {f.selector} and line {line_num}")
                vuln.add_code(statement)
                vuln.print_vulnerability()
                return
        print_ok("✅ Not vulnerable to selfdestruct, al ok")

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
