#!/usr/bin/env python

import pymongo
import sys
import json
import codecs
from pymongo import MongoClient
from time import sleep

# TODO when running script:::: change the mongo username/password
username='loader-app'
password='f00b@r2012'

# establish a connection to the local mongo database
client=MongoClient('10.8.135.92',read_preference=pymongo.ReadPreference.SECONDARY,slaveOk=True)
db=client['expedia-reviews']
db.authenticate(username, password, mechanism='MONGODB-CR')

Prim=MongoClient('10.8.134.36',read_preference=pymongo.ReadPreference.PRIMARY,slaveOk=False)
dbh=Prim['expedia-reviews']
dbh.authenticate(username, password, mechanism='MONGODB-CR')

def main(argv):
    filw = '/tmp/query_02.out'
    fileout = codecs.open(filw,mode='w',encoding='utf-8')
    #var_first = "08fe57854fb47e3d853aecc48cd72815"
    var_first = "58489363"
    var_last  = "fd4a2cc311eaa2600e2a26feb9a035a2"
    var_sec_last = "99982504"
    var_id = var_first
    var_new = " "
    out_query = " "
    counter = 0
    while var_id < var_last :
        try:
            cursor = db.Review.find({"bt":"Hotels","isreco":{"$exists":True},"_id":{"$gt":var_id}},{"_id":1}).sort("_id",1).skip(2500).limit(1)
            for doc in cursor:
                var_new = doc['_id']
                out_query = "var_id_gte:{0}|var_new_lt:{1}".format(var_id,var_new)
                print out_query
                rcode = dbh.Review.update({"bt":"Hotels","isreco":{"$exists":True},"_id":{"$gte":var_id,"$lt":var_new}},{"$unset":{"isreco":True}},mul
ti=True)
                sleep(30)
                print "No. of records updated : {0}".format(rcode['nModified'])
                fileout.write(out_query + "\n")
                var_id = var_new

            counter = counter + 1
            if var_sec_last <=  var_new :
               break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            break
    out_query = "var_id_gte:{0} ".format(var_id)
    print out_query
    fileout.write(out_query + "\n")
    rcode = dbh.Review.update({"bt":"Hotels","isreco":{"$exists":True},"_id":{"$gte":var_id,"$lt":var_last}},{"$unset":{"isreco":True}},multi=True)
    print "No. of records updated : {0}".format(rcode['nModified'])
    fileout.close()
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))