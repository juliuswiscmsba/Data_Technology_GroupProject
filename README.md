#### Milestone 1: Simple Read Sort folder

* server.py: Read tweets from the Twitter API or a file, write tweets to a file

* test.json: Json file for testing

* tweets.txt: Store the tweets in tweets.txt file

* vocabulary_size.py: Compute the number of unique words

* word_count.py: Compute frequencies of words and phrases


#### Milestone 2: PostgreSQL folder

* schema_postgres.sql: SQL Table Schema

* server_postgres.py: Read tweets from the Twitter API or a file, write the information needed to compute the trendiness score to PostgreSQL

* test.json: Json file for testing

* trendiness_postgres.py: Compute the trendiness score

* tweets.txt: Store the tweets in tweets.txt file

* vocabulary_size_postgres.py: Compute the number of unique words in the current minute

* word_count_postgres.py: Compute frequencies of words and phrases in the current minute


#### Milestone 3: SQL interact with Kafka 

* consumer.py: Kafka consumer file

* server_from_kafka.py: Read tweets from Kafka, write the information needed to compute the trendiness score to PostgreSQL

* server_to_kafka.py: Read tweets from the Twitter API or a file, write tweets to a Kafka queue

* test.json: Json file for testing

* trendiness_kafka.py: Continuously compute the most up-to-date trendiness score of a word/phrase

* tweets.txt: Store the tweets in tweets.txt file
