from lib.vulnerabilities import Vulnerability


class Timestamp_Dependence(Vulnerability):
    info = """
    SWC: 116
    CWE RELATED: CWE-829
    Title: Timestamp dependence
    Description: TIMESTAMP opcode can be altered by miners.
                 Now it can be altered more than 15sec in the Ethereum network.
                 Miners can give advantage to perform actions before or after the timestamp.

    Detection cases: Can occur when block.timestamp is used.
        1. block.timestamp appears in the code
        2. block.timestamp is in a comment
        Final conlcusion: 1 && !2
    """

    def __init__(self, confidence: str = "potential"):
        description = ["⚠️ The contract uses block.timestamp",
                       "The contract is vulnerable to 15sec edit and function manipulation"]
        super().__init__(
            116,
            "CWE-829",
            "Timestamp Dependence",
            description,
            "High",
            confidence,
        )
