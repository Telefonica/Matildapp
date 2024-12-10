from web3 import Web3
from web3.exceptions import InvalidAddress

from console import print_error, print_info


class BlockchainConnection:
    """Singleton class to manage Web3 blockchain connections."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of Web3 connection is created."""
        if not cls._instance:
            cls._instance = super(BlockchainConnection, cls).__new__(
                cls, *args, **kwargs
            )
            cls._instance.web3 = None
        return cls._instance

    def __init__(self):
        self.web3 = None  # Web3 connection

    @classmethod
    def get_instance(cls):
        """Retrieve the singleton instance of BlockchainConnection."""
        if cls._instance is None:
            cls._instance = BlockchainConnection()
        return cls._instance

    def connect(self, rpc_url):
        """
        Connect to the blockchain via Web3 using the given RPC URL.

        Args:
            rpc_url (str): The RPC URL to connect to.

        Returns:
            Web3: The Web3 instance connected to the blockchain.
        """
        if self.web3:
            print_info("Already connected.")
            return self.web3

        print_info(f"Connecting to {rpc_url}...")
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if self.web3.is_connected():
            print_info(f"Successfully connected to {rpc_url}")
            return self.web3
        else:
            print_error(f"Failed to connect to {rpc_url}")
            self.web3 = None
            return None

    def disconnect(self):
        """Disconnect the Web3 connection."""
        if self.web3:
            print_info("Disconnecting...")
            self.web3 = None
        else:
            print_error("No active connection to disconnect.")

    def contract_interact(self, contract_address):
        """
        Connect to a contract using its address.

        Args:
            contract_address (str): The address of the contract to connect to.

        Returns:
            Contract: A Web3 contract instance if connection is successful.
        """
        if not self.web3 or not self.web3.is_connected():
            raise ConnectionError("Not connected to any blockchain. Connect first.")

        try:
            # Validate contract address
            if not self.web3.is_address(contract_address):
                raise InvalidAddress(f"Invalid contract address: {contract_address}")

            # Create contract instance
            bytecode = self.web3.eth.get_code(contract_address)
            contract_instance = self.web3.eth.contract(
                address=contract_address, bytecode=bytecode
            )
            return contract_instance
        except InvalidAddress as e:
            raise InvalidAddress(f"Invalid address provided: {e}")
        except Exception as e:
            raise Exception(f"Error connecting to contract: {e}")
