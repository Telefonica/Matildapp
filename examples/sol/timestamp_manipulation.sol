// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.13;

contract RandomGenerator{

    function random(uint Max) view private returns (uint256 result){
        uint256 salt =  block.timestamp;
        //get the best seed for randomness
        uint256 x = salt * 100/Max;
        uint256 y = salt * block.number/(salt % 5) ;
        uint256 seed = block.number/3 + (salt % 300) + y;
        uint256 h = uint256(blockhash(seed));

        return uint256((h / x)) % Max + 1; //random number between 1 and Max
    }
}
