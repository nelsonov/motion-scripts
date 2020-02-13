#!/usr/bin/python3

#from slackclient import SlackClient
from slack import WebClient
import os
import sys

slack_token = os.environ["SLACK_API_TOKEN"]
sc = WebClient(slack_token)
alert=sys.argv[1]

sc.chat_postMessage(
    channel='homeassistant',
    text=alert
)
