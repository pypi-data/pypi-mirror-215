from sys import path
path.append('../Tweet')
from os import environ
from Tweet import Tweet

tweet = Tweet(
    client_id=environ["TWITTER_CLIENT_ID"],
    client_secret=environ["TWITTER_CLIENT_SECRET"],
    callback_uri=environ["TWITTER_CALLBACK_URI"]
)

response = tweet.tweet(
    text="Hello world!",
    image_path="../test/test.jpg"
)
print(response[0], response[1])
