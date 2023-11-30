#from asyncio.windows_events import NULL
from socket import create_connection
from termcolor import colored, cprint
import sys
from web3 import Web3
from printib import *


class Connect:
    __instance = None

    @staticmethod
    def get_instance():
        if Connect.__instance == None:
            Connect()
        return Connect.__instance

    def __init__(self):
        if Connect.__instance == None:
            Connect.__instance = self
            self.variables = {}
            self.w3 = None
    
    def add_connection(self, values={}):
        for k,v in values.items():
            self.variables[k] = v
        self.create_connection()

    def create_connection(self):
        if self.w3 == None:
            connection = self.variables["provider"] + ":" + self.variables["port"]
            self.w3 = Web3(Web3.HTTPProvider(connection))
            if self.w3.isConnected():
                print("Connection created with Blockchain")
            else:
                print("Connection error")
                self.del_connection()
        else:
            print("Connection already exists")
    
    def has_connection(self):
        return self.w3 != None
            
    def del_connection(self):
        self.w3 = None
        self.variables = {}

    def deploy_contract(self,abi,bytecode,opcode,address,pkey):
        if self.has_connection():
            contract = self.w3.eth.contract(abi=abi,opcodes=opcode,bytecode=bytecode)
            nonce = self.w3.eth.getTransactionCount(address)
            gas_price = self.w3.eth.gas_price
            params_transaction = {"from":address,"nonce":nonce,"gasPrice":gas_price,"chainId":int(self.variables["chainid"])}
            transaction = contract.constructor().build_transaction(params_transaction)
            #sign transaction
            signed = self.w3.eth.account.sign_transaction(transaction, private_key=pkey)
            hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(hash)
            print_info("Contract deployed!")
            print_info("Contract Address: {}".format(receipt.contractAddress))
            return receipt.contractAddress
        else:
            return {"No connection to blockchain"}

    def get_bytecode(self,address):
        if self.has_connection():
            address = Web3.toChecksumAddress(address)
            bytecode = self.w3.eth.get_code(address).hex()
            return bytecode
        else:
            print_error("No connection to blockchain")

    def get_variables(self):
        return self.variables
    
    def show_variables(self):
        cprint(" Connection data on Blockchain",'yellow')
        print (" -----------------------------")
        flag = 0
        for key, value in self.variables.items():
            flag += 1
            if flag > 1:
                print (" |")
            sys.stdout.write(" |_")
            sys.stdout.write("%s" % key)
            sys.stdout.write(" = %s \n" % (value))
        print("")