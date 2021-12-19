import numpy as np
import pandas as pd
import re

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
	

    return(df_trendiness.values.tolist())



if __name__ == "__main__":
	lines = readin_file()
	for i in calculate_trendiness(lines):
		print(i)
