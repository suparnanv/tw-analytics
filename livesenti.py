# -*- coding: utf-8 -*
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

"# -- coding: utf-8 --"

def calctime(a):
    return time.time()-a

positive=0
negative=0
compound=0
poscount=0
posavg=0
negcount=0
negavg=0
count=0
initime=time.time()
plt.ion()

import test
from sensitive import *
'''placeholder for private variables
ckey=...
csecret=..
atoken=
asecret=
'''

class listener(StreamListener):
    
    def on_data(self,data):
        global initime
        t=int(calctime(initime))
        all_data=json.loads(data)
        tweet=all_data["text"].encode("utf-8")
        #username=all_data["user"]["screen_name"]
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet))
        blob=TextBlob(tweet.strip())

        global positive
        global poscount
        global posavg
        global negative
        global negcount
        global negavg
        global compound
        global average
        global count
        senti=0
        count=count+1
       
        
        for sen in blob.sentences:
            senti+=sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive+=sen.sentiment.polarity
                poscount=poscount+1
                posavg=positive/poscount
            else:
                negative+=sen.sentiment.polarity
                negcount=negcount+1
                negavg=negative/negcount
        compound=compound+senti
        average=(posavg+negavg)/2
    
    
        print count
        print tweet.strip()
        print senti
        print t
        print str(positive) + ' ' + str(negative) + ' ' + str(compound) 
        
        #graph definition
        plt.axis([ 0, 100, -1,1])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[posavg],'go',[t] ,[negavg],'ro',[t],[average],'bo')
        plt.show()
        plt.savefig('foo.png')
        plt.pause(0.0001)
        
        #exit condition
        if count==2000:
            return False
        else:
            return True
        
    def on_error(self,status):
        print status


auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream=  Stream(auth, listener(count))
twitterStream.filter(track=["ripple", "XRP" ])
      
 

