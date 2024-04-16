import os
from utils.commons import hold
from core.parsers.eml_parser import parse_eml
from core.parsers.msg_parser import parse_msg
from core.menu import email_menu, perform_action


class EmailProcessor:
    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir

    def load_emails(self):
        emails = []
        try:
            files = os.listdir(self.root_dir)
        except FileNotFoundError:
            print(f"{self.root_dir} Not Found.")
            raise SystemExit
        except OSError:
            print(f"{self.root_dir} is incorrect.")
            raise SystemExit

        if files:
            mode = email_menu()
            for file in files:
                if file.endswith(("eml", "msg")):
                    file_path = os.path.join(self.root_dir, file)
                    file_name = os.path.basename(file_path)
                    if file_name.endswith('eml'):
                        emails.append(parse_eml(file_name, file_path, mode))
                    elif file_name.endswith('msg'):
                        emails.append(parse_msg(file_name, file_path, mode))
            perform_action(emails, mode)
            hold()


if __name__ == "__main__":
    folder_path = input("Enter Folder Path: ")
    ep = EmailProcessor(folder_path)
    ep.load_emails()
