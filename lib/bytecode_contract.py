from printib import print_error
from pyevmasm import disassemble_hex
from lib.contract import Contract, Contract_Function


class ByteCode_Contract(Contract):
    """
    Bytecode smart contract
    :param bytecode: The compiled code of the smart contract
    """
    bytecode: str
    opcodes: list[str]

    def __init__(self, byte_code):
        self.bytecode = byte_code
        self.opcodes = self.from_bytecode_to_opcode(byte_code)
        super().__init__(self.__get_functions())

    def __get_functions(self) -> list[Contract_Function]:
        """
        Get the functions from the bytecode
        """
        # TODO: Implement this
        return []

    @staticmethod
    def from_bytecode_to_opcode(hexcode):
        """
        Convert the bytecode to opcodes
        :param hexcode: The bytecode
        :return: The opcodes in a str array
        """
        try:
            return disassemble_hex(hexcode).split("\n")
        except Exception as e:
            print_error("Error, provided bytecode is corrupted")
            return []
