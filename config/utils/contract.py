class Contract_Util(object):
    def __init__(self,abi,address,web3):
        self.abi =abi
        self.web3 = web3
        self.contractAddress = self.web3.toChecksumAddress(address)
        self.contract = self.getContract()
    
    def getContract(self):
        contract = self.web3.eth.contract(address=self.contractAddress, abi=self.abi)
        return contract