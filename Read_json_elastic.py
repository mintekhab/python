import os
import sys
import json
import pprint
import codecs
import pymongo
import optparse
import urllib2 as urllib
from bson import json_util
from datetime import datetime
from pymongo import MongoClient
from pymongo import ReadPreference
from bson.objectid import ObjectId



def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func


def main(argv):
    print "*********start ****************"
    print datetime.utcnow()
    p = optparse.OptionParser(conflict_handler="resolve", description= "The input file get data from elastic search")
    p.add_option('-i', '--file', action='store', type='string', dest='file', default='/Users/mintekhab/Downloads/expedia-reviews/RTRResponseTracker.json', help='The filename you want to read')
    p.add_option('-o', '--outf', action='store', type='string', dest='outf', default='/Users/mintekhab/Downloads/expedia-reviews/out.json', help='The name of output file')
    p.add_option('-l', '--logf', action='store', type='string', dest='logf', default='/Users/mintekhab/Downloads/expedia-reviews/out.log', help='The name of log file')
    options, arguments = p.parse_args()
    filr = options.file
    filw = options.outf
    logfile = options.logf

    serviceurl='<url>'
    count = 0
    modrec = 10
    try:
        frin = codecs.open(filr,mode='r',encoding='utf-8')
        fout = codecs.open(filw,mode='a',encoding='utf-8')
        logf = codecs.open(logfile,mode='a',encoding='utf-8')
        for line in frin:
            count = count + 1
            doc = json.loads(line)
            print doc['_id']['$oid']
            createdate = datetime.strptime(doc["cr"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ")
            updatedate = datetime.strptime(doc["upd"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if count % modrec == 0:
                logf.write(datetime.utcnow().strftime('%y%m%d %H:%M:%S%f')+'\n')
                logf.write(json.dumps(doc,default=json_util.default,sort_keys=False)+'\n')
            timedelta = updatedate - createdate
            if timedelta.total_seconds() > 1800 :
                fout.write(json.dumps(doc,default=json_util.default,sort_keys=False)+'\n')
        fout.close()
        frin.close()
        logf.close()
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
    print "************ END *********"
    print datetime.utcnow()

#
# main app
#
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
