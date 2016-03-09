import pymongo
import re

from pymongo import Connection
from datetime import datetime
import codecs

print "*********start ****************"
print datetime.utcnow()
##regx = re.compile("^0.+", re.IGNORECASE)
counter = 0
valProd = 0
conn = Connection(host="10.8.6.6",port=27017)
connPrim = Connection(host="10.8.135.97",port=27017)
dbh = conn ['expedia-reviews']
dbp = connPrim ['expedia-reviews']
assert dbh.connection == conn
assert dbp.connection == connPrim

### Authenticate ####

db = conn['admin']
dbauth = connPrim['admin']
if dbauth.authenticate('reviews','expedia123'):
   dbh.read_preference = pymongo.ReadPreference.PRIMARY
   valProd = 1
   
if db.authenticate('reviews','expedia123'):
   dbh.read_preference = pymongo.ReadPreference.SECONDARY

file = '/home/mintekhab/inputsbr.in'
filw = '/home/mintekhab/inputsbr.out'
fin = open(file,'r')
fout = codecs.open(filw,mode='w',encoding='utf-16') 
try:
    for line in fin.readlines():
        doc = dbh.Review.find({"h":line.strip()},{"h":1,"itin":1})
        fout.write(doc)
    fin.close()
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
print ' doc count %s ', counter
print datetime.utcnow()
