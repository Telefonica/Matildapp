import os
from this import d
from tkinter import E
from complete import Completer
import signal
import argparse
import banners
from termcolor import cprint
from printib import *
from help import show_help
from connect import Connect
from datastore import DataStore
from config import Config
from session import Session
from pathlib import Path
from subprocess import Popen, PIPE
from pynput.keyboard import Controller
import threading
from setglobal import Global
#from jobs import Jobs
from time import sleep
try:
    import readline
    import rlcompleter
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except:
    pass


class Console:
    def console(self):

        # Configuring the commpleter
        self.comp = Completer(['load', 'set', 'unset', 'global', 'show', 'run',
                              'jobs', 'back', 'quit', 'help', 'connect', 'disconnect', 'datastore'])
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.comp.complete)

        # commands & functions
        self.switcher = {
            "load": self.load,
            "set": self.set,
            "unset": self.unset,
            "global": self.setglobal,
            "show": self.show,
            "run": self.run,
            # "jobs": self.jobs,
            "back": self.back,
            "quit": self.quit,
            "exit": self.quit,
            "help": self.help,
            "connect": self.connect,
            "disconnect": self.disconnect,
            "datastore": self.datastore,
        }

        print(banners.get_banner())
        cprint(' [+]', 'yellow', end='')
        print(' Starting the console...')
        cprint(' [*]', 'green', end='')
        print(' Console ready!\n')

        self.session = None

        while True:
            try:
                if self.session is None:
                    # /* Definitions available for use by readline clients. */
                    # define RL_PROMPT_START_IGNORE  '\001'
                    # define RL_PROMPT_END_IGNORE    '\002'
                    user_input = input(
                        '\001\033[1;32m\002sc $ > \001\033[0m\002').strip()
                else:
                    user_input = input('sc $ >[' +
                                       '\001\033[1;32m\002' +
                                       self.session.header() +
                                       '\001\033[0m\002' +
                                       ']> ').strip()

                if user_input == "":
                    continue
                else:
                    self.switch(user_input)
            except KeyboardInterrupt:
                signal.signal(signal.SIGINT, self.keyboard_interrupt_handler)
                print("")
            except Exception as e:
                print_error(e)

    def keyboard_interrupt_handler(self, signal, frame):
        print_error("Closing sc, Wait...")

    # Switcher

    def switch(self, u_input):
        try:
            if u_input.startswith("#"):
                self.execute_command(u_input[1:])
            else:
                u_input = u_input.split()
                if len(u_input) >= 2:
                    self.switcher.get(
                        u_input[0], self._command_error)(u_input[1:])
                else:
                    self.switcher.get(u_input[0], self._command_error)()
        except Exception as e:
            print_error(e)

    # Functions to check errors begin
    def _command_error(self):
        raise Exception('Command not found')

    def _raise_exception_specify(self, option):
        raise Exception("Specify %s" % (option))

    def _check_load_module(self):
        if not self.session:
            raise Exception('Please, load a module')

    def _check_set(self, user_input, op=2):
        self._check_load_module()
        throw = False
        if op == 1:
            if not user_input:
                throw = True
        else:
            if not (len(user_input) >= 2):
                throw = True
        if throw:
            self._raise_exception_specify("value")
    # Functions to check errors end

    # Command functionality begin
    def execute_command(self, command):
        try:
            data = Popen(command, shell=True, stdout=PIPE).stdout.read()
            print("")
            for line in data.decode().split("\n"):
                print_info(line)
        except Exception as e:
            raise Exception(str(e))

    def load(self, user_input=None):
        if not user_input:
            self._raise_exception_specify("module")
        self.session = Session(user_input[0])
        # The module is incorrect
        if not(self.session.correct_module()):
            print_error('Invalid module')
            self.session = None
        else:
            self.comp.set_commands_to_set(self.session.get_options_name())

    '''def jobs(self, user_input=None):
        if not user_input:
            Jobs.get_instance().show_jobs()
        elif len(user_input) > 0 and  user_input[0] == "-k":
            if len(user_input) == 2:
                id = user_input[1]
                if Jobs.get_instance().is_id_job(id):
                    print_info("ID job found")
                    Jobs.get_instance().kill_jobs(id)
                else:
                    print_error("ID job not found")
            else:
                print_error("ID job with multiple parameters")
        elif len(user_input) > 0 and  user_input[0] == "-K":
            Jobs.get_instance().kill_all_jobs()'''

    def set(self, user_input=[]):
        self._check_set(user_input)
        value = ' '.join([str(x) for x in user_input[1:]])
        self.session.set(user_input[0], value)

    def unset(self, user_input=[]):
        self._check_set(user_input, op=1)
        self.session.unset(user_input[0])

    def setglobal(self, user_input=[]):
        self._check_set(user_input)
        try:
            value = ' '.join([str(x) for x in user_input[1:]])
            self.session.set(user_input[0], value)
            Global.get_instance().add_value(user_input[0], value)
        except:
            print_error("Option not found for your configuration, use show")

    def show(self, user_input=[]):
        self._check_load_module()
        self.session.show()

    def run(self, user_input=[]):
        self._check_load_module()
        self.session.run()

    def back(self, user_input=[]):
        self.session = None

    def quit(self, user_input=[]):
        '''if Jobs.get_instance().hasjobs():
            Jobs.get_instance().kill_all_jobs()'''
        print_info("bye!")
        exit(0)

    def help(self, user_input=[]):
        show_help()
        # Command functionality end

    def connect(self, user_input=[]):
        '''
            usage: connect provider <url> port <port> chainid <chain_id>
            six params!
        '''
        # Connect.get_instance().del_connection()
        values = {}
        if len(user_input) == 6:
            if "provider" == user_input[0] or "port" == user_input[0] or "chainid" == user_input[0]:
                values[user_input[0]] = user_input[1]
            if "provider" == user_input[2] or "port" == user_input[2] or "chainid" == user_input[2]:
                if user_input[0] != user_input[2]:
                    values[user_input[2]] = user_input[3]
            if "provider" == user_input[4] or "port" == user_input[4] or "chainid" == user_input[4]:
                if user_input[0] != user_input[2] and user_input[2] != user_input[4]:
                    values[user_input[4]] = user_input[5]

            if len(values.keys()) != 3:
                print_error(
                    "Arguments incorrect: connect provider <url> port <port> chainid <chain_id>")
            else:
                Connect.get_instance().add_connection(values)
        else:
            print_error(
                "Arguments incorrect: connect provider <url> port <port> chainid <chain_id>")

    def disconnect(self, user_input=[]):
        if Connect.get_instance().has_connection():
            Connect.get_instance().del_connection()
            print_ok("Disconnected Blockchain OK!")
        else:
            print_info("No connection found")

    def datastore(self, user_input=[]):
        if len(user_input) == 0:
            DataStore.get_instance().help()

        elif len(user_input) == 1:
            if user_input[0] == "save":
                DataStore.get_instance().save()
            else:
                DataStore.get_instance().help()

        elif len(user_input) == 2:
            if user_input[0] == "contract" and user_input[1] == "show":
                DataStore.get_instance().show("contract")
            elif user_input[0] == "wallet" and user_input[1] == "show":
                DataStore.get_instance().show("wallet")
            else:
                DataStore.get_instance().help()

        elif len(user_input) == 3:
            if user_input[0] == "contract" and user_input[1] == "show":
                DataStore.get_instance().show_name("contract",user_input[2])
            elif user_input[0] == "contract" and user_input[1] == "create":
                DataStore.get_instance().create_name("contract",user_input[2])
            elif user_input[0] == "contract" and user_input[1] == "delete":
                DataStore.get_instance().delete_name("contract",user_input[2])
            elif user_input[0] == "wallet" and user_input[1] == "show":
                DataStore.get_instance().show_name("wallet",user_input[2])
            elif user_input[0] == "wallet" and user_input[1] == "create":
                DataStore.get_instance().create_name("wallet",user_input[2])
            elif user_input[0] == "wallet" and user_input[1] == "delete":
                DataStore.get_instance().delete_name("wallet",user_input[2])
            else:
                DataStore.get_instance().help()

        elif len(user_input) == 4:
            if user_input[0] == "contract" and user_input[1] == "del":
                DataStore.get_instance().del_value("contract",user_input[2],user_input[3])
            elif user_input[0] == "contract" and user_input[1] == "name":
                DataStore.get_instance().change_name("contract",user_input[2],user_input[3])
            elif user_input[0] == "wallet" and user_input[1] == "del":
                DataStore.get_instance().del_value("wallet",user_input[2],user_input[3])
            elif user_input[0] == "wallet" and user_input[1] == "name":
                DataStore.get_instance().change_name("wallet",user_input[2],user_input[3])
            else:
                DataStore.get_instance().help()

        elif len(user_input) == 5:
            if user_input[0] == "contract" and user_input[1] == "add":
                DataStore.get_instance().add_value("contract",user_input[2],user_input[3],user_input[4])
            elif user_input[0] == "contract" and user_input[1] == "mod":
                DataStore.get_instance().mod_value("contract",user_input[2],user_input[3],user_input[4])
            elif user_input[0] == "contract" and user_input[1] == "set":
                if DataStore.get_instance().is_valid_set("contract",user_input[2],user_input[4]):
                    self.set([user_input[3],DataStore.get_instance().get_param("contract",user_input[2],user_input[4])])
            elif user_input[0] == "wallet" and user_input[1] == "add":
                DataStore.get_instance().add_value("wallet",user_input[2],user_input[3],user_input[4])
            elif user_input[0] == "wallet" and user_input[1] == "del":
                DataStore.get_instance().del_value("wallet",user_input[2],user_input[3],user_input[4])
            elif user_input[0] == "wallet" and user_input[1] == "mod":
                DataStore.get_instance().mod_value("wallet",user_input[2],user_input[3],user_input[4])
            elif user_input[0] == "wallet" and user_input[1] == "set":
                if DataStore.get_instance().is_valid_set("wallet",user_input[2],user_input[4]):
                    self.set([user_input[3],DataStore.get_instance().get_param("wallet",user_input[2],user_input[4])])
            else:
                DataStore.get_instance().help()

        else:
            DataStore.get_instance().help()
            


def load_instructions(f):
    keyboard = Controller()
    sleep(1)
    data_file = open(f)
    for line in data_file.readlines():
        keyboard.type(line + "\n")
        sleep(0.2)

def exist_datastore_contract():
    config = Config.get_instance().get_config()
    contracts_datastore = config['datastore_path'] + config['datastore_filename_contracts']
    return (os.path.exists(contracts_datastore))

def exist_datastore_wallet():
    config = Config.get_instance().get_config()
    wallets_datastore = config['datastore_path'] + config['datastore_filename_wallets']
    return (os.path.exists(wallets_datastore))

if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    if exist_datastore_contract():
        DataStore.get_instance().read_file_contracts_datastore()
    if exist_datastore_wallet():
        DataStore.get_instance().read_file_wallets_datastore()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="File with instructions, one per line...")
    args = parser.parse_args()
    if args.file:
        th = threading.Thread(target=load_instructions, args=(args.file,))
        th.start()
    Console().console()
