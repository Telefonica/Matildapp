from lib.vulnerabilities import Vulnerability


class Safeguading_Constructor(Vulnerability):
    info = """
    SWC: N/A
    CWE RELATED: CWE-665
    Title: Constructor safeguarding
    Description: Prior versions of Solidity used the function keyword to define constructors.
                 In version mayor 0.4.0, the constructor keyword was introduced to define constructors.
                 If using wrong it can introduce many security vulnerabilities.

    Detection cases: Can occur when contract version >= 0.4.0 and constructor is defined with function keyword.
        1. Contract version >= 0.4.0
        2. Constructor is defined with function keyword
        Final conlcusion: 1 && 2
    """

    def __init__(self, confidence: str = "surely"):
        description = ["❌ Deprecated use of functions as constructor",
                       "Version of compiler higher than 0.4.22",
                       "The contract is vulnerable to safeguarding constructor with care"]
        super().__init__(
            "N/A",
            "CWE-665",
            "Constructor Safeguarding",
            description,
            "Critical",
            confidence,
        )
