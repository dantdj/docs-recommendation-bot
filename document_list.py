class DocumentList:
    """Constructs the list of documents to send in the message"""

    INTRO_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "I found the below docs that might be useful:"
            )
        }
    }

    DIVIDER_BLOCK = {"type": "divider"}

    DOC_TEMPLATE_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ""
        }
    }

    def __init__(self):
        pass

    def get_message_payload(self, documents):
        document_block = self.DOC_TEMPLATE_BLOCK
        for document in documents:
            document_block["text"]["text"] += "- " + document + "\n"

        return [
                self.INTRO_BLOCK,
                self.DIVIDER_BLOCK,
                document_block
        ]
    