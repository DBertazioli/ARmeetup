#!/usr/bin/env python
# coding: utf-8

# In[36]:


from __future__ import print_function

import platform
import pandas as pd
import subprocess
import time
import json
try:
    from kafka import KafkaConsumer
except ImportError as e:
    #process = subprocess.Popen("pip install --user pyorient".split(), stdout=subprocess.PIPE)
    process = subprocess.Popen("pip install kafka --user".split(), stdout=subprocess.PIPE)

    output, error = process.communicate()
    print(output, ", error = {}, ".format(error), e)
    process.kill()
    from kafka import KafkaConsumer
import kafka

try:
    import arango
except ImportError as e:
    #process = subprocess.Popen("pip install --user pyorient".split(), stdout=subprocess.PIPE)
    process = subprocess.Popen("pip install python-arango --user".split(), stdout=subprocess.PIPE)

    output, error = process.communicate()
    print(output, ", error = {}, ".format(error), e)
    process.kill()
    import arango
from arango import ArangoClient


# In[31]:


db_name="meetup2"
graph_name="MeetupGraph"
my_auth="root"

if platform.release()=="4.9.0-8-amd64":
    local=False #set to false for vm 
else:
    local=True

if local:
    host= "10.9.13.4"
    port= "7474"
else:
    host= "localhost"
    port= "7474"


# In[1]:


kafka_consumer = KafkaConsumer(bootstrap_servers = "sandbox-hdf.hortonworks.com:6667",
                         auto_offset_reset = 'earliest',
                         consumer_timeout_ms = 1000)
consumer.subscribe(['april_topic'])
print("subscribed to april meetup topic")


# In[3]:





# In[4]:


try:
    client = ArangoClient(protocol="http", host=host, port=port)
except Exception as e:
    print(e)
client


# In[5]:


drop=True
create=True

sys_db=client.db('_system', username=_, password=_)

if drop:
    if sys_db.has_database(db_name):
        print ("dropping db: {}".format(db_name))
        sys_db.delete_database(db_name)
        
if create:
    try:
        if not sys_db.has_database(db_name):
            print ("creating db: {}".format(db_name))
            sys_db.create_database(db_name)
        db = client.db(db_name)
            
        if not db.has_graph(graph_name):
            print("creating graph: {}".format(graph_name))
            theGraph = db.create_graph(graph_name)
        else:
            print("resuming graph: {}".format(graph_name))
            theGraph= db.graph(graph_name)
        
        if not theGraph.has_vertex_collection("Member"):
            print ("creating vertex_coll: {}".format("Member"))
            Member=theGraph.create_vertex_collection("Member")
        else:
            print ("resuming vertex_coll: {}".format("Member"))
            Member=theGraph.vertex_collection("Member")
            
        if not theGraph.has_vertex_collection("Group"):
            print ("creating vertex_coll: {}".format("Group"))
            Group=theGraph.create_vertex_collection("Group")
        else:
            print ("resuming vertex_coll: {}".format("Group"))
            Group=theGraph.vertex_collection("Group")
            
        if theGraph.has_edge_definition('MEMBER_OF'):
            MEMBER_OF = theGraph.edge_collection("MEMBER_OF")
            print("creating edge_collection: {}".format("MEMBER_OF"))
            
        else:
            MEMBER_OF = theGraph.create_edge_definition(
                    edge_collection='MEMBER_OF',
                    from_vertex_collections=['Member'],
                    to_vertex_collections=['Group']
                )
            print("creating edge_definition: {}".format("MEMBER_OF"))
            
        #print(theGraph.vertex_collections())
            
            print("vertex colls: ", theGraph.vertex_collections())
    except Exception as err:
       #logging.critical(
       #   "Failed to create neomeetup DB: %" 
       #   % err)
        print(err, "\n err while resetting")


# # Trying Batch Execution

# In[15]:


go=True
if go:#stop=True
    stop=True

    #skip=True
    skip=False

    #verbose=True
    verbose=True

    n=10
    n_skip=400000 #just debug purpose
    n_stop=100

    start_t=time.time()

    if verbose:
        m_time=start_t
    
    groups= []
    members=[]
    
    batch_db = db.begin_batch_execution(return_result=True)
    for count, filename in enumerate(consumer):
        
        if not skip:
            m_key="Member/"+str(line.member_id)
            try:        
                j = json.loads(filename.value)
                group_id = j['group']['group_id']
                group = j['group']
                member_id = j['member']['member_id']
                member=j['member']
                
                m_key="Member/"+str(member_id)
                g_key="Group/"+str(group_id)
                try:
                    if member_id not in members:
                        members.append(member_id)
                        print("appending member")
                        batch_db.collection('Member').insert(member)
                    else:
                        print("member already into db")
                    if group_id not in groups:
                        groups.append(group_id)
                        print("appending group")
                        batch_db.collection('Group').insert(group)
                    else:
                        print("group already into db")
                except Exception, ex:
                    print("inner for")
                    print ex

            except Exception as e:
                if Member.has(m_key):
                    #print("member already present")
                    pass
                if Group.has(g_key):
                    pass
                else:
                    print(e)
                    break

            if (count % n == 0 and count!=0):    
                batch_db.commit()
                batch_db = db.begin_batch_execution(return_result=True)
                if verbose: print("line is ", line.Index)
                if verbose: 
                    if m_time:
                        print("committed in {} s".format((time.time()-m_time)))
                    else:
                        print("committed in {} s".format((time.time()-start_t)))
                    m_time=time.time()

        else:
            if count >= n_skip:
                key="Member/"+str(line.member_id)
                try:
                    #print("inserting")
                    Member.insert({"_id":key ,"member_id": line.member_id, "member_name": line.member_name })
                    #print("inserted")
                except Exception as e:
                    if Member.has(key):
                        #print("member already present")
                        pass
                    else:
                        print(e)
                        break

                if count % n == 0:    
                    if verbose: print("line is ", line.Index)
                    if verbose: 
                        print("committed in {} s".format((time.time()-m_time)))
                        m_time=time.time()

        if stop:
            if skip:
                if count == n_stop+n_skip:
                    print("reached line {} in {} s".format(line.Index, (time.time()-start_t)))
                    print("breaking")
                    break
            else:
                if count == n_stop:
                    print("reached line {} in {} s".format(line.Index, (time.time()-start_t)))
                    print("breaking")
                    break

    batch_db.commit()


    if not stop:
        print("reached line {} in {} s".format(len(df), (time.time()-start_t)))


# In[ ]:




