The first version of our schema is made by Fangzhou, and the second version of schema is made by Mil. The following steps in milestone 2 adopts the second version.

# The first version
Table_cde(unique_id, timestamp, timegroup, word_phrase_in_sequence, trendiness_score)

‘unique_id’ is artificially added to distinguish different words and phrases at different timestamp. It has no real meaning. 

‘timestamp’ is the time each word or phrase appear exactly.

‘timegroup’ cuts the whole time we extract from Twitter into one minute. We can easily calculate the current minute interval by “timegroup minus timestamp”.

‘word_phrase_in_sequence’ is the column which cuts each sentence into word pieces, and sort them in order of appearance. 

‘trendiness_score’ calculates trendiness score(see formula at page 2) for each word at each timestamp. The detailed calculation will be accomplished in Milestone Part B. All the thing we need to do in Part E is to query.

The ‘unique_id’ serves as the primary key.

# The second version
WORD_STREAM(stream_id, word, timestamp)
WORD_TRENDINESS(word, trendiness, time)
