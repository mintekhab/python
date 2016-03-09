#!/usr/bin/python
import sys
import time
import optparse
import textwrap
import re
import os

def main(argv):
    p = optparse.OptionParser(conflict_handler="resolve", description= "This pushes the sql stats to graphite.")
    p.add_option('-f', '--file', action='store', type='string', dest='file', default='/Users/mintekhab/Desktop/test.log', help='The filename you want to read')
    options, arguments = p.parse_args()
    filein = options.file
    try :
        fin =  open( filein , 'r' )
        p1 = re.compile(r'([0-9]+)ms',re.IGNORECASE)
        for line in fin.readlines():
            if p1.search(line.strip()):
               print p1.findall(line.strip())[0]         
        fin.close()
    except IOError as e:
       print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except ValueError:
       print "Could not convert data to an integer."
    except:
       print "Unexpected error:", sys.exc_info()[0]
       raise

#
# main app
#
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
