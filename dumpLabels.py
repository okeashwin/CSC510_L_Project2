from __future__ import print_function
import urllib2
import json
import re
import datetime
import sys
import sqlite3
import ConfigParser
import os.path
import argparse

class L():
  "Anonymous container"
  def __init__(i,**fields) :
    i.override(fields)
  def override(i,d): i.__dict__.update(d); return i
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,pretty(d[k]))
                     for k in i.show()])+ '}'
  def show(i):
    lst = [str(k)+" : "+str(v) for k,v in i.__dict__.iteritems() if v != None]
    return ',\t'.join(map(str,lst))


def labelDump(u,labels,token):
  try:
	  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
	  v = urllib2.urlopen(request).read()
	  w = json.loads(v)
	  if not w or ('message' in w and w['message'] == "Not Found"): return False
	  issueID=0
	  for label in w:
	  	labelName=label['name']
	  	labelObj= L(id=issueID, name=labelName)
	  	labels.append(labelObj)
	  	issueID+=1
	  return True    
  except urllib2.HTTPError as e:
    if e.code != 404:
      print(e)
      print("404 Contact TA")
    return False
  except Exception as e:
    print(u)
    print(e)
    print("other Contact TA")
    return False
def launchDump():
  if os.path.isfile("./gitable.conf"):
    config = ConfigParser.ConfigParser()
    config.read("./gitable.conf")
  else:
    print("gitable.conf not found, make sure to make one!")
    sys.exit()

  if not config.has_option('options', 'token'):
    print("gitable.conf does not have token, fix!")
    sys.exit()

  parser = argparse.ArgumentParser(description='Process GitHub issue records and record to SQLite database')
  parser.add_argument('repo',help='repo to process')
  parser.add_argument('groupname',help='anonymization to apply to project title')
  parser.add_argument('-db','--database',default='', help='specify db filename, default (repo).db')

  args = parser.parse_args()
  dbFile = '{}.db'.format(args.groupname.replace('\\','_').replace('/','_'))
  if len(args.database)>0:
    dbFile = args.database.format(args.repo.replace('\\','_').replace('/','_'))
  repo = args.repo
  group = args.groupname
  token = config.get('options','token')

  conn = sqlite3.connect(dbFile)
  conn.execute('''CREATE TABLE IF NOT EXISTS labels(id INTEGER, name VARCHAR(128),
        CONSTRAINT pk_issue PRIMARY KEY (id) ON CONFLICT ABORT)''')

  labels=[]

  url='https://api.github.com/repos/'+repo+'/labels?state=all'
  print("Retrieving labels for this repo")
  labelDump(url,labels,token)
  print("Received "+str(len(labels))+" labels from the repo")
  labelTuples=[]
  for label in labels:
  	labelTuples.append([label.id, label.name])

  try:
    if len(labels) > 0:
      conn.executemany('INSERT INTO labels VALUES (?,?)', labelTuples)
      conn.commit()
      print('committed labels')
  except sqlite3.Error as er:
    print(er)

  conn.close()


launchDump()