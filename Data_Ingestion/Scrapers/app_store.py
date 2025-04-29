from app_store_web_scraper import AppStoreEntry, AppStoreSession
import pandas as pd

def App_store(app_id):
    session = AppStoreSession(
        delay=0.5,
        delay_jitter=0.1,
        retries=5,
        retries_backoff_factor=3,
        retries_backoff_max=20,
    )
    

    country_code = "ke"  
    

    app = AppStoreEntry(app_id=app_id, country=country_code, session=session)
    
    review_data = {
        "rating": [],
        "review": [],
        "userName": [],
        "title": [],
        "date": [] 
    }

    
    for review in app.reviews(limit=1000):
        review_data["rating"].append(review.rating)
        review_data["review"].append(review.content)
        review_data["userName"].append(review.user_name)
        review_data["title"].append(review.title)
        review_data["date"].append(review.date) 
    
    df = pd.DataFrame(review_data)
    
    return df

if __name__ == "__main__":
    reviews_df = App_store("1616854301")


