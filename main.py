from config.common.contract_base import Contract_Base
# from contract.contract_config import * as sender_config
from contract.contract_config import *
from vote.vote_util import Vote_Util
from flask import request,Flask,abort
from config.common.exception import Error_Messages
from config.common.response import Result_Factory
from config.common.exception import CommonError,Error_Messages
from config.utils.address import AddressUtil
from config.common.response import Result_Util
from config.utils.eth import EthUtil
import uuid
from config.common.utils import *
contract_base = Contract_Base(contract_address ,abi,ipcPath=ipc_path,rpcPath=None)
vote_util = Vote_Util(contract_base)
address_util = AddressUtil(contract_base.web3)
eth_util = EthUtil(contract_base.web3)
app = Flask(__name__)
app.secret_key=bytes(str(uuid.uuid4()),'utf-8')

@app.before_request
def limit_remote_addr():
    addr = request.remote_addr
<<<<<<< HEAD
    if addr != '127.0.0.1' and addr != '47.102.96.204' and addr!= '106.14.9.53' and addr!="39.98.199.155":
        abort(403)  # Forbidde


=======
    if addr != '127.0.0.1' and addr != '':
        abort(403)  # Forbidde
>>>>>>> a6d7b5e3f2ea9058a99a5a0578124a822d246eaf
@app.route('/vote',methods=['Post'])
def vote():
    try:
        form  = Result_Util.get_json_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'sender'
        raw_from =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result


    from_account = address_util.toChecksumAddress(raw_from)

    try:
        field_name = 'to'
        raw_to =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    to = address_util.toChecksumAddress(raw_to)

    if not (from_account and to):
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result

    try:
        field_name = 'operate_type'
        operate_type =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    if  operate_type is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Operate_Type_None_Error)
        return result

    if operate_type!=0 and operate_type!=1:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Operate_Type_Error)
        return result
    try:
        field_name = 'amount'
        raw_amount =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    if raw_amount is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Vote_Amount_None_Error)
        return result

    amount = raw_amount


    if not isinstance(amount,int):
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Vote_Amount_Type_Error)
        return result

    print("参数是  {} {} {} {}".format(from_account,to,amount,operate_type))
    # if from_account and password,to,amount
    try:
        details= vote_util.vote(from_account,to,amount,operate_type,owner,owner_pri_key)
        if details is None:
            result = Result_Factory.generate_result(status=False,message=Error_Messages.No_Enough_Balance)
            return result
    except CommonError as e:
        print(e)
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result

@app.route('/is_finish')
def is_finish():
    try:
        args  = Result_Util.get_args_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'transaction_hash'
        transaction_hash =  Result_Util.get_field_from_request_args(args,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    details= vote_util.is_mined(transaction_hash)
    if details is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transaction_Id_Error)
        return result

    result = Result_Factory.generate_result(status=True,data=details)
    return result

