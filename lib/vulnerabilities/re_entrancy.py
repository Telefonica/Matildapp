from lib.vulnerabilities import Vulnerability


class Re_Entrancy(Vulnerability):
    info = """
    SWC: 107
    CWE RELATED: CWE-841
    Title: Reentrancy
    Description: One of the major dangers of calling external contracts is that they can take
                 over the control flow. In the reentrancy attack (a.k.a. recursive call attack),
                 a malicious contract calls back into the calling contract before the first 
                 invocation of the function is finished. This may cause the different invocations
                 of the function to interact in undesirable ways.

    Detection cases:
        1. call method appears in the code
        2. a '-=' or '-' operator is used in the code
        Final conlcusion: 1 && 2 && 1 before 2
    """

    def __init__(self, confidence: str = "potential"):
        description = ["❌ Reentrancy alert", "The contract is using a call that could be vulnerable to reentrancy attacks"]
        super().__init__(
            107,
            "CWE-841",
            "Reentrancy",
            description,
            "Critical",
            confidence,
        )
