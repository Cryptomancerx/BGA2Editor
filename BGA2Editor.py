import sys, os, mmap
#2:1000, 3:2500, 4:4500, 5:7000, 6:10000, 7:13500, 8:17500, 9:22000, 10:27000, 11:32500, 12:38500, 13:45500, 14:54500
def Main():
  print("Battlefleet Gothic: Armada 2 Saved Game Editor v1.1 by Cryptomancer\n")

  while True:
    print("1: Edit Campaign Save")
    #print("2: Edit Solo Skirmish Profile")
    print("2: Exit")
    EditMode = input("\nSelect Mode: "); print("")

    if (EditMode == "1"):
      BGAEdit(os.path.join(os.path.expandvars("%LOCALAPPDATA%"),"BattleFleetGothic2\Saved\SaveGames\Campaign"),1)
    #elif (EditMode == "2"):
      #BGAEdit(os.path.join(os.path.expandvars("%LOCALAPPDATA%"),"BattleFleetGothic2\Saved\SaveGames\Profile"),0)
    elif (EditMode == "2"):
      sys.exit()
    else:
      print("Invalid Selection - Try Again\n")
      continue
  return

def BGAEdit(BGAProfilePath,isCampaign):
  FileList = os.listdir(BGAProfilePath)
  ProfileList = []

  for File in FileList:
    ProfileList.append(File)

  while True: #Saved game selection input loop
    ProfileCounter = 1
    for Profile in ProfileList: #Display list of games
      print(ProfileCounter,": ",ProfileList[ProfileCounter-1].replace('.sav',''),sep='')
      ProfileCounter += 1

    EditProfile = int(input("\nSelect Profile: ")); print("")
    if (EditProfile < 1 or EditProfile >= ProfileCounter):
      print("Invalid Selection - Try Again\n")
      continue
    else:
      break

  with open(os.path.join(BGAProfilePath,ProfileList[EditProfile-1]),"rb+") as Profile:
    ProfileMM = mmap.mmap(Profile.fileno(), 0)

  while True: #Campaign property edit input loop
    ProfileMM.seek(0)
    ProfileMM.seek(ProfileMM.find(b'\x45\x6E\x75\x6D\x46\x61\x63\x74\x69\x6F\x6E\x00')+13) #EnumFaction
    StrLength = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    ProfileMM.seek(13,os.SEEK_CUR)
    Faction = ProfileMM.read(StrLength-14).decode("utf-8").title()

    Difficulty = ProfileMM.find(b'\x45\x6E\x75\x6D\x44\x69\x66\x66\x69\x63\x75\x6C\x74\x79') #EnumDifficulty
    if (Difficulty == -1): #If difficulty is EASY there is no EnumDifficulty field so this will fail
      Difficulty = "Easy"
    else:
      ProfileMM.seek(Difficulty+16)
      StrLength = int.from_bytes(ProfileMM.read(4),sys.byteorder)
      ProfileMM.seek(16, os.SEEK_CUR)
      Difficulty = ProfileMM.read(StrLength-17).decode("utf-8").title()

    OffsetStr = "CampaignCommander_" + Faction + "_C"
    ProfileMM.seek(ProfileMM.find(OffsetStr.encode())+len(OffsetStr)+6)
    CampaignOffset = ProfileMM.tell()
    Level = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    Renown = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    ProfileMM.seek(5,os.SEEK_CUR)
    Leadership = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    Income = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    UpgradePoints = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    ProfileMM.seek(ProfileMM.find("Game_ProperNoun_GenericFleetName".encode())-12)
    FleetPoints = int.from_bytes(ProfileMM.read(4),sys.byteorder)
    ProfileMM.seek(ProfileMM.find(b'\xD2\x02\x96\x49')+4) #No clue what this is, but it seems to provide the correct location
    BattlePlans = int.from_bytes(ProfileMM.read(4),sys.byteorder)

    ProfileMM.seek(0)

    print("Campaign Properties:\n")
    print("(Faction):",Faction)
    print("(Difficulty):",Difficulty)
    print("(Level):",Level)
    print("Renown:",Renown)
    print("Leadership:",Leadership)
    print("FleetPoints:",FleetPoints)
    print("Income:",Income)
    print("UpgradePoints:",UpgradePoints)
    print("BattlePlans:",BattlePlans)
    print("HEALSHIPS!: Restores hull and crew values to max for all ships")
    print("MAXSHIPS!: Raises level of all ships to 4")
    print("\nBack: Go Back")
    EditProperty = input("\nSelect Property: "); print("")

    if (EditProperty == "Renown"):
      RenownNew = int(input("Enter new renown: ")); print("")
      ProfileMM.seek(CampaignOffset+4)
      ProfileMM.write(RenownNew.to_bytes(4,sys.byteorder))
    elif (EditProperty == "Leadership"):
      LeadershipNew = int(input("Enter new leadership: ")); print("")
      ProfileMM.seek(CampaignOffset+13)
      ProfileMM.write(LeadershipNew.to_bytes(4,sys.byteorder))
    elif (EditProperty == "FleetPoints"):
      FleetPointsNew = int(input("Enter new fleet points: ")); print("")
      ProfileMM.seek(ProfileMM.find("Game_ProperNoun_GenericFleetName".encode())-12)
      ProfileMM.write(FleetPointsNew.to_bytes(4,sys.byteorder))
    elif (EditProperty == "Income"):
      IncomeNew = int(input("Enter new income: ")); print("")
      ProfileMM.seek(CampaignOffset+17)
      ProfileMM.write(IncomeNew.to_bytes(4,sys.byteorder))
    elif (EditProperty == "UpgradePoints"):
      UpgradePointsNew = int(input("Enter new upgrade points: ")); print("")
      ProfileMM.seek(CampaignOffset+21)
      ProfileMM.write(UpgradePointsNew.to_bytes(4,sys.byteorder))
    elif (EditProperty == "BattlePlans"):
      BattlePlansNew = int(input("Enter new BattlePlans: ")); print("")
      ProfileMM.seek(ProfileMM.find(b'\xD2\x02\x96\x49')+4)
      ProfileMM.write(BattlePlansNew.to_bytes(4,sys.byteorder))
    elif (EditProperty == "HEALSHIPS!"):
      EditShips(ProfileMM, Faction,0)
    elif (EditProperty == "MAXSHIPS!"):
      EditShips(ProfileMM, Faction,1)
    elif (EditProperty == "Back"):
      break
    else:
      print("Invalid Selection - Try Again\n")
      continue

  ProfileMM.flush()
  return

