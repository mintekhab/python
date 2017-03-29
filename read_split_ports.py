import os
import sys
import json
import pprint
import codecs
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

def main(argv):
    print "*********start ****************"
    print datetime.utcnow()

    p = optparse.OptionParser(conflict_handler="resolve", description= "The input file get data from elastic search")
    p.add_option('-i', '--file', action='store', type='string', dest='file', default='D:/CruiseOffer/Batch/test_ports.json', help='The filename you want to read')
    p.add_option('-o', '--outf', action='store', type='string', dest='outf', default='D:/CruiseOffer/Batch/ports_sailing.out', help='The name of output file for ports data')
    p.add_option('-l', '--logf', action='store', type='string', dest='logf', default='D:/CruiseOffer/Batch/out.log', help='The name of log file')
    p.add_option('-b', '--batchDate', action='store', type='string', dest='batchDate', default='2017-03-01', help='BatchRunDate')
    options, arguments = p.parse_args()
    filr = options.file
    filw = options.outf
    logfile = options.logf
    var_batchRunDate = options.batchDate
    var_header='objectid|sid|originsailingcode|CountryCode|subcode|portcode|Dayno|seq|arriveday|arrivehrmin|departureday|departHrmin|batchdate'
    try:
        frin = codecs.open(filr,mode='r',encoding='utf-8')
        fout = codecs.open(filw,mode='a',encoding='utf-8')
        logf = codecs.open(logfile,mode='a',encoding='utf-8')
        fout.write(var_header+"\n")
        for line in frin:
            doc = json.loads(line)
            var_objectid = " "
            var_sailingobjid = " "
            var_saillingcode = " "
            var_cc   = " "
            var_pc   = " "
            var_sc   = " "
            var_dn   = " "
            var_seq  = " "
            var_ad   = " "
            var_ahm  = " "
            var_dd   = " "
            var_dhm  = " "            
            param_str = " "
            var_objectid = str(doc['_id']['$oid'])
            
            for sailing in doc['ss'] :
                var_sailingobjid = sailing['sid']
                var_sailingcode = sailing['sc']
                for ports,tims in zip(doc['pos'],sailing['tim']):
                    var_cc   = str(ports['cc'])
                    var_sc   = str(ports['sc'])
                    var_pc   = str(ports['pc'])
                    var_dn   = str(ports['dn'])
                    var_seq  = str(ports['seq'])
                    var_ad   = str(tims['ad'])
                    var_adm  = str(tims['ahm'])
                    var_dd   = str(tims['dd'])
                    var_dhm  = str(tims['dhm'])
                    param_str = ""
                    param_str = var_objectid + "|" + var_sailingobjid + "|" + var_sailingcode + "|" + var_cc + "|" + var_pc + "|" + var_sc+ "|" + var_dn + "|" + var_seq + "|" + var_ad + "|" + var_adm + "|" + var_dd + "|" + var_dhm + "|"+  var_batchRunDate +"\n"
                    fout.write(param_str)
        fout.close()
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
