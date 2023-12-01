from lib.vulnerabilities import Vulnerability


class Unprotected_Selfdestruct(Vulnerability):
    info = """
    SWC: 106
    CWE RELATED: CWE-284
    Title: Unprotected Selfdestruct
    Description: SELFDESTRUCT is a dangerous opcode that will destroy the contract when called.
                 Also it will transfer all aviable funds to an specified address.
                 If not protected this instruction in your code it will be used to destroy the contract.

    Detection cases: If the opcode SELFDESTRUCT is present with no protection.
        1. selfdestruct(address) appears in the code
        2. No access control to the function using it
        Final conlcusion: 1 && !2
    """

    def __init__(self, confidence: str = "surely"):
        description = ["⚠️ The contract uses selfdestruct() without any protection."
                       "This can lead to the contract being destroyed."]
        super().__init__(
            106,
            "CWE-284",
            "Unprotected Selfdestruct",
            description,
            "Critical",
            confidence,
        )
