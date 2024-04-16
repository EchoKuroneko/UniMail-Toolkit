import json
import pandas as pd
import smtplib
from email import encoders
from core.email_model import EmailJsonEncoder
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from config import Config
from utils.commons import isfile


class Publish:
    def __init__(self, emails: object):
        self.emails = emails
        self.json_data = None
        self.server = None

    def export(self):
        self.json_data = json.loads(self.to_json())
        self.to_xlsx()

    def to_json(self, file_name="output"):
        json_data = []
        if self.emails:
            with open(f"results/{file_name}.json", "w") as json_file:
                json.dump(self.emails, json_file, cls=EmailJsonEncoder, indent=4)
            json_data = json.dumps(self.emails, cls=EmailJsonEncoder, indent=4)
            email_count = len(json_data)
            print(
                f"Dumped {email_count} email{'s' if email_count != 1 else ''} to {file_name}.json..."
            )
        return json_data

    def to_xlsx(self, file_name="output"):
        if self.json_data:
            df = pd.DataFrame.from_dict(self.json_data)
            if not df.empty:
                row_count = len(df)
                df.to_excel(f"results/{file_name}.xlsx", index=False)
                print(
                    f"Wrote {row_count} row{'s' if row_count != 1 else ''} to  {file_name}.xlsx..."
                )

    def build_connection(self):
        sender = Config.SMTP_USERNAME
        receiver = Config.SMTP_RECEIVER
        server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
        server.starttls()
        print(f"\nLogging in as <{sender}>...")
        try:
            server.login(sender, Config.SMTP_PASSWORD)
            print("Logged in Successfully.")
        except smtplib.SMTPAuthenticationError:
            error_message = (
                "Failed to authenticate with SMTP server. Please ensure your credentials are correct. "
                "If you have two-factor authentication enabled, you may need to use an app-specific password. "
                "Visit https://myaccount.google.com/apppasswords to set this up."
            )
            self.close_connection()
            raise Exception(error_message)
        self.server = server

        return sender, receiver

    def close_connection(self):
        self.server.halt()

    def mail(self, email_datas: json, opt: str):
        sender, receiver = self.build_connection()
        for email_data in email_datas:
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = receiver
            has_content = False
            if opt in ("Contents", "Both"):
                msg["Subject"] = email_data.subject
                msg.attach(MIMEText(email_data.body, "plain"))
                has_content = True
            if opt in ("Attachments", "Both"):
                for attachment in email_data.attachments:
                    if attachment and isfile(attachment):
                        file_name = attachment.replace("results\\", "")
                        msg["Subject"] = (
                            file_name if not email_data.subject else email_data.subject
                        )
                        try:
                            with open(attachment, "rb") as att:
                                part = MIMEBase("application", "octet-stream")
                                part.set_payload(att.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename= {attachment}",
                            )
                            msg.attach(part)
                            has_content = True
                        except IOError:
                            print(
                                f"Could not open attachment {attachment}. It will not be included in the email."
                            )
                            continue
            if has_content:
                self.server.send_message(msg)
                print(f"Email sent with subject: {msg['Subject']}")
            else:
                print(
                    f"Email not sent due to lack of content or attachment in {email_data.file_name}"
                )
        self.close_connection()
