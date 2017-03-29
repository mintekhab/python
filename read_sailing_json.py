#!/usr/bin/python 

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
    p.add_option('-i', '--file', action='store', type='string', dest='file', default='/Users/mintekhab/Downloads/sailings.json', help='The filename you want to read')
    p.add_option('-o1', '--outfOne', action='store', type='string', dest='outfOne', default='/Users/mintekhab/Downloads/superCatCodeOne.out', help='The name of output file for SuperCategoryCode 1')
    p.add_option('-o2', '--outfTwo', action='store', type='string', dest='outfTwo', default='/Users/mintekhab/Downloads/superCatCodeTwo.out', help='The name of output file for SuperCategoryCode 2')
    p.add_option('-o3', '--outfThr', action='store', type='string', dest='outfThr', default='/Users/mintekhab/Downloads/superCatCodeThree.out', help='The name of output file for SuperCategoryCode 3')
    p.add_option('-o4', '--outfFur', action='store', type='string', dest='outfFur', default='/Users/mintekhab/Downloads/superCatCodeFour.out', help='The name of output file for SuperCategoryCode 4')
    p.add_option('-l', '--logf', action='store', type='string', dest='logf', default='/Users/mintekhab/Downloads/out.log', help='The name of log file')
    p.add_option('-b', '--batchDate', action='store', type='string', dest='batchDate', default='/Users/mintekhab/Downloads/out.log', help='BatchRunDate')
    options, arguments = p.parse_args()
    filr = options.file
    filwOne = options.outfOne
    filwTwo = options.outfTwo
    filwThr = options.outfThr
    filwFur = options.outfFur
    logfile = options.logf
    var_batchRunDate = options.batchDate

    try:
        frin = codecs.open(filr,mode='r',encoding='utf-8')
        foutOne = codecs.open(filwOne,mode='a',encoding='utf-8')
        foutTwo = codecs.open(filwTwo,mode='a',encoding='utf-8')
        foutThr = codecs.open(filwThr,mode='a',encoding='utf-8')
        foutFur = codecs.open(filwFur,mode='a',encoding='utf-8')
        logf = codecs.open(logfile,mode='a',encoding='utf-8')
        for line in frin:
            doc = json.loads(line)
            var_objectid = " "
            var_sailingobjid = " "
            var_saillingcode = " "
            var_departuredate = " "
            var_discount = " "
            var_pav =  " "
            var_prs = " "
            var_lps = " "
            param_str = " "
            var_objectid = str(doc['_id']['$oid'])
            for sailing in doc['ss'] :
                var_sailingobjid = sailing['sid']
                var_sailingcode = sailing['sc']
                var_discount = str(sailing['di'])
                #var_prs = '-'.join(map(str, sailing['prs']))
                var_departuredate = str(sailing['dd']['$date'])
                var_pav = str(sailing['pav'])
                for attr,val in sailing['lps'].iteritems():
                    var_lps = ""
                    if attr == '1' :
                       var_lps = str(val)
                       param_str = var_objectid +"|"+ var_sailingobjid +"|"+ var_sailingcode +"|"+ var_discount +"|"+"1|"+ var_lps + "|" + var_pav +"|"+ var_departuredate + "|" + var_batchRunDate
                       foutOne.write(param_str+"\n")
                    elif attr == '2' :
                       var_lps = str(val)
                       param_str = var_objectid +"|"+ var_sailingobjid +"|"+ var_sailingcode +"|"+ var_discount +"|"+"2|"+ var_lps + "|" + var_pav +"|"+ var_departuredate + "|" + var_batchRunDate
                       foutTwo.write(param_str+"\n")
                    elif attr == '3' :
                       var_lps = str(val)
                       param_str = var_objectid +"|"+ var_sailingobjid +"|"+ var_sailingcode +"|"+ var_discount +"|"+"3|"+ var_lps + "|" + var_pav +"|"+ var_departuredate + "|" + var_batchRunDate
                       foutThr.write(param_str+"\n")
                    elif attr == '4' :
                       var_lps = str(val)
                       param_str = var_objectid +"|"+ var_sailingobjid +"|"+ var_sailingcode +"|"+ var_discount +"|"+"4|"+ var_lps + "|" + var_pav +"|"+ var_departuredate + "|" + var_batchRunDate
                       foutFur.write(param_str+"\n")
                    else :
                       param_str = var_objectid +"|"+ var_sailingobjid +"|"+ var_sailingcode +"|"+ var_discount +"|"+"|"+"|"+ "|" + var_pav +"|"+ var_departuredate + "|" + var_batchRunDate
                       logf.write(param_str+"\n")
        foutOne.close()
        foutTwo.close()
        foutThr.close()
        foutFur.close()
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
