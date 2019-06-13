
#============================================================
"""경로잡기, 자주사용하는 개발용 모듈."""
#============================================================

import sys
sys.path.append("/Users/sambong/pjts/career/env/lib/python3.7/site-packages")
sys.path.append('/Users/sambong/libs/idebug')
sys.path.append('/Users/sambong/libs/ilib')
other_pjts = ['stock']
for other in other_pjts:
    path = f"/Users/sambong/pjts/{other}/env/lib/python3.7/site-packages"
    if path in sys.path:
        sys.path.remove(path)
import pprint
pp = pprint.PrettyPrinter(indent=2)
import importlib
