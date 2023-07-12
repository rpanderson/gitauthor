import sys
import time
import shutil
from pathlib import Path
import configparser
import easygui

config_path = Path(".git/config")


def user_choice(authors, default_name=None):
    """
    Prompt the user to choose a commit author from a list or enter a new author.

    Args:
        authors (dict): Dictionary containing the authors' names and email addresses.
        default_name (str, optional): Default author name. Defaults to None.

    Returns:
        tuple: Tuple containing the chosen author's name and email address, or (None, None) if a new author is entered.
    """
    names = list(authors.keys())
    names.append("Other")
    if default_name in names:
        ix = names.index(default_name)
    else:
        ix = 0
    response = easygui.choicebox(
        msg="Choose from the list or press 'Cancel' to enter a new author",
        title="Choose a commit author",
        choices=names,
        preselect=ix,
    )
    if response is None or response == "Other":
        return None, None
    else:
        return response, authors[response]


def user_prompt():
    """
    Prompt the user to enter commit author details manually.

    Returns:
        tuple: Tuple containing the entered author's name and email address, or (None, None) if the prompt is canceled.
    """
    response = easygui.multenterbox(
        msg="Enter commit author details",
        title="Git commit author",
        fields=["Full name", "Email address"],
    )
    if response is None:
        return None, None
    else:
        return response


def remember_prompt(remember_minutes):
    """
    Prompt the user to choose whether to remember the commit author for a certain duration.

    Args:
        remember_minutes (float): Number of minutes to remember the commit author.

    Returns:
        bool: True if the user chooses to remember, False otherwise.
    """
    response = easygui.ynbox(
        msg=f"Remember commit author for {remember_minutes} minutes?",
        title="Git commit author",
        choices=("Yes", "No"),
        image=None,
    )
    return response


def main():
    if config_path.exists():
        # Read .git/config
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(config_path)

        # Check if [user] section exists in .git/config
        if "user" not in config.sections():
            config.add_section("user")

        # Check if [authors] section exists in .git/config
        if "authors" not in config.sections():
            config.add_section("authors")

        # Get user details
        user = config["user"]

        # Get author list
        authors = config["authors"]

        # Determine if user has expired and permit commit if not
        if time.time() < user.getfloat("expires", 0.0):
            print("User has not expired.")
            sys.exit(0)

        # Get expired user details
        old_name = user.get("name", None)
        old_email = user.get("email", None)

        # Present a list of authors to choose from
        if len(authors):
            name, email = user_choice(authors, old_name)
        else:
            name = None

        # Get new user details if dialog was cancelled
        if name is None:
            name, email = user_prompt()
            # Exit if cancel is pressed or null entry
            if name is None or name is "":
                print(
                    f"Please choose or enter a new user and commit again.",
                    file=sys.stderr,
                )
                sys.exit(1)
            # Add the name and email to the author list if new
            elif name not in authors:
                authors[name] = email

        # Finally, set the user name and email in config
        user["name"], user["email"] = name, email

        # Check if remember duration exists
        remember_minutes = user.getfloat("rememberminutes", 1.0)
        user["rememberminutes"] = f"{remember_minutes:.1f}"

        # Prompt to remember user for remember_minutes
        if remember_prompt(user["rememberminutes"]):
            expires = time.time() + 60 * remember_minutes
            user["expires"] = f"{expires:.1f}"

        # Backup config file before updating it
        backup_path = config_path.parent / (config_path.name + ".bak")
        shutil.copy(config_path, backup_path)
        with open(config_path, "w") as config_file:
            config.write(config_file)

        # If the user has changed, fail process and require recommit
        if old_name != user["name"] or old_email != user["email"]:
            print("Git username changed. Please commit again.", file=sys.stderr)
            sys.exit(1)

        # Otherwise permit commit to proceed
        else:
            print("Git username has not changed.")
            sys.exit(0)

    else:
        print(
            f"{config_path} not found. Please create and commit again.", file=sys.stderr
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
