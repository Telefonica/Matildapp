from printib import *
from module import Module
from modules.utils import get_bytecode_from_address
from lib.bytecode_contract import ByteCode_Contract
from lib.vulnerabilities.hardcoded_gas_call import Hardcoded_Gas_Call


class CustomModule(Module):
    """
    Module to detect the vulnerability: Hardcoded_Gas_Call
    See lib.vulnerabilities.hardcoded_gas_call for more info
    """

    def __init__(self):
        information = {"Name": "Hardcoded Gass Call Bytecode check",
                       "Description": Hardcoded_Gas_Call.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"bytecode": [
            None, "Bytecode or path to .txt containing the bytecode", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: ByteCode_Contract) -> None:
        """
        Check the contract
        :param contract: The solidity smart contract

        Send value from a call to a contract
        PUSH32 <memoutsz>         # size of the offset in memory
        PUSH32 <memoutstart>      # start of memory output
        PUSH32 <meminsz>          # size of the input in memory
        PUSH32 <meminstart>       # start of the input
        PUSH32 <value>
        PUSH20 <to>
        PUSh32 <gas>
        CALL

        detectar cuando hay un gas en el call (solo solidity)
            1. Detectar instruccion CALL
            2. Ir hacia atras para encontrar el PUSH20 0xfff...
            3. En las siguientes 4 instrucciones a PUSH20 debe haber un PUSHX 0x<hexval>
        """
        found = False
        hardcoded_gas_call = Hardcoded_Gas_Call()

        # TODO: clean this
        for i in range(len(contract.opcodes)):
            opcode = contract.opcodes[i]
            if not opcode == "CALL":
                continue

            # go back till find the push20 0xffffffffffffffffffffffffffffffffffffffff instruction
            lastJ = 0
            for j in range(i-1, 0, -1):
                opcode = contract.opcodes[j]
                if opcode == "PUSH20 0xffffffffffffffffffffffffffffffffffffffff":
                    lastJ = j
                    break

            for k in range(lastJ+1, lastJ+4):
                instruction = contract.opcodes[k].split(" ")
                if not instruction[0].startswith("PUSH") or not instruction[1].startswith("0x"):
                    continue
                gas_amount = 0
                try:
                    gas_amount = int(instruction[1], 16)
                except ValueError:
                    continue
                if gas_amount == 2300:
                    hardcoded_gas_call.add_code(
                        f"Found a address.send() or address.transfer() call in the contract")
                    hardcoded_gas_call.add_code(
                        f"   Please do not use send() or transfer() since it sends a fixed amount of gas")
                if not gas_amount == 2300:
                    hardcoded_gas_call.add_code(
                        f"Found a call with hardcoded gas amount in the contract")

                hardcoded_gas_call.add_code(
                    f"   If you use a fixed amount of gas your contract can suffer DoS in the future, see EIP-150 for more info")
                found = True
                break

        if not found:
            print_ok("✅ Not vulnerable to hardcoded gas call denegation, al ok")
        hardcoded_gas_call.print_vulnerability()

    def run_module(self) -> None:
        bytecode: (ByteCode_Contract | None) =\
            get_bytecode_from_address(self.args)
        return self.check_contract(bytecode) if bytecode else None
