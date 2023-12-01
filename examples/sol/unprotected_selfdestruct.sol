// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.1;

import '@openzeppelin/contracts/access/Ownable.sol';

contract Wallet is Ownable {
    function executeTransacion(address _to, bytes memory data) public onlyOwner {
        (bool success, ) = _to.call(data);
        require(success, 'Transaction failed.');
    }
    function destroyWallet(address to) public onlyOwner {
        selfdestruct(to);
    }
}
