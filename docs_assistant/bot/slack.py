import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ..chain import get_retrieval_qa_chain, ask
import logging

app = App(token=os.environ['SLACK_BOT_TOKEN'])
qa = get_retrieval_qa_chain(os.environ['CHROMA_DB_DIR'])

def answer(event, say):
    response = ask(qa, event['text'])
    say(text=response, channel=event['channel'], mrkdwn=True)

@app.event('message')
def on_message(event, say):
    if event.get('subtype') or event.get('channel_type') != 'im':
        return
    answer(event, say)

@app.event('app_mention')
def on_app_mention(event, say):
    answer(event, say)

if __name__ == '__main__':
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
