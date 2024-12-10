// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.1;

import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

contract Token is Ownable, ERC20 {
	constructor () ERC20("HOLA","H") public {
		_mint(tx.origin, 10000 * (10**uint256(decimals())));
	}

	function mint(address _to, uint256 amount) public onlyOwner {
		_mint(_to, amount * (10**uint256(decimals())));
	}

	function burn(address _from, uint256 amount) external onlyOwner {
		_burn(_from, amount * (10**uint256(decimals())));
	}

    function unuafeDelegateCall(address _to, bytes memory _data) public onlyOwner {
        (bool success, bytes memory returnData) = _to.delegatecall(_data);
        require(success, "delegatecall failed");
    }
}
