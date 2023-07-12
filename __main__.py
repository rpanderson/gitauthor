import sys
import time
import shutil
from pathlib import Path
import configparser
import easygui

# A script for setting commit author in git.
#
# It will remember your user details for remember_minutes
# before prompting again, if you say yes to 'Remember commit author?'.

config_path = Path(".git/config")


def user_prompt():
    new_name, new_email = easygui.multenterbox(
        msg="Enter commit author details",
        title="Git commit author",
        fields=["Full name", "Email address"],
    )
    return new_name, new_email


def remember_prompt(remember_minutes):
    response = easygui.ynbox(
        msg=f"Remember commit author for {remember_minutes} minutes?",
        title="Git commit author",
        choices=("Yes", "No"),
        image=None,
    )
    return response


if config_path.exists():
    # Read .git/config
    config = configparser.ConfigParser()
    config.read(config_path)

    # Check if [user] section exists in .git/config
    if "user" not in config.sections():
        config.add_section("user")

    # Get user details
    user = config["user"]

    # Determine if user has expired and permit commit if not
    if time.time() < user.getfloat("expires", 0.0):
        print("User has not expired.")
        sys.exit(0)

    # Get expired user details
    old_name = user.get("name", "")
    old_email = user.get("email", "")

    # Get new user details
    user["name"], user["email"] = user_prompt()
    # TODO: check if username was entered

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
    print(f"{config_path} not found. Please create and commit again.", file=sys.stderr)
    sys.exit(1)
