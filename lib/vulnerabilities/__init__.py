from printib import *


class Vulnerability:
    """
    Class to show vulnerability info to the user
    :param swc: The SWC ID
    :param cwe_related: The CWE ID
    :param title: The title of the vulnerability
    :param description: A list of lines for describing the vulnerability to the user
    :param effect: The effect of the vulnerability
    :param confidence: The confidence of the vulnerability
    """
    swc: (int | str)
    cwe_realted: str
    title: str
    description: list[str]
    effect: str
    confidence: str

    # set these statically on the inheriting class
    info: str = "Vulnerability info"
    code: list[str]

    def __init__(self, swc: (int | str),
                 cve_related: str,
                 title: str,
                 description: list[str],
                 effect: str,
                 confidence: str = "Potential"):
        self.swc = swc
        self.code = []
        self.title = title
        self.effect = effect
        self.confidence = confidence
        self.cwe_realted = cve_related
        self.description = description

    def print_vulnerability(self) -> None:
        """
        Print the vulnerability info
        """
        print()
        lines: list[str] = str(self).splitlines()
        for line in lines:
            print_info(line)
        print()

    def add_description(self, line: str) -> None:
        """
        Adds a line to the description
        """
        self.description.append(line)

    def add_code(self, code: str) -> None:
        """
        Add code to the vulnerability
        """
        self.code.append(code)

    def __str__(self) -> str:
        """
        Return the vulnerability info as a string
        """
        result: str = ""
        result += f"Vulnerability found \033[91m({self.confidence})\033[0m\n"
        result += f"    -  SWC: {self.swc}\n"
        result += f"    -  CWE-realted: {self.cwe_realted}\n"
        result += f"    -  Title: \033[1m{self.title}\033[0m\n"
        result += f"    -  Effect: \033[91m{self.effect}\033[0m\n"
        result += f"    -  Description:\n"
        for line in self.description:
            result += f"      >  {line}\n"
        if self.code != []:
            for code_line in self.code:
                result += f"      >  \033[1m\x1B[3m{code_line}\x1B[0m\033[0m\n"
        if type(self.swc) == int:
            result += f"    -  More info: https://swcregistry.io/docs/SWC-{self.swc}\n"
        return result
