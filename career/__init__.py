
import __future__
print(f"\n __future__.division : {__future__.division}")
import os
PKG_PATH = os.path.dirname(os.path.abspath(__file__))
PJT_PATH = os.path.dirname(PKG_PATH)
ROOT_PATH = os.path.dirname(PJT_PATH)

__all__ = ['tests','iiterator','linkedin']
