1. Twitter authorization failure. 
Problem: It came up with 403 in I first run of my code. 
Solve method: Export ‘BEARER_TOKEN’ = ‘<your_bearer_token>’ in my terminal and run.
Resource: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Tweet-Lookup/get_tweets_with_bearer_token.py

2. Convert timestamp failure.
Problem: Fail to convert the timestamp into the format “YYYY-MM-DD-HH-MM-SS”
Solve method: Using the function ‘strftime’ and’ strptime’ in the Python time library to convert the format.
Resource: https://stackoverflow.com/questions/214777/how-do-you-convert-yyyy-mm-ddthhmmss-000z-time-format-to-mm-dd-yyyy-time-forma/215313

3. Read JSON file failure.
Problem: Fail to read a JSON file line by line.
Solve method: Create a list to store the content.
Resource: https://stackoverflow.com/questions/12451431/loading-and-parsing-a-json-file-with-multiple-json-objects


