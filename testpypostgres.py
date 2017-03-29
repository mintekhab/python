#!/usr/bin/env python
#
#
#load the adapter
import psycopg2

#load the psycopg2 extras module 
import psycopg2.extras

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
    p = optparse.OptionParser(conflict_handler="resolve", description= "This Nagios plugin checks the health of mongodb.")

    p.add_option('-H', '--host', action='store', type='string', dest='host', default='ewe-recon-db-featuredev.cmguqnu4wehw.us-west-2.rds.amazonaws.com', help='The hostname you want to connect to')
    p.add_option('-P', '--port', action='store', type='int', dest='port', default=5432, help='The port postgres is runnung on')
    p.add_option('-u', '--user', action='store', type='string', dest='user', default='InsBookMaster', help='The username you want to login as')
    p.add_option('-p', '--pass', action='store', type='string', dest='passwd', default='In$B00k*90Poi', help='The password you want to use for that user')
    p.add_option('-d', '--database', action='store', dest='database', default='InsuranceBookingEuro', help='Specify the database to check')

    options, arguments = p.parse_args()
    host = options.host
    port = options.port
    user = options.user
    passwd = options.passwd
    database = options.database
    err,conn=postgresq_connect(host, port, user, passwd, database)
    if err!=0:
        return err;
	sql = "SELECT relname FROM pg_class WHERE relkind = 'S' AND relnamespace IN ( SELECT oid FROM pg_namespace WHERE  nspname in ('dbo'));"	
    err,curr=execute_sql(conn,sql)
    if err!=0:
        return err;
	rows = cur.fetchall()
	
	for row in rows:
	    print "   ", row['relname'][1]
				


def postgresq_connect(host=None, port=None, user=None, passwd=None, database=None):
    try:
	   con = psycopg2.connect(database=database, user=user , password=passwd, host=host) 
    except Exception, e:
	   sys.exit(0)
	   return 2,None
    return 0,con

def execute_sql(conn,sql) :
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
	   cur.execute(sql)
	except psycopg2.Error as e:
	   print e.pgerror
	   return 2, None

    return 0,cur




#
# main app
#
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))