import re
import os
from solcx import *
from printib import *
from connect import Connect
from solcx.install import Version
from lib.bytecode_contract import ByteCode_Contract
from lib.contract_solidity import Solidity_Contract


def get_solidity_contract(args):
    """
    Get the Solidity from the path
    :param args: The arguments of the module
    :return: The Solidity_Contract
    """
    contract_content = get_contract_from_path(args["contract"])
    # compile
    if os.path.exists(args["contract"]) and str(args["contract"]).endswith('.sol'):
        with open(args["contract"], "r") as c:
            contract_content = c.read().splitlines()
        return Solidity_Contract(contract_content)
    print_error("❌ Contract not found")


def get_bytecode_from_path(args) -> (ByteCode_Contract | None):
    """
    Get the bytecode from the path
    :param args: The arguments of the module
    :return: The bytecode of the contract
    """
    if not args["bytecode"]:
        raise Exception("Bytecode not provided")

    if os.path.exists(args["bytecode"]) and str(args["bytecode"]).endswith('.txt'):
        with open(args["bytecode"], "r") as c:
            contract_content = c.read().splitlines()
            contract_content = "".join(contract_content)
            if not contract_content.startswith("0x"):
                print_error("❌ The bytecode must start with 0x")
                return
        return ByteCode_Contract(contract_content)

    if args["bytecode"].startswith('0x'):
        return ByteCode_Contract(args["bytecode"])
    print_error("❌ Bytecode not found")


def get_bytecode_from_address(args) -> (ByteCode_Contract | None):
    """
    Get the bytecode from the address
    :param args: The arguments of the module
    :return: The bytecode of the contract
    """
    connection = Connect.get_instance()
    if not connection or not connection.has_connection():
        print_error("No connection to the blockchain")
        return
    if not args["address"]:
        print_error("❌ Address not provided")
        return
    if not re.match("^0x[a-fA-F0-9]{40}$", args["address"]):
        print_error("❌ Address not valid")
        return
    bytecode: str = connection.get_bytecode(args["address"])
    return ByteCode_Contract(bytecode) if bytecode else None


def count_till_line(line: str, contract: Solidity_Contract | ByteCode_Contract) -> int:
    count = 0
    code: list[str] = contract.original_code if isinstance(
        contract, Solidity_Contract) else contract.opcodes
    for l in code:
        count += 1
        if line in l:
            return count
    raise Exception("Line not found")


def get_contract_from_path(path: str) -> str:
    """
    Get the contract name from the path
    :param path: The path of the contract
    :return: The name of the contract
    :raise: Exception if the contract is not found
    """
    if not os.path.exists(path) or not path.endswith('.sol'):
        raise Exception("❌ Contract not found")
    with open(path, "r") as c:
        return c.read()


def compile_contract(
        path: str,
        contract_content: str,
        metadata=False,
        bytecode=True,
        ast=False,
        abi=True,
):
    """
    Compile the contract with solcx with the compiler specified in the contract
    It can return the bytecode, ABI, metadata or the Abstract tree sintaxis
    :param path: The solidity contract path
    :param bytecode: If the bytecode should be returned
    :param abi: If the ABI should be returned
    :param metadata: If the metadata should be returned
    :param ast: If the AST should be returned
    :return: The bytecode, ABI, metadata or AST
    """

    version = next(
        (
            line.split()[2].strip(";").strip('^')
            for line in contract_content.splitlines()
            if line.startswith("pragma ")
        ), ''
    )

    if version == '':
        return print_error("❌ Contract not found")

    already_installed = next(
        (
            v
            for v in get_installed_solc_versions()
            if str(v) == version
        ), None
    )

    if already_installed:
        print(f'Using solc version {version}')
        set_solc_version(already_installed)
        version = already_installed
    else:
        version = install_solc(version, show_progress=True)

    try:
        compiled = compile_standard(
            {
                "language": "Solidity",
                "sources": {path: {"content": contract_content}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": [],
                            "": [
                                "ast",
                            ]
                        }
                    }
                },
            },
            solc_version=version,
        )
        print(compiled)
    except Exception as e:
        print(e)
