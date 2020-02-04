import pymongo
import sys
import json
import codecs
from pymongo import MongoClient
from time import sleep

# TODO when running script:::: change the mongo username/password
username='<username>'
password='<password>'

# establish a connection to the local mongo database
client=MongoClient('<ipaddress>',read_preference=pymongo.ReadPreference.SECONDARY,slaveOk=True)
db=client['<dbname>']
db.authenticate(username, password, mechanism='MONGODB-CR')

Prim=MongoClient('<ipaddress>',read_preference=pymongo.ReadPreference.PRIMARY,slaveOk=False)
dbh=client['<dbname>']
dbh.authenticate(username, password, mechanism='MONGODB-CR')

def main(argv):
    filw = '/home/mintekhab/query.out'
    fileout = codecs.open(filw,mode='w',encoding='utf-8')
    var_first = "08fe57854fb47e3d853aecc48cd72815"
    var_last  = "fd4a2cc311eaa2600e2a26feb9a035a2"
    var_id = var_first
    var_new = " "
    out_query = "{{bt:\"Hotels\",isreco:{{$exists:true}},\"_id\":{{$gte:{0},$lt:{1}}}}},{{$unset:{{isreco:true}}}},{{multi:true}}".format(var_id,var_new)
    counter = 1
    while var_id < var_last :
        try:
            cursor = db.Review.find({"bt":"Hotels","isreco":{"$exists":True},"_id":{"$gt":var_id}},{"_id":1}).sort("_id",1).skip(5000).limit(1)
            for doc in cursor:
                var_new = doc['_id']
                out_query = "{{bt:\"Hotels\",isreco:{{$exists:true}},\"_id\":{{$gte:\"{0}\",$lt:\"{1}\"}}}},{{$unset:{{isreco:true}}}},{{multi:true}}".format(var_id,var_new
)
                print out_query
                fileout.write(out_query + "\n")
                rcode = dbh.Review.update({"bt":"Hotels","isreco":{"$exists":True},"_id":{"$gte":var_id,"$lt":var_new}},{"$unset":{"isreco":True}},{multi:true})
                var_id = var_new
                sleep(30)
            counter = counter + 1
            if counter > 3500 :
               break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            break
    out_query = "{{bt:\"Hotels\",isreco:{{$exists:true}},\"_id\":{{$gte:\"{0}\"}}}},{{$unset:{{isreco:true}}}},{{multi:true}}".format(var_id)
    rcode = dbh.Review.update({"bt":"Hotels","isreco":{"$exists":True},"_id":{"$gte":var_id,"$lt":var_last}},{"$unset":{"isreco":True}},{multi:true})
    print out_query
    fileout.write(out_query + "\n")
    fileout.close()
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))