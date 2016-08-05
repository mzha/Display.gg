<h1 align="center">
	<font color="lightblue">
  	Display.gg
  </font>
</h1>

### What is Display.gg?
A loading screen display for League of Legends. <font color="red">(CURRENTLY MAC ONLY)</font>
<img src='http://oi68.tinypic.com/b4yfq9.jpg' alt='Demo'></img>
### More Details
<font color="lightblue">Display.gg</font> is a python script that you keep running on your computer. It detects when you are loading into a game and pulls up the game's details.
### Information Displayed
- Game type
- Summoner name
- Champion
- Summoner spells
- Keystone mastery
- Rank
- Runes
- Average ranked KDA
- Win Rate
- Ranked games on champion
- Player skill
- Tilt factor (Tilt)

### Player skill? Tilt factor?
Player skill is split into three categories: ***ONE TRICK***, ***NOOB***, and ***NORMAL***. If there is nothing on top of the summoner
name, their skill level is ***NORMAL***. ***ONE TRICK*** means they have played at least **50%** of their ranked games with that
champion, while ***NOOB*** means they have played less than **2.5%** of their ranked games with that champion.

Tilt factor measures the player's tilt on a scale from **0.0** (untilted) to **10.0** (extremeley tilted).
It is a custom calculation made by analyzing their win-loss record from the past **10** matched games, with more weight
being given to more recent games.
### Installation instructions
Download and unzip the ZIP file or clone the project into a directory of your choice. Rename to "DisplayGG" or
whatever name you want.

Make sure you have Python 2.7 installed on your computer. The easiest way to check is to go to Terminal and entering
"python" (without quotes). If it says "command does not exist" or displays a version lower than 2.7, install the latest 2.x from
[here](https://www.python.org/downloads/).

Make sure you have pip by entering the command "pip" (without quotes) into Terminal. If it
gives you a long list of commands, you have it. If not, follow the instructions [here](https://pip.pypa.io/en/stable/installing/).

Navigate to the DisplayGG folder in Terminal (For example, if it is in Downloads/DisplayGG, enter "cd ~/Downloads/DisplayGG"). Now enter the following commands (if it prompts you for
  your password, enter it because it needs admin permissions to install):

`sudo pip install psutil`

`sudo pip install --upgrade --trusted-host wxpython.org --pre -f http://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix`

`sudo pip install appscript`

Go to [league's developer website](https://developer.riotgames.com/) and sign in with your league account.

Follow the on-screen instructions
until you reach a screen that displays your "Development API Key". It will be a line of numbers, letters, and dashes.

Copy that line and put it into the config.json file, where it says "PUT API KEY 1 HERE". Make sure there are quotes
around it.

It is recommended that you use a smurf or create a new league account and repeat this process for a second
API key and put it where it says "PUT API KEY 2 HERE". It will halve the amount of time it takes to load the information.

Now change the other values in the config.json file. Where it says "Omega Rex", enter your summoner name with quotes around it. You can play around with the scale_factor until you find one that suits your tastes. Going under 6 is not
recommended because it will cause visual clashes.

<font color="blue">Congratulations! Display.gg is installed!</font>
### Running Instructions
In Terminal, from the DisplayGG folder, run this command, replacing x with 0 if you're on Windows, or 1 if you're on Mac:

`python script.py x`

You can put a summoner name in quotes afterwards if you want the program to load data for a different summoner, like so:

`python script.py x 'SUMMONERNAME'`

Now the program is running and will automatically open when you load into game. You can exit the program from the Terminal window by pressing Ctrl-C.
