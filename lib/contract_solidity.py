from lib.contract import Contract, Contract_Function, evm_var_types


class Solidity_Contract(Contract):
    """
    A Solidity Smart contract object
    :param code: The code of the actual smart contract
    """
    #code: list[str]
    #pragma_version: list[str]

    def __init__(self, code):
        self.code = code
        self.pragma_version = self.__get_pragma_version()
        super().__init__(self.__get_contract_name(), self.__get_functions())

    def __get_contract_name(self) -> str:
        for line in self.code:
            if "contract " in line:
                return line.split()[1].strip("{")
        raise Exception("No Solidity Version setted")

    def __get_pragma_version(self):
        for line in self.code:
            if line.startswith("pragma "):
                version: str = line.split()[2].strip(";")
                return version.split(".")
        raise Exception("No Solidity Version setted")

    def __get_functions(self):
        functions: list[Contract_Function] = []

        for i in range(len(self.code)):
            if "function " in self.code[i]:
                code: list[str] = []
                function_name: str = self.code[i].split()[1].split("(")[0]

                # get the code body of the function started by
                for j in range(i, len(self.code)):
                    if "}" in self.code[j]:
                        break
                    # clean tabs and line ends
                    code.append(self.code[j].strip("\t").strip("\n"))

                # add new function to the list
                new_function: Contract_Function = Contract_Function(
                    function_name, self.__get_parameters(self.code[i]), code)
                functions.append(new_function)

        return functions

    def __get_parameters(self, line: str):
        parameters: list[evm_var_types] = []
        for parameter in line.split("(")[1].split(")")[0].split(","):
            if "address" in parameter:
                parameters.append(evm_var_types.address)
            elif "uint" in parameter:
                parameters.append(evm_var_types.uint)
            elif "int" in parameter:
                parameters.append(evm_var_types.int)
            elif "bool" in parameter:
                parameters.append(evm_var_types.bool)
            elif "bytes" in parameter:
                parameters.append(evm_var_types.bytes)
            elif "string" in parameter:
                parameters.append(evm_var_types.string)
            else:
                parameters.append(evm_var_types.unknown)

        return parameters
