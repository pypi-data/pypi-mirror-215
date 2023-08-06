import os

import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter

from langpack import apis

# This is slack token
langchain_app = apis.unpack("app.json")

SLACK_TOKEN = os.environ["SLACK_TOKEN"]
SIGNING_SECRET = os.environ["SIGNING_SECRET"]

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)

client = slack.WebClient(token=SLACK_TOKEN)

history_msg_id = []


@slack_event_adapter.on("app_mention")
@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    client_msg_id = event.get("client_msg_id")
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if not user_id == os.environ["MEMBER_ID"]:
        if client_msg_id not in history_msg_id:
            history_msg_id.append(client_msg_id)

            langchain_app.memory.chat_memory.clear()

            result = langchain_app.run(text)

            client.chat_postMessage(channel=channel_id, text=result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
