import inquirer
from utils.ascii_art import action_header, email_header
from utils.commons import clear, create_dir
from core.publish import Publish


def menu(name: str, desc: str, opt: list) -> dict:
    question = [inquirer.List(name, message=desc, choices=opt)]
    answer = inquirer.prompt(question)
    return answer


def halt():
    clear()
    response = menu("exit", "Do you want to quit?", ["Y", "N"])
    if response["exit"] == "Y":
        clear()
        exit()
    else:
        pass


def perform_action(emails: object, mode: str):
    clear()
    print(action_header)
    print()
    if emails:
        message = f"Choose an Option: (Auto Exports when Mailing)"
        if mode == "Contents":
            response = menu("action", message, ["Export", "Mail Contents", "Exit"])
        elif mode == "Attachments":
            response = menu("action", message, ["Mail Attachments", "Exit"])
        else:
            response = menu(
                "action",
                message,
                ["Export", "Mail Contents", "Mail Attachments", "Mail Both", "Exit"],
            )
        response = response["action"]
        clear()
        if response == "Exit":
            halt()

        p = Publish(emails)
        p.export()
        if "Contents" in response:
            p.mail(emails, "Contents")

        elif "Attachments" in response:
            p.mail(emails, "Attachments")

        elif "Both" in response:
            p.mail(emails, "Both")
    else:
        print("No Content or Email Found.")


def email_menu():
    clear()
    print(email_header)
    print()
    response = menu(
        "mode",
        "Choose an option",
        ["Extract Contents", "Extract Attachments", "Extract Both", "Exit"],
    )
    response = response["mode"]
    clear()
    create_dir("results")
    if "Content" in response:
        return "Contents"

    elif "Attachment" in response:
        return "Attachments"

    elif "Both" in response:
        return "Both"

    elif response == "Exit":
        halt()