@app.route('/get_amount')
def get_amount():
    try:
        args  = Result_Util.get_args_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'address'
        address =  Result_Util.get_field_from_request_args(args,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    details= vote_util.get_amount(address)
    if details is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result


@app.route('/who_vote_i')
def who_vote_i():
    try:
        args  = Result_Util.get_args_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'address'
        address =  Result_Util.get_field_from_request_args(args,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    details= vote_util.get_who_vote_i(address)
    if details is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result

@app.route('/who_i_vote_to')
def who_i_vote_to():
    try:
        args  = Result_Util.get_args_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'address'
        address =  Result_Util.get_field_from_request_args(args,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    details= vote_util.get_who_i_vote_to(address)
    if details is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result




@app.route('/transfer',methods=['Post'])
def transfer():
    try:
        form  = Result_Util.get_json_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    # raw_amount = owner
    from_account = address_util.toChecksumAddress(owner)
    try:
        field_name = 'to'
        raw_to =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    to = address_util.toChecksumAddress(raw_to)
    # if from_account == to:
    #     result = Result_Factory.generate_result(status=False,message=Error_Messages.From_And_to_Same_Error)
    #     return result
    if not (from_account and to):
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result

    try:
        field_name = 'amount'
        raw_amount =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    if raw_amount is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_None_Error)
        return result
    amount = raw_amount
    if isinstance(amount,str):
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_type_Error)
        return result
    sender_key  = owner_pri_key
    print("参数是  {} {} {} {}".format(from_account,sender_key,to,amount))
    # if from_account and password,to,amount
    try:
        details= eth_util.sign_transfer(from_account,sender_key,to,amount)
        if details is None:
            result = Result_Factory.generate_result(status=False,message=Error_Messages.No_Enough_Balance)
            return result
    except CommonError as e:
        print(e)
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result



# @app.route('/transfer',methods=['Post'])
# def transfer():
#     try:
#         form  = Result_Util.get_json_from_request(request)
#     except CommonError as e:
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result

#     # raw_amount = owner
#     from_account = address_util.toChecksumAddress(owner)
#     try:
#         field_name = 'to'
#         raw_to =  Result_Util.get_field_from_json(form,field_name)
#     except CommonError as e:
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result
#     to = address_util.toChecksumAddress(raw_to)
#     # if from_account == to:
#     #     result = Result_Factory.generate_result(status=False,message=Error_Messages.From_And_to_Same_Error)
#     #     return result
#     if not (from_account and to):
#         result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
#         return result
#     password = owner_password

#     try:
#         field_name = 'amount'
#         raw_amount =  Result_Util.get_field_from_json(form,field_name)
#     except CommonError as e:
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result

#     if raw_amount is None:
#         result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_None_Error)
#         return result
#     amount = raw_amount
#     if isinstance(amount,str):
#         result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_type_Error)
#         return result
#     print("参数是  {} {} {} {}".format(from_account,password,to,amount))
#     # if from_account and password,to,amount
#     try:
#         details= eth_util.transfer_ether(from_account,password,to,amount)
#         if details is None:
#             result = Result_Factory.generate_result(status=False,message=Error_Messages.No_Enough_Balance)
#             return result
#     except Exception as e:
#         print(e)
#         result = Result_Factory.generate_result(status=False,message=e.args[0]['message'])
#         return result
#     else:
#         result = Result_Factory.generate_result(status=True,data=details)
#         return result


@app.route('/get_balance')
def get_eth_balance():

    try:
        args  = Result_Util.get_args_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'address'
        address =  Result_Util.get_field_from_request_args(args,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    details= eth_util.getEtherBalance(address)
    if details is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result

@app.route('/is_mined')
def is_mined():
    try:
        args  = Result_Util.get_args_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    try:
        field_name = 'transaction_hash'
        transaction_hash =  Result_Util.get_field_from_request_args(args,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    details= eth_util.is_mined(transaction_hash)
    if details is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transaction_Id_Error)
        return result
    result = Result_Factory.generate_result(status=True,data=details)
    return result
@app.route('/get_candidates')
def get_candidate():
    details= vote_util.get_candidates()
    result = Result_Factory.generate_result(status=True,data=details)
    return result

@app.route('/create_account')
def create_account():
    details=None
    while True:
        details= vote_util.new_account()
        if is_valid_key(details):
            break
    result = Result_Factory.generate_result(status=True,data=details)
    return result

@app.route('/send_signed_transaction',methods=['Post'])
def send_transaction():
    try:
        form  = Result_Util.get_json_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    try:
        field_name = 'transaction'
        transaction  =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
<<<<<<< HEAD

=======
    
>>>>>>> a6d7b5e3f2ea9058a99a5a0578124a822d246eaf

    if not transaction:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transaction_Hash_None_Error)
        return result
<<<<<<< HEAD

    # if from_account and password,to,amount
    try:
        details= eth_util.send_transaction(transaction)
=======
    
    # if from_account and password,to,amount
    try:
        details= eth_util.send_transaction(transaction)    
>>>>>>> a6d7b5e3f2ea9058a99a5a0578124a822d246eaf
    except Exception as e:
        print(e)
        result = Result_Factory.generate_result(status=False,message=e.args[0]['message'])
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result
<<<<<<< HEAD
# @app.route('/generate',methods=['Post'])
# def generate_transfer_transaction():
#     try:
#         form  = Result_Util.get_json_from_request(request)
#     except CommonError as e:
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result

#     # raw_amount = owner
#     from_account = address_util.toChecksumAddress(owner)
#     try:
#         field_name = 'to'
#         raw_to =  Result_Util.get_field_from_json(form,field_name)
#     except CommonError as e:
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result
#     to = address_util.toChecksumAddress(raw_to)
#     # if from_account == to:
#     #     result = Result_Factory.generate_result(status=False,message=Error_Messages.From_And_to_Same_Error)
#     #     return result
#     if not (from_account and to):
#         result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
#         return result

#     try:
#         field_name = 'amount'
#         raw_amount =  Result_Util.get_field_from_json(form,field_name)
#     except CommonError as e:
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result

#     if raw_amount is None:
#         result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_None_Error)
#         return result
#     amount = raw_amount
#     if isinstance(amount,str):
#         result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_type_Error)
#         return result
#     sender_key  = owner_pri_key
#     print("参数是  {} {} {} {}".format(from_account,sender_key,to,amount))
#     # if from_account and password,to,amount
#     try:
#         details= eth_util.generate_transfer_transaction(from_account,sender_key,to,amount)
#         if details is None:
#             result = Result_Factory.generate_result(status=False,message=Error_Messages.No_Enough_Balance)
#             return result
#     except CommonError as e:
#         print(e)
#         result = Result_Factory.generate_result(status=False,message=e.args[0])
#         return result
#     else:
#         result = Result_Factory.generate_result(status=True,data=details)
#         return result

=======
@app.route('/generate',methods=['Post'])
def generate_transfer_transaction():
    try:
        form  = Result_Util.get_json_from_request(request)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    
    # raw_amount = owner
    from_account = address_util.toChecksumAddress(owner)
    try:
        field_name = 'to'
        raw_to =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    to = address_util.toChecksumAddress(raw_to)
    # if from_account == to:
    #     result = Result_Factory.generate_result(status=False,message=Error_Messages.From_And_to_Same_Error)
    #     return result
    if not (from_account and to):
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Address_Length_Error)
        return result

    try:
        field_name = 'amount'
        raw_amount =  Result_Util.get_field_from_json(form,field_name)
    except CommonError as e:
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result

    if raw_amount is None:
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_None_Error)
        return result
    amount = raw_amount
    if isinstance(amount,str):
        result = Result_Factory.generate_result(status=False,message=Error_Messages.Transfer_Amount_type_Error)
        return result
    sender_key  = owner_pri_key
    print("参数是  {} {} {} {}".format(from_account,sender_key,to,amount))
    # if from_account and password,to,amount
    try:
        details= eth_util.generate_transfer_transaction(from_account,sender_key,to,amount)        
        if details is None:
            result = Result_Factory.generate_result(status=False,message=Error_Messages.No_Enough_Balance)
            return result    
    except CommonError as e:
        print(e)
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result
    
>>>>>>> a6d7b5e3f2ea9058a99a5a0578124a822d246eaf

@app.route('/')
def root():
    return "root index "


if __name__ == "__main__":
    print(app.url_map)
<<<<<<< HEAD
    app.run(host="0.0.0.0",port=3333)
=======
    app.run(debug=True)




#  curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{ "transaction": "0xf86d8201558307a120831e848094df96f2fc9e7ccd8a5cd517876391bcbb1cf315a1880de0b6b3a7640000801ba03b9474623bfed37c95315510c2c95f40f71ffad0a33ddad664d80eb27e936156a04f648bab4078e887ebcd642cc354abcfef7fdec95c7cb2a364e3fb16b2b42105"}' http://127.0.0.1:3333/send_signed_transaction
>>>>>>> a6d7b5e3f2ea9058a99a5a0578124a822d246eaf
