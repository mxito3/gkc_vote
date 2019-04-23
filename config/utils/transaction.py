from .address import AddressUtil
class TransactionUtil(object):
    def __init__(self,address_util:AddressUtil,web3,contract=None):
        self.address_util = address_util
        self.web3 = web3
        self.contract = contract
    def getNonce(self,raw_address):
        addr=self.address_util.toChecksumAddress(raw_address)
        if not addr:
            return None
        else:
            return self.web3.eth.getTransactionCount(addr)
    def build_Transaction(self,raw_transaction,nonce,sender):
        transaction=raw_transaction.buildTransaction({
                'nonce': nonce,
                'from':sender
        })
        return transaction
    def send_transaction(self,raw_transaction):

        transactionHash=self.web3.eth.sendRawTransaction(raw_transaction) 
        return transactionHash.hex()

    def waitingMined(self,transaction_hash):
        print("waiting mined")
        try:
            tx_receipt=self.web3.eth.waitForTransactionReceipt(transaction_hash, timeout=120).transactionHash.hex()
            return tx_receipt
        except Exception as e:
            print(e)
            print("交易在120秒后未被确认")
            return None
    def sign_and_send(self,raw_transaction,nonce,key,sender):
        transaction = self.build_Transaction(raw_transaction,nonce,sender)
        signed = self.web3.eth.account.signTransaction(transaction,key)
        transaction_hash=self.send_transaction(signed.rawTransaction) 
        # if not transactionHash:
        #     return None
        # tx_receipt=self.waitingMined(transactionHash)
        # if not tx_receipt:
            # return None
        return transaction_hash