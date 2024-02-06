from typing import Union
from lib.contract import Contract, Contract_Function, Contract_Parameter, evm_var_types


class Solidity_Function(Contract_Function):
    """
    Function for EVM based Smart Contract
    """
    access_modifiers: list[str]

    def __init__(self,
                 selector: str,
                 parameters: list[Contract_Parameter],
                 code: list[str],
                 access_modifiers: list[str]):

        super(Solidity_Function, self).__init__(selector, parameters, code)
        self.access_modifiers = access_modifiers

    def __str__(self):
        return f"Selector: {self.selector}\n \
                Parameters: {self.parameters}\n \
                Code: {self.code}\n \
                Access Modifiers: {self.access_modifiers}"


class Solidity_Contract(Contract):
    """
    A Solidity Smart contract object
    :param code: The code of the actual smart contract
    """
    code: list[str]
    original_code: list[str]
    storage: list[str]
    pragma_version: list[str]
    constructor: Union[Solidity_Function, None]
    functions: list[Solidity_Function]
    modifiers: list[Contract_Function]
    events: list[tuple[str, list[Contract_Parameter]]]

    def __init__(self, code: list[str]):
        self.original_code = code
        self.code = self.preprocess_code(self.original_code)
        self.name = self.__get_contract_name()
        self.constructor = self.__get_constructor()
        self.pragma_version = self.__get_pragma_version()
        self.storage = self.__get_contract_storage()
        # TODO: update this
        self.events = []
        super().__init__(self.__get_functions())

    @staticmethod
    def preprocess_code(code: list[str]):
        """
        Eliminates all the innecesary elements like spaces and tabs
        and comments
        """
        def is_comment(line: str) -> bool:
            for i in ["//", "/*", "*", "*/"]:
                if line.strip().startswith(i):
                    return True
            return False

        new_code = []
        for line in code:
            if not is_comment(line) and line.strip() != "":
                new_code.append(line.strip().split("//")[0].strip())

        return new_code

    # TODO: refactor this
    def __get_contract_storage(self) -> list[str]:
        """
        Get the storage of the contract
        :param code: The code of the contract
        :return: The storage of the contract
        """
        storage: list[str] = []
        is_in_contract = False
        is_in_function = False
        # is storage if is inside contract x {} and is not a function
        for line in self.code:
            if line.startswith("contract") and "{" in line:
                is_in_contract = True
            elif line.startswith("function") and "{" in line:
                is_in_function = False
            elif "}" in line and is_in_function:
                is_in_function = False
            elif "}" in line and is_in_contract:
                is_in_contract = False
            elif is_in_contract and not is_in_function and not line.startswith("event "):
                storage.append(line)
        return storage

    def __get_contract_name(self) -> str:
        for line in self.code:
            if "contract " in line:
                return line.split()[1].strip("{")
        raise Exception("No Solidity Version setted")

    def __get_pragma_version(self):
        for line in self.code:
            if line.startswith("pragma "):
                version = line.split()[2].strip(";")
                return version.split(".")
        raise Exception("No Solidity Version setted")

    def __get_constructor(self) -> Union[Solidity_Function, None]:
        """
        Get the constructor of the contract
        """
        for i in range(len(self.code)):
            line = self.code[i]
            if not "constructor " in line:
                continue
            return Solidity_Function("constructor",
                                     self.__get_parameters(line),
                                     self.__get_function_body(
                                         self.code, i),
                                     self.__get_access_modifiers(line))

    def __get_functions(self):
        functions = []
        # TODO: optimize this
        for i in range(len(self.code)):
            line = self.code[i]
            if not "function " in line:
                continue
            new_function = Solidity_Function(
                line.split()[1].split("(")[0],
                self.__get_parameters(line),
                self.__get_function_body(self.code, i),
                self.__get_access_modifiers(line))
            functions.append(new_function)

        return functions

    def __get_parameters(self, line: str) -> list[Contract_Parameter]:
        """
        Get the parameters of a function
        :param line: The line of the function
        :return: The parameters of the function
        """
        parameters = []
        # TODO: refactor this parameter [1] can be a payable or memory
        parameter_string = line.split("(")[1].split(")")[0]
        if parameter_string != "":
            for parameter in parameter_string.split(","):
                parameter = parameter.split()
                parameters.append(Contract_Parameter(
                    evm_var_types.get_type(parameter[0]), parameter[1]))
        return parameters

    def __get_access_modifiers(self, line: str):
        """
        Get the access modifiers of a function
        :param line: The line of the function
        :return: The access modifiers of the function
        """
        modifiers: list[str] = []
        modifier_string = line.split(")", 1)[1].split("{")[0]
        if modifier_string != "":
            for modifier in modifier_string.split():
                modifiers.append(modifier)
        return modifiers

    def __get_function_body(self, code: list[str], line: int) -> list[str]:
        """
        Get the body of a function
        :param line: The line of the function
        :return: The body of the function
        """

        body: list[str] = []
        for inside_line in code[line:]:
            if "}" in inside_line:
                break
            body.append(inside_line.strip("\t").strip("\n"))
        return body
