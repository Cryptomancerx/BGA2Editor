# BGA2Editor

Readme for BGA2Editor2 v1.0 by Cryptomancer

INTRODUCTION

This is a saved game editor for Battlefleet Gothic: Armada 2. Currently it supports editing campaign saved games. It will be updated to support new factions and features as they're released.

BGA2Editor is a purely Command Line Interface (CLI) application written in Python 3.7.1. You do not need a Python interpreter to run this editor as it is distributed in Windows binary form along with this file and the original source code.

FEATURES SUPPORTED

Edit admiral level, renown, leadership, maximum fleet points, and global income.

INTERFACE

The interface is purely CLI. I don't know how to code a GUI and I have no interest in learning. I will not release a GUI for this editor so don't ask.

Input is done through a series of text prompts in the form of:

number:Explanation
or
property:value

To select a given option enter everything to the left of the colon verbatim. This includes capitalization. If you see a property enclosed in parenthesis then it is displayed purely FYI and is not editable. For example:

(Faction): Imperium -- This is NOT editable
Renown: 100 -- This is editable

NOTE THAT INPUTS ARE NOT VALIDATED. THIS EDITOR WILL BLINDLY EDIT YOUR PROFILE WITH WHATEVER VALUES YOU PROVIDE AND INVALID VALUES WILL BREAK YOUR GAMES!!!

NOTE THAT THIS EDITOR DOES NOT CREATE BACKUPS OF YOUR SAVED GAMES SO TAKE MANUAL BACKUPS
Saved games location: C:\Users\%USERNAME%\AppData\Local\BattleFleetGothic2\Saved\SaveGames

If you don't see the AppData folder then enable Show Hidden Folders in Folder Options.

DETAILED EXPLANATION AND VALID INPUT VALUES

Here I will cover non-self explanatory input prompts and provide proper values where appropriate.

Campaign Properties:
Renown -- This will set your Renown to the chosen value, but you'll need to fight 1 battle to have the game level you up. It will use the modified Renown value to determine your new level.
Leadership -- Although this value is determined by your level, you can modify it individually if you so desire.
FleetPoints -- Although this value is determined by your level, you can modify it individually if you so desire.
Income -- I suggest setting this to 10000 or so as that should be plenty.
