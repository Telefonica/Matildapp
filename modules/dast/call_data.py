from web3 import Web3
from eth_abi import encode
from eth_account import Account

from module import Module
from console import print_ok, print_info, print_error


class CustomModule(Module):
    """
    Module to call a contract function by function selector
    """

    def __init__(self):
        information = {
            "Name": "Call contract function by function selector",
            "Description": """Call a contract function by function selector using a wallet and a network.

   Function selector:
   - The function selector is a unique identifier of the function in the contract.
   - The function selector can be found in the contract's ABI or using find_function_selector module.
   Parameters:
   - Parameters must follow the format: type:value (e.g., uint256:18,bytes:0x1234).
   - The parameters of the function are optional and should be separated by commas.""",
            "Author": "@jalvarezz13",
        }

        # -----------name-----default_value--description--required?
        options = {
            "contract": [None, "Contract address or contract alias in the datastore", True],
            "network": [None, "Network alias to use", True],
            "wallet": [None, "Wallet alias to use", True],
            "function_selector": [None, "Function selector to call", True],
            "params": [None, "Parameters of the function separated by commas (e.g., uint256:value,bytes:value)", False],
        }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class attributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    @staticmethod
    def _convert_param_value(param_type: str, param_value: str):
        """
        Convert the parameter value based on its type to handle encoding properly.
        """
        if param_type in ["uint256", "int256", "uint", "int"]:
            return int(param_value)
        elif param_type == "bytes":
            return bytes.fromhex(param_value.lstrip("0x"))
        elif param_type == "address":
            return Web3.to_checksum_address(param_value)
        elif param_type == "bool":
            return param_value.lower() in ["true", "1"]
        elif param_type == "string":
            return param_value
        else:
            raise ValueError(f"Unsupported type: {param_type}")

    def run_module(self) -> None:
        private_key = self.args["wallet"]
        from_address = Account.from_key(private_key).address
        contract_address = self.args["contract"]
        function_selector = self.args["function_selector"]
        raw_params = self.args["params"]
        network_rpc = self.args["network"]

        web3 = Web3(Web3.HTTPProvider(network_rpc))

        # Process params if provided
        encoded_params = ""
        if raw_params:
            try:
                param_list = raw_params.split(",")
                types, values = zip(
                    *[
                        (param_type.strip(), self._convert_param_value(param_type.strip(), param_value.strip()))
                        for param_type, param_value in (p.split(":") for p in param_list)
                    ]
                )
                encoded_params = encode(types, values).hex()
            except Exception as e:
                print_error(f"Error encoding parameters: {e}")
                return

        print_info(f"Calling function selector {function_selector} with parameters {encoded_params}")

        # Get the nonce and send the transaction
        nonce = web3.eth.get_transaction_count(from_address)
        transaction = {
            "to": contract_address,
            "value": 0,
            "gas": 200000,
            "gasPrice": web3.eth.gas_price,
            "nonce": nonce,
            "data": function_selector + encoded_params,
        }
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction.hex())
            print(f"Transacción enviada. Hash: {web3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"Error al enviar la transacción: {e}")
