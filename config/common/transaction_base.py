from abc import ABCMeta,abstractmethod
class Transaction_Base(metaclass=ABCMeta):
    @abstractmethod
    def build_raw_transaction(self,args,nonce):
        raise NotImplementedError