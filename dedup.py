#!/usr/bin/env python
import os
import sys
import csv
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
    p.add_option('-i', '--file', action='store', type='string', dest='file', default='/tmp/trigger.out', help='The filename you want to read')
    p.add_option('-o', '--outf', action='store', type='string', dest='outf', default='/tmp/query.out', help='The name of output file')
    p.add_option('-l', '--logf', action='store', type='string', dest='logf', default='/tmp/query.log', help='The name of log file')
    p.add_option('-c', '--count', action='store', type='int',   dest='rec_cnt', default=1000, help='number of line after which to split out file')
    options, arguments = p.parse_args()
    csv.register_dialect('piper',delimiter='|',quoting=csv.QUOTE_NONE)
    filr = options.file
    filw = options.outf
    logfile = options.logf
    count = 0
    rec_cnt = options.rec_cnt
    # TODO when running script:::: change the mongo username/password
    username='<username>'
    password='<password>'

    # establish a connection to the local mongo database
    #client=MongoClient('<ipaddress>',read_preference=pymongo.ReadPreference.SECONDARY,slaveOk=True)
    client=MongoClient('<ipaddress>',27018)
    dbs=client['<dbname>']
    dbs.authenticate(username, password, mechanism='SCRAM-SHA-1')

    #Prim=MongoClient('<ipaddress>',read_preference=pymongo.ReadPreference.PRIMARY,slaveOk=False)
    Prim=MongoClient('<ipaddress>',27018)
    db=Prim['']
    db.authenticate(username, password, mechanism='SCRAM-SHA-1')
    try:
        rec = 0
        frin = open(filr,'r')
        fout = codecs.open(filw,mode='a',encoding='utf-8')
        logf = codecs.open(logfile,mode='a',encoding='utf-8')
        out_query="db = db.getSiblingDB('<dbname>');"
        fout.write(out_query + "\n")
        for row in csv.DictReader(frin, dialect='piper'):
            #print (row['pi'],row['tuid'],row['dd'],row['tid'])
            cursor = dbs.reviewsTriggers.find({"pi": row['pi'] , "trip.tuid": row['tuid'] ,"dt.dd": row['dd'] },{"_id":1}).sort("_id",1)
            count = 1
            for doc in cursor :
                var_ms = 6
                var_new = str(doc['_id'])
                #print var_new
                if count > 1 :
                   var_ms = 7
                   out_query = "db.reviewsTriggers.findAndModify({query:{\"_id\":ObjectId(\""+ var_new +"\")},update:{$set:{\"cid\":\"DBCRQ\",\"ms\":NumberInt("+ str(var_ms) +")}}})"
                else : 
                  out_query = "db.reviewsTriggers.findAndModify({query:{\"_id\":ObjectId(\""+ var_new +"\")},update:{$set:{\"ms\":NumberInt("+ str(var_ms) +")}}})"
                fout.write(out_query + "\n")
                logf.write(var_new + "|" + "record:" + str(rec) + "\n")
                count = count + 1
            rec = rec + 1
            if rec % rec_cnt == 0 :
               out_query="db = db.getSiblingDB('expedia-reviews');"
               fout.write(out_query + "\n")

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

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
