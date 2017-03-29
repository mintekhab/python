#!/usr/bin/env python
import os
import sys
import json
import pprint
import codecs
import socket
import optparse
from datetime import datetime



def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func

def socket_connect():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return 0,sock
    except Exception,e:
        exit_with_general_critical(e),None

def main(argv):
    print "*********start ****************"
    print datetime.utcnow()
    p = optparse.OptionParser(conflict_handler="resolve", description= "Push RDS metrics to STATSD server")
    p.add_option('-i', '--file', action='store', type='string', dest='file', default='/tmp/metric.json', help='The filename you want to read')
    p.add_option('--gaugepath', action='store', type='string', dest='hostname', default='', help='The hostname you want displayed in statsd')
    p.add_option('--statsd_host', action='store', type='string', dest='statsd_host', default='127.0.0.1', help='The name of the statsd host')
    p.add_option('--statsd_port', action='store', type='int', dest='statsd_port', default=8125, help='The port of the statsd host')

    options, arguments = p.parse_args()
    statsd_host = options.statsd_host
    statsd_port = options.statsd_port
    if options.hostname!='':
      hostname = options.hostname
    filr = options.file
    err,sock=socket_connect()
    if err!=0:
        return err;
    try:
        frin = codecs.open(filr,mode='r',encoding='utf-8').read()
        logf = codecs.open(logfile,mode='a',encoding='utf-8')
        gauge_data=''
        docs = json.loads(frin)
        metric = docs['Label']
        for points in docs['Datapoints']:
            gauge_data = "%s.%s:%s|g" % (hostname,metric,str(points['Average']))
            sock.sendto(gauge_data, (statsd_host, statsd_port))
            print gauge_data
            print 'metric name: {0} timestamp: {1} value: {2} unit: {3}'.format(metric,points['Timestamp'],points['Average'],points['Unit'])
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