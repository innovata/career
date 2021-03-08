
from pymongo import MongoClient, ASCENDING, DESCENDING
db = MongoClient()['career']
import pandas as pd
import copy
import re
import inspect
from career.ide import *
import idebug as dbg


class ModelHandler:

    def __init__(self):
        self.doc = {}
        self.docs = []

    def attributize(self, dic):
        for key, value in dic.items():
            setattr(self, key, value)
        return self

    def schematize(self):
        for attr in list(self.__dict__):
            if attr in self.schema:
                self.doc[attr] = getattr(self, attr)
        return self

    def handle_flocals(self, frame):
        dic = {k:v for k,v in frame.f_locals.items() if k not in ['self','__class__']}
        return self.attributize(dic)

    def get_df(self):
        return pd.DataFrame(self.docs)

    def to_csv(self, filepath, index=True):
        """경로여부체크 시 존재이유 있음."""
        df = self.get_df()
        df.to_csv(filepath, index=index)
        return self

class Model(ModelHandler):
    
    def __init__(self, modelclass):
        self.tbl = db[modelclass.__name__]
        # self.modelname = modelclass.__name__
        # self.tblname = self.modelname
        super().__init__()

    def insert_docs(self):
        self.InsertManyResult = self.tbl.insert_many(self.docs)
        return self

    def insert_doc(self):
        self.schematize()
        self.InsertOneResult = self.tbl.insert_one(self.doc)
        del(self.doc['_id'])
        return self

    def update_doc(self, filter, upsert=False):
        self.schematize()
        update = {'$set':self.doc}
        self.UpdateResult = self.tbl.update_one(filter, update, upsert)
        return self

    def iter_updating_docs(self, filter, upsert=False):
        self.UpdateResults = []
        for d in self.docs:
            self.doc = d
            UpdateResult = self.tbl.update_one(filter, update, upsert)
            self.UpdateResults.append(UpdateResult)
        return self

    def update_one_result(self, filter, update, upsert=False):
        self.UpdateResult = self.tbl.update_one(filter, update, upsert)
        return self

    def update_many_result(self, filter, update, upsert=False):
        self.UpdateResult = self.tbl.update_many(filter, update, upsert)
        return self

    def delete_many_result(self, filter, report=False):
        self.DeleteResult = self.tbl.delete_many(filter)
        if report:
            dbg.DeleteResult(clss=self.DeleteResult, caller=f"{self.__class__} | {inspect.stack()[0][3]}")
        return self

    def load(self, report=False):
        self.docs = list(self.cursor)
        if report:
            print(f"{'*'*60}\n{self.__class__} | {inspect.stack()[0][3]}\n len(docs) : {len(self.docs)}")
        return self

class DatabaseMigrator:
    """서로 다른 데이터베이스 간에 테이블을 마이그
    비정상 동작 --> 지워야 할듯.
    """
    def __init__(self, dbname1, dbname2):
        self.db1 = MongoClient()[dbname1]
        self.db2 = MongoClient()[dbname2]

    def migrate_all_tables(self, skippable_docscnt=pow(10,6)):
        db1 = self.db1
        db2 = self.db2
        tblnames = sorted(db1.list_collection_names())
        for tblname in tblnames:
            print(f"\n tblname : {tblname}\n")
            res = db1.command('collstats', tblname)
            print(f"\n docs_count : {res['count']}\n")
            tbl1 = db1[tblname]
            if res['count'] > skippable_docscnt:
                pass
            else:
                cursor1 = tbl1.find(filter=None, projection={'_id'})
                docs1 = list(cursor1)
                tbl2 = db2[tblname]
                tbl2.drop()
                InsertManyResult = tbl2.insert_many(docs1)
                tbl1.drop()

class DatabaseManager:

    def list_collection_names(self):
        tbls = db.list_collection_names()
        return sorted(tbls)

    def list_collections(self):
        cursor = db.list_collections()
        return cursor

    def command_collstats(self, tblname):
        response = db.command('collstats', tblname)
        return response

    def command_connpoolstats(self):
        pp.pprint(db.command({'connPoolStats':1}))

    def rename_collections(self, pattern, repl):
        tbls = self.list_collection_names()
        p = re.compile(pattern)
        for tbl in tbls:
            if p.search(string=tbl) is not None:
                print(f"\n old : {tbl}")
                #new_tbl = p.sub(repl=repl, string=tbl)
                new_tbl = tbl.replace('Rawdata', '')
                print(f" new : {new_tbl}")
                #db[tbl].rename(new_tbl)

    def get_collections(self, regex):
        tbls = self.list_collection_names()
        p = re.compile(regex)
        tables = []
        for tbl in tbls:
            if p.search(string=tbl) is not None:
                tables.append(tbl)
        return tables

    def drop_all_tables(self):
        tblnames = db.list_collection_names()
        for tblname in tblnames:
            print(f"\n tblname : {tblname}")
            db[tblname].drop()
