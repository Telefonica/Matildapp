// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.5/contracts/utils/cryptography/ECDSA.sol";

contract MultiSigWallet {
    using ECDSA for bytes32;

    address[] public owners;

    modifier isOwner(){
        bool isOneOwner = false;
        for (uint i = 0; i < owners.length; i++) {
            isOneOwner = owners[i] == msg.sender || isOneOwner;
        }
        require(isOneOwner,"Not the owner");
        _;
    }

    constructor() payable {
        owners.push(msg.sender);
    }

    function addOwner(address _owner) public isOwner {
        owners.push(_owner);
    }

    function deposit() external payable {}

    function transfer(
        address _to,
        uint _amount,
        bytes[] memory _sigs
    ) external {
        bytes32 txHash = getTxHash(_to, _amount);
        require(_checkSigs(_sigs, txHash), "invalid sig");

        (bool sent, ) = _to.call{value: _amount}("");
        require(sent, "Failed to send Ether");
    }

    function getTxHash(address _to, uint _amount) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_to, _amount));
    }

    function _checkSigs(bytes[] memory _sigs, bytes32 _txHash)
        private
        view
        returns (bool)
    {
        bytes32 ethSignedHash = _txHash.toEthSignedMessageHash();

        for (uint i = 0; i < _sigs.length; i++) {
            address signer = ethSignedHash.recover(_sigs[i]);
            bool valid = signer == owners[i];

            if (!valid) {
                return false;
            }
        }

        return true;
    }

    function getBalance() public view returns(uint){
        return address(this).balance;
    }
}
