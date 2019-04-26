
from config.common.contract_base import Contract_Base
# from contract.contract_config import * as sender_config
from contract.contract_config import *
from vote.vote_util import Vote_Util
from flask import request,Flask
from config.common.exception import Error_Messages
from config.common.response import Result_Factory
from config.common.exception import CommonError,Error_Messages
from config.utils.address import AddressUtil
from config.common.response import Result_Util
from config.utils.eth import EthUtil
import uuid 
contract_base = Contract_Base(contract_address ,abi,ipcPath=ipc_path,rpcPath=None)
vote_util = Vote_Util(contract_base)
address_util = AddressUtil(contract_base.web3)
eth_util = EthUtil(contract_base.web3)
app = Flask(__name__)
app.secret_key=bytes(str(uuid.uuid4()),'utf-8')

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
    password = owner_password

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
    print("参数是  {} {} {} {}".format(from_account,password,to,amount))
    # if from_account and password,to,amount
    try:
        details= eth_util.transfer_ether(from_account,password,to,amount)        
        if details is None:
            result = Result_Factory.generate_result(status=False,message=Error_Messages.No_Enough_Balance)
            return result    
    except Exception as e:
        print(e)
        result = Result_Factory.generate_result(status=False,message=e.args[0])
        return result
    else:
        result = Result_Factory.generate_result(status=True,data=details)
        return result


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
    details= vote_util.new_account()
    result = Result_Factory.generate_result(status=True,data=details)
    return result
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)