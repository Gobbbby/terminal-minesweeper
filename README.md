# terminal-minesweeper
I re-created a version of Minesweeper, primarily with Python 3's Curses package, which runs fully in the terminal. Numpy was also used a bit for the creation of the board and it's features.
This runs natively on Unix-based systems (like Linux and MacOS), but not Windows. This can be mitigated fixed by downloading the windows-curses package with PIP on any Windows machine. Whether it actually, fully works or not on any certain platform is a different story.
The 2 featuers in particular that may be especially tricky to get right are the colours and the controls. I use a checkerboard pattern and coloured background on the board during playing, and seeing these colours is essential to the game. The control interface (which is revolved around the mouse cursor) is also essential.
During it's creation, I used VScode's internal terminal (on MacOS), and iTerm 2, after goofing around in it's settings (also on MacOS). They're both (especially iTerm) full, feature-rich terminals, so this wasn't a surprise. When moving to the Mac's pre-installed, default Terminal.app, however, I had a different outcome. The colours showed up, but I wasn't able to click around, making it literally unplayable. I was also told on StackOverflow that the built-in Linux console isn't able to see it's colours (and possibly not be able to use the mouse cursor). The good part is, on any platform, there's something like iTerm 2, which is free and able to run this. Guake on Linux and Terminus on Windows would be good starting-points, since they're both premium and heavily-documented, though they haven't been directly tested by me.
