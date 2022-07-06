import requests
import json
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv()

# f = open("sample.json")

# event1 = json.load(f)

def parse_embeds(event):
    return   [
                {
                    "name": "account",
                    "value": event['account'],
                    "inline": True
                },
                {
                    "name": "region",
                    "value": event['region'],
                    "inline": True
                },
                {
                    "name": "resource",
                    "value": ", ".join([resource.split('/')[-1] for resource in event['resources']]),
                    "inline": True
                },
                {
                    "name": "detail.eventType",
                    "value": event['detail']['eventType'],
                    "inline": True
                },
                {
                    "name": "detail.eventName",
                    "value": event['detail']['eventName'],
                    "inline": True
                },
                {
                    "name": "detail.clusterArn",
                    "value": event['detail']['clusterArn'].split('/')[-1],
                    "inline": True
                },
                {
                    "name": "detail.reason",
                    "value": event['detail']['reason'],
                    "inline": True
                }
            ]

      

def lambda_handler(event, context):
    embeds = parse_embeds(event)
    webhook_url = os.getenv("WEBHOOK_URL")
    
    headers = {'Content-Type': 'application/json'}
    dicord_data = {
        'username': 'AWS',
        'avatar_url': 'https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png',
        "embeds":[{
            "color": 1127128,
            "fields": embeds
        }]
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(dicord_data)
                                 )
    logging.info(f'Discord response: {response.status_code}')
    logging.info(response.content)
