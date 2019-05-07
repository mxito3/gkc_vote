import sys
import os.path
root_directory=os.path.abspath(os.path.join(os.path.abspath(__file__),"../../"))
sys.path.append(root_directory)

from urllib import request
from config.common.utils import *
class Test_API(object):
    def setup_class(self):
        self.api_base = "http://127.0.0.1:3333/{}"
    def test_create_account(self):
        url = self.api_base.format('create_account')
        test_time = 1000
        for index in range(test_time):
            u = request.urlopen(url)
            raw_result = u.read()
            
            result = raw_result.decode('utf8').replace("'", '"')
            key_pair = json.loads(raw_result)['data']
            assert(is_valid_key(key_pair))