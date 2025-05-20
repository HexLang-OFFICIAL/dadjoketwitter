import tweepy
import time
import random
import os  # for environment variables

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

dad_jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Did you hear about the restaurant on the moon? Great food, no atmosphere.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I would tell you a construction joke, but I'm still working on it."
]

def tweet_joke():
    joke = random.choice(dad_jokes)
    try:
        api.update_status(joke)
        print(f"Tweeted: {joke}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    tweet_joke()  # Only tweet once per workflow run
