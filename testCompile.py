from solcx import *
from solcx.install import Version

contract_path = './examples/sol/array_length_manipulation.sol'

with open(contract_path) as f:
    contract_content = f.read()

version = next((line.split()[2].strip(";").strip(
    '^') for line in contract_content.splitlines() if line.startswith("pragma ")), '')

if version == '':
    print("No version specified")
    exit(1)

installed = next(
    (v for v in get_installed_solc_versions() if str(v) == version), None)

if installed:
    print(f'Using solc version {version}')
    set_solc_version(installed)
    version = installed
else:
    version = install_solc(version, show_progress=True)

try:
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_path: {"content": contract_content}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": [],
                        "": [
                            "ast",
                        ]
                    }
                }
            },
        },
        solc_version=version,
    )
    keys = compiled.keys()
    print(keys)
    # print(compiled['sources'])
    for error in compiled['errors']:
        print('\n\n\n')
        print(error['formattedMessage'])
except Exception as e:
    print(e)
