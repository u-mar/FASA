from google_play_scraper import app, Sort, reviews_all,reviews
import json
import numpy as np
import pandas as pd


def play(app_id, last_review, first_time=False):
    try:
        total = app(app_id, 'en', 'ke')['reviews']
        print(total)
        
        if total <= last_review:
            print("No new reviews")
            return None,last_review
            
        fetch = None
        
        if first_time:
            fetch = reviews_all(
                app_id,
                sleep_milliseconds=0,
                lang='en', 
                country='ke', 
                sort=Sort.NEWEST,
            )    
        else:
            count = total - last_review
            print(f"Fetching New {count} Review")
            fetch = reviews(
                app_id,
                lang='en', 
                country='ke', 
                sort=Sort.NEWEST,
                count=count
            )
            fetch = fetch[0]
        
        if fetch:
            fetch = pd.DataFrame(np.array(fetch),columns=['review'])
            df = fetch.join(pd.DataFrame(fetch.pop('review').tolist()))
            return df,total
            
        return None,last_review
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None,last_review


if __name__ == '__main__':
    print(play("com.ubercab",0,first_time=True).columns)