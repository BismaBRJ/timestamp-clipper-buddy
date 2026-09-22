# Timestamp Clipper Buddy

Copyright (c) 2026 Bisma Rohpanca Joyosumarto - BismaBRJ (<https://www.github.com/BismaBRJ/>)

Repository: <https://github.com/BismaBRJ/timestamp-clipper-repl/>

In short: a little REPL (read-eval-print loop) program to extract video/audio at specified timestamps, acting as an ongoing inventory towards doing so, using FFmpeg and written in Python 3.

## Installation and running

This is a [uv](https://docs.astral.sh/uv/) project, so it is best installed and run using uv, though for now it is practically just a collection of scripts; so if you want, you may also directly run the `main.py` file.

Either way, the first step is to get this repository on your computer. If you want, there's a "Download ZIP" button after clicking the green "Code" button on the GitHub repository page; then, to get the folder, you can unzip the file after downloading. If you have [git](https://git-scm.com/) installed, you can clone the repository via the command prompt or Terminal or whatever it's called on your system using the following command:

```
git clone https://github.com/BismaBRJ/timestamp-clipper-buddy.git
```

Once the repo is on your computer, regardless of whether you clicked Download ZIP or ran `git clone`, the next step is to open the terminal on the folder. You may need to use the `cv` command, such as `cv <folder-name>` or `cd ..` (to exit the current folder) to navigate there. You can check whether or not you're there by listing the files in the current folder, using the `dir` command if on Windows or using `ls` otherwise; if you see the same files as on the GitHub repo page, then the terminal is at the right folder.

### By using uv

[Install uv](https://docs.astral.sh/uv/#installation) if you haven't already.

You may want to [install Python](https://www.python.org/downloads/) before installing uv. If you don't already have Python installed, uv would install its own version of Python anyway.

Once you have uv installed and have opened the terminal on the folder, first run

```
uv sync
```

This you only have to do once.

Now you can run the app whenever by running `uv run timestamp-clipper-buddy`, but to do so would always require first opening the terminal on the folder if not already.

Thus, to avoid such hassle, after the `uv sync` command, I highly recommend also running the following two commands, in order:

```
uv tool install .
uv tool update-shell
```

(don't forget that period on the first command!). By doing so, from now on, you can open the terminal whenever on any folder and run `timestamp-clipper-buddy` to start the app there.

If you use git, you may want to run the `uv tool install . -e` command with that `-e` flag for easier updating; see below.

### By manually running `main.py`

You must first [install Python](https://www.python.org/downloads/) if not already, which also comes with `pip`. So far, this project depends on the `pathvalidate` package, which can be installed using `pip` by running

```
pip install pathvalidate
```

or `pip3 install pathvalidate` if that doesn't work.

With that out of the way, open the terminal on the folder if not already, then navigate further to `src/timestamp-clipper-buddy/` by running `cd src/timestamp-clipper-buddy/` or, one-by-one, `cd src` followed by `cd timestamp-clipper-buddy`. Finally, run `python main.py`, or `python3 main.py` if that doesn't work. So long as you have the terminal open in this inner folder within `src`, you can quit and re-run `python main.py` as much as you want.

Using this method, you will indeed have to manually navigate to that folder on the terminal and run `main.py` that way every single time you want to run the app, at least if you close the terminal after use. (Hence you may consider using uv instead.)

## How to update 

The most straightforward answer is to just delete the entire repo on your computer (but make sure you don't put any of your stuff in there! Move them elsewhere if not already!) then re-install using the instructions above.

But if you use git, a single command suffices, regardless of whether you initially installed by the "Download ZIP" button or by `git clone`.

Simply navigate to the repo folder on the terminal, then run

```
git pull
```

and you are all set. It will either pull the latest version of the repo if it is different from the version on your computer, or simply confirm that it is the same, i.e. it is still up-to-date.

## Usage

The app starts with the following greeting:

```
Hello from timestamp-clipper-buddy!
=== Inventory of timestamps ===
Inventory not saved to a file
No media selected
No folder selected for saving clips
No timestamps yet
=== Actions ===
i: set inventory path
m: set media path
c: set folder for saving clips
n: new timestamp
e: edit timestamp
d: delete timestamp
x: delete ALL timestamps
r: run clipping
q: quit
Enter next action:
```

The available controls/actions should be self-explanatory. You can select a media file (that is, a video file or an audio file), input some timestamp ranges, select the output folder, then input `r` to save/export the inputted timestamp ranges each as their own file, clipped from the selected media file (which will not be deleted, don't worry).

The "inventory" system, which you never have to touch if you don't want to, is simply a way to save the inputted data as a .json file if you are not done, say you want to input so many timestamps, or maybe you don't want to have to select the same media file and/or the same output folder every single time. If you do choose to save the inputted data as such an inventory file, it will autosave (but not auto-export) after every change, after every new input or edit.

If you know some Python, feel free to peek into the source code (that is, files inside the `src` folder) to look at the inner workings, edge cases etc. I'm welcome to suggestions; you can start a new GitHub issue or even pull request if you want to.
