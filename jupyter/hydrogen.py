
#============================================================
"""경로잡기, 자주사용하는 개발용 모듈."""
#============================================================

from career import PJT_PATH
import sys
sys.path.append(f"{PJT_PATH}/env/lib/python3.7/site-packages")
sys.path.append('/Users/sambong/libs/idebug')
sys.path.append('/Users/sambong/libs/ilib')
import pprint
pp = pprint.PrettyPrinter(indent=2)
import importlib
