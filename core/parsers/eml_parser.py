import email
from core.email_model import Email
from os import path


def parse_eml(file_name, file_path, mode):
    try:
        message = email.message_from_file(
            open(file_path, encoding="utf-8"), policy=email.policy.default
        )
    except UnicodeDecodeError:
        message = email.message_from_file(
            open(file_path, encoding="latin-1"), policy=email.policy.default
        )
    date = ""
    sender = ""
    recipients = ""
    subject = ""
    body = ""
    attachments = []

    for part in message.walk():
        if mode in ("Contents", "Both"):
            try:
                parsed_date = email.utils.parsedate_to_datetime(message["date"])
                if parsed_date is None:
                    raise ValueError(
                        "Parsed date is None, likely an invalid date format."
                    )
                date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            except (TypeError, ValueError, email.errors.HeaderParseError) as e:
                date = ""
                print(f"{e}")
            sender = message["to"]
            recipients = message["from"]
            subject = message["subject"]
            content_type = part.get_content_type()
            if content_type in ("text/plain", "text/html"):
                payload = part.get_payload(decode=True)
                try:
                    decoded_payload = payload.decode("utf-8")
                except UnicodeDecodeError:
                    decoded_payload = payload.decode("latin-1", errors="replace")
                body += decoded_payload
        if mode in ("Attachments", "Both") and message.is_multipart():
            content_disposition = part.get("Content-Disposition")
            if content_disposition and "attachment" in content_disposition:
                file_name = part.get_filename()
                if not file_name:
                    file_name = "default"
                payload = part.get_payload(decode=True)
                file_path = path.join("results", file_name)
                with open(file_path, "wb") as f:
                    f.write(payload)
                attachments.append(file_path)
    return Email(file_name, date, subject, sender, recipients, body, attachments)
