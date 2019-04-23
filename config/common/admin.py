from config.utils.transaction import TransactionUtil
from config.utils.address import AddressUtil
# from config.utils import common
from config.common.utils import *
from config.common.transaction_base import Transaction_Base
class AdminUtil(Transaction_Base):
    def __init__(self,contract_util):
        self.web3 = contract_util.web3
        self.contract = contract_util.contract_util.contract
        self.address_util = contract_util.address_util
        self.transaction_util = contract_util.transaction_util
        self.key = contract_util.key
    def set_admin(self,rawAddress,key,raw_sender):
        if not (self.address_util.isAddress(rawAddress) and self.address_util.isAddress(raw_sender)):
            print("{}或{}不是合法地址".format(rawAddress,sender))
            return False
        address  = self.web3.toChecksumAddress(rawAddress)
        sender=self.web3.toChecksumAddress(raw_sender)
        func="setAdmin"
        raw_args = []
        raw_args.append(func)
        raw_args.append(address)
        args = contract_func_serialization(raw_args)
        nonce=self.transaction_util.getNonce(sender)
        raw_transaction = self.build_raw_transaction(args,nonce)
        tx_receipt = self.transaction_util.sign_and_send(raw_transaction,nonce,key,sender)
        if tx_receipt:
            print("设置管理员 "+rawAddress+" 交易打包成功,hash值是" + tx_receipt)
            return True 
        else:
            return False

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
        if func_name == "setAdmin":
            if len(args) != 2:
                print("请输入需要设置的管理员账户")
            address = args[1]
            raw_transaction = self.contract.functions.setAdmin(address)
        return raw_transaction