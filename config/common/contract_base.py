from web3 import Web3, HTTPProvider,IPCProvider
from web3.middleware import geth_poa_middleware
import time 
from  .admin import AdminUtil
from config.utils.address import AddressUtil
from config.utils.transaction import TransactionUtil
from config.utils.eth import EthUtil
from config.utils.contract import Contract_Util
class Contract_Base(object):
    def __init__(self,contractAddress,abi,ipcPath:None,rpcPath:None):
        assert ipcPath or rpcPath,"请提供ipc或rpc路径"
        if ipcPath:
            self.web3 = Web3(IPCProvider(ipcPath))
        else:
            self.web3=Web3(Web3.HTTPProvider(rpcPath))
        self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
        assert self.web3.isConnected(),'connect fail 请打开节点'
        self.address_util =  AddressUtil(self.web3)
        self.contract_util = Contract_Util(abi,contractAddress,self.web3)
        self.transaction_util =TransactionUtil(self.address_util,self.web3,self.contract_util.contract)

