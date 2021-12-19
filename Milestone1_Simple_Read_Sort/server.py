import requests
import os
import json
import time
import sys
import spacy
import re
import argparse

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

def clean_text(text):
   if type(text) != str:
       text = text.decode("utf-8")
   doc = re.sub(regex, '', text, flags=re.MULTILINE) # remove URLs
   sentences = []
   for sentence in doc.split("\n"):
       if len(sentence) == 0:
           continue
       sentences.append(sentence)
   doc = nlp("\n".join(sentences))
   doc = " ".join([token.lemma_.lower().strip() for token in doc
                       if (not token.is_stop)
                           and (not token.like_url)
                           and (not token.lemma_ == "-PRON-")
                           and (not len(token) < 4)])
   return doc


def create_url():
    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at%2Clang"
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url,f):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response.status_code)
    old_tt = '1111-11-11-11-11-11'
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response["data"]["lang"] == "en":
            	json_response["data"]["created_at"] = time.strftime("%Y-%m-%d-%H-%M-%S", time.strptime(json_response["data"]["created_at"][:19], "%Y-%m-%dT%H:%M:%S"))
            	json_response["data"]["text"] = clean_text(json_response["data"]["text"])
            	new_json_response = json_response["data"]["created_at"]+","+json_response["data"]["text"]+"\n"
            	#from: https://stackoverflow.com/questions/214777/how-do-you-convert-yyyy-mm-ddthhmmss-000z-time-format-to-mm-dd-yyyy-time-forma/215313
            	
            	new_tt = json_response["data"]["created_at"]
            	f.write(new_json_response)
            	if new_tt > old_tt:
            	 print(new_tt)
            	 old_tt = new_tt
            	#print(new_json_response)
            	
            	
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main():
    url = create_url()
    f = open('tweets.txt','w')
    timeout = 0
    while True:
        connect_to_endpoint(url,f)
        timeout += 1
   
   
def tweets_or_jsonfile():
    parser = argparse.ArgumentParser(description='filename')
    parser.add_argument('--filename', type=str, default='no file then read from twitter API', help='Enter a Json file name or enter nothing to read from twitter API')
    args = parser.parse_args() 
    if args.filename == 'no file then read from twitter API':
     main()  
    else:
     with open(args.filename, 'r') as fjson:
      f = open('tweets.txt','w') 
      data_line = []
      for line in fjson:
       data_line.append(json.loads(line))

      for i in range(len(data_line)):
       zcontent = data_line[i]['data']['created_at'] +','+ data_line[i]['data']['text']
       #print(zcontent)
       f.write(zcontent)
       f.write('\n')
       

if __name__ == "__main__":
    tweets_or_jsonfile()
    
    
    
    
    
    
    

