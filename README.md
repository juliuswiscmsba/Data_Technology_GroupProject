#Milestone 1
Part A 

Set your environment in your terminal run the following line: 
export ‘BEARER_TOKEN’ = ‘<your_bearer_token>’

For example: 
export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAKVkVAEAAAAAUnzDwyYuL6V%2BUB4%2FOc%2BsJBHo%2BL0%3DPy1K9NUa4V3W8KU9vruHBcMwYN8k7gE855Hkpt4J2mDe3i5Ak5'

Run the server.py file 
Enter the following line to open the file:
python server.py

If it shows 200 and starts to print Datetime, then we successfully execute the file.

Press ctrl c to jump out.

Run the server.py file with json file
Enter the following line to open the file:
python server.py --filename <your_jsonfile>

For example:
python server.py --filename test.json

By doing so, the python file will read the content in json file and write on tweets.txt.

Part B

Run the word_count.py file
Enter the following line to execute the file code:
python word_count.py '<your_word_or_phrase>'

For example (to count instance of single word):
python word_count.py 'hello' 

For example (to count instances of multi-word phrase):
python word_count.py 'different check'

Part C

Run the vocabulary_size.py file:
Enter the following line to execute the file code:
python vocabulary_size.py

It will print out a number indicating the number of unique words in tweets.txt


#Milestone 2
Create PostgreSQL tables
Run the command in your terminal: `psql`
Then run the SQL command: `create database twitter;`
Then run the terminal: `psql twitter < schema_postgres.sql`

Read tweets and load into database
Run the Python code in your terminal to read from twitter API: `python server_postgres.py`
Run the Python code in your terminal to read from json file: `python server_postgres.py -- filename <json_file_name>`

Compute the frequency of words in the current minute
Run the Python code in your terminal: `python word_count_postgres.py`

Compute the number of unique words in the current minute
Run the Python code in your terminal: `python vocabulary_size_postgres.py`

Compute the trendiness score
Run the Python code in your terminal: `python trendiness_postgres.py`



#Milestone 3
Install the Kafka and kafka-python (pip install kafka-python)

All Kafka related files should store in the "kafka" folder (server_to_kafka.py, server_from_kafka.py, trendiness_kafka.py, consumer.py, test.json)

First, we need to create a "topic"
Move to kafka folder: cd kafka
Run the following code in your terminal: ~/kafka/bin/kafka-topics.sh --create --topic final_project --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

Part A

Run the server_to_kafka.py file (download tweets from Twitter API): python server_to_kafka.py
Same as milestone 1 part A, if it shows 200 and starts to print Datetime, then we successfully downloading the data.
Run the server_to_kafka.py file (download tweets from JSON file): python server_to_kafka.py –filename <json_filename>  Ex: python server_to_kafka.py –filename test.json

Part B 

While server_kafka.py file is running, open another terminal and run the server_from_python.py file.
(We should wait more than 1 minute because the trendiness needs previous minute to calculate) 
The terminal will show only the time (Ex: "2021-12-03-11-12-13") if the the execute time is less than one minute.
The terminal will show "Loading to postgreSQL" when we load data into our SQL table.

Part C

While server_to_kafka.py and server_from_kafka.py files are both running, open another terminal and execute trendiness_kafka.py file.(python teendiness_kafka.py '<your_word_or_phrase>')
For example, we want to know the latest trendiness of the word "awesome": python trendiness_kafka,py awesome

The terminal will show the latest word, trendiness, and time every minute.


