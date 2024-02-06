
from tkinter import E
from termcolor import colored, cprint
import sys
from printib import *
import random
from config import Config
import json
import os

'''class Contract:
    def __init__(self,name=None,address=None,abi=None,opcode=None,bytecode=None,source=None,source_content=None):
        self.contract = {}
        self.contract['name'] = name
        self.contract['address'] = address
        self.contract['abi'] = abi 
        self.contract['opcode'] = opcode
        self.contract['bytecode'] = bytecode
        self.contract['source'] = source
        self.contract['source_content'] = source_content


class Wallet:
    def __init__(self,name=None,address=None,pkey=None,phrase=None):
        self.wallet = {}
        self.wallet['name'] = name
        self.wallet['address'] = address
        self.wallet['pkey'] = pkey
        self.wallet['phrase'] = phrase'''


class DataStore:
    __instance = None

    @staticmethod
    def get_instance():
        if DataStore.__instance == None:
            DataStore()
        return DataStore.__instance

    def __init__(self):
        if DataStore.__instance == None:
            DataStore.__instance = self
            self.contracts = {}
            self.wallet = {}

    def show(self, type):
        if type == "contract":
            print_info("")
            print_info("Contract structure list")
            print_info("=======================")
            print_info("")
            for key in self.contracts.keys():
                print_info("Contract: {}".format(key))

        if type == "wallet":
            print_info("")
            print_info("Wallet structure list")
            print_info("=======================")
            print_info("")
            for key in self.wallet.keys():
                print_info("Wallet: {}".format(key))

    def show_name(self, type, name):
        if type == "contract" and name in self.contracts.keys():
            print_info(self.contracts[name])
        elif type == "wallet" and name in self.wallet.keys():
            print_info(self.wallet[name])
        else:
            print_error("{} name not found!".format(type))

    def show_param(self, type, name, param):
        if type == "contract" and name in self.contracts.keys() and param in self.contracts[name].keys():
            print_info(self.contracts[name][param])
        elif type == "wallet" and name in self.wallet.keys() and param in self.wallet[name].keys():
            print_info(self.wallet[name][param])
        else:
            print_error("{} name not found!".format(type))

    def get_param(self, type, name, param):
        if type == "contract" and name in self.contracts.keys() and param in self.contracts[name].keys():
            return self.contracts[name][param]
        elif type == "wallet" and name in self.wallet.keys() and param in self.wallet[name].keys():
            return self.wallet[name][param]
        else:
            return "{} name not found!".format(type)

    def create_name(self, type, name):
        if type == "contract" and not name in self.contracts.keys():
            self.contracts[name] = {'address':'','abi':'','opcode':'','bytecode':'','source':'','source_content':''}
            print_ok("contract structure created")
        if type == "wallet" and not name in self.wallet.keys():
            self.wallet[name] = {'address':'','pkey':'','phrase':''}
            print_ok("wallet structure created")

    def delete_name(self, type, name):
        if type == "contract" and name in self.contracts.keys():
            self.contracts.pop(name)
            print_ok("contract structure deleted")
        if type == "wallet" and name in self.wallet.keys():
            self.wallet.pop(name)
            print_ok("wallet structure deleted")

    def add_value(self, type, name, param, value):
        if type == "contract" and name in self.contracts.keys() and param in self.contracts[name].keys():
            self.contracts[name][param] = value
            print_ok("param {} value added to {} contract structure".format(param,name))
        if type == "wallet" and name in self.wallet.keys() and param in self.wallet[name].keys():
            self.wallet[name][param] = value
            print_ok("param {} value added to {} wallet structure".format(param,name))

    def del_value(self, type, name, param):
        if type == "contract" and name in self.contracts.keys() and param in self.contracts[name].keys():
            self.contracts[name][param] = ''
            print_ok("param {} value deleted on {} contract structure".format(param,name))
        if type == "wallet" and name in self.wallet.keys() and param in self.wallet[name].keys():
            self.wallet[name][param] = ''
            print_ok("param {} value deleted on {} wallet structure".format(param,name))

    def mod_value(self, type, name, param, value):
        if type == "contract" and name in self.contracts.keys() and param in self.contracts[name].keys():
            self.contracts[name][param] = value
            print_ok("param {} value modified on {} contract structure".format(param,name))
        if type == "wallet" and name in self.wallet.keys() and param in self.wallet[name].keys():
            self.wallet[name][param] = value
            print_ok("param {} value modified on {} wallet structure".format(param,name))

    def change_name(self,type,name,new_name):
        if type == "contract" and name in self.contracts.keys():
            self.contracts[new_name] = self.contracts[name]
            del(self.contracts[name])
            print_ok("Contract name changed")
        if type == "wallet" and name in self.wallet.keys():
            self.wallet[new_name] = self.wallet[name]
            del(self.wallet[name])
            print_ok("Wallet name changed")
        
    def is_valid_set(self,type,name,param):
        if type == "contract":
            return type == "contract" and name in self.contracts.keys() and param in self.contracts[name].keys()
        if type == "wallet":
            return type == "wallet" and name in self.wallet.keys() and param in self.wallet[name].keys()
        return False

    def is_key(self, type, key):
        if type == "contract":
            return key in self.contracts.keys()
        if type == "wallet":
            return key in self.wallet.keys()
        else:
            return False

    def random_name(self):
        key = "P"
        rand = random.randrange(0, 9999999)
        key = key + str(rand)
        return key

    def save(self):
        config = Config.get_instance().get_config()
        if not os.path.exists(config['datastore_path']):
            os.makedirs(config['datastore_path'])
        filepath = config['datastore_path'] + config['datastore_filename_contracts']
        filepath2 = config['datastore_path'] + config['datastore_filename_wallets']
        with open(filepath,"w") as outfile:
            json.dump(self.contracts,outfile)
            print_ok("datastore (contracts) saved")
        with open(filepath2,"w") as outfile2:
            json.dump(self.wallet,outfile2)
            print_ok("datastore (wallets) saved")
        
    def read_file_contracts_datastore(self):
        config = Config.get_instance().get_config()
        filepath = config['datastore_path'] + config['datastore_filename_contracts']
        with open(filepath) as c:
            self.contracts = json.load(c)
            print("datastore (contracts) read")

    def read_file_wallets_datastore(self):
        config = Config.get_instance().get_config()
        filepath = config['datastore_path'] + config['datastore_filename_wallets']
        with open(filepath) as c:
            self.wallet = json.load(c)
            print("datastore (wallets) read")

        
    def help(self):
        print_info("")
        print_info("Datastore help")
        print_info("")
        print_info("")
        print_info(
            "Usage: datastore <option> <action> <name contract | wallet> [<param> <value>]")
        print_info("")
        print_info("Options:")
        print_info("")
        print_info("contract - Manage your (smart) contracts")
        print_info("wallet - Manage your wallets")
        print_info("")
        print_info("Actions:")
        print_info("")
        print_info("create - create your [contract | wallet] info - Ex: datastore contract create <name>")
        print_info("delete - delete your [contract | wallet] info - Ex: datastore contract delete <name>")
        print_info("show - show your [contract | wallet] info - Ex: datastore contract show [contract_name]")
        print_info("name - modify name [contract | wallet] - Ex: datastore contract name <old_name> <new_name>")
        print_info("add - add info about [contract | wallet] - Ex: datastore contract add <contract_name> <param_name> <value>")
        print_info("del - delete info about [contract | wallet] - Ex: datastore contract del <contract_name> <param_name>")
        print_info("mod - modify info about [contract | wallet] - Ex: datastore contract mod <contract_name> <param_name> <value>")
        print_info("set - set value on module params (fast link) - Ex: datastore contract set <contract_name> <param_module_name> <param_name> (only with module loaded)")
        print_info("save - save your datastore info on filesystem - Ex: datastore save")
        print_info("")
        
    def show_variables(self):
        cprint(" Connection data on Blockchain", 'yellow')
        print(" -----------------------------")
        flag = 0
        for key, value in self.variables.items():
            flag += 1
            if flag > 1:
                print(" |")
            sys.stdout.write(" |_")
            sys.stdout.write("%s" % key)
            sys.stdout.write(" = %s \n" % (value))
        print("")

