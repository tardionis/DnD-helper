# DnD-helper

This is a DnD helper, who should help me and later the players in my campaign to remember things like prices, 
names and other things during the game that can be quickly forgotten in the course of a longer campaign. Towards the end, 
it should even be possible to create and edit your own lists.

## Motivation

I decided to write this program because I couldn't find a DnD helper who could satisfactorily meet my needs. 
I decided to put my software on a server so that I could share it with others on my network or even later on a website.
But a lot has to happen before that happens.

## Build status

The software is currently under development, but you can already use first features.
Numerous features wil be added.

## Screenshots

![Kampfsystem](/images/Kampfsystem.png)
![Tabelle](/images/Tabelle.png)
![Hinzufügen](/images/Hinzufügen.png)

## Requirements

To start the server you need:

* [Python3.6 or higher](https://www.python.org)

* [Flask](https://palletsprojects.com/p/flask/)

## Installation

You can find and install python [here](https://www.python.org).
To install Flask with pip, enter the following command in the command line:

    pip install -U Flask
    
## Getting started 

Go to the this directory in your command-line interpreter and 
enter the following command to start the program:

    py index.py or python3 index.py
    
Now enter in the address bar:

    http://localhost:8080
    
You should now be able to see and use the DnD helper.

## Features

* A combat system with which you can check whether the attack roll hits and deduct the damage rolled from the HP.

* Tables with which spells, attacks, items etc. can be viewed (these cannot yet be added to the PC's).

* The ability to add new spells, attacks, items etc. to the lists.

## Planned features

* Remove items from lists

* Edit the items in the lists

* Select the order of the fighters beforehand in the combat system.

* Individual search for each list.

* Easier addition to any list.

* Add your own lists.

* The individual spells, attacks and item buttons become dropdown buttons.

* The spells, attacks and item buttons are only shown if characters have at least one.
