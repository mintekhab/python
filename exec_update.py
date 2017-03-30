import os
import sys
import json
import pprint
import codecs
import pymongo
import optparse
from time import sleep
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
    #p.add_option('-c', '--cnt', action='store', type='int', dest='count', default=0, help='counter for restart')
    p.add_option('-i', '--file', action='store', type='string', dest='file', default="/Users/mintekhab/Downloads/query.out", help="Input file")
    p.add_option('-l', '--logf', action='store', type='string', dest='logf', default="/Users/mintekhab/Downloads/out.log", help="log file")
    options, arguments = p.parse_args()

# TODO when running script:::: change the mongo username/password
    username='<username>'
    password='<password>'

# establish a connection to the local mongo database
    client=MongoClient('<ipaddress>',read_preference=pymongo.ReadPreference.SECONDARY,slaveOk=True)
    db=client['<dbname>']
    db.authenticate(username, password, mechanism='MONGODB-CR')

    filr = options.file
    logfile = options.logf
    #count = options.count
    count = 0
    line_cnt = 0
    match_cnt = 0
    log_str = " "
    restart_string = " "
    try:
        if os.stat(logfile).st_size != 0:
            print 'in logfile'
            logf = codecs.open(logfile,mode='r+',encoding='utf-8')
            for log in logf:
                restart_string = log.strip()
            if restart_string != "":
               match = restart_string.split("|")
               match_cnt = int(match[1].split(":")[1])
            else:
               match_cnt = 0
            logf.close()
        else:
            match_cnt = 0
    except IOError as e:
        print "I/O logfile error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    count = match_cnt
    try:
        frin = codecs.open(filr,mode='r',encoding='utf-8')
        for line in frin:
            line_cnt = line_cnt + 1
            if line_cnt > count :
                count = count + 1
                doc = json.loads(line.strip())
                print doc
                #rcode = db.Review.update(doc)
                log_str = "timestamp:{0}|Counter:{1}|query:{2}".format(datetime.utcnow().strftime('%y%m%d %H:%M:%S%f'),count,line)
                print log_str
                logf.write(log_str +'\n')
                sleep(30)
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
    print "************ END *********"
    print datetime.utcnow()

#
# main app
#
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
