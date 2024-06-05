import os
import json
import requests
from string import Template
from twikit import Client
import telegram

# Apply patch to twikit
from twikit_patch import apply_patch
apply_patch()

last_messages = {}

def load_last_messages():
    try:
        with open('last_messages.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('last_messages.json', 'w') as file:
            file.write('{}')
        return {}
    except json.JSONDecodeError:
        return {}

def save_last_message(user_id, message):
    last_messages = load_last_messages()
    last_messages[user_id] = message
    with open('last_messages.json', 'w') as file:
        json.dump(last_messages, file, indent=4)

def create_message_template(user_name, followers_list):
    last_messages = load_last_messages()
    template = Template("<b>New followers: $user! 📈</b>\n<b>$followers</b>")
    new_followers = [f for f in followers_list if f.name not in last_messages.get(f.name, [])]
    if not new_followers:
        print(f"No new followers for {user_name}.")
        return None
    followers_formatted = '\n'.join([f'<a href="https://twitter.com/{follower.screen_name}">{follower.name}</a>' for follower in new_followers])
    for tweet in followers_list:
        save_last_message(str(tweet.name), tweet.name)
    return template.substitute(user=user_name, followers=followers_formatted)

USERNAME = os.getenv('TWITTER_USERNAME')
EMAIL = os.getenv('TWITTER_EMAIL')
PASSWORD = os.getenv('TWITTER_PASSWORD')

client = Client('en-US')

client.login(
    auth_info_1=USERNAME,
    auth_info_2=EMAIL,
    password=PASSWORD
)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

twitter_usernames = [
    'DeFiTracer', 'ShmooNFT', 'MacnBTC', 'TheCryptoKazi',
    'rektfencer', 'KashKysh', 'liamdnft', 'nobrainflip', 'W0LF0FCRYPT0'
]

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def fetch_and_notify_new_followers():
    for twitter_username in twitter_usernames:
        user = client.get_user_by_screen_name(twitter_username)
        user_id = user.id
        followers = client.get_user_following(user_id, 1)
        message = create_message_template(twitter_username, followers)
        if message:
            data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
            response = requests.get(url, params=data)

if __name__ == "__main__":
    fetch_and_notify_new_followers()
