from __future__ import division
import json
from hexbytes import HexBytes
from web3 import Web3
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