from config.utils.transaction import TransactionUtil
from config.utils.address import AddressUtil
from config.common.transaction_base import Transaction_Base
from config.common.utils import *
from config.common.contract_base import Contract_Base
from config.common.exception import CommonError,Error_Messages
from urllib import request
class Vote_Util(Transaction_Base):
    def __init__(self,contract_util:Contract_Base):
        self.web3 = contract_util.web3
        self.contract = contract_util.contract_util.contract
        self.address_util = contract_util.address_util
        self.transaction_util = contract_util.transaction_util
    def vote(self,raw_from_address,raw_to,amount,operate_type,raw_sender,pri_key):
        if operate_type!=0 and operate_type!=1:
            print("操作类型错误")
            return None
        if not isinstance(amount,int):
            print("票amount只能是int")
            return None
        if amount<=0:
            print("票数不能为负数")
            return None
        from_address = self.address_util.toChecksumAddress(raw_from_address)
        to = self.address_util.toChecksumAddress(raw_to)
        if not (self.address_util.isAddress(from_address) and self.address_util.isAddress(to)):
            print("投票节点地址或投票发起账户不合法")
            return None
        sender=self.address_util.toChecksumAddress(raw_sender)
        if not sender:
            print("交易发起账户不合法")
            return None
        func="vote"
        raw_args = []
        raw_args.append(func)
        raw_args.append(from_address)
        raw_args.append(to)
        raw_args.append(amount)
        raw_args.append(operate_type)
        args = contract_func_serialization(raw_args)
        nonce=self.transaction_util.getNonce(sender)
        raw_transaction = self.build_raw_transaction(args,nonce)
        try:
            tx_receipt = self.transaction_util.sign_and_send(raw_transaction,nonce,pri_key,sender)    
            print("投票交易发起成功")
            return tx_receipt
        except Exception as e:
            # print(e.args[0]["message"])
            raise CommonError(e.args[0]["message"])

    def is_admin(self,raw_admin):
        admin = self.address_util.toChecksumAddress(raw_admin)
        if not admin:
            return None
        return self.contract.functions.isAdmin(admin).call()

    def build_raw_transaction(self,args,nonce):
        raw_transaction = None
        if not nonce:
            return None
        if len(args) < 1:
            print("请传入需要调用的函数名")
            return None
        func_name = args[0]
        if func_name == "vote":
            if len(args) != 5:
                print("参数数量错误")
            from_address = args[1]
            to = args[2]
            amount = args[3]
            operate_type = args[4]
            raw_transaction = self.contract.functions.vote(from_address,to,amount,operate_type)
        return raw_transaction
    

    #判断交易有没被打包
    def is_mined(self,transaction_hash):
        if not is_transaction_hash(transaction_hash):
            return None
        if self.web3.eth.getTransactionReceipt(transaction_hash):
            return True
        else:
            return False
    def get_amount(self,raw_address):
        address = self.address_util.toChecksumAddress(raw_address)
        if not address:
            return None
        return self.contract.functions.amounts(address).call()

    def get_who_vote_i_length(self,raw_address):
        address = self.address_util.toChecksumAddress(raw_address)
        if not address:
            return None
        return self.contract.functions.who_vote_i_length(address).call()

    def get_who_i_vote_to_length(self,raw_address):
        address = self.address_util.toChecksumAddress(raw_address)
        if not address:
            return None
        return self.contract.functions.who_i_vote_to_length(address).call()

    def get_who_i_vote_to(self,raw_address):
        result = []
        address = self.address_util.toChecksumAddress(raw_address)
        if not address:
            return None
        length = self.get_who_i_vote_to_length(address)
        print("length is {}".format(length))
        for index in range(length):
            per_item = {}
            raw_per_item = self.contract.functions.who_i_vote_to(address,index).call()
            per_item['receiver'] = raw_address = raw_per_item[0]
            per_item['amount'] = raw_address = raw_per_item[1]
            result.append(json.dumps(per_item))
        return result

    def get_who_vote_i(self,raw_address):
        result = []
        address = self.address_util.toChecksumAddress(raw_address)
        if not address:
            return None
        length = self.get_who_vote_i_length(address)
        for index in range(length):
            per_item = {}
            raw_per_item = self.contract.functions.who_vote_i(address,index).call()
            per_item['sender'] = raw_per_item[0]
            per_item['amount'] = raw_per_item[1]
            result.append(json.dumps(per_item))
        return result

    def get_candidate_length(self):
        return self.contract.functions.candidates_length().call()

    def get_candidates(self):
        length = self.get_candidate_length()
        print("candidates length is {}".format(length))
        result = [] 
        per_item = {}
        for index in range(length):
            candidate = self.contract.functions.candidates(index).call()
            ticket = self.get_amount(candidate)
            per_item['address'] = candidate 
            per_item['amount'] = ticket 
            result.append(json.dumps(per_item)) 
        return result
    def new_account(self):
        url = "http://localhost:9527"
        u = request.urlopen(url)
        raw_result = u.read()
        result = raw_result.decode('utf8').replace("'", '"')
        print("new account is {}".format(result))
        return result