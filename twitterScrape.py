import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from tweepy.streaming import StreamListener
import gc
import json
#authentication
consumer_key = "CONSUMER KEY"
consumer_secret = "SECRET KEY"
#oAuthA authentication for twitter
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
api = tweepy.API(auth)

#getting results to a list
results = []
for tweet in tweepy.Cursor(api.search, q="alienware",rpp=50,locale='en').items(100):
    results.append(tweet)


createdate=[]
createauth=[]
createtext=[]
createscore=[]
index=0
jasonobj="{"

def process_results(results):
    score = ""
    for t in results:
        if (t.lang == 'en'):
            #print(t.created_at)

            #print(t.author.id)
            #print(t.text)
            #print('\n')
            analyse = TextBlob(t.text)
            #print(analyse.sentiment.polarity)
            if 0.6 <= analyse.sentiment.polarity:
                score = "Positive"
            elif analyse.sentiment.polarity < 0.6 and -0.6 < analyse.sentiment.polarity:
                score = "Neutral"
            else:
                score = "Negative"

            createdate.append(t.created_at.isoformat())
            createauth.append(t.author.name)
            createtext.append(t.text)
            createscore.append(score)
            pythonDictionary = {'Time': t.created_at.isoformat(), 'Author': t.author.name, 'Text': t.text,'Score':score}
            print(pythonDictionary)
            gc.collect()


            #createdds.append({'Time': t.created_at, 'Author': t.author.id, 'Text': t.text, 'Score': score})

gc.collect()
process_results(results)
ds=pd.concat([pd.DataFrame(createdate),pd.DataFrame(createauth),pd.DataFrame(createtext),pd.DataFrame(createscore)],axis=1)
ds.columns = ["Time", "Author", "Text", "Score"]
gc.collect()

#jsons=createdds.to_json(orient='records')
#print(jsons)