from lib.vulnerabilities import Vulnerability


class Sender_Phising(Vulnerability):
    info = """
    SWC: 115
    CWE RELATED: CWE-477
    Title: Authorization through tx.origin
    Description: tx.origin is used for finding the wallet that triggered the original transaction.
                 Can be used for Phising if a wallet calls a malicious smart contract.
                 Can be catastrophic if the wallet is a multisig wallet, as it will only store the
                 reference to the person who triggered the last vote.

    Detection cases: Can occur when tx.origin is used.
        1. tx.origin appears in the code
        2. tx.origin is in a comment
        Final conlcusion: 1 && !2
    """

    def __init__(self, confidence: str = "surely"):
        description = ["❌ Phising alert",
                       "The contract uses tx.origin, which can be used for phising attacks"]
        super().__init__(
            115,
            "CWE-477",
            "Authorization through tx.origin",
            description,
            "Critical",
            confidence,
        )
