import sys
import importlib
from os import sep

from rich import print

from console import print_error, print_info, print_ok
from datastore.datastore import contracts, networks, wallets


class Session(object):
    def __init__(self, path):
        self._module = None
        try:
            self._module = self.instantiate_module(self.import_path(path))
        except Exception as e:
            print(e)
            pass

        self._path = path

    def header(self):
        return self._path.split(sep)[-1]

    def show(self):
        self.information()
        self.options()

    def information(self):
        info = self._module.get_information()
        print("")
        for key, value in info.items():
            print(f" [yellow]{key}[/yellow]")
            # TODO: Review this
            print(" " + "-" * len(key))
            print(" |_%s\n" % value)

    def options(self):
        opts = self._module.get_options_dict()
        print_info("Options (Field = Value)")
        print(" -----------------------")
        flag = 0
        for key, value in opts.items():
            flag += 1
            if flag > 1:
                print(" |")
            # Parameter is mandataroy
            if value[2]:
                if str(value[0]) == "None":
                    print(f" |_[[red]REQUIRED[/red]] {key} = {value[0]} ({value[1]})")
                else:
                    print(f" |_{key} = [green]{value[0]}[/green] ({value[1]})")

            # Parameter is optional
            else:
                if str(value[0]) == "None":
                    print(
                        " |_[[yellow]OPTIONAL[/yellow]] %s" % key
                        + " = %s (%s)" % (value[0], value[1])
                    )
                else:
                    sys.stdout.write(" |_%s" % key)
                    sys.stdout.write(" = ")
                    print(f"[green]{value[0]}[/green]")
                    sys.stdout.write(" (% s)\n" % (value[1]))

        print("\n")

    def run(self):
        if not (self._module.check_arguments()):
            raise Exception("REQUIRED ARGUMENTS NOT SET...exiting")

        print_ok("Running module...")
        try:
            self._module.run_module()
        except KeyboardInterrupt:
            print_error("Exiting the module...")
        except Exception as error:
            m = "Error running the module: " + str(error)
            print_error(m)
            print_ok("Module exited")

    def set(self, name, value):
        if name not in self._module.get_options_names():
            raise Exception("Field not found")
        if name == "network":
            for _, network in networks.items():
                if network.alias == value:
                    self._module.set_value(name, network.rpc)
                    return
        if name == "contract":
            for _, contract in contracts.items():
                if contract.alias == value:
                    self._module.set_value(name, contract.address)
                    return
        if name == "wallet":
            for _, wallet in wallets.items():
                if wallet.alias == value:
                    self._module.set_value(name, wallet.private_key)
                    return
        if name == "bytecode":
            for _, contract in contracts.items():
                if contract.alias == value:
                    self._module.set_value(name, contract.bytecode)
                    return
        self._module.set_value(name, value)

    def unset(self, name):
        if name not in self._module.get_options_names():
            raise Exception("Field not found")
        self._module.set_value(name, None)

    def instantiate_module(self, path):
        try:
            print_ok("Loading module...")
            m = importlib.import_module(path)
            print_ok("Module loaded!")
            return m.CustomModule()
        except ImportError as error:
            m = "Error importing the module: " + str(error)
            print_error(m)
            return None

    def correct_module(self):
        if self._module is None:
            return False
        return True

    def import_path(self, path):
        path = path.replace(sep, ".")
        return path.replace(".py", "")

    def get_options(self):
        return ["set " + key for key, value in self._module.get_options_dict().items()]

    def get_options_name(self):
        return list(self._module.get_options_names())
