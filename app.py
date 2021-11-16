import logging
import os
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from document_list import DocumentList
from document_finder import DocumentFinder

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN")
)

config = {}

def discover_documents(query, directory_list):
    document_list = DocumentList()
    document_finder = DocumentFinder()
    documents, directory = document_finder.get_recommended_documents(query, directory_list)
    
    if not documents:
        return

    return document_list.get_message_payload(documents, config["GIT_URL"], directory)

@app.event("message")
def generate_docs(body, say):
    threadTs = ""
    if "thread_ts" in body["event"].keys() :
        threadTs = body["event"]["thread_ts"]
    else:
        threadTs = body["event"]["ts"]
    query = body["event"]["text"]
    print(query)

    documents = discover_documents(query, config["DOC_DIRECTORIES"])
    # If no documents to provide, don't bother responding to the message
    if documents == None:
        return None

    say(
        blocks=documents,
        text="Here's some docs",
        thread_ts=threadTs
    )

if __name__ == "__main__":
    load_dotenv()

    with open('config.json') as f:
        config = json.load(f)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()