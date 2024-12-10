import json
import atexit

from console import print_error, print_info, print_ok
from dataclasses import asdict
from datastore.contract_info import ContractInfo
from datastore.network import Network
from datastore.wallet import Wallet
from utils import generate_alias

CONTRACTS_FILE = "contracts.json"
NETWORKS_FILE = "networks.json"
WALLETS_FILE = "wallets.json"

contracts = {}
networks = {}
wallets = {}


def load_contracts():
    """Load contract data from the JSON file into the contracts dictionary."""
    try:
        with open(CONTRACTS_FILE, "r") as file:
            data = json.load(file)
            for address, contract_data in data.items():
                contracts[address] = ContractInfo(**contract_data)
    except FileNotFoundError:
        print_error(
            f"{CONTRACTS_FILE} not found, starting with an empty contracts dictionary."
        )
    except json.JSONDecodeError:
        print_error(
            f"Error decoding JSON in {CONTRACTS_FILE}. Starting with an empty contracts dictionary."
        )


def save_contracts():
    """Save the contracts dictionary to a JSON file."""
    with open(CONTRACTS_FILE, "w") as file:
        # Convert each ContractInfo instance to a dictionary
        json_data = {
            address: asdict(contract) for address, contract in contracts.items()
        }
        json.dump(json_data, file, indent=4)
    print_info(f"Contract data saved to {CONTRACTS_FILE}")


def load_networks():
    """Load network data from the JSON file into the networks dictionary."""
    try:
        with open(NETWORKS_FILE, "r") as file:
            data = json.load(file)
            for rpc, network_data in data.items():
                networks[rpc] = Network(**network_data)
    except FileNotFoundError:
        print_error(
            f"{NETWORKS_FILE} not found, starting with an empty network dictionary."
        )
    except json.JSONDecodeError:
        print_error(
            f"Error decoding JSON in {NETWORKS_FILE}. Starting with an empty network dictionary."
        )


def save_networks():
    """Save the networks dictionary to a JSON file."""
    with open(NETWORKS_FILE, "w") as file:
        # Convert each Network instance to a dictionary
        json_data = {rpc: asdict(network) for rpc, network in networks.items()}
        json.dump(json_data, file, indent=4)
    print_info(f"Network data saved to {NETWORKS_FILE}")


def load_wallets():
    """Load wallet data from the JSON file into the wallets dictionary."""
    try:
        with open(WALLETS_FILE, "r") as file:
            data = json.load(file)
            for address, wallet_data in data.items():
                if wallet_data["private_key"]:
                    wallets[address] = Wallet(private_key=wallet_data["private_key"])
                else:
                    wallets[address] = Wallet(address=address)

                if wallet_data["alias"]:
                    wallets[address].alias = wallet_data["alias"]
    except FileNotFoundError:
        print_error(
            f"{WALLETS_FILE} not found, starting with an empty wallet dictionary."
        )
    except json.JSONDecodeError:
        print_error(
            f"Error decoding JSON in {WALLETS_FILE}. Starting with an empty wallet dictionary."
        )


def save_wallets():
    """Save the wallets dictionary to a JSON file."""
    with open(WALLETS_FILE, "w") as file:
        # Convert each Wallet instance to a dictionary
        json_data = {address: asdict(wallet) for address, wallet in wallets.items()}
        json.dump(json_data, file, indent=4)
    print_info(f"Wallet data saved to {WALLETS_FILE}")


# Register the save function to be called at program exit
atexit.register(save_contracts)
atexit.register(save_networks)
atexit.register(save_wallets)

# Initialize networks and wallets from the JSON file at program start
try:
    print_info("Loading contracts...")
    load_contracts()
except Exception as e:
    print(e)

try:
    print_info("Loading networks...")
    load_networks()
except Exception as e:
    print(e)

try:
    print_info("Loading wallets...")
    load_wallets()
except Exception as e:
    print(e)


# --- Contracts management functions ---
def add_contract(
    address, abi=None, alias=None, file=None, source=None, bytecode=None, network=None
):
    """
    Add a new contract instance to the contracts dictionary.

    Args:
        address (str): The contract's address.
        abi (dict, optional): The ABI of the contract.
        alias (str, optional): A user-friendly alias for the contract. Defaults to None.
        file (str, optional): The source file of the contract. Defaults to None.
        source (str, optional): The source URL of the contract. Defaults to None.
        bytecode (str, optional): The bytecode of the contract. Defaults to None.
        network (str, optional): The network associated with the contract. Defaults to None.
    """
    if address in contracts:
        print_error(f"Contract with address {address} already exists.")
        return

    if alias is None:
        alias = generate_alias()

    new_contract = ContractInfo(
        address=address,
        abi=abi,
        alias=alias,
        file=file,
        source=source,
        bytecode=bytecode,
        network=network,
    )
    contracts[address] = new_contract
    save_contracts()
    print_info(f"Added contract: {address}")


