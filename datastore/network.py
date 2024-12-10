import re
from dataclasses import dataclass, field


@dataclass
class Network:
    """
    A class representing a blockchain network, including information such as RPC URL, chain ID, symbol, and block explorer URL.

    Attributes:
        rpc (str): The RPC URL for accessing the network. Required.
        chain_id (int): The unique chain ID for the network. Must be a positive integer. Required.
        alias (str): A unique alias for the network. Defaults to the RPC URL if not provided.
        symbol (str): The network’s symbol, typically 3-5 characters (e.g., "ETH"). Defaults to "ETH".
        block_explorer (str): Optional URL of a block explorer for the network.

    Raises:
        ValueError: If the RPC URL is invalid, or if chain_id is not a positive integer.
    """

    rpc: str
    chain_id: int
    alias: str = field(default=None)
    symbol: str = field(default_factory=lambda: "ETH")
    block_explorer: str = field(default=None)

    def __post_init__(self):
        """
        Post-initialization validations to ensure the integrity of the network data.

        - Validates that the RPC URL and optional block explorer URL (if provided) follow a valid URL format.
        - Ensures that chain_id is a positive integer.
        - Sets alias to RPC if alias is not provided.

        Raises:
            ValueError: If any validation fails.
        """

        if not self.validate_url(self.rpc):
            raise ValueError("Invalid RPC URL provided.")

        if not isinstance(self.chain_id, int) or self.chain_id < 1:
            raise ValueError("chain_id must be a positive integer.")

        if self.block_explorer and not self.validate_url(self.block_explorer):
            raise ValueError("Invalid block explorer URL provided.")

        if not self.alias:
            self.alias = self.rpc

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validates the format of a URL to ensure it is a well-formed HTTP, HTTPS, or WebSocket (WS/WSS) URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        url_pattern = re.compile(
            r"^(https?|wss)://"  # Allow http, https, ws, or wss protocols
            r"(\S+\.\S+)"  # Ensure a valid domain format
        )
        return bool(url_pattern.match(url))
