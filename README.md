![Supported Python versions](https://img.shields.io/badge/python-3.9-blue.svg?style=flat-square)
![License](https://img.shields.io/badge/license-AGPL-green.svg?style=flat-square)

# **Matildapp**

```
                __  .__.__       .___
  _____ _____ _/  |_|__|  |    __| _/____  ______ ______
 /     \\__  \\   __\    |  |   / __ |\__  \ \____ \\____ \
|  Y Y  \/ __ \|  | |  |  |__/ /_/ | / __ \|  |_> >  |_> >
|__|_|  (____  /__| |__|____/\____ |(____  /   __/|   __/
      \/     \/                   \/     \/|__|   |__|
```

In our modern, interconnected world, the concept of Web3, also known as the decentralized web, represents the next significant shift in Internet technology. Web3, underpinned by blockchain technology and smart contracts, offers unprecedented decentralization, transparency, and user sovereignty possibilities. However, with these new possibilities come new challenges – one of the most crucial is security. Web3's decentralized nature eliminates central points of failure typical in Web2 applications, leading many to view it as inherently more secure. However, the security dynamics in Web3 are different, and a unique set of vulnerabilities has emerged. The secure design, development, and operation of Web3 applications and platforms have become crucial skills in the rapidly evolving digital landscape. It's no longer sufficient to build on top of blockchain technologies; developers, cybersecurity professionals, and even end-users must grasp the principles of securing these systems.

'**Matildapp**' (Multi Analysis Toolkit -by IdeasLocas- on DAPPs) is an Open Source project providing a framework for Web3 environments in the field of cybersecurity and pentesting. The tool offers
modules to interact with different types of blockchains and to conduct SAST and DAST evaluations of potential vulnerabilities in smart contracts. The tool is designed to be modular, allowing for the addition of new modules and functionalities.

# Prerequisities

'_Matildapp_' is written in Python and uses libraries to work with Web3 such as `pyweb3` and `py-solc-x`. Version management of these libraries is crucial, as well as the Python version used. It has been tested to work in a Python environment with version 3.10.14 and pyweb3 version 5.31.4 and py-solc-x version 2.0.2.

Other versions of Python and the libraries could cause issues preventing the tool from running correctly.

A `requirements.txt` file should be executed the first time the tool is started using `pip install -r requirements.txt`. Again, the pip version should correspond to a tested Python version like 3.10.14.

For working in a blockchain test environment, it is also necessary to have a utility that provides this service. Tools like Ganache or Hardhat can be used for this purpose.

# Usage

```[python]
python sc.py
```

# License

This project is licensed under the terms of the GNU Affero General Public License v3.0.

# Contact

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. WHENEVER YOU MAKE A CONTRIBUTION TO A REPOSITORY CONTAINING NOTICE OF A LICENSE, YOU LICENSE YOUR CONTRIBUTION UNDER THE SAME TERMS, AND YOU AGREE THAT YOU HAVE THE RIGHT TO LICENSE YOUR CONTRIBUTION UNDER THOSE TERMS. IF YOU HAVE A SEPARATE AGREEMENT TO LICENSE YOUR CONTRIBUTIONS UNDER DIFFERENT TERMS, SUCH AS A CONTRIBUTOR LICENSE AGREEMENT, THAT AGREEMENT WILL SUPERSEDE.

This software doesn't have a QA Process. This software is a Proof of Concept.

If you have any problems, you can contact:

ideaslocas@telefonica.com
