pragma solidity ^0.5.7;
contract owned {
    address public owner;
     constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    //转移所有权
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }

}

contract admin
{
    mapping(address => bool) public isAdmin;
}


contract peer_vote is admin,owned 
{
    struct receiver  //投票人信息
    {
        address from_address;
        uint256 amount;
    }
    mapping (address => uint256) public  amounts; /// 获得竞选者获得的票数
    
    mapping (address => bool ) public is_candidate; // 判断一个地址是不是竞选地址
    
    mapping(address=> receiver[]) public who_vote_i;  ///谁投给了我,投了多少  
    mapping(address=> receiver[]) public who_i_vote_to;   ///我投给谁,投了多少
    address[] public candidates; 
    mapping(address=> uint256) public who_vote_i_length;
    mapping(address=> uint256) public who_i_vote_to_length;
    uint256 public candidates_length=0;
    modifier candidate(address to)
    {
        require(is_candidate[to] == true);
        _;
    }

    function  vote(address sender, address to,uint256  amount,uint8 operate_type) public owner_or_admin //传入投给谁,投多少,投票类型
    {
        assert(amount > 0);
        if(operate_type == 0)  //参加竞选.投给自己
        {
            if (is_candidate[sender] ==false)
            {
                is_candidate[sender] = true;
                candidates.push(sender);
                candidates_length++;
            }
            
            who_vote_i[sender].push(receiver(sender,amount));
            amounts[sender]+=amount;
            who_i_vote_to[sender].push(receiver(sender,amount));    //应该push(to,amount)但是有可能to和sender不一样,,以from为准
            who_vote_i_length[sender]++;
            who_i_vote_to_length[sender]++;
        }
        else if (operate_type == 1) // 投别人
        {
            who_vote_i[to].push(receiver(sender,amount));
            amounts[to]+=amount;
            who_i_vote_to[sender].push(receiver(to,amount));    //应该push(to,amount)但是有可能to和sender不一样,,以from为准
            who_vote_i_length[to]++;
            who_i_vote_to_length[sender]++;
        }
    }
    
    function setAdmin(address new_admin) onlyOwner public
    {
        isAdmin[new_admin] = true;
    }
    modifier owner_or_admin
    {
        require(msg.sender ==owner || isAdmin[msg.sender] == true);
        _;
    }
    
}