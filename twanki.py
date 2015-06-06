from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import MeCab
import json
import unicodedata
from pprint import pprint as pp
from blitzdb import Document
from blitzdb import FileBackend
import senddata

consumer_key = "m03RgEpgBDLsODQZ7ew6yxstf"
consumer_secret = "fhsKFBvYHs0d097F09ijpv3WRxg2Fi8BnHOrMJxvW8QstBFOXl"
access_token = "16979832-LdYmktTeGmAj7IK7sTg9YrU2N5RebroA8deJ7FO9L"
access_token_secret = "Az1ABD07L8BvtFk0Pq7fjaSNNwLIOlCESrXQLjXfSArWn"
DESIRED_KEYS = ['timestamp_ms', 'text']
tweet_count = 0




class Tweet(Document):

    class Meta(Document.Meta):
        primary_key = 'text'

import sys
import os


class Actor(Document):

    class Meta(Document.Meta):
        primary_key = 'first_name'






def kata2hira(kata):
    hira_string = ""
    for char in kata:
        char_string = unicodedata.name(char)
        char_string = char_string.split(" ")
        if "SMALL" in char_string:
            char_name = char_string[-2:]
            hira_name = "HIRAGANA LETTER %s %s" % (char_name[0], char_name[1])
            hira_char = unicodedata.lookup(hira_name)
            hira_string += hira_char
        else:
            char_name = char_string[-1:]
            hira_name = "HIRAGANA LETTER %s" % char_name[0]
            hira_char = unicodedata.lookup(hira_name)
            hira_string += hira_char
    return hira_string


def parse_text(sentence):
    t = MeCab.Tagger("-Ochasen")
    # t.Tagger_formatNode("%f[5]")
    parsed_string = t.parse(sentence)
    parsed_array = parsed_string.split("\n")
    # pp(parsed_array)
    parsed_lines = []
    for line in parsed_array:
        parsed_lines.append(line.split("\t"))
    data = {}
    try:
        for line in parsed_lines:
            if "CJK" in unicodedata.name(line[2][0]):
                data[line[0]] = [line[1]]
    except:
        pass
    for key in data:
        data[key][0] = kata2hira(data[key][0])
    return data


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        dict_data = json.loads(data)
        db_data = {}
        try:
            # Ignore retweets
            if dict_data['retweeted'] == False:
                try:
                    pp("GET DATA")

                    # Get relevant key value pairs only
                    for KEY in DESIRED_KEYS:
                        db_data[KEY] = dict_data[KEY]
                    db_data['screen_name'] = dict_data['user']['screen_name']
                    cards = parse_text(db_data['text'])

                    # Add it to the db_data dict to import into BlitzDB
                    db_data['cards'] = cards
                    pp(db_data)
                except:
                    pp("GET DATA FAILED")
                try:
                    # Import into BlitzDB
                    backend = FileBackend("./test-db")
                    tweet = Tweet(db_data)
                    backend.save(tweet)
                    # backend.commit()
                    pp("DATABASE INSERTION SUCCESSFUL")
                except:
                    pp("DATA INSERTION FAILED")
        except:
            pp("Retweet detected, skipping...")

        return True

    def on_error(self, status):
        print(status)


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    backend = FileBackend("./test-db")
    stream = Stream(auth, l)
    stream.filter(track=['トレクル'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Keyboard interrupt detected')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)