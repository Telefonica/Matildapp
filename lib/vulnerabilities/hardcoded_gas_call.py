from lib.vulnerabilities import Vulnerability


class Hardcoded_Gas_Call(Vulnerability):
    info = """
    SWC: 134
    CWE RELATED: CWE-665
    Title: Message call with hardcoded gas amount
    Description: When calling to other contract if the gas passed is consumed the transaction will fail.
                 Sending ethereum with transfer() or send() uses fixed amount of gas of 2300 which only
                 allows a contract to emit an event and will mostly throw and fail.
                 Recommendation is not to use transfer() or send(), use call() instead but do not hardhcoded
                 a gas amount

                 !!Important!!: This weakness my not be exploitable now, but if gas prices increase for a
                 certains opcode it can be exploited.

    Detection cases:
        1. transfer() used in the smart contract
        2. send() used in the smart contract
        3. call() used in the smart contract with hardcoded gas amount
        4. (For bytecode you can see the module implementation)
        Final conlcusion: 1 or 2 or 3
    """

    def __init__(self, confidence: str = "surely"):
        description = ["⚠️ The contract uses fixed gas amount for message calls",
                       "Can lean to unusable message call when interacting with other contracts"]
        super().__init__(
            134,
            "CWE-665",
            "Hardcoded gas amount in call",
            description,
            "High",
            confidence,
        )
