from lib.vulnerabilities import Vulnerability


class Untrusted_Delegatecall(Vulnerability):
    info = """
    SWC: 112
    CWE RELATED: CWE-829
    Title: Delegatecall to Untrusted Contract
    Description: Delegatecall can be used to execute code from another contract.
                 This can be used to execute code from an untrusted contract.
    Detection Cases: See implementation of the module
    """

    def __init__(self, confidence: str = "potential"):
        description = ["❌ Unsecure delegatecall to contract",
                       "If the contract you are using is not trusted, it can be used to destroy the contract."]

        super().__init__(
            112,
            "CWE-829",
            "Delegatecall to Untrusted Contract",
            description,
            "Critical",
            confidence,
        )
