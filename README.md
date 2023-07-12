# Git Commit Author Setter

This Python script is used as a pre-commit hook to set, remember, and forget the commit author of a Git repository. It utilizes a graphical user interface (GUI) for user interaction.

## Usage

1. Copy the script to your Git repository's `.git/hooks` directory and name it `pre-commit`.
2. Make sure the script is executable by running `chmod +x pre-commit`.
3. When you make a commit, the script will prompt you to choose a commit author from a list or enter a new author manually.
4. If you choose an author from the list, the script will set the author's name and email for the current commit.
5. If you enter a new author manually, the script will add the author's name and email to the list of authors for future reference.
6. Optionally, the script can remember the commit author for a specified duration, so you don't have to choose it again in subsequent commits within that timeframe.

## Dependencies

The script relies on the following dependencies:

- Python 3.x
- `easygui` library

Install the `easygui` library by running `pip install easygui`.

## Configuration

The script reads the Git configuration from the `.git/config` file in your repository. It expects the following sections to exist:

- `[user]`: Contains the current commit author details and expiration timestamp.
- `[authors]`: Contains a list of previously used commit authors.

If any of these sections or options are missing, the script will add them automatically.

## Limitations

- The script assumes that the Git repository is initialized and has a valid `.git/config` file.
- The script requires a graphical environment to display the GUI prompts, so it may not work in terminal-only environments.

## License

This script is provided under the [MIT License](LICENSE).
