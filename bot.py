import pynder
import config
import time
import datetime
import requests
from messages import messages

requests.packages.urllib3.disable_warnings()  # Find way around this...

session = pynder.Session(config.FACEBOOK_ID, config.FACEBOOK_AUTH_TOKEN)


def log(msg):
    print '[' + str(datetime.datetime.now()) + ']' + ' ' + msg


def send(match, message_no):
    for m in messages[message_no]:
        session._api._post('/user/matches/' + match['id'],
                           {"message": m})
        time.sleep(3)
    log('Sent message ' + str(message_no) + ' to ' + match['person']['name'])


def message(match):
    ms = match['messages']
    khaled = session.profile.id
    if not ms:
        send(match, 0)
        return
    said = False
    count = 0
    name = match['person']['name']
    for m in ms:
        if m['from'] == khaled:
            count += 1
            said = False
        elif 'dj khaled' in m['message'].lower():
            said = True
    if count >= len(messages):
        log('Finished conversation with ' + name)
        return
    if said:
        send(match, count)
    else:
        log('No new messages from ' + name)


def handle_likes():
    while True:
        try:
            users = session.nearby_users()
            for u in users:
                if u.name == 'Tinder Team':
                    log('Out of swipes.')
                    return
                u.like()
                log('Liked ' + u.name)
        except ValueError:
            continue
        except pynder.errors.RequestError:
            continue


def handle_matches():
    log(str(len(session._api.matches())) + ' matches')
    matches = session._api.matches()
    for m in matches:
        message(m)


while True:
    handle_likes()
    handle_matches()
    log('Pausing for ten minutes...')
    time.sleep(600)
