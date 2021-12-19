import argparse
import psycopg2
import time



def load_in(targetWord):
	# open a connection (make sure to close it later)
	conn = psycopg2.connect(user="gb760", dbname = "twitter")

	# create a cursor
	cur = conn.cursor()
	
	cur.execute(""" select word, trendiness, time from word_trendiness WHERE word = (%s);""", [targetWord])
	
	for row in cur:
	 print(row)	

	if conn:            
		cur.close()
		conn.close()



# User the argument parser to get the word that was passed in
parser = argparse.ArgumentParser()
parser.add_argument("word")
args = parser.parse_args()
targetWord = args.word
while True:
 #time.sleep(60)
 time.sleep(1) #For testing!
 load_in(targetWord)





