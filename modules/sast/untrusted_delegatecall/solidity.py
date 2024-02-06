from printib import *
from module import Module
from lib.contract import Contract_Parameter, evm_var_types
from modules.utils import count_till_line, get_solidity_contract
from lib.contract_solidity import Solidity_Contract, Solidity_Function
from lib.vulnerabilities.untrusted_delegatecall import Untrusted_Delegatecall


class CustomModule(Module):
    """
    Module to detect the vulnerability: Untrusted Delegatecall
    See lib.vulnerabilities.untrusted_delegatecall for more info
    """

    def __init__(self):
        information = {"Name": "Untrusted delegate",
                       "Description": Untrusted_Delegatecall.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"contract": [None, "Contract path DESCRIPTION", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: Solidity_Contract) -> None:
        """
        Detection cases: Can occur when delegatecall is used without address "verification".
            1. Directly used address from parameter
            2. Saving in contract storage
            3. Validating in require of a function
            4. Validating in modifier of function
            5. Validating in if statement
            Final conlcusion: 1 && !2 && !3 && !4 && !5
        """
        unsafe_delegate_vuln = Untrusted_Delegatecall()

        # TODO add check_if_validated
        if self.first_check(contract, unsafe_delegate_vuln):
            unsafe_delegate_vuln.print_vulnerability()
        return

    def first_check(self, contract: Solidity_Contract, vuln: Untrusted_Delegatecall) -> bool:
        """
        Check if given from parameter address is used
        :param contract: Solidity_Contract object
        """
        # TODO: refactor how this works, can be done better
        found = False
        for f in contract.functions:
            if not "public" in f.access_modifiers and not "external" in f.access_modifiers:
                continue
            for statement in f.code:
                if not ".delegatecall(" in statement:
                    continue
                for p in f.parameters:
                    if not p.type == evm_var_types.ADDRESS:
                        continue
                    if p.name in statement:
                        line_num = count_till_line(statement, contract)
                        vuln.add_description(
                            f"Found in function {f.selector} and line {line_num}")
                        vuln.add_code(statement)
        return found

    def check_if_validated(self, func: Solidity_Function, parameter: Contract_Parameter) -> bool:
        """
        Check if the address is validated in a require or somewhere else
        :param contract: Solidity_Contract object
        """
        for modifier in func.access_modifiers:
            if parameter.name in modifier:
                return True
        for statement in func.code:
            if parameter.name in statement and not ".delegatecall(" in statement:
                if "require(" in statement or "if(" in statement:
                    return True
        return False

    def run_module(self):
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
