from __future__ import division
import json,uuid
from hexbytes import HexBytes
from web3 import Web3
from eth_account import Account
class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)

def contract_func_serialization(paras):
        args=[]
        for index in range(len(paras)):
                args.append(paras[index])
        return args
#判断交易hash值是否合法    
def is_transaction_hash(transaction_hash):
        if len(transaction_hash) == 66:
                return True
        else:
                return False


def to_ether(number):
        print("number in to_ether {}".format(number))
        return number/10**18
def to_wei(number):
        return Web3.toWei(number,'ether')
def decode_transaction(raw_transaction):
        tx_dict = dict(raw_transaction)
        transaction= json.dumps(tx_dict, cls=HexJsonEncoder)
        # transaction = json.dumps(transaction_json)
        return transaction
def deal_with_transaction_except(e_args):
        message_json = e_args[0]
        message_obj = json.loads(message_json)
        message = message_obj['message']
        return message


def is_valid_key(key_pair):
        # print(type(key_pair))
        invalid = {}
        detials_json = json.loads(key_pair)
        # print("details is {}".format(detials_json))
        private_key = detials_json['private_key']
        account = detials_json['address']
        if len(account)!=42 or len(private_key)!=66:
                print("生成了无效地址,地址长度是{}，私钥长度是{}".format(len(account),len(private_key)))
                # invalid['{}'.format]
                return False
        else:
                return True

def new_key_pair():
        password =str(uuid.uuid4())
        account = Account.create(password)
        private_key = account.privateKey.hex()
        address = account.address
        key_pair = {}
        key_pair['private_key'] = private_key
        key_pair['address'] = address
        key_pair_json = json.dumps(key_pair)
        return key_pair_json

