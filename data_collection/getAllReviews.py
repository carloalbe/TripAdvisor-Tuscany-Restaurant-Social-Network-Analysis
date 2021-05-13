import pandas as pd
import os
import sys

if __name__ == "__main__":

    province = sys.argv[1] 
    df = pd.read_csv(f'data/{province}.csv')
    
    if len(sys.argv) <3 : start = 0
    else: start = int(sys.argv[2])
    if len(sys.argv) <4 : end = len(df)
    else: end = int(sys.argv[3])

    for i, link in enumerate(df['link'][start:end]):

        baseurl = "http://www.tripadvisor.com"+link
        command = f"scrapy crawl reviewsRestaurant -a url={baseurl} -O data/{province}/{str(i+start)}.json"
        os.system(command)

