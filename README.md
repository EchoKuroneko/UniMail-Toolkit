# UniMailToolkit

UniMailToolkit offers a range of specialized tools for precise email file (.eml and .msg) management. This toolkit extracts contents and attachments, convert them to JSON or XLSX formats, and tailor email forwarding based on specific needs. Whether it's for data migration, archival purposes, or streamlined communication. Optimize email processing.

## Features

- **Email Extraction**: Extract content and attachments from .eml and .msg files.
- **Data Conversion**: Convert emails contents to JSON or XLSX format for easy analysis and reporting.
- **Custom Email Dispatch**: Send extracted emails with contents or attachments.
- **Batch Processing**: Handle multiple emails at once, saving time and improving productivity.

## Requirements

Install the required dependencies using the following command:
```
pip install -r requirements.txt
```

## Installation

1. Modify Config File
```
    SMTP_HOST (Mail Service)
    SMTP_USERNAME (Your mail address)
    SMTP_PASSWORD (Your mail Password)
    SMTP_RECEIVER (Receiver mail)
```
2. Run the Script `python main.py`
3. Provide dir path containing `eml` or `msg`
4. Check extraction in `results` dir.