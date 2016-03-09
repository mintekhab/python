import pymongo
import sys
import urllib2
import urllib
import json
from pymongo import MongoClient
# TODO when running script:::: change the mongo username/password
username='reviews-sha'
password='expedia123'
# establish a connection to the local mongo database
client=MongoClient('10.0.18.52',replicaset='reviews')
db=client['expedia-reviews']
assert db.name == 'expedia-reviews'
print client.read_preference
db.authenticate(username, password, mechanism='SCRAM-SHA-1')
dbh = db.BrandReviewSummary
print str(dbh.count())
print 'end'