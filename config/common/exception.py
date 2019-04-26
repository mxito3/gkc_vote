
class CommonError(Exception):
    def __init__(self,message):
        super().__init__(message)
        self.message = message
        

class Error_Messages():
    Transaction_Id_Error = "the length of transaction id should be 66 and prefix with 0x"
    Transaction_Not_Mined = "no such transaction or transaction has not been mined "
    Address_Length_Error = "invalid address "
    Password_None_Error = "password can't be empty"
    Transfer_Amount_None_Error = "transfer amount can't be empty"
    Transfer_Amount_type_Error = "transfer amount must be a number"
    Password_Error="password wrong"
    Transaction_Hash_None_Error = "transaction hash can't be empty"
    Transaction_Hash_Wrong_Error = "invalid sign"
    Invalid_Post_Format = "invalid parameter format,please use json"
    No_Such_field = "please pass {} field"
    NO_Requst_Args_Error = "please pass args "
    From_And_to_Same_Error = "from address and to address can't be the same "
    No_Enough_Balance = "from address has no enough balance "



    '''
        投票
    '''
    Operate_Type_Error  = 'operate type can only be 0 or 1 '
    Operate_Type_None_Error = " operate type can't be empty"
    Vote_Amount_None_Error = "vote amount can't be empty "
    Vote_Amount_Type_Error = "vote amount type can only be int"
    def __init__(self):
        pass
        


