import extract_msg, re
from core.email_model import Email
from os import path


def parse_msg(file_name, file_path, mode):
    message = extract_msg.Message(file_path)
    date = ""
    sender = ""
    recipients = ""
    subject = ""
    body = ""
    atts = []
    if mode in ("Contents", "Both"):
        headers = str(message.header).splitlines()
        sender_name = ""
        sender_email = ""
        for header in headers:
            if header.startswith("From:"):
                sender_info = re.search(r'From:\s+"?(.*?)"?\s*(<.*?>)', header)
                if sender_info:
                    sender_name = sender_info.group(1).strip(' "')
                    sender_email = sender_info.group(2).strip(' "')
        sender = sender_name + " " + sender_email
        recipients = message.to
        subject = message.subject
        body = message.body
    if mode in ("Attachments", "Both") and message.attachments:
        for att in message.attachments:
            file_name = att.longFilename or att.shortFilename
            att.save(customPath="results")
            file_path = path.join("results", file_name)
            atts.append(file_path)
    return Email(file_name, date, subject, sender, recipients, body, atts)
