
import uuid
class AddressUtil(object):
    def __init__(self,web3):
        self.web3 = web3
    def isAddress(self,address):
        return self.web3.isAddress(address)
    
    def toChecksumAddress(self,address):
        if  not self.web3.isAddress(address):
            print("地址不合法")
            return None
        if not self.web3.isChecksumAddress(address):
            return self.web3.toChecksumAddress(address)
        else:
            return address
    

