#!/usr/bin/python

######## packages
from kafka import KafkaConsumer
import time
import json
import pandas as pd


######## connecting to Kafka
consumer = KafkaConsumer(bootstrap_servers ='sandbox-hdf.hortonworks.com:6667',
                        auto_offset_reset = 'earliest',
                        consumer_timeout_ms = 1000)
consumer.subscribe(['project_april'])
print "subscribed to topic project_april"
print "It's time to make some benchmark"
########### 100 messages

#using lists
start = time.time()
messages = []
messages_proxy = []
count_list = 0
for message in consumer:
    try:
        j = json.loads(message.value)
        if j['member']['member_id'] not in messages_proxy:
            count_list += 1
            messages_proxy.append(j['member']['member_id'])
            messages.append(j['member'])
            if count_list == 100:
                break
    except Exception as e:
        print e
        break
end = time.time()
time_list_100 = end-start

#using dict
start = time.time()
messages = []
names = {}
count_dict = 0
for message in consumer:
    try:        
        j = json.loads(message.value)
        name_id = j['member']['member_id']
        member_name=j['member']['member_name']
        try:
            if name_id not in names:
                count_dict += 1
                names[name_id]=member_name.encode('utf-8')                
        except Exception, ex:
            print("inner for")
            print ex
    except Exception, e:
        print("outer for")
        print e
        
    if count_dict == 100:
        break

end = time.time()
time_dict_100 = end-start

print "Completed benchmark for 100 messages"
########## 1000 messages

#using lists
start = time.time()
messages = []
messages_proxy = []
count_list = 0
for message in consumer:
    try:
        j = json.loads(message.value)
        if j['member']['member_id'] not in messages_proxy:
            count_list += 1
            messages_proxy.append(j['member']['member_id'])
            messages.append(j['member'])
            if count_list == 1000:
                break
    except Exception as e:
        print e
        break
end = time.time()
time_list_1000 = end-start


#using dict
start = time.time()
messages = []
names = {}
count_dict = 0
for message in consumer:
    try:        
        j = json.loads(message.value)
        name_id = j['member']['member_id']
        member_name=j['member']['member_name']
        try:
            if name_id not in names:
                count_dict += 1
                names[name_id]=member_name.encode('utf-8')                
        except Exception, ex:
            print("inner for")
            print ex
    except Exception, e:
        print("outer for")
        print e
        
    if count_dict == 1000:
        break

end = time.time()
time_dict_1000 = end-start


print "Completed benchmark for 1000 messages"
################## 10000 messages

#using lists
start = time.time()
messages = []
messages_proxy = []
count_list = 0
for message in consumer:
    try:
        j = json.loads(message.value)
        if j['member']['member_id'] not in messages_proxy:
            count_list += 1
            messages_proxy.append(j['member']['member_id'])
            messages.append(j['member'])
            if count_list == 10000:
                break
    except Exception as e:
        print e
        break
end = time.time()
time_list_10000 = end-start


#using dict
start = time.time()
messages = []
names = {}
count_dict = 0
for message in consumer:
    try:        
        j = json.loads(message.value)
        name_id = j['member']['member_id']
        member_name=j['member']['member_name']
        try:
            if name_id not in names:
                count_dict += 1
                names[name_id]=member_name.encode('utf-8')                
        except Exception, ex:
            print("inner for")
            print ex
    except Exception, e:
        print("outer for")
        print e
        
    if count_dict == 10000:
        break

end = time.time()
time_dict_10000 = end-start

print "Completed benchmark for 10k messages"
############## 100.000 messages

#using lists
start = time.time()
messages = []
messages_proxy = []
count_list = 0
for message in consumer:
    try:
        j = json.loads(message.value)
        if j['member']['member_id'] not in messages_proxy:
            count_list += 1
            messages_proxy.append(j['member']['member_id'])
            messages.append(j['member'])
            if count_list == 100000:
                break
    except Exception as e:
        print e
        break
end = time.time()
time_list_100000 = end-start


#using dict
start = time.time()
messages = []
names = {}
count_dict = 0
for message in consumer:
    try:        
        j = json.loads(message.value)
        name_id = j['member']['member_id']
        member_name=j['member']['member_name']
        try:
            if name_id not in names:
                count_dict += 1
                names[name_id]=member_name.encode('utf-8')                
        except Exception, ex:
            print("inner for")
            print ex
    except Exception, e:
        print("outer for")
        print e
        
    if count_dict == 100000:
        break

end = time.time()
time_dict_100000 = end-start

print "Completed benchmark for 100k messages"

############ 500.000 messages
#this one is the most difficult for lists
#using lists
start = time.time()
messages = []
messages_proxy = []
count_list = 0
for message in consumer:
    try:
        j = json.loads(message.value)
        if j['member']['member_id'] not in messages_proxy:
            count_list += 1
            messages_proxy.append(j['member']['member_id'])
            messages.append(j['member'])
            if count_list == 500000:
                break
    except Exception as e:
        print e
        break
end = time.time()
time_list_500000 = end-start

print "Finished with lists in 500k tasks"
#using dict
start = time.time()
messages = []
names = {}
count_dict = 0
for message in consumer:
    try:        
        j = json.loads(message.value)
        name_id = j['member']['member_id']
        member_name=j['member']['member_name']
        try:
            if name_id not in names:
                count_dict += 1
                names[name_id]=member_name.encode('utf-8')                
        except Exception, ex:
            print("inner for")
            print ex
    except Exception, e:
        print("outer for")
        print e
        
    if count_dict == 500000:
        break

end = time.time()
time_dict_500000 = end-start
print "Completed benchmark for 500k messages"
print "Now it's time to compile our dataframe"
######### making dataframe of times

total_times_dict = time_dict_100 + time_dict_1000 + time_dict_10000 + time_dict_100000 + time_dict_500000
total_times_list = time_list_100 + time_list_1000 + time_list_10000 + time_list_100000 + time_list_500000

print "I could take a look to the times!"
if total_times_list > total_times_dict:
    print "I wish I could say I'm surprised but.. dicts beat lists with " + str(total_times_dict/60) + "minutes vs " +str(total_times_list/60) + " minutes"
else:
    print "Woh, this is totally inespected, lists beat dicts with " + str(total_times_list/60) + " minutes vs " + (total_times_dict/60) + " minutes"

times_lists = []
times_dicts = []

times_lists.append(time_list_100)
times_dicts.append(time_dict_100)
times_lists.append(time_list_1000)
times_dicts.append(time_dict_1000)
times_lists.append(time_list_10000)
times_dicts.append(time_dict_10000)
times_lists.append(time_list_100000)
times_dicts.append(time_dict_100000)
times_lists.append(time_list_500000)
times_dicts.append(time_dict_500000)
print "Creating the dataframe"
times = pd.DataFrame({'Times_lists' : times_lists, 'Times_dicts' : times_dicts}, index = ['100','1000', '10000', '100000', '500000'])
print "Finished, take a look!"
print times
print "Making our beloved csv"
times.to_csv("/root/benchmark_lists_dicts.csv", index = True)
print "Done!"