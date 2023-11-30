from module import Module
from printib import * 
import os
from connect import Connect
from datastore import DataStore
from lib.contract_solidity import Solidity_Contract


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "NAME HERE",
                       "Description": "DESCRIPTION HERE",
                       "Author": "AUTHOR HERE"}

        # -----------name-----default_value--description--required?
        options = {"contract": [None, "Contract path DESCRIPTION", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None


    def checkContract(self,contract):
        """
        Check the contract depending on the pragma version
        :param version: The pragma version
        :param file_content: The file content

        If you want you can add more checks
        """
        pragma_version = contract.pragma_version

        vuln = False
        
        if ([int(x) for x in pragma_version] > [0, 4, 22]):
            for f in contract.functions:
                vuln = contract.name == f.selector
                if vuln:
                    print_error("Deprecated use of functions\n"+"  -> Version of compiler higher than 0.4.22\n"+"  -> Your contract is vulnerable to safeguarding constructor with care")
                    break   

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        if os.path.exists(self.args["contract"]) and str(self.args["contract"]).endswith('.sol'):
            with open(self.args["contract"],"r") as c:
                contract_content = c.read().splitlines()

            solidity_contract = Solidity_Contract(contract_content)
            self.checkContract(solidity_contract)

