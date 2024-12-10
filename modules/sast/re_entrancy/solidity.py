from console import print_ok
from lib.contract_solidity import Solidity_Contract
from lib.vulnerabilities.re_entrancy import Re_Entrancy
from module import Module
from utils import get_solidity_contract


class CustomModule(Module):
    """
    Module to detect the vulnerability: Reentrancy
    See lib.vulnerabilities.re_entrancy for more info
    """

    def __init__(self):
        information = {
            "Name": "Reentrancy Solidity check",
            "Description": Re_Entrancy.info,
            "Author": "@chgara",
        }

        # -----------name-----default_value--description--required?
        options = {"contract": [None, "Contract path, should be a solidity file", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    def check_contract(self, contract: Solidity_Contract) -> None:
        """
        Check the contract in search of reentrancy
        :param contract: The solidity smart contract
        """
        order = []
        nline = 0

        for line in contract.code:
            if "call{value:" in line:
                element = {}
                element["value"] = "call{value:"
                element["nline"] = nline
                order.append(element)
            if any(op in line for op in ["-=", "-", "+=", "+"]):
                element = {}
                element["value"] = "operation"
                element["nline"] = nline
                order.append(element)
            nline += 1

        i = 0
        if len(order) >= 2:
            for e in order:
                if e["value"] == "operation":
                    continue
                if i + 1 < len(order):
                    next = order[i + 1]
                    if next["value"] == "operation":
                        if (next["nline"] - e["nline"]) <= 2:
                            reentrancy_vuln = Re_Entrancy()
                            reentrancy_vuln.add_description(
                                f"    found in line {next.get('nline')} and {e.get('nline')} of contract {contract.name}"
                            )
                            reentrancy_vuln.add_code(f"    {e.get('value')}")
                            reentrancy_vuln.print_vulnerability()
                            return

        print_ok("✅ Reentrancy not found, all ok")

    def run_module(self) -> None:
        contract = get_solidity_contract(self.args)
        return self.check_contract(contract) if contract else None
