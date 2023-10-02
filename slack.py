import configparser
import json
import requests

config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')

class Slack:
    def __init__(self):
        self.hook = config["SLACK"]['SLACK_HOOK']
        self.hist_url = config["SLACK"]['HISTORY']
        self.token = config["SLACK"]["TOKEN"]
        self.channel = config["SLACK"]["CHANNEL"]

    def post(self):
        res = requests.post(self.hook,json.dumps(self.msg_payload))

    def post_reply(self):
        res = requests.post(self.hook,json.dumps(self.reply_payload))
     
    def get_last_msg_id(self):
        header = {'Content-Type':'application/x-www-form-urlencoded', 'Authorization': 'Bearer {}'.format(self.token)}
        res = requests.get(self.hist_url, params={'channel':self.channel,'limit':1},headers=header).json()
        msg = res['messages'][0]
        return msg['ts']

    def create_payload(self,name,pic):
        self.msg_payload = {
            "text" : "15時をお知らせします。そろそろ一息つきませんか？",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "15時をお知らせします。そろそろ一息つきませんか？"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "かわいい"+ name + "の写真です↓"
                    }
                },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": name
                    },
                    "image_url": pic,
                    "alt_text": "marg"
                }
            ]
        }

    def create_reply(self,name,desc):
        msg_id = self.get_last_msg_id()
        self.reply_payload = {
            "thread_ts": msg_id,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": name
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": desc
                    }
                }
            ]
        }