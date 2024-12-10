from lib.vulnerabilities import Vulnerability


class Right_To_Left_Override_Character(Vulnerability):
    info = """
    SWC: 130
    CWE RELATED: CWE-451
    Title: Rigth to left override control character
    Description: If the contract has present the (U+202E) character, it can be used to change
                 of side params of a function call. This can lead to malinterpretation of the confidence
                 by the users and result in a scam. Example: transferFrom(address from, address to, uint256 value)

    Detection cases: (Solidity only)
        1. The contract has present the (U+202E) character
        Final conlusion: 1
    """

    def __init__(self, confidence: str = "surely"):
        description = ["Found the (U+202E) character in the contract",
                       "It can be used to scam the contract readers by changing the side of the params"]
        super().__init__(
            130,
            "CWE-451",
            "Right to left override control character",
            description,
            "High",
            confidence,
        )
