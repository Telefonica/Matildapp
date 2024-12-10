from dataclasses import dataclass, field

from utils import generate_alias


@dataclass
class ContractInfo:
    address: str = field(default=None)
    alias: str = field(default_factory=lambda: generate_alias())
    abi: dict = field(default=None)
    file: str = field(default=None)
    source: str = field(default=None)
    contract: object = field(default=None)
    bytecode: str = field(default=None)
    network: str = field(default=None)
    selectors: list = field(default_factory=list)
