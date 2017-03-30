from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo import ReadPreference
from bson import json_util
from datetime import datetime
import pymongo
import urllib
import codecs
import json
import sys



print "*********start ****************"
print datetime.utcnow()
serviceurl='<elastic url>'
conn = MongoClient('<ipaddress>:27017',replicaSet='reviews',readPreference='secondaryPreferred')
dbh = conn ['expedia-reviews']
assert dbh.connection == conn

### Authenticate ####
db = conn['admin']
if db.authenticate('<username>','<apssword>'):
   print "Authenticated"

filw = '/home/mintekhab/data.out'
fout = codecs.open(filw,mode='w',encoding='utf-8') 
queryOut = dbh.RTRResponseTracker.find({"res.rqs":{"$exists":False},"_id":{"$gt":ObjectId("5636a9baa5177813ad09ee01")}}).sort("_id",pymongo.ASCENDING)
try:
    for doc in queryOut:
        timedelta = doc['upd'] - doc['cr']
        if timedelta.seconds > 1800 :
           obj = '_id:'+str(doc['_id'])
           url = serviceurl + urllib.urlencode({'q':obj})
           print url
           data = urllib.urlopen(url).read()
           try:
               js = json.loads(str(data))
               print js['hits']['total']
               if js['hits']['total'] > 0 :
                  fout.write(json.dumps(doc,default=json_util.default,sort_keys=False)+'\n') 
           except:
               js = None
               print 'in elastic search error'
    fout.close()
except IOError as e:
       print "I/O error({0}): {1}".format(e.errno, e.strerror)
except UnicodeEncodeError,err:
       print 'Error :' , err
except ValueError , err:
       print "Error :" , err
       print "Could not convert data to an integer."
except:
       print "Unexpected error:", sys.exc_info()[0]
       raise
print datetime.utcnow()