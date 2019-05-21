#!/usr/bin/python

from py2neo import Graph, Path, Node, NodeMatcher, Relationship
import pandas as pd
import time


#connect with neo4j and create the graph

graph = Graph(password="neomeetup")
graph.delete_all() #delete all existing graph

#connect with csv and create a new node for each member

member_df = pd.read_csv("/var/lib/neo4j/import/member.csv")
print "Updated the csv"
print "Time to work"
###### 100 nodes

start = time.time()
graph.schema.create_uniqueness_constraint('Member', 'id')
count = 0
for row in member_df.iterrows():
    try:
        count += 1
        attr = row[1]
        new_node = Node("Member",
                name = attr['member_name'],
                id = attr['member_id'])

        graph.create(new_node)
    except Exception as e:
        print e
        break
    if count == 100:
        break

end = time.time()
time_py2neo_100 = end - start
print "Completed import of 100 nodes with measurement on time required"

###### 1000 nodes
graph.delete_all() #delete all existing graph
start = time.time()
count = 0
for row in member_df.iterrows():
    try:
        count += 1
        attr = row[1]
        new_node = Node("Member",
                name = attr['member_name'],
                id = attr['member_id'])

        graph.create(new_node)
    except Exception as e:
        print e
        break
    if count == 1000:
        break

end = time.time()
time_py2neo_1000 = end - start
print "Completed import of 1000 nodes with measurement on time required"

###### 10000 nodes
graph.delete_all() #delete all existing graph
start = time.time()
count = 0
for row in member_df.iterrows():
    try:
        count += 1
        attr = row[1]
        new_node = Node("Member",
                name = attr['member_name'],
                id = attr['member_id'])

        graph.create(new_node)
    except Exception as e:
        print e
        break
    if count == 10000:
        break

end = time.time()
time_py2neo_10000 = end - start
print "Completed import of 10k nodes with measurement on time required"

###### 100.000 nodes
graph.delete_all() #delete all existing graph
start = time.time()
count = 0
for row in member_df.iterrows():
    try:
        count += 1
        attr = row[1]
        new_node = Node("Member",
                name = attr['member_name'],
                id = attr['member_id'])

        graph.create(new_node)
    except Exception as e:
        print e
        break
    if count == 100000:
        break

end = time.time()
time_py2neo_100000 = end - start
print "Completed import of 100k nodes with measurement on time required"

###### 500.000 nodes
graph.delete_all() #delete all existing graph
start = time.time()
count = 0
for row in member_df.iterrows():
    try:
        count += 1
        attr = row[1]
        new_node = Node("Member",
                name = attr['member_name'],
                id = attr['member_id'])

        graph.create(new_node)
    except Exception as e:
        print e
        break
    if count == 500000:
        break

end = time.time()
time_py2neo_500000 = end - start
print "Completed import of 500k nodes with measurement on time required"

print "Time to make some measurements"
###### Measurements

time_py2neo = []
time_py2neo.append(time_py2neo_100)
time_py2neo.append(time_py2neo_1000)
time_py2neo.append(time_py2neo_10000)
time_py2neo.append(time_py2neo_100000)
time_py2neo.append(time_py2neo_500000)

total_time_py2neo = time_py2neo_100 + time_py2neo_1000 + time_py2neo_10000 + time_py2neo_100000 + time_py2neo_500000
print "The total time required to make all the operations is " + str(total_time_py2neo/60) + " minutes"

print "Time to realize our csv for the py2neo performance"
index_list = [100, 1000, 10000, 100000, 500000]
data = pd.DataFrame({"Time" : time_py2neo, "index_list" : index_list})
print "Take a look to the results"
print data
data.to_csv("/root/py2neo_import_performance.csv", index = False)