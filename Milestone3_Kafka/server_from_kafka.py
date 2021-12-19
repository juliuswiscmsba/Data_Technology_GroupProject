from kafka import KafkaConsumer
import sys
import json
import time
import numpy as np
import pandas as pd
import re
import psycopg2
import datetime


def readin_file():
	f = open('tweets.txt','r')
	lines = f.readlines()
	f.close()
	return lines



def split_tweet(testline):
    pattern_special = re.compile(r'[\#\@\_]+')
    testline = re.sub(pattern_special, ' ', testline)

    pattern_interval = re.compile(r'[\s\,\;\.]+')
    test_list = re.split(pattern_interval, testline)

    word_list = []
    for item in range(len(test_list)):
        if item > 0:
            if test_list[item] != '' :
                word_list.append([test_list[0], test_list[item]])
    return word_list



def word_stream(lines):
    stream = []
    for line in lines:
        stream += split_tweet(line)
    return stream



def word_count(lines, current_timestamp = None):

    flow = word_stream(lines)
    if current_timestamp == None: 
    	current_timestamp = flow[-1][0]
    flow = np.array(flow)

    current_min_start = current_timestamp[0:-2]+"00"
    #print(current_min_start)
    previous_min_start = current_timestamp[0:-5]+str(int(current_timestamp[14:16])-1)+"-00"
    #print(previous_min_start)

    pattern_current = current_min_start[:-2]
    flow_current = []
    for entry in flow:
        if re.match(pattern_current, entry[0]):
            flow_current.append(list(entry))

    df_current = pd.DataFrame(flow_current, columns = ['time', 'word'])
    series_current_word_count = df_current.groupby('word').size()
    df_current_word_count = pd.DataFrame({'word':series_current_word_count.index, 'count':series_current_word_count.values})
    return(df_current_word_count.values.tolist())



def vocabulary_size(lines, current_timestamp = None):

    flow = word_stream(lines)
    if current_timestamp == None: 
    	current_timestamp = flow[-1][0]
    flow = np.array(flow)

    current_min_start = current_timestamp[0:-2]+"00"
    previous_min_start = current_timestamp[0:-5]+str(int(current_timestamp[14:16])-1)+"-00"

    pattern_current = current_min_start[:-2]
    flow_current = []
    for entry in flow:
        if re.match(pattern_current, entry[0]):
            flow_current.append(list(entry))

    df_current = pd.DataFrame(flow_current, columns = ['time', 'word'])
    return(len(pd.unique(df_current['word'])))



def calculate_trendiness(lines, current_timestamp=None):

    flow = word_stream(lines)
    if current_timestamp == None: 
    	current_timestamp = flow[-1][0]   

    current_min_start = current_timestamp[0:-2]+"00"
    #print(current_min_start)
    previous_min_start = current_timestamp[0:-5]+str(int(current_timestamp[14:16])-1)+"-00"
    #print(previous_min_start)

    current_word_count = word_count(lines, current_timestamp)
    #prior_word_count = word_count(lines, current_timestamp)
    prior_word_count = word_count(lines, previous_min_start)

    current_V = vocabulary_size(lines, current_timestamp)
    prior_V = vocabulary_size(lines, previous_min_start)

    current_total_num = np.array(current_word_count)[:,1].astype(np.int).sum()
    prior_total_num = np.array(prior_word_count)[:,1].astype(np.int).sum()
    df_trendiness = pd.DataFrame(current_word_count, columns = ["word", "count"])
    #print(current_V, prior_V, current_total_num, prior_total_num)

    for entry1 in current_word_count:

        p1 = (1 + entry1[1])/(current_V + current_total_num)
        p0 = (1 + 0)/(prior_V + prior_total_num)
        trendiness = np.log10(p1/p0)

        for entry0 in prior_word_count:
            if entry1[0] == entry0[0]:
                p1 = (1 + entry1[1])/(current_V + current_total_num)
                p0 = (1 + entry0[1])/(prior_V + prior_total_num)
                trendiness = np.log10(p1/p0)   

        df_trendiness.loc[df_trendiness["word"]==entry1[0], "trendiness"] = trendiness
        df_trendiness.loc[df_trendiness["word"]==entry1[0], "time"] = current_timestamp


    return(df_trendiness.values.tolist())




def load_in(stream):
	# open a connection (make sure to close it later)
	conn = psycopg2.connect(user="gb760", dbname = "twitter")

	# create a cursor
	cur = conn.cursor()

	# execute a SQL command
	for entry in stream:
		#print(entry)
				
		cur.execute("""INSERT INTO WORD_TRENDINESS (word, TRENDINESS, time) VALUES (%s,%s,%s) ON CONFLICT(word) DO UPDATE SET word = excluded.word, trendiness = excluded.trendiness, time = excluded.time""", (entry[0], entry[2], entry[3]))
		conn.commit()	
	if conn:            
		cur.close()
		conn.close()
		

		
		
if __name__ == "__main__":
	consumer = KafkaConsumer(
	    'final_project',
	     bootstrap_servers=['localhost:9092'],
	     auto_offset_reset='earliest',
	     enable_auto_commit=True,
	     group_id='my-group-' + str(time.time()),
	     value_deserializer=lambda x: x.decode('utf-8'))

	count = 0
	f = open('tweets.txt','w')
	curr_kafka_time = datetime.datetime.strptime("1211-11-11-11-11-11", "%Y-%m-%d-%H-%M-%S")
	for message in consumer:
	 if count == 0:
	  first_kafka_t = message[6][10:29]
	  first_kafka_time = datetime.datetime.strptime(first_kafka_t, "%Y-%m-%d-%H-%M-%S")
	  count += 1
	 else:
	  curr_kafka_t = message[6][10:29]
	  print(curr_kafka_t)
	  curr_kafka_time = datetime.datetime.strptime(curr_kafka_t, "%Y-%m-%d-%H-%M-%S")-datetime.timedelta(minutes=1)
	 
	 
	 kafka_data = message[6]	  
	 new_kafka_data = kafka_data[10:29] +','+kafka_data[41:-2]+'\n'
	 f.write(new_kafka_data)
	  
	 if curr_kafka_time > first_kafka_time:
	  print("Loading to PostgreSQL...")
	  f.close()
	  lines = readin_file()
	  load_in(calculate_trendiness(lines))
	  f = open('tweets.txt','a')

	sys.exit()
