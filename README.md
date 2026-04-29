![Banner](https://github.com/Managor/Decky-Clipper/blob/main/assets/screenshot.jpg?raw=true)
# Decky Clipper

A sequel to the beloved [Decky Recorder](https://github.com/SDH-Stewardship/decky-recorder-fork/tree/main). Built from the ground-up with much of the code cherrypicked from the previous projects.

Decky Clipper uses the PipeWire node provided by Gamescope for recording. This will allow you to record the Steam UI whenever a game is NOT running. Unfortunately this is a limitation of set by Gamescope. Game recording otherwise works exactly like Steam native game recording.

After a clip has been created, it can then be viewed in gamemode from the Decky Clipper side menu. Currently gamescope has a limitation that if the underlying application doesn't send any frames, gamescope will do the same. This leads to a 0-byte file that will get automatically deleted.

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
