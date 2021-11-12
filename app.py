import logging
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from document_list import DocumentList
from document_finder import DocumentFinder

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN")
)

document_messages_sent = {}

def discover_documents(query):
    document_list = DocumentList()
    document_finder = DocumentFinder()
    documents = document_finder.get_recommended_documents(query)

    return document_list.get_message_payload(documents)

@app.event("message")
def generate_docs(body, say):
    threadTs = ""
    if "thread_ts" in body["event"].keys() :
        threadTs = body["event"]["thread_ts"]
    else:
        threadTs = body["event"]["ts"]
    query = body["event"]["text"]
    print(query)
    
    say(
        blocks=discover_documents(query),
        text="Here's some docs",
        thread_ts=threadTs
    )

if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()