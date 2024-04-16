import os, re
from bs4 import BeautifulSoup


def clear():
    os.system("cls")


def hold():
    input("Press Enter to exit...")


def create_dir(name: str):
    if not os.path.exists(name):
        os.mkdir(name)


def isfile(fpath: str):
    if os.path.isfile(fpath):
        return True
    else:
        False


# Sanitize the given text by removing non-printable characters
def sanitize_text(text):
    if text is not None:
        cleaned_text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]", "", text
        )  # Remove non-printable characters
        cleaned_text = re.sub(r"\n(?:\s*\n){1,}", "\n", cleaned_text)
        cleaned_text = re.sub(r"\A[\n\s]+", "", cleaned_text)
    else:
        cleaned_text = text
    return cleaned_text


def remove_html_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return text
