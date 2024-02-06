from lib.vulnerabilities import Vulnerability


class Signature_Replay_Attack(Vulnerability):
    info = """
    SWC: 121
    CWE RELATED: CWE-347
    Title: Missing protection against signature replay attacks
    Description: A contract that enables gasless signature based verification for premission
                 control must protect that the sended signature is unique and can't be replayed.
                 If replayed a transaction it can lead to undesired behaviour of the contract.

                 Example: An ERC20 token that allows users to transfer tokens in behalf of other
                 users by signing a message. The contract does not ensure that the signature is uniquie
                 and can be replayed by an attacker.

                 Remediation: It can be remediated by using a nonce or a timestamp in the signed message.

    Detection cases:
        1. Use of signature verification
        2. (IF ERC20) Standard version of signature function only have 3 params
            Params: (_to, _value, _signature)
        2. (ELSE) The contract uses keccak256(getHasFunctionX) and not use of nonce of timestamp
        3. Dinamically try to replay the signature and check if the transaction is successful
    """

    def __init__(self, is_erc_20: bool):
        description = ["⚠️ The contract uses signatures for user based actions verification",
                       "It does not protect against signature replay attacks"]
        confidence = "surely" if is_erc_20 else "potential"
        super().__init__(
            121,
            "CWE-347",
            "Signature replay attack",
            description,
            "Critical",
            confidence,
        )
