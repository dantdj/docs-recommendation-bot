import os

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

    def extract_document_title(self, document):
        # Take the first line, remove the first two characters to remove the Markdown
        # formatting for the header, and then strip to remove whitespace
        with open(document) as f:
            return f.readline()[2:].strip()

    def get_message_payload(self, documents, base_url, directory):
        document_block = self.DOC_TEMPLATE_BLOCK
        document_list = []
        
        for document in documents:
            separated_url = document.split(os.sep)
            # TODO: Oh god this is hacky
            url = f'{base_url}/projects/{directory["project"]}/repos/{separated_url[4]}/browse/{"/".join(separated_url[5:])}'
            mrkdwn_url = f'<{url}|{self.extract_document_title(document)}>'
            document_list.append("- " + mrkdwn_url)

        document_block["text"]["text"] = '\n'.join(document_list)

        return [
                self.INTRO_BLOCK,
                self.DIVIDER_BLOCK,
                document_block
        ]
    