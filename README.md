# Decky Clipper

A sequel to the beloved [Decky Recorder](https://github.com/SDH-Stewardship/decky-recorder-fork/tree/main). Built from the ground-up with much of the code cherrypicked from the previous projects.

Currently only supports direct screencapture with only one file format, but the plan is to expand the functionality in the future.

# Building
Easiest way to build the project is to open it in VSCode, pressing `Ctrl + Shift + P`, selecting "Tasks: Run Task" and then selecting "build". You will need to have docker running and have the user be of the group `docker`. You can check the `tasks.json` file for what this task corresponds to.

# Deploying

To have the "builddeploy" task work is a bit more involved:

- Enable ssh in you Steam Deck with `systemctl start sshd`
- Generate an SSH key with `ssh-keygen -f ~/.ssh/deck -N ""`
- Copy your key to your Deck for automatic login `ssh-copy-id -i ~/.ssh/deck deck@deck_IP`
- Then set up `settings.json` to contain the correct information (it appears after building the project once)

Now running the Task should automatically set up the plugin after building.

# Installation

Either pick the prebuilt zip in [releases](https://github.com/Managor/Decky-Clipper/releases) or use the one you built yourself. Enable Developer mode in decky settings so that you get access to the Instal Plugin from ZIP File setting.
