# Torn Console

This application is purposed to provide a console-like view of Torn to avoid
having the web browser open.

The only feature it currently provide is access to the Torn API using the user's
API KEY, allowing to see the following:

* Player status
* Travel status
* Current Chain status
* Bazaar information
* Initiated attacks information
* Notifications window

Timers on different windows should countdown to provide real-time information back 
to the user, and a status bar on the bottom of the screen displays when the next
API call will be performed (default to 5 seconds)

Other features can be added as requested.

# Dependencies

This application supports Python 3+, and it also requires a special module 
called **curses**. Download this module for the right platform from the following
website:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses

__For Linux, in theory, curses is a default module so no extra steps should be required.
However, this was not tested on my end.__

The application also needs **requests**, which can be installed by either of the
following commands:

```
pip install requests
```

From the tornconsole root folder:
```
pip install -r requirements.txt
```

After these two basic requirements, you are set to go!

# First time use

After all dependencies have been installed, just execute the main.py file and
a window should appear

```
python main.py
```

The application uses a file to store the user's Torn API key and to hold the
refresh interval for the API calls. If the file does not exist, a copy is
created using the included settings.ini.example file so that the user can
then go ahead and modify the file using the text editor of their choice.

The only contents of the settings.ini file right now are:

```
#BASE INFORMATION
API_KEY = <Your API KEY here>
REFRESH_INTERVAL = 5
```

On the above, lines starting with the # character are considered comments.
The user should replace the <Your API KEY here> for their own Torn API key.
  
The application does NOT send any information over the internet, there is
no way that the original application will EVER send the key over to anyone.

# How this works

The console is setup to perform the least amounts of API calls at possible to avoid
going over the 60 calls per minute limit imposed by Torn. For this, the application
currently performs:

* At launch, 2 API calls are performed: 1 for the "User" endpoint required to fetch all
information for the multiple windows, and 1 for the "Torn" endpoint required to fetch
Torn information (e.g. Item names)

* At each refresh interval, only the "User" enpoint is queried again to update the
information on the screen.

** Currently, the "Torn" endpoint response is not being used but is there since it will
be needed for future functionality.

# Application "Windows"

## Status Window

The status window displays basic information of the player and the values
of the different bars (Life, Nerve, Happiness) as well as the amount
of time remaining to have a full bar.

## Travel Window

The travel window displays current flight information:
* Destination
* Flight departure time
* Flight arrival time
* Time Left timer

If no travel is currently happening. A notification will appear indicating so.

## Chain Window

The chain window has two modes:

### Cooldown

In cooldown mode, information related to the cooldown of the chain is displayed:
* Maximum hits achieved
* Current hits
* Cooldown timer 

### Active

While in active mode, information related to the current chain is displayed:
* Current amount of hits
* Chain timeout timer
* Current modifier

## Bazaar Window

The Bazaar window displays current items in the player's bazaar
along with their quantity, set price and their RRP value.

If the Bazaar is not active (either not available or closed), a notification
is displayed indicating so.

The intent of this window is to work closely with the Market window so that the
player can validate the prices of their bazaar against the current market value.

## Market Window

Not implemented yed, this window will probably display the price of a list of
particular items and their value.

## Initiated Attacks Window

The Attacks window displays a list of attacks initiated by the player against 
unique targets and their results, including the amount of respect earned from
said attack.

As new attacks happen on a particular target, the list will update and keep only
the most recent attack.

**Note: This could be changed to use the fullattack list from Torn API, providing
a longer attacks list at the cost of not being able to see the player name, displaying
only the ID.

## Notifications window

The Notifications window allows the player to have a quick glance of unseen events
or messages. A maximum of 10 notifications are displayed.

## Status Bar

The Status bar at the bottom of the window displays the amount of time left until
the next Torn API call.
