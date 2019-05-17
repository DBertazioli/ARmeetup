#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function

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


# In[2]:


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

local=False #set to false for vm use


if local:
    addr= "http://10.9.13.4:7474"
else:
    addr= "http://localhost:7474"


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
if reset:
    db.dropAllCollections()


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


# create the collections (do this only if they don't already exist in the database)
if not db.hasCollection("Member"):
    print ("creating coll: {}".format("Member"))
    db.createCollection("Member")
    
if not db.hasCollection("subscribed_to"):
    print ("creating coll: {}".format("subscribed_to"))
    db.createCollection("subscribed_to")


# In[10]:


# same for the graph
if not db.hasGraph("MyGraph"):
    print("creating graph: {}".format("MyGraph"))
    theGraph = db.createGraph("MyGraph")


# In[11]:


# creating some documents
#h1 = theGraph.createVertex('Member', {"member_id": "2", "member_name":"yolo" })
#h1.save()
#h2 = theGraph.createVertex('Humans', {"name": "simba2"})
# linking them
#theGraph.link('Friend', h1, h2, {"lifetime": "eternal"})
# deleting one of them along with the edge
#theGraph.deleteVertex(h2)


# In[12]:


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


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[13]:


#useful funct
go=False
if go:
    def reset_db(client, name):

        # Remove Old Database
        client.db_drop(name)

        # Create New Database
        try:
            client.db_create(
               db,
               pyorient.DB_TYPE_GRAPH,
               pyorient.STORAGE_TYPE_PLOCAL)
           #logging.info("neomeetup1 Database Created.")
        except pyorient.PyOrientException as err:
           #logging.critical(
           #   "Failed to create neomeetup DB: %" 
           #   % err)
            print(err, "\n err while resetting")

    def _my_callback(for_every_record):
        print(for_every_record) 
    
    
    if client.db_exists(db):
       # Open Database
        print("opening db: {}".format(db))
        try:
            client.db_open(db, my_auth, my_auth)
        except pyorient.PyOrientException as err:
            print(err)

    else:
        try:
            client.db_create(
               db,
               pyorient.DB_TYPE_GRAPH,
               pyorient.STORAGE_TYPE_PLOCAL)
           #logging.info("neomeetup1 Database Created.")
        except pyorient.PyOrientException as err:
           #logging.critical(
           #   "Failed to create neomeetup DB: %" 
           #   % err)
            print(err)  


# In[ ]:




