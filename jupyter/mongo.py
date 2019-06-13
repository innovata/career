
from jupyter.hydrogen import *
importlib.reload(mongo_v2)
from career import mongo_v2 as mongo

#============================================================
"""MongoClient."""
#============================================================

dir(mongo)

tbl = mongo.db['SampleModel']
type(tbl)
tbl.__dict__
dir(tbl)

#============================================================
"""Model."""
#============================================================

class SampleModel(mongo.Model):

    def __init__(self):
        super().__init__(__class__)

md = SampleModel()
dir(md)
md.tbl
dir(md.tbl)
