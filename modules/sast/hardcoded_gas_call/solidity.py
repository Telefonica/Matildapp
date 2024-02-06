from printib import *
from module import Module
from lib.contract_solidity import Solidity_Contract
from modules.utils import count_till_line, get_solidity_contract
from lib.vulnerabilities.hardcoded_gas_call import Hardcoded_Gas_Call


class CustomModule(Module):
    """
    Module to detect the vulnerability: Hardcoded Gas Call
    See lib.vulnerabilities.hardcoded_gas_call for more info
    """

    def __init__(self):
        information = {"Name": "Hardcoded Gas call Solidity check",
                       "Description": Hardcoded_Gas_Call.info,
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

        Detection cases:
            1. transfer() used in the smart contract
            2. send() used in the smart contract
            3. call() used in the smart contract with hardcoded gas amount
            4. (For bytecode you can see the module implementation)
            Final conlcusion: 1 or 2 or 3
        """
        found: bool = False
        hardcoded_gas_call = Hardcoded_Gas_Call()
        # TODO: refactor this
        for statement in contract.code:
            if ".send(" in statement:
                found = True
                line_num = count_till_line(statement, contract)
                hardcoded_gas_call.add_description(
                    f"Found send() in line {line_num} of contract {contract.name}"
                )
                hardcoded_gas_call.add_code(f"    {statement}")
            if ".transfer(" in statement:
                found = True
                line_num = count_till_line(statement, contract)
                hardcoded_gas_call.add_description(
                    f"Found transfer() in line {line_num} of contract {contract.name}"
                )
                hardcoded_gas_call.add_code(f"    {statement}")
            if ".call" in statement and ".gas(" in statement:
                # TODO: add check to expect a not variable inside the gas()
                found = True
                line_num = count_till_line(statement, contract)
                hardcoded_gas_call.add_description(
                    f"Found .call.gas() in line {line_num} of contract {contract.name}")
                hardcoded_gas_call.add_code(f"    {statement}")

            if ".call{" in statement and "gas:" in statement:
                # TODO: add check to expect a not variable inside the gas()
                found = True
                line_num = count_till_line(statement, contract)
                hardcoded_gas_call.add_description(
                    f"Found .call{'{gas:limit}'} in line {line_num} of contract {contract.name}")
                hardcoded_gas_call.add_code(f"    {statement}")

        if found:
            hardcoded_gas_call.add_description(
                "Remove the use of send(), transfer() and .call.gas()")
            hardcoded_gas_call.print_vulnerability()
            return
        print_ok("✅ Not vulnerable to hardcoded gas call denegation, al ok")

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
