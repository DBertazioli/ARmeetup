#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function

import platform
import pandas as pd
import subprocess
import time

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


# In[2]:


db_name="meetup1"
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


# In[3]:


df=pd.read_csv("~/ARmeetup/csv/struttura/member.csv")
#df.head()


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
            
    
    except Exception as err:
       #logging.critical(
       #   "Failed to create neomeetup DB: %" 
       #   % err)
        print(err, "\n err while resetting")


# In[6]:


print(theGraph.vertex_collections())


# In[7]:


# creating some documents
#h1 = theGraph.createVertex('Member', {"member_id": "2", "member_name":"yolo" })
#h1.save()
#h2 = theGraph.createVertex('Humans', {"name": "simba2"})
# linking them
#theGraph.link('Friend', h1, h2, {"lifetime": "eternal"})
# deleting one of them along with the edge
#theGraph.deleteVertex(h2)


# In[8]:


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


# In[9]:


Member.properties()


# In[10]:


Member.insert({"_id":"Member/2","member_id":"1", "member_name":"yolo", "member_age":"18"})


# In[11]:


if Member.has('Member/1'):
    print("hello")


# In[12]:


a=18
key="Member/"+str(a)
key


# In[13]:


go=False
if go:#stop=True
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


# # Trying Batch Execution

# In[14]:


batch_db = db.begin_batch_execution(return_result=True)
batch_db.collection('Member').insert({'_key': 'Jake'})
batch_db.collection('Member').insert({'_key': 'Jill'})

# The commit must be called explicitly.
batch_db.commit()
assert 'Jake' in Member
assert 'Jill' in Member


# In[15]:


go=True
if go:#stop=True
    stop=True

    #skip=True
    skip=False

    #verbose=True
    verbose=True

    n=10000
    n_skip=400000 #just debug purpose
    n_stop=100000

    start_t=time.time()

    if verbose:
        m_time=start_t
        
    batch_db = db.begin_batch_execution(return_result=True)
    
    for line in df.itertuples():
        if not skip:
            key="Member/"+str(line.member_id)
            try:
                batch_db.collection('Member').insert({"_id":key ,"member_id": line.member_id, "member_name": line.member_name })                
            except Exception as e:
                if Member.has(key):
                    #print("member already present")
                    pass
                else:
                    print(e)
                    break

            if (line.Index % n == 0 and line.Index!=0):    
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
            if line.Index >= n_skip:
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




