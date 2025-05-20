import tweepy
import time
import requests
import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def get_dad_joke():
    headers = {"Accept": "application/json"}
    try:
        response = requests.get("https://icanhazdadjoke.com/", headers=headers)
        if response.status_code == 200:
            joke = response.json().get("joke")
            return joke
        else:
            print(f"Failed to get joke: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception during joke fetch: {e}")
        return None

def tweet_joke():
    joke = get_dad_joke()
    if joke:
        try:
            api.update_status(joke)
            print(f"Tweeted: {joke}")
        except Exception as e:
            print(f"Error tweeting: {e}")
    else:
        print("No joke fetched, skipping tweet.")

if __name__ == "__main__":
    tweet_joke()
