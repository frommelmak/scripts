#!/usr/bin/env python
import argparse
import time
import tweetstream
from colorama import Fore, Style


def print_tweet(tweet):
    print Style.BRIGHT + "Name:" + \
          Style.NORMAL + " %s" % tweet['user']['name']
    print Style.BRIGHT + "Username:" + \
          Style.NORMAL + " @%s" % tweet['user']['screen_name']
    print Fore.CYAN + "%s" % tweet['text']
    print Fore.RESET + "Location: %s, Lang: %s, followers: %s" % (
          tweet['user']['location'],
          tweet['user']['lang'],
          tweet['user']['followers_count'])


def bind(user, password, words, lang, n, t):

    words = [words, ]
    count = 0
    try:
        with tweetstream.FilterStream(user, password, track=words) as stream:
            print "Connecting..."
            duration = 0
            start = time.time()
            for tweet in stream:
                if lang == 'all':
                    print Fore.BLUE
                    print "------ Counter: %s -- Duration: %.2f secs -----" % (
                          stream.count, duration)
                    print Fore.RESET
                    print_tweet(tweet)
                elif tweet['user']['lang'] in lang:
                    print Fore.BLUE
                    print "------ Counter: %s -- Duration: %.2f secs -----" % (
                          stream.count, duration)
                    print Fore.RESET
                    print_tweet(tweet)
                duration = time.time() - start
                if int(stream.count) == int(n):
                    print "number of requested tweets reached!"
                    return [stream.count, duration]
                if duration >= t:
                    print "requested execution time reached!"
                    return [stream.count, duration]
    except tweetstream.ConnectionError, e:
        print "Disconnected from twitter. Reason:", e.reason


def main():
    parser = argparse.ArgumentParser(description='Command line tool for live Twitter search')
    parser.add_argument('-u', '--user', required=True, help="Tweeter user name")
    parser.add_argument('-p', '--password', required=True, help="Tweeter password")
    parser.add_argument('word', help="The word you are looking for about")
    parser.add_argument('-l', '--lang', nargs='+', default='all', help="The language for the tweets you are looking for")
    parser.add_argument('-t', '--time', type=int, default=60, help="Max execution time in seconds")
    parser.add_argument('-n', '--number', type=int, default=10, help="Number of tweets to retrieve")
    arg = parser.parse_args()
    stats = bind(arg.user, arg.password, arg.word, arg.lang, arg.number, arg.time)
    print "Number of tweets: %d, Duration: %.2f" % (stats[0], stats[1])
if __name__ == "__main__":
    main()