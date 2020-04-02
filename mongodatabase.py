# !/usr/bin/env python
# _*_ coding:utf-8 _*_


import pymongo

class database_mongo(object):
    def __init__(self, host, port, dbname, dbcollection):
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[dbname]
        self.collection = self.db[dbcollection]

    def save_data(self, data):
        self.collection.insert(data)
        print('保存成功!')

    def get_one(self,query):
        return self.collection.find_one(query,project={"_id":False})

    def get_all(self,query):
        return self.collection.find(query)

    def add(self,kv_dict):
        return self.collection.insert(kv_dict)

    def delete(self,query):
        return self.collection.delete_many(query)

    def check_exist(self,query):
        ret = self.collection.find_one(query)
        return ret != None

    def update(self,query,kv_dict):
        self.collection.update(query,{'$set':kv_dict},upsert = Ture)
