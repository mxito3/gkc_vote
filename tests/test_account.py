import sys
import os.path
root_directory=os.path.abspath(os.path.join(os.path.abspath(__file__),"../../"))
sys.path.append(root_directory)
from config.common.utils import *
def test_create_account():
        test_time = 1000
        for index in range(test_time):
            key_pair = new_key_pair()
            assert(is_valid_key(key_pair))
