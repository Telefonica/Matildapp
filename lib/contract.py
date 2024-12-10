from enum import Enum


class evm_var_types(Enum):
    """
    Enum for the types of the parameters
    """
    UNKNOWN = 0
    ADDRESS = 1
    UINT256 = 2
    UINT8 = 3
    STRING = 4
    BOOL = 5
    BYTES32 = 6
    BYTES = 7
    INT256 = 8
    STRUCT = 9

    @staticmethod
    def get_type(type_name: str) -> "evm_var_types":
        """
        Get the type of the parameter
        :param type_name: The name of the type
        :return: The type of the parameter
        """
        if type_name == "address":
            return evm_var_types.ADDRESS
        elif type_name == "uint256":
            return evm_var_types.UINT256
        elif type_name == "uint8":
            return evm_var_types.UINT8
        elif type_name == "string":
            return evm_var_types.STRING
        elif type_name == "bool":
            return evm_var_types.BOOL
        elif type_name == "bytes32":
            return evm_var_types.BYTES32
        elif type_name == "bytes":
            return evm_var_types.BYTES
        elif type_name == "int256":
            return evm_var_types.INT256
        elif type_name == "struct":
            return evm_var_types.STRUCT
        elif type_name.split(" ")[0] == "address":
            return evm_var_types.ADDRESS
        else:
            return evm_var_types.UNKNOWN


class Contract_Parameter:
    type: evm_var_types
    name: str

    def __init__(self, type: evm_var_types, name: str):
        self.type = type
        self.name = name

    def __str__(self):
        return f"Parameter: {self.name} - {self.type}"


class Contract_Function:
    """
    Function for EVM based Smart Contract
    """
    selector: str
    parameters: list[Contract_Parameter]
    code: list[str]

    def __init__(self, selector, parameters, code):
        self.selector = selector
        self.parameters = parameters
        self.code = code

    def __str__(self):
        return f"Selector: {self.selector}\nParameters: {self.parameters}\nCode: {self.code}"


class Contract:
    """
    EVM contract intended to be used as an interface containing the data of
    a base EVM Smart contact
    """
    functions: list[Contract_Function]

    def __init__(self, functions):
        self.functions = functions

    def __str__(self):
        return f"Functions: {self.functions}"
