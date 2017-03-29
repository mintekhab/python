import os
import sys
import json
import pprint
import codecs
import optparse
from datetime import datetime

try:
    import pyodbc
except ImportError, e:
    print e
    sys.exit(2)
    
try:
    import requests
except ImportError, e:
    print e
    sys.exit(2)

# Parse command line arguments
def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func

# Push data to the required end point
def request_push(endpoint,row):
    try:
        print(row)
        list_url = {'test':'https://collector.test.expedia.com','int':'https://collector.int.expedia.com','prod':'https://collector.prod.expedia.com','pci':'https://collector-pci.prod-p.expedia.com'}
        request_url = list_url[endpoint]
        request_url = request_url+ "/SterlingRewardsProc.json?stream=true&persist=true&rollup=Day&batch=false"
        request_headers = {'Content-Type': 'application/json'}
        #request_data = {'ProcName': 'SterlingMemberOfferCodeGet#4','execution_count':1107379030,'total_physical_reads':23054946,'min_physical_reads':0,'max_physical_reads':136,'total_logical_writes': 0,'min_logical_writes': 0,'max_logical_writes': 0,'total_logical_reads':9332892584,'min_logical_reads':4,'max_logical_reads':131,'total_elapsed_time':358462469284,'min_elapsed_time': 45,'max_elapsed_time':50052844}
        request_data = row
        r = requests.post(request_url,data=json.dumps(request_data),headers=request_headers)
        print r.status_code
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return 2
    return 0    
      

# Build the data as JSON to the required endpoint
def build_json_data(endpoint,row):
    attriblist = ['ProcName','execution_count','total_physical_reads','min_physical_reads','max_physical_reads',
                   'total_logical_writes','min_logical_writes','max_logical_writes','total_logical_reads','min_logical_reads',
                   'max_logical_reads','total_elapsed_time','min_elapsed_time','max_elapsed_time']
    try:
        payload = {key:value for key,value in zip(attriblist,row)}
        err = request_push(endpoint,payload)
        if err != 0 :
           return err
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return 2
    return 0

# Establish connectivity with DB
def db_connect(hostname=None, dbname=None, username=None, password=None, domain=False, port=None):
    driver = '{ODBC Driver 11 for SQL Server}'
    try :
      if domain :
         conn = pyodbc.connect('DRIVER='+driver+';PORT='+port+';SERVER='+hostname+';PORT='+port+';DATABASE='+dbname+';Trusted_Connection=yes')
      else :
         conn = pyodbc.connect('DRIVER='+driver+';PORT='+port+';SERVER='+hostname+';PORT='+port+';DATABASE='+dbname+';UID='+username+';PWD='+ password)
    except pyodbc.Error, e:
         traceback.print_exc(file=sys.stdout)
         return 2,None
    return 0,conn

# Get the latest execution time available in the table
def get_latest_exec_time(conn):
    latest_exec_time = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 Execution_Time FROM dbo.tblStats_DMV_exec_procedure_stats order by ID DESC")
        row = cursor.fetchone()
        if row :
           latest_exec_time = row[0]
           print 'executionTime: ' + str(row[0]) + ' type: ' + str(type(row[0]))
    except pyodbc.Error, e:
         traceback.print_exc(file=sys.stdout)
         return 2,None
    return 0,latest_exec_time

# Get the last execution of the script 
def get_last_exec_time(btchfile):
    last_exec_time = None
    try:
        fopen = open(btchfile,'r')
        last_exec_time = fopen.readlines()[-1]
        print 'executionTime: ' + str(last_exec_time) + ' type: ' + str(last_exec_time)
        fopen.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except UnicodeEncodeError,err:
        print 'Error :' , err
    except ValueError , err:
        print "Error :" , err
        print "Could not convert data to an integer."
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return 2,None
    return 0,datetime.strptime(last_exec_time,"%Y-%m-%d %H:%M:%S.%f")

#Append latest execution time to batch input file
def append_latest_exec_time(btchfile,latest_execution_time):
    latest_exec_time = datetime.strftime(latest_execution_time,"%Y-%m-%d %H:%M:%S.%f")
    try:
        fopen = open(btchfile,'a')
        fopen.write(latest_exec_time+"\n")
        fopen.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except UnicodeEncodeError,err:
        print 'Error :' , err
    except ValueError , err:
        print "Error :" , err
        print "Could not convert data to an integer."
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return 2,None 
    return 0,last_exec_time


