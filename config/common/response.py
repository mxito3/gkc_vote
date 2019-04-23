from __future__ import unicode_literals
import json
from flask import jsonify,make_response
from .exception import CommonError,Error_Messages
class Result(object):
    def __init__(self,code,message,data):
        self.code = code
        self.message  =message
        self.data = data
        

class Response_Code(object):
    success=200
    fail = 500
    def __init__(self):
        pass


class Result_Factory(object):
    @staticmethod
    def generate_result(status,data=None,message=None):
        result=None
        if status is True:
            result = Result(Response_Code.success,"success",data)
        else:
            result = Result(Response_Code.fail,message,None)
        serilized_result = Result_Util.serilization_result(result)
        return serilized_result

class Result_Util(object):
    @staticmethod
    def serilization_result(result:Result):
        print(result.__dict__)
        response =jsonify(result.__dict__)
        # response.headers['Access-Control-Allow-Origin'] = '*'
        # response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response


    @staticmethod
    def get_json_from_request(request):
        try:
            json = request.json
            print("json is {}".format(json))
            return json 
        except Exception as e:
            raise CommonError(Error_Messages.Invalid_Post_Format)
    @staticmethod
    def get_field_from_json(json,field):
        try:
            value = json[field]
            print("value is {}".format(value))
            return value
        except Exception as identifier:
            raise CommonError(Error_Messages.No_Such_field.format(field))
    @staticmethod
    def get_args_from_request(request):
        try:
            args = request.args
            print("request args  is {}".format(args))
            return args
        except Exception as e:
            raise CommonError(Error_Messages.NO_Requst_Args_Error)
    @staticmethod
    def get_field_from_request_args(args,field):
        try:
            value = args[field]
            print("value is {}".format(value))
            return value
        except Exception as identifier:
            raise CommonError(Error_Messages.No_Such_field.format(field))

      


