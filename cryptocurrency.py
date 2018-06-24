import os
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import datetime as datetime

# maximum size of API query for currency prices is 23
currency_top = ["BTC", "ETH", "XRP", "XEM", "LTC", "XLM", "ETC", "BCN", "DASH",
                            "DGB", "XMR", "SC", "DOGE", "BTS", "GNT", "ARDR", "EMC2", "ZEC",
                            "STRAT", "NXT", "STEEM", "RDD", "GNO"]
                            
columns = ['LASTUPDATE', 'HIGH24HOUR',  'LASTVOLUMETO',
                                'MKTCAP', 'LASTVOLUME', 'PRICE', 'SUPPLY', 'CHANGEPCT24HOUR',
                                'LOW24HOUR', 'OPEN24HOUR', 'VOLUME24HOURTO', 'FLAGS',
                                'VOLUME24HOUR', 'CHANGE24HOUR', 'TYPE', 'LASTTRADEID',
                                'FROMSYMBOL', 'LASTMARKET', 'MARKET', 'TOSYMBOL']
df = pd.DataFrame({}, columns=columns)

currency_str = ','.join(currency_top)
parameters  = {'fsyms': currency_str, 'tsyms': 'USD'}


while True:
    try:
        response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull', params=parameters)
        for currency in currency_top:
            crypt = response.json()['RAW'][currency]['USD']
            df = df.append(crypt, ignore_index=True)
        print df.loc[:, ['FROMSYMBOL', 'TOSYMBOL', 'PRICE', 'MARKET', 'CHANGEPCT24HOUR']].tail(23)
        print "number of observations in current df: {0}".format(len(df))
        time.sleep(10)

        if len(df) > 10000:
            print "new csv file outputted"
            df.to_csv("cryptcoin_{0}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")))
            df = pd.DataFrame({}, columns=columns)
    
        #plt.axis([ 0, 100, -1,1])
    #plt.xlabel('Time')
    #plt.ylabel('Sentiment')
    #plt.plot([t],[currency_str],'go)
    #plt.show()
    #plt.savefig('foo.png')
    #plt.pause(0.0001)
    
    except:
        time.sleep(15)
        continue
