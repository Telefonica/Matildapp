from lib.vulnerabilities import Vulnerability


class Array_Length_Manipulation(Vulnerability):
    info = """
    SWC: N/A
    CWE RELATED: CWE-121
    Title: Array Length Manipulation
    Description: EVM memory works storing unsigned integers of 256 bits in each memory position,
                 and you access to it by a 256 bit integer index. All memory values stored will
                 be padded to 256 bits and to access you will need the corresponding 256bit index.

                 Arrays in solidity are dynamic, this means that the can be resized and can occupy
                 more storage slots in the future. This slots can overlap with other variables in
                 the contract if the array is resized to 2^256 length. So if the array length can be
                 manipulated to 2^256-1 and the user have access to the array eventually he will have
                 access to manage all the storage of the contract.

                 The access via indexing to array position are done hashing the integer with the array
                 name variable, but since the keckack256 function produces 256 bits the user can control
                 all the storage of the contract.

    Detection cases: Is vulnerable to array length manipulation if
        1. Storage array exists
        2. array.length = value is used
        3. The value of 2. is a value easily manipulable
        4. Normal user have access to the array
        Final conlcusion: 1. and 2. and 3. and 4.
    """

    def __init__(self, confidence: str = "surely"):
        description = ["💀 Array length manipulation vulnerability detected",
                       "Can be used to overwrite all the storage of the contract"]
        super().__init__(
            "N/A",
            "CWE-121",
            "Array Length Manipulation",
            description,
            "Critical",
            confidence,
        )
