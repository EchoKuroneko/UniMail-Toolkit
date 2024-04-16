from utils.commons import sanitize_text, remove_html_tags
import json


class Email:
    def __init__(
        self,
        file_name,
        date=None,
        subject=None,
        sender=None,
        recipients=None,
        body=None,
        attachments=None,
    ):
        self.file_name = sanitize_text(file_name)
        self.date = date if date else ""
        self.subject = sanitize_text(subject) if subject else ""
        self.sender = sanitize_text(sender) if sender else ""
        self.recipients = sanitize_text(recipients) if recipients else ""
        self.body = sanitize_text(remove_html_tags(body)) if body else ""
        self.attachments = attachments if attachments else []


class EmailJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Email):
            return {
                "file_name": obj.file_name,
                "date": obj.date,
                "subject": obj.subject,
                "sender": obj.sender,
                "recipients": obj.recipients,
                "body": obj.body,
                "attachments": [name for name in obj.attachments],
            }
        return json.JSONEncoder.default(self, obj)