## Get all DB records greater than equal to the lastest execution time
def get_stats_records(conn,latest_execution_time,endpoint):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT ProcName,execution_count,total_physical_reads,min_physical_reads,max_physical_reads, ' \
                       'total_logical_writes,min_logical_writes,max_logical_writes,total_logical_reads,min_logical_reads, ' \
                       'max_logical_reads,total_elapsed_time,min_elapsed_time,max_elapsed_time ' \
                       'FROM dbo.tblStats_DMV_exec_procedure_stats where Execution_time >= ? ',latest_execution_time)
        rows = cursor.fetchall()
        for row in rows:
           print (row.ProcName,row.execution_count)
           err = build_json_data(endpoint,row)
           if err !=0 :
              return err
    except pyodbc.Error, e:
         print "Error :", e
         return 2
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return 2
    return 0    

def main(agrv):
    
    print "*************************** start ************************"
    print datetime.utcnow()
    print "**********************************************************"
    
    p = optparse.OptionParser(usage="usage: %prog -s [d|f] [options]", version="%prog 1.0")   
    p.add_option('-s', '--datasrc', action='store', type='string', dest='datasrc', default=None, help='source for data ingestion acceptable values are d and f ')
    p.add_option('-H', '--servername', action='store', type='string', dest='servername', default='CHWXSQLNRT010.datawarehouse.expecn.com', help='The servername which houses the Database ')
    p.add_option('-D', '--dbname', action='store', type='string', dest='dbname', default='SterlingRewards', help='The database to ingest data from ')
    p.add_option('-P', '--port', action='store', type='int', dest='port', default=1433, help='The port on which the database is runnung on default is 1433')
    p.add_option('-u', '--user', action='store', type='string', dest='user', default=None, help='The username to connect the database')
    p.add_option('-p', '--passwd', action='store', type='string', dest='passwd', default=None, help='The password for the user above')
    p.add_option('-t', '--trust', action='store_true', dest='trust', default=False , help='Using windows auth for connection by dfault False')
    p.add_option('-d', '--delim', action='store', type='string', dest='delim', default=None, help='Delimiter for input file')    
    p.add_option('-i', '--file', action='store', type='string', dest='file', default=None, help='The filename you want to read')
    p.add_option('-l', '--logf', action='store', type='string', dest='logf', default='D:/SterlingTicker/out.log', help='The name of log file')
    p.add_option('-b', '--btch', action='store', type='string', dest='btch', default='D:/SterlingTicker/batch.out', help='The name of batch file')
    p.add_option('-e', '--env', action='store', type='string', dest='env', default='test', help='The environment to push data to , acceptable values are test,int,prod,pci')
    
    options, arguments = p.parse_args()
    
    logfile = options.logf
    btchfile = options.btch
    port = options.port
    endpoint = options.env
    filr = None
    domain = False
    hostname = None
    dbname= None
    username = None
    password = None
    delim = None
    err = None
    conn = None
    if endpoint not in ['test','int','prod','pci']:
       print "the allowable values for environment variable are test int prod pci"
       sys.exit(0)
    if options.datasrc is None :
       print "Please specify an input data source , the input data source can either be delimited file(f) or database (d)"
       sys.exit(0)
    if options.datasrc not in ['d','f'] :
       print "the input data source can either be delimited file(f) or database (d)"
       sys.exit(0)
    if options.datasrc == 'd' :
       hostname = options.servername
       dbname = options.dbname
       if not options.trust :
          username = options.user
          password = options.passwd
       else :
          domain = options.trust
          
    if options.datasrc == 'f' :
       filr = options.file
       delim = options.delim
       
    if options.datasrc == 'd' :
       err,conn = db_connect(hostname,dbname,username,password,domain,str(port))
    if err!= 0 :
       return err;

    #get the latest execution time
    err,latest_execution_time = get_latest_exec_time(conn)
    if err!= 0 :
       return err;
   
    #get the last execution time from batch file
    err,last_exec_time = get_last_exec_time(btchfile)
    print 'before db get records'
    if err!= 0 :
       return err;

    if not latest_execution_time > last_exec_time :
       return 0

    err = get_stats_records(conn,latest_execution_time,endpoint)
    if err!= 0 :
       return err;
        

#
# main app
#
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
