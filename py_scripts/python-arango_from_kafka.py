#!/usr/bin/env python3.6
# coding: utf-8

# In[36]:


from __future__ import print_function

import sys #std output redirection
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

std_output_redir=True

if std_output_redir:
    orig_stdout = sys.stdout
    f = open('log.txt', 'w')
    sys.stdout = f
    

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


consumer = KafkaConsumer(bootstrap_servers = "sandbox-hdf.hortonworks.com:6667",
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

sys_db=client.db('_system')# username=_, password=_)

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
        
        if not theGraph.has_vertex_collection("Topic"):
            print ("creating vertex_coll: {}".format("Topic"))
            Group=theGraph.create_vertex_collection("Topic")
        else:
            print ("resuming vertex_coll: {}".format("Topic"))
            Group=theGraph.vertex_collection("Topic")    
        
        if not theGraph.has_vertex_collection("Event"):
            print ("creating vertex_coll: {}".format("Event"))
            Group=theGraph.create_vertex_collection("Event")
        else:
            print ("resuming vertex_coll: {}".format("Event"))
            Group=theGraph.vertex_collection("Event")
        
        if not theGraph.has_vertex_collection("Venue"):
            print ("creating vertex_coll: {}".format("Venue"))
            Group=theGraph.create_vertex_collection("Venue")
        else:
            print ("resuming vertex_coll: {}".format("Venue"))
            Group=theGraph.vertex_collection("Venue")
        
        
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
        
        
        if theGraph.has_edge_definition('HOSTED_EVENT'):
            HOSTED_EVENT = theGraph.edge_collection("HOSTED_EVENT")
            print("creating edge_collection: {}".format("HOSTED_EVENT"))
            
        else:
            HOSTED_EVENT = theGraph.create_edge_definition(
                    edge_collection='HOSTED_EVENT',
                    from_vertex_collections=['Group'],
                    to_vertex_collections=['Event']
                )
            print("creating edge_definition: {}".format("HOSTED_EVENT"))
        
        if theGraph.has_edge_definition('DEALS_WITH'):
            DEALS_WITH = theGraph.edge_collection("DEALS_WITH")
            print("creating edge_collection: {}".format("DEALS_WITH"))
            
        else:
            DEALS_WITH = theGraph.create_edge_definition(
                    edge_collection='DEALS_WITH',
                    from_vertex_collections=['Group'],
                    to_vertex_collections=['Topic']
                )
            print("creating edge_definition: {}".format("DEALS_WITH"))
         
        if theGraph.has_edge_definition('WILL_PARTICIPATE'):
            WILL_PARTICIPATE = theGraph.edge_collection("WILL_PARTICIPATE")
            print("creating edge_collection: {}".format("WILL_PARTICIPATE"))
            
        else:
            WILL_PARTICIPATE = theGraph.create_edge_definition(
                    edge_collection='WILL_PARTICIPATE',
                    from_vertex_collections=['Member'],
                    to_vertex_collections=['Event']
                )
            print("creating edge_definition: {}".format("WILL_PARTICIPATE"))
        
        if theGraph.has_edge_definition('HOSTED_AT'):
            HOSTED_AT = theGraph.edge_collection("HOSTED_AT")
            print("creating edge_collection: {}".format("HOSTED_AT"))
            
        else:
            HOSTED_AT = theGraph.create_edge_definition(
                    edge_collection='HOSTED_AT',
                    from_vertex_collections=['Event'],
                    to_vertex_collections=['Venue']
                )
            print("creating edge_definition: {}".format("HOSTED_AT"))
         
        if theGraph.has_edge_definition('IS_INTERESTED_IN'):
            IS_INTERESTED_IN = theGraph.edge_collection("IS_INTERESTED_IN")
            print("creating edge_collection: {}".format("IS_INTERESTED_IN"))
            
        else:
            IS_INTERESTED_IN = theGraph.create_edge_definition(
                    edge_collection='IS_INTERESTED_IN',
                    from_vertex_collections=['Member'],
                    to_vertex_collections=['Topic']
                )
            print("creating edge_definition: {}".format("WILL_PARTICIPATE"))
        
            
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
if go:
    #stop=True
    stop=False

    #skip=True
    skip=False

    #verbose=True
    verbose=True

    n=20000
    n_skip=400000 #just debug purpose
    n_stop=200000

    start_t=time.time()

    if verbose:
        m_time=start_t
    
    groups= []
    members=[]
    events=[]
    venues=[]
    topics={}
    
    t_idfier=0
    
    batch_db = db.begin_batch_execution(return_result=True)
    for count, filename in enumerate(consumer):
        
        if not skip:
            try:        
                j = json.loads(filename.value)
                group_id = j['group']['group_id']
                g_id="Group/"+str(group_id)
                j['group'].update({'_id':g_id})             
                group = j['group']
                
                member_id = j['member']['member_id']
                m_id="Member/"+str(member_id)
                #j['member']['_key']=m_key
                j['member'].update({'_id':m_id})
                member=j['member']
                
                group_topics = j['group']['group_topics']
                
                
                        
                
                event_id = j['event']['event_id']
                e_id="Event/"+str(event_id)
                j['event'].update({'_id':e_id})             
                event=j['event']
                
                if j.get('venue'):
                    has_venue=True
                    venue_id = j['venue']['venue_id']
                    v_id="Venue/"+str(venue_id)
                    j['venue'].update({'_id':v_id})             
                    venue=j['venue']
                
                try:
                    if member_id not in members: #could avoid checking?
                        members.append(member_id)
                        #print("appending member")
                        batch_db.collection('Member').insert(member)
                    #else:
                    #    print("member already into db")
                    if group_id not in groups:
                        groups.append(group_id)
                        #print("appending group")
                        batch_db.collection('Group').insert(group)
                    #else:
                    #    print("group already into db")
                    batch_db.collection('MEMBER_OF').insert({'_from': m_id,'_to': g_id, 'name':"MEMBER_OF"})
                    for top in group_topics:
                    #print(group_topics)
                        urlkey=top['urlkey']
                        if count < 80000: #empirical optimization, better on count or on topics lenght?
                            if urlkey not in topics:
                                #print(top)
                                topics[urlkey]=t_idfier
                                #topics[idfier]=top['urlkey']
                                t_idfier+=1
                                t_id="Topic/"+str(t_idfier)
                                top.update({'_id':t_id})
                                batch_db.collection('Topic').insert(top)
                                batch_db.collection('DEALS_WITH').insert({'_from': g_id,'_to': t_id, 'name':"DEALS_WITH"})
                                batch_db.collection('IS_INTERESTED_IN').insert({'_from': m_id,'_to': t_id, 'name':"IS_INTERESTED_IN"})
                            else:
                                tid=topics[urlkey]
                                t_id="Topic/"+str(tid)

                                batch_db.collection('DEALS_WITH').insert({'_from': g_id,'_to': t_id, 'name':"DEALS_WITH"})
                                batch_db.collection('IS_INTERESTED_IN').insert({'_from': m_id,'_to': t_id, 'name':"IS_INTERESTED_IN"})
                        else:
                            #after some iteration, might be faster this way
                            try:
                                tid=topics[urlkey]
                                t_id="Topic/"+str(tid)

                                batch_db.collection('DEALS_WITH').insert({'_from': g_id,'_to': t_id, 'name':"DEALS_WITH"})
                                batch_db.collection('IS_INTERESTED_IN').insert({'_from': m_id,'_to': t_id, 'name':"IS_INTERESTED_IN"})
                            except KeyError as e:
                                topics[urlkey]=t_idfier
                                #topics[idfier]=top['urlkey']
                                t_idfier+=1
                                t_id="Topic/"+str(t_idfier)
                                top.update({'_id':t_id})
                                batch_db.collection('Topic').insert(top)
                                batch_db.collection('DEALS_WITH').insert({'_from': g_id,'_to': t_id, 'name':"DEALS_WITH"})
                                batch_db.collection('IS_INTERESTED_IN').insert({'_from': m_id,'_to': t_id, 'name':"IS_INTERESTED_IN"})
                            
                            
                    if event_id not in events:
                        events.append(event_id)
                        batch_db.collection('Event').insert(event)
                        if has_venue:
                            if venue_id not in venues:
                                venues.append(venue_id)
                                batch_db.collection('Venue').insert(venue)

                            batch_db.collection('HOSTED_AT').insert({'_from': e_id,'_to': v_id, 'name':"HOSTED_AT"})
                    
                    batch_db.collection('HOSTED_EVENT').insert({'_from': g_id,'_to': e_id, 'name':"HOSTED_EVENT"})
                    batch_db.collection('WILL_PARTICIPATE').insert({'_from': m_id,'_to': e_id, 'name':"WILL_PARTICIPATE"})
                    
                       
                    
                except Exception as ex:
                    print("inner for")
                    print(ex)

            except Exception as e:
                '''
                if Member.has(m_id):
                    #print("member already present")
                    pass
                if Group.has(g_id):
                    pass
                else:
                    print(e)
                    break
                '''
                print(e)
                
            if (count % n == 0 and count!=0):    
                batch_db.commit()
                batch_db = db.begin_batch_execution(return_result=True)
                if verbose: print("count is ", count)
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
                    if verbose: print("line is ", count)
                    if verbose: 
                        print("committed in {} s".format((time.time()-m_time)))
                        m_time=time.time()

        if stop:
            if skip:
                if count == n_stop+n_skip:
                    print("reached line {} in {} s".format(count, (time.time()-start_t)))
                    print("breaking")
                    break
            else:
                if count == n_stop:
                    print("reached line {} in {} s".format(count, (time.time()-start_t)))
                    print("breaking")
                    break

    batch_db.commit()


    if not stop:
        print("reached line {} in {} s".format(len(enumerate(consumer)), (time.time()-start_t)))

#print(topics)
# In[ ]:

sys.stdout = orig_stdout
f.close()





