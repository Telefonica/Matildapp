from printib import *
from module import Module
from lib.contract import Contract_Parameter, evm_var_types
from modules.utils import count_till_line, get_solidity_contract
from lib.contract_solidity import Solidity_Contract, Solidity_Function
from lib.vulnerabilities.signature_replay_attack import Signature_Replay_Attack


class CustomModule(Module):
    """
    Module to detect the vulnerability: Untrusted Delegatecall
    See lib.vulnerabilities.signature_replay_attack for more info
    """

    def __init__(self):
        information = {"Name": "Signature replay attack",
                       "Description": Signature_Replay_Attack.info,
                       "Author": "@chgara"}

        # -----------name-----default_value--description--required?
        options = {"contract": [None, "Contract path, Solidity only", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: Solidity_Contract) -> None:
        """
        Detection cases:
            1. Use of signature verification
            2. (IF ERC20) Standard version of signature function only have 3 params
               Params: (_to, _value, _signature)
            2. (ELSE) The contract uses keccak256(getHasFunctionX) and not use of nonce of timestamp
            3. Dinamically try to replay the signature and check if the transaction is successful
        """
        replay_attack = Signature_Replay_Attack(is_erc_20=True)
        pass

    def run_module(self):
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
