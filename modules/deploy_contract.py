from termcolor import colored, cprint
from module import Module
from printib import *
import os
from web3 import Web3
from solcx import *
from connect import Connect
from datastore import DataStore


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Deploy contract module",
                       "Description": "This module compiles a contract (solidity) and deploys it on a blockchain. You need private key, public address and chain_id.",
                       "Author": "@pablogonzalezpe"}

        # -----------name-----default_value--description--required?
        options = {"contract": [None, "Contract path in order to compile", True],
                   "address": [None, "Public address", True],
                   "pkey": [None, "Private key", True],
                   "show_bytecode": ["true", "Show bytecode value", True],
                   "show_opcode": ["true", "Show opcodes value", True],
                   "show_abi": ["true", "Show ABI value", True],
                   "compiler_version": ["0.8.4", "Solidity version", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # This module must be always implemented, it is called by the run option

    def run_module(self):

       # read contract path

        if self.args["show_bytecode"] in ["true", "false"] and self.args["show_bytecode"] == "true":
            show_bytecode = True
        elif self.args["show_bytecode"] in ["true", "false"] and self.args["show_bytecode"] == "false":
            show_bytecode = False
        else:
            print_error(
                "The value in show_bytecode is not correct (by default set to true)")
            show_bytecode = True

        if self.args["show_opcode"] in ["true", "false"] and self.args["show_opcode"] == "true":
            show_opcode = True
        elif self.args["show_opcode"] in ["true", "false"] and self.args["show_opcode"] == "false":
            show_opcode = False
        else:
            print_error(
                "The value in show_opcode is not correct (by default set to true)")
            show_opcode = True

        if self.args["show_abi"] in ["true", "false"] and self.args["show_abi"] == "true":
            show_abi = True
        elif self.args["show_abi"] in ["true", "false"] and self.args["show_abi"] == "false":
            show_abi = False
        else:
            print_error(
                "The value in show_abi is not correct (by default set to true)")
            show_abi = True

        if os.path.exists(self.args["contract"]) and str(self.args["contract"]).endswith('.sol'):
            with open(self.args["contract"], "r") as c:
                contract_content = c.read()

        install_solc(self.args["compiler_version"])

        print_info("compilating contract...")

        compiled = compile_standard(
            {
                "language": "Solidity",
                "sources": {self.args["contract"]: {"content": contract_content}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": [
                                "metadata",
                                "abi",
                                "evm.bytecode",
                                # "evm.bytecode.sourceMap",
                            ]
                        }
                    }
                },
            },
            solc_version=self.args["compiler_version"],
        )

        k = list(compiled["contracts"][self.args["contract"]].keys())
        bytecode = compiled["contracts"][self.args["contract"]
                                         ][k[0]]["evm"]["bytecode"]["object"]
        opcode = compiled["contracts"][self.args["contract"]
                                       ][k[0]]["evm"]["bytecode"]["opcodes"]
        abi = compiled["contracts"][self.args["contract"]][k[0]]["abi"]

        if show_bytecode:
            print_ok("")
            print_ok("bytecode generated")
            print_info(bytecode)

        if show_opcode:
            print_ok("")
            print_ok("opcodes generated")
            print_info(opcode)

        if show_abi:
            print_ok("")
            print_ok("ABI generated")
            print_info(abi)

        # deploy contract
        print_info("Deploying contract...")
        contract_address = Connect.get_instance().deploy_contract(
            abi, bytecode, opcode, self.args["address"], self.args["pkey"])
        #name = DataStore.get_instance().random_name()
        if not DataStore.get_instance().is_key("contract", self.args['contract']):
            DataStore.get_instance().create_name(
                "contract", self.args['contract'])
            DataStore.get_instance().add_value(
                "contract", self.args['contract'], 'address', contract_address)
            DataStore.get_instance().add_value(
                "contract", self.args['contract'], 'abi', abi)
            DataStore.get_instance().add_value(
                "contract", self.args['contract'], 'opcode', opcode)
            DataStore.get_instance().add_value(
                "contract", self.args['contract'], 'bytecode', bytecode)
            DataStore.get_instance().add_value(
                "contract", self.args['contract'], 'source', self.args['contract'])
            DataStore.get_instance().add_value(
                "contract", self.args['contract'], 'source_content', contract_content)

        if not DataStore.get_instance().is_key("wallet", self.args['contract']):
            DataStore.get_instance().create_name(
                "wallet", self.args['contract'])
            DataStore.get_instance().add_value(
                "wallet", self.args['contract'], 'address', self.args['address'])
            DataStore.get_instance().add_value(
                "wallet", self.args['contract'], 'pkey', self.args['pkey'])

        #super(CustomModule, self).run(t=thread1)
