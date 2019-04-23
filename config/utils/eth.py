from __future__ import division
from config.utils.address import AddressUtil
from web3 import Web3
from config.common.exception import CommonError,Error_Messages
import json
from config.common.utils import *
from config.utils.transaction import TransactionUtil

class EthUtil():
    def __init__(self,web3):
        self.web3 = web3
        self.address_util = AddressUtil(self.web3)
        self.transaction_util = TransactionUtil(self.address_util,self.web3)
    #获得eth余额
    def getEtherBalance(self,raw_address):
        address = self.address_util.toChecksumAddress(raw_address)
        if not address:
            return None
        balance = to_ether(self.web3.eth.getBalance(address))
        return balance
    
    #新建账户
    def newAccount(self,password):
        # password="bc502f8b-7823-49e7-bc5c-6f3d71bb50f9"
        return self.web3.personal.newAccount(password)
    
    #获取区块高度
    def get_block_height(self):
        return self.web3.eth.blockNumber
    
    #转化成最小单位
    def to_wei(self,raw_amount):
        return Web3.toWei(raw_amount,'ether')
    
    #获得gas price
    def get_gas_price(self):
        return self.web3.eth.gasPrice()
    
    #获得某个交易使用的以太币数量
    def get_transaction_fees(self,transaction_hash):
        is_mined = self.is_mined(transaction_hash)
        if  not is_mined:
            return is_mined
        transaction_receipt = self.web3.eth.getTransactionReceipt(transaction_hash) 
        gas_used = transaction_receipt['gasUsed']
        transaction = self.web3.eth.getTransaction(transaction_hash)
        gas_price =  transaction['gasPrice']  
        fees = to_ether(gas_used*gas_price)
        return fees

    #通过交易hash获得交易详情
    def get_transaction_details(self,transaction_hash):
        is_mined =  self.is_mined(transaction_hash)
        if not is_mined:
            return is_mined
        raw_transaction = self.web3.eth.getTransaction(transaction_hash)
        # raw_transaction['fees'] = self.get_transaction_fees(transaction_hash)
        tx_dict = dict(raw_transaction)
        tx_json= json.dumps(tx_dict, cls=HexJsonEncoder)
        raw_result = json.loads(tx_json)
        raw_result['fees'] = self.get_transaction_fees(transaction_hash)
        result = json.dumps(raw_result)
        # transaction = Web3. toJson(raw_transaction)
        print("result is {}".format(result))
        return str(result)
    
    #判断交易有没被打包
    def is_mined(self,transaction_hash):
        if not is_transaction_hash(transaction_hash):
            return None
        if self.web3.eth.getTransactionReceipt(transaction_hash):
            return True
        else:
            return False

    
            
    def transfer_ether(self,raw_address,password,to,raw_amount):
        address = self.address_util.toChecksumAddress(raw_address)

        from_balance = to_wei(self.getEtherBalance(raw_address))
        if from_balance<raw_amount:
            return None
        amount = to_wei(raw_amount)
        print("amount in transfer is {}".format(amount))
        print("to in transfer is {}".format(to))
        sendToBuyerResult = self.web3.personal.sendTransaction(
            {'from': address,'to':to,'value':amount},password)
        if (sendToBuyerResult):
            return self.web3.toHex(sendToBuyerResult)
        else:
            return False
        
        
    def send_transaction(self,signed_transaction):
        return self.transaction_util.send_transaction(signed_transaction)


    def get_nonce(self,address):
        return self.transaction_util.getNonce(address)

    def get_transactions(self,raw_address):
        address = self.address_util.toChecksumAddress(raw_address)


    # def get
    # def transfer(self,raw_to,raw_amount):
    #  nonce = self.web3.eth.getTransactionCount(ourAddress) 
    #  amount = self.to_wei(raw_amount)
    #  to = self.address_util.toChecksumAddress(raw_to)
    #  transaction = {
    #       'to': to,
    #       'value': amount,       
    #       'gasPrice': 1000000000,
    #       'nonce': nonce,
    #       'gas':200000
    #  }
    #  print("主链币余额{}".format(w3.eth.getBalance(ourAddress)))
    #  #签名
    #  signed = w3.eth.account.signTransaction(transaction, key)


    #  #When you run sendRawTransaction, you get back the hash of the transaction:
    #  transactionHash=w3.eth.sendRawTransaction(signed.rawTransaction)  
    #  # watingMined(transactionHash)
    #  print("waiting for mined")
    #  transaction=w3.eth.waitForTransactionReceipt(transactionHash, timeout=120)
    #  print("打包成功 接受地址余额是{}".format(w3.eth.getBalance(to)))



