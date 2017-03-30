import pymongo
import sys
import urllib2
import urllib
import json
from pymongo import MongoClient

# TODO when running script:::: change the mongo username/password
username='<username>'
password='password>'
# establish a connection to the local mongo database
client=MongoClient('localhost')
db=client['<dbname>']
db.authenticate(username, password, mechanism='MONGODB-CR')
tracker = db.RTRResponseTracker

# TODO when running script:::: change the base URL as per environment
baseURL="<elasticurl>"
#baseURL="http://privileged.test.reviewsvc.expedia.com/"

def migrateData():

    query = {"res.rqs.q": {"$exists":"true"}}

    try:
        cursor = tracker.find(query)
        cursor = cursor.sort([('upd',pymongo.ASCENDING)])
    except:
        print "Unexpected error:", sys.exc_info()[0]
    for doc in cursor:
        doc_id = doc['_id']
        doc_rqs = doc["res"]["rqs"]
        rt = doc['res']['rt']
        rtStr = 'LX'
        if rt == 2:
            rtStr = 'CAR'
        elif rt == 5:
            rtStr = 'GT'
        ques=doc_rqs[0]
        print ques
        tgs = None
        if 'tgs' in ques["a"]:
            tgs = ques["a"]["tgs"]
            print tgs;
        if tgs is None:
            print "saving without tags"
            url = baseURL+"reviews-api/response/save/"+rtStr+"/"+str(doc_id)+"/"+str(ques["q"])+"/"+str(ques["a"]["aId"]);
            print url
            f=urllib2.urlopen(url)
        else:
            print "saving with tags"
            url = baseURL+"reviews-api/response/save/"+rtStr+"/"+str(doc_id)+"/"+str(ques["q"])+"/"+str(ques["a"]["aId"])+"/tags";
            print url
            for t in tgs:
                if 'tid' in t:
                    t["tagId"]=t["tid"]
                elif 'ts' in t:
                    t["tagStr"]=t["ts"]
            print "Sending tags: "+str(tgs)
            data_json = json.dumps(tgs)
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, data = data_json)

migrateData()