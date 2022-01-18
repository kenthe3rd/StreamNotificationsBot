import requests
import os
from dotenv import load_dotenv

load_dotenv('../.env')

class TwitchHelper:

    def userOnline(self, user_login):
        url = "https://api.twitch.tv/helix/streams?user_login=" + user_login
        headers={
            "Authorization":"Bearer " + os.getenv("TWITCH_TOKEN"),
            "Client-Id": os.getenv("TWITCH_CLIENT_ID")
        }
        res = requests.get(url, headers=headers)
        result = res.json()
        if result['data'] ==  []:
            return False
        else:
            return True
        
    def getStream(self, user_login):
        url = "https://api.twitch.tv/helix/streams?user_login=" + user_login
        headers={
            "Authorization":"Bearer " + os.getenv("TWITCH_TOKEN"),
            "Client-Id": os.getenv("TWITCH_CLIENT_ID")
        }
        res = requests.get(url, headers=headers)
        result = res.json()
        return result