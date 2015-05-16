import pynder
import config
import time
import datetime
import urllib3

urllib3.disable_warnings() # Find way around this...

session = pynder.Session(config.FACEBOOK_ID, config.FACEBOOK_AUTH_TOKEN)


def log(msg):
    print '[' + str(datetime.datetime.now()) + ']' + ' ' + msg


def handle_likes():
    while True:
        try:
            users = session.nearby_users()
            for u in users:
                if u.name == 'Tinder Team':
                    log('Out of swipes, pausing one hour...')
                    return
                u.like()
                log('Liked ' + u.name)
        except ValueError:
            continue


def handle_matches():
    log(str(len(session._api.matches())) + ' matches')


while True:
    handle_matches()
    handle_likes()
    time.sleep(3600)