def EditShips(ProfileMM,Faction,Mode):
  if (Faction == "Imperium"):
    FindStrings = ["Imp_Escort", "Imp_Lightcruiser", "Imp_Cruiser", "Imp_Battlecruiser", "Imp_Grandcruiser", "Imp_Battleship", "SpaceMarines_Escort", "SpaceMarines_Lightcruiser", "SpaceMarines_Cruiser", "SpaceMarines_Battleship", "AdeptusMechanicus_Escort", "AdeptusMechanicus_Lightcruiser", "AdeptusMechanicus_Cruiser", "AdeptusMechanicus_Battleship"]
    MaxHullValues = {"Cobra":200, "CobraWidowmaker":200, "Firestorm":400, "Sword":400, "Falchion":400}
  elif (Faction == "Necron"):
    FindStrings = ["Necron_Escort", "Necron_Lightcruiser", "Necron_Cruiser", "Necron_Battlecruiser", "Necron_Battleship"]
    MaxHullValues = {"DirgeRaider":200, "Jackal":400, "Cartouche":800, "Shroud":800, "Khopesh":1200, "ScytheHarvester":1600, "ScytheReaper":2000, "Cairn":2400}
  elif (Faction == "Tyranids"):
    FindStrings = ["Tyranids_Escort", "Tyranids_Lightcruiser", "Tyranids_Cruiser", "Tyranids_Battlecruiser", "Tyranids_Battleship"]

  for str in FindStrings:
    ProfileMM.seek(0)
    while True:
      FindPos = ProfileMM.find(str.encode())
      if (FindPos > 0):
        ProfileMM.seek(FindPos-5)
        ShipLevel = int.from_bytes(ProfileMM.read(1),sys.byteorder)
        ShipTypeLen = int.from_bytes(ProfileMM.read(4),sys.byteorder)-len(str)-2
        ProfileMM.seek(len(str)+1,os.SEEK_CUR)
        ShipType = ProfileMM.read(ShipTypeLen).decode("utf-8")
        ProfileMM.seek(17,os.SEEK_CUR)
        if (ShipLevel > 0 and ProfileMM.read(7).decode("utf-8") != "[ERROR]"): #Limit to valid ships
          if (Mode == 0): #HEAL!
            if (Faction == "Imperium"):
              if ("Escort" in str): MaxHull = MaxHullValues[ShipType]
              elif ("Lightcruiser" in str): MaxHull = 1200
              elif ("Cruiser" in str or "Battlecruiser" in str): MaxHull = 1600
              elif ("Grandcruiser" in str): MaxHull = 2000
              elif("Battleship" in str): MaxHull = 2400
            elif (Faction == "Necron"):
              MaxHull = MaxHullValues[ShipType]
            elif (Faction == "Tyranids"):
              if ("Drone" in ShipType or "Vanguard" in ShipType): MaxHull = 200
              elif ("Kraken" in ShipType): MaxHull = 400
              elif ("Cruiser" in str): MaxHull = 1200
              elif ("Battlecruiser" in str): MaxHull = 1600
              elif("Battleship" in str): MaxHull = 2000
            ProfileMM.seek(FindPos+len(str)+ShipTypeLen+10)
            ProfileMM.write(MaxHull.to_bytes(4,sys.byteorder))
            ProfileMM.seek(int.from_bytes(ProfileMM.read(4),sys.byteorder)+4,os.SEEK_CUR)
            MaxCrew = int.from_bytes(ProfileMM.read(4),sys.byteorder)
            ProfileMM.seek(-8,os.SEEK_CUR)
            ProfileMM.write(MaxCrew.to_bytes(4,sys.byteorder))
            ProfileMM.seek(4,os.SEEK_CUR)
            ProfileMM.write(int("2").to_bytes(4,sys.byteorder))
          else: #MAX!
            ProfileMM.seek(FindPos-5)
            ProfileMM.write(int("4").to_bytes(1,sys.byteorder))
        ProfileMM.seek(FindPos+6)
      else:
        break
  return

if __name__ == "__main__":
    Main()