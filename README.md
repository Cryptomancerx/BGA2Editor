# BGA2Editor

Readme for BGA2Editor v1.1 by Cryptomancer

INTRODUCTION:  
This is a saved game editor for Battlefleet Gothic: Armada 2. Currently it supports editing campaign saved games.

FEATURES SUPPORTED:  
Edit renown, leadership, maximum fleet points, global income, upgrade points, and battleplans. Also you can set all ships to max level and repair all ships hull and crew values (will not repair critical damages).  

INTERFACE:  
The interface is purely CLI. Input is done through a series of text prompts in the form of: Number:Value or Command:Explanation.  

To select a given option enter everything to the left of the colon verbatim. This includes capitalization and punctuation. If you see a property enclosed in parenthesis then it is displayed purely FYI and is not editable. For example:  

(Faction): Imperium -- This is NOT editable  
Renown: 100 -- This is editable  

NOTE THAT INPUTS ARE NOT VALIDATED. THIS EDITOR WILL BLINDLY EDIT YOUR PROFILE WITH WHATEVER VALUES YOU PROVIDE AND INVALID VALUES WILL BREAK YOUR GAMES!!!  
NOTE THAT THIS EDITOR DOES NOT CREATE BACKUPS OF YOUR SAVED GAMES SO TAKE MANUAL BACKUPS  
Saved games location: C:\Users\%USERNAME%\AppData\Local\BattleFleetGothic2\Saved\SaveGames  
If you don't see the AppData folder then enable Show Hidden Folders in Folder Options.  

CHANGELOG:
v1.1 - Added UpgradePoints, BattlePlans, HEALSHIPS!, and MAXSHIPS! commands.

To compile BGA2Editor into a Windows binary you will need pyinstaller which can be installed via pip. Use the following command:  
pyinstaller -F -i BGA2.ico BGA2Editor.py
