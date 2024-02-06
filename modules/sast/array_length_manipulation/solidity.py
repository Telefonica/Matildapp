from printib import *
from module import Module
from lib.contract_solidity import Solidity_Contract
from modules.utils import count_till_line, get_solidity_contract
from lib.vulnerabilities.array_length_manipulation import Array_Length_Manipulation


class CustomModule(Module):
    """
    Module to detect the vulnerability: Array Length Manipulation
    See lib.vulnerabilities.array_length_manipulation for more info
    """

    def __init__(self):
        information = {"Name": "Array Length manipulation Solidity check",
                       "Description": Array_Length_Manipulation.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"contract": [
            None, "Contract path, should be a solidity file", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # TODO: check if variable
    def check_contract(self, contract: Solidity_Contract) -> None:
        """
        Check the contract
        :param contract: The solidity smart contract

        Detection cases:
            1. Storage array exists
            2. array.length = value is used
            3. The value of 2. is a value easily manipulable
            4. Normal user have access to the   array
        Final conlcusion: 1. and 2. and 3. and 4.
        """
        arrays = [
            x.split("[]")[1].split(" ")[-1].strip(";")
            for x in contract.code if "[]" in x
        ]

        if len(arrays) == 0:
            return

        found = False
        length_manipultion = Array_Length_Manipulation()
        for line in contract.code:
            if not '.length=' in line.replace(" ", ""):
                continue
            if not line.split(".length")[0].split()[-1] in arrays:
                continue
            found = True
            line_num = count_till_line(line, contract)
            length_manipultion.add_code(
                f'{line_num}: {line.strip()}'
            )

        length_manipultion.print_vulnerability() if found else None

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        self.check_contract(contract) if contract else None
