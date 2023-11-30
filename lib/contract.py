from enum import Enum


class evm_var_types(Enum):
    """
    Enum for the types of the parameters
    """
    address = 1
    uint = 2
    int = 3
    bool = 4
    bytes = 5
    string = 6
    unknown = 7


class Contract_Function:
    """
    Function for EVM based Smart Contract
    """
    #selector: str
    #parameters: list[evm_var_types]
    #code: list[str]

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
    #name: str
    #functions: list[Contract_Function]

    def __init__(self, name, functions):
        self.name = name
        self.functions = functions
