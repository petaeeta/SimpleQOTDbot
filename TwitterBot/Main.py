import tweepy
import time
import os
from io import StringIO
from dotenv import load_dotenv


# Simple Quote Of The Day -bot
# 
# @Author petaeeta, created 4.2.2021.
#
# This is a very simple quote of the day -bot, that
# posts quote of the days to a twitter profile through twitters API
# using tweepy -library. You will need consumer keys that twitter gives you
# when registering as a developer, and you will also need access tokens for
# the bot-profile of your choosing.
#
# Requirements in requirements.txt.
#

def main():

    # loading environment variables(keys and tokens) out of an .env-file(keyexamples.env). Used instead of hardcoding them in for increased security.
    load_dotenv()

    # Open a file "quotes.txt" for reading "r", with encoding utf-8
    # Initializing a list as lines for reading quotes line by line.
    file = open("quotes.txt", "r", encoding="utf8")
    lines = file.readlines()

    # Twitter authorization keys and tokens for the API(consumer keys),
    # and for the twitter bot profile itself(access tokens).
    # They are given when you register for a twitter developer -account.
    #
    # In this example my said keys are stored as environment variables(for security),
    # which are declared by reading them from an .env-file
    # with the load_dotenv() function.
    #
    twitter_auth_keys = {
        "consumer_key": os.getenv("API_key"),
        "consumer_secret": os.getenv("API_secret"),
        "access_token": os.getenv("Access_token"),
        "access_token_secret": os.getenv("Access_token_secret")
    }
    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )

    # Connecting to API with
    api = tweepy.API(auth)

    # TODO: Changing the algorithm so the bot can tweet potentially endless
    # quotes, and isn't limited by twitters' 280-character cap.
    while True:
        concatonatedString = StringIO()
        nextTweet = ""
        for line in lines:
            if line != "\n":
                concatonatedString.write(line)
            else:
                nextTweet = concatonatedString.getvalue()

                # This if-statement checks if the quote is under 280-characters,
                # which is the max amount of characters allowed by twitter.
                # if true -> Post tweet, and wait for 24 hours
                # if false -> Dismiss quote, and start reading the next quote available from the txt-file
                if len(nextTweet) <= 280:
                    api.update_status(status=nextTweet)
                    print(nextTweet)

                    # The interval-length the bot waits between tweets in seconds.
                    # 86 400 for 24-hours.
                    time.sleep(86400) 
                
                # Emptying the strings for the next quote read.
                concatonatedString = StringIO()
                nextTweet = ""
                
# For executing the program from command line
if __name__ == "__main__":
    main()