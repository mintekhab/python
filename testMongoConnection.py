import pymongo
import sys
import urllib2
import urllib
import json
from pymongo import MongoClient
# TODO when running script:::: change the mongo username/password
username='<username>'
password='<password>'
# establish a connection to the local mongo database
client=MongoClient('<ipaddress>',replicaset='reviews')
db=client['<dbname>']
assert db.name == '<dbname>'
print client.read_preference
db.authenticate(username, password, mechanism='SCRAM-SHA-1')
dbh = db.BrandReviewSummary
print str(dbh.count())
print 'end'