def update_contract(address, new_selectors=None):
    """
    TODO: Extend this function to update other contract attributes.
    
    Update the function selectors of an existing contract in the contracts dictionary.

    Args:
        address (str): The address of the contract to update.
        new_selectors (list, optional): The new list of function selectors to assign to the contract.

    Raises:
        ValueError: If the specified address does not exist in the dictionary.
    """
    if address in contracts:
        contracts[address].selectors = new_selectors
        save_contracts()
        print_ok(f"Function selectors updated for contract {address}")
    else:
        raise ValueError(f"No contract found with address: {address}")


def remove_contract(address):
    """
    Remove a contract instance from the contracts dictionary.

    Args:
        address (str): The contract's address to remove.

    Raises:
        ValueError: If no contract is found with the specified address.
    """
    if address in contracts:
        del contracts[address]
        save_contracts()
        print_info(f"Removed contract: {address}")
    else:
        print_error(f"No contract found with address: {address}")


def update_contract_alias(address, new_alias):
    """
    Update the alias of an existing contract in the contracts dictionary.

    Args:
        address (str): The address of the contract to update.
        new_alias (str): The new alias to assign to the contract.

    Raises:
        ValueError: If the specified address does not exist in the dictionary.
    """
    if address in contracts:
        contracts[address].alias = new_alias
        save_contracts()
        print_info(f"Updated alias for contract {address} to '{new_alias}'")
    else:
        raise ValueError(f"No contract found with address: {address}")


# --- Networks management functions ---
def add_network(rpc, chain_id, alias=None, symbol="ETH", block_explorer=None):
    """Add a new network instance to the networks dictionary."""
    if rpc in networks:
        print(f"Network with RPC {rpc} already exists.")
        return

    if alias is None:
        alias = generate_alias()

    if symbol is None:
        symbol = "ETH"

    new_network = Network(
        rpc=rpc,
        chain_id=chain_id,
        alias=alias,
        symbol=symbol,
        block_explorer=block_explorer,
    )
    networks[rpc] = new_network
    save_networks()
    print_info(f"Added network: {rpc}")


def remove_network(rpc):
    """Remove a network instance from the networks dictionary."""
    if rpc in networks:
        del networks[rpc]
        save_networks()
        print_info(f"Removed network: {rpc}")
    else:
        print_error(f"No network found with RPC: {rpc}")


def update_network_alias(rpc, new_alias):
    """
    Update the alias of an existing network in the networks dictionary.

    Args:
        rpc (str): The RPC URL of the network to update.
        new_alias (str): The new alias to assign to the network.

    Raises:
        ValueError: If the specified RPC does not exist in the dictionary.
    """
    if rpc in networks:
        networks[rpc].alias = new_alias
        save_networks()
        print_info(f"Updated alias for network {rpc} to '{new_alias}'")
    else:
        raise ValueError(f"No network found with RPC: {rpc}")


# --- Wallets management functions ---
def add_wallet(private_key=None, address=None, alias=None):
    """Add a new wallet instance to the wallets dictionary."""
    if private_key:
        new_wallet = Wallet(private_key=private_key)
    elif address:
        new_wallet = Wallet(address=address)
    else:
        raise ValueError("Must provide a private key or address to create a wallet.")

    if alias:
        new_wallet.alias = alias

    wallets[new_wallet.address] = new_wallet
    save_wallets()
    print_info(f"Added wallet: {new_wallet.address}")


def remove_wallet(address):
    """Remove a wallet instance from the wallets dictionary."""
    if address in wallets:
        del wallets[address]
        save_wallets()
        print_info(f"Removed wallet: {address}")
    else:
        print_error(f"No wallet found with address: {address}")


def update_wallet_alias(address, new_alias):
    """
    Update the alias of an existing wallet in the wallets dictionary.

    Args:
        address (str): The address of the wallet to update.
        new_alias (str): The new alias to assign to the wallet.

    Raises:
        ValueError: If the specified address does not exist in the dictionary.
    """
    if address in wallets:
        wallets[address].alias = new_alias
        save_wallets()
        print_info(f"Updated alias for wallet {address} to '{new_alias}'")
    else:
        raise ValueError(f"No wallet found with address: {address}")
