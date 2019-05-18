#!/usr/bin/env python
# coding: utf-8

# In[16]:


from __future__ import print_function

import platform
import pandas as pd
import subprocess
import time

try:
    import pyArango
except ImportError as e:
    #process = subprocess.Popen("pip install --user pyorient".split(), stdout=subprocess.PIPE)
    process = subprocess.Popen("pip install pyArango --user".split(), stdout=subprocess.PIPE)

    output, error = process.communicate()
    print(output, "error = {}".format(error), e)
    import pyArango


# In[17]:


from pyArango.connection import *
from pyArango import database
from pyArango.collection import Edges

from pyArango.collection import *
from pyArango.graph import *


# In[3]:


db_name="meetup1"
graph_name="MeetupGraph"
my_auth="root"

reset=True

if platform.release()=="4.9.0-8-amd64":
    
    local=False #set to false for vm 
else:
    local=True
    

if local:
    addr= "http://10.9.13.4:7474"
else:
    addr= "localhost:7474"


# In[4]:


df=pd.read_csv("~/ARmeetup/csv/struttura/member.csv")
df.head()


# In[5]:


try:
    conn = Connection(addr, verbose=True,verify=True)
except Exception as e:
    print(e)
    sys.exit()


# In[6]:


if not conn.hasDatabase(db_name):
    print ("creating db: {}".format(db_name))
    conn.createDatabase(name=db_name)


# In[7]:


db = conn[db_name] # all databases are loaded automatically into the connection and are accessible in this fashion


# In[8]:


class Member(Collection):
    _fields = {
        "member_id": Field(),
        "member_name": Field()
    }
class Group(Collection):
    _fields = {
        "group_id": Field(),
        "group_name": Field()
    }

class subscribed_to(Edges): # theGraphtheGraph
    _fields = {
        "response": Field()
    }
    
# Here's how you define a graph
class MyGraph(Graph) :
    _edgeDefinitions = [EdgeDefinition("subscribed_to", fromCollections=["Member"], toCollections=["Group"])]
    _orphanedCollections = []


# In[9]:


def reset_coll(db,drop=True, create=True):
    if drop:
        db.dropAllCollections()
    if create:
        try:
            if not conn.hasDatabase(db_name):
                print ("creating db: {}".format(db_name))
                conn.createDatabase(name=db_name)
            if not db.hasCollection("Member"):
                print ("creating coll: {}".format("Member"))
                db.createCollection("Member")

            if not db.hasCollection("subscribed_to"):
                print ("creating coll: {}".format("subscribed_to"))
                db.createCollection("subscribed_to")
            if not db.hasGraph("MyGraph"):
                print("creating graph: {}".format("MyGraph"))
                theGraph = db.createGraph("MyGraph")

        except Exception as err:
           #logging.critical(
           #   "Failed to create neomeetup DB: %" 
           #   % err)
            print(err, "\n err while resetting")


# In[10]:


if reset:
    reset_coll(db, create=False)


# In[8]:





# In[13]:


# create the collections (do this only if they don't already exist in the database)
if not db.hasCollection("Member"):
    print ("creating coll: {}".format("Member"))
    db.createCollection("Member")
    
if not db.hasCollection("subscribed_to"):
    print ("creating coll: {}".format("subscribed_to"))
    db.createCollection("subscribed_to")
# same for the graph
if not db.hasGraph("MyGraph"):
    print("creating graph: {}".format("MyGraph"))
    theGraph = db.createGraph("MyGraph")


# In[12]:





# In[11]:


# creating some documents
#h1 = theGraph.createVertex('Member', {"member_id": "2", "member_name":"yolo" })
#h1.save()
#h2 = theGraph.createVertex('Humans', {"name": "simba2"})
# linking them
#theGraph.link('Friend', h1, h2, {"lifetime": "eternal"})
# deleting one of them along with the edge
#theGraph.deleteVertex(h2)


# In[14]:


go=False
if go:
    #stop=True
    stop=True

    #skip=True
    skip=False

    #verbose=True
    verbose=True

    n=100
    n_skip=400000 #just debug purpose
    n_stop=1000

    start_t=time.time()

    if verbose:
        m_time=start_t

    for line in df.itertuples():
        if not skip:
            theGraph.createVertex('Member', {"member_id": line.member_id, "member_name": line.member_name })
            if (line.Index % n == 0 and line.Index!=0):    
                if verbose: print("line is ", line.Index)
                if verbose: 
                    if m_time:
                        print("committed in {} s".format((time.time()-m_time)))
                    else:
                        print("committed in {} s".format((time.time()-start_t)))
                    m_time=time.time()

        else:
            if line.Index >= n_skip:
                theGraph.createVertex('Member', {"member_id": line.member_id, "member_name": line.member_name })
                if line.Index % n == 0:    
                    if verbose: print("line is ", line.Index)
                    if verbose: 
                        print("committed in {} s".format((time.time()-m_time)))
                        m_time=time.time()

        if stop:
            if skip:
                if line.Index == n_stop+n_skip:
                    print("reached line {} in {} s".format(line.Index, (time.time()-start_t)))
                    print("breaking")
                    break
            else:
                if line.Index == n_stop:
                    print("reached line {} in {} s".format(line.Index, (time.time()-start_t)))
                    print("breaking")
                    break


    if not stop:
        print("reached line {} in {} s".format(len(df), (time.time()-start_t)))

