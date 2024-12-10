// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.5.0;

contract VulnerableWallet {
    event OwnerAdded(address);
    event TransactionProposed(address , bytes);

    uint256 public nonce;
    address[] public owners;
    uint[] transactions;

    mapping(uint256 => bytes) transactionData;
    mapping(uint256 => mapping(address => bool)) transactionConfirmations;

    modifier onlyOwner() {
        bool isOwner = false;
        for (uint256 i = 0; i < owners.length; i++) {
            if (owners[i] == msg.sender) {
                isOwner = true;
                break;
            }
        }
        require(isOwner, "Not an owner");
        _;
    }

    constructor (address[] memory _owners) public {
        owners = _owners;
    }

    function executeTransacion(uint256 _nonce) public onlyOwner {
        require(_isConfirmed(_nonce), 'Transaction not confirmed by all owners');
        (bool success, ) = address(this).delegatecall(transactionData[nonce]);
    }

    function proposeTransaction(address _to, bytes memory data) public onlyOwner {
        transactionData[nonce] = data;
        transactionConfirmations[nonce][msg.sender] = true;
        nonce++;
    }

    function confirmTransaction(uint256 _nonce) public onlyOwner {
        transactionConfirmations[_nonce][msg.sender] = true;
    }

    // VULNERABLE FUNCTION -> can be used to overwrite all contract storage
    function addOwner(address newOwner, uint256 newLenght) public onlyOwner {
        owners.length = newLenght;
        owners[newLenght - 1] = newOwner;
    }

    function _isConfirmed(uint256 _nonce) internal view returns (bool) {
        uint256 count = 0;
        for (uint256 i = 0; i < owners.length; i++) {
            if (transactionConfirmations[nonce][owners[i]]) {
                count += 1;
            }
        }
        return count >= owners.length / 2 + 1;
    }
}
