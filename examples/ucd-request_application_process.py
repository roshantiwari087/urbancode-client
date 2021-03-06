#!/usr/bin/env python
'''

Script to trigger a scheduled deployment to run every 15m for any component versions that are passing the required status gates.

'''
import json
from pprint import pprint
import getopt

import os, sys, inspect, time
import random
sys.path.insert( 0, '/Users/swilbur2/dev-workspaces/urbancode-client')
from urbancode_client.deploy import ucdclient


debug = 0
user = 'swilbur2@us.ibm.com'
password = ''
base_url = ''
application = ''
environment = ''
process = 'install'
snapshot = '0.7.020170412'

def usage():
  print ''' ucd-schedule_deployment
  [-h|--help] - Optional, show usage
  [-v|--verbose] - Optional, turn on debugging
  -s|--server http[s]://server[:port] - Set server url
  [-u|--user username (do not supply when using a token) ]
  --password [password|token] - Supply password or token to connect with
  -a|--application <name>
  -e|--environment <name>
  -p|--process <name>
  -s|--snapshot <name>
'''

def __main__():

  global debug, user, password, base_url

  try:
    #opts, args = getopt.getopt(sys.argv[1:], "hs:u:p:a:ve:", ['help','server=', 'user=', 'password=', 'application=','environment='])
    opts, args = getopt.getopt(sys.argv[1:], "hs:u:p:a:ve:P:S:", ['help','server=', 'user=', 'password=', 'application=','environment=', 'process=', 'snapshot='])
  except getopt.GetoptError as err:
  # print help information and exit:
    print(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

  for o, a in opts:
    if o == '-v':
      debug = True
    elif o in ('-h', '--help'):
      usage()
      sys.exit()
    elif o in ( '-s', '--server'):
      base_url = a
    elif o in ( '-u', '--user'):
      user = a
    elif o in ( '-p', '--password'):
      password = a
    elif o in ( '-a', '--application'):
      application = a
    elif o in ( '-e', '--environment'):
      environment = a
    elif o in ( '-P', '--process'):
      process = a
    elif o in ( '-S', '--snapshot'):
      snapshot = a
    else:
      assert False, "unhandled option"
      usage()
      sys.exit()

  if not base_url or not password:
    print('Missing required arguments')
    usage()
    sys.exit()

  ucd = ucdclient.ucdclient( base_url, user, password , debug )

  # process = 'install'
  # snapshot = '0.7.020170412'

  request_body = {
    'application': application,
    'applicationProcess': process,
    'environment': environment,
    'snapshot' : snapshot,
    'onlyChanged' : 'false'
  }
  print '%s: Calling %s on %s environment with snapshot %s' %( request_body['application'], request_body['applicationProcess'], request_body['environment'], request_body['snapshot'] )
  pprint( request_body )

  request_id = ucd.put_json( uri='/cli/applicationProcessRequest/request', data=json.dumps( request_body ) )
  print request_id
  # ucd.

if __name__ == '__main__':
  __main__()
