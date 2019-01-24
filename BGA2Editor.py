import sys, os, mmap

def Main():
  print("Battlefleet Gothic: Armada 2 Saved Game Editor v1.0 by Cryptomancer\n")

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
    ProfileMM.seek(ProfileMM.find("Game_ProperNoun_GenericFleetName".encode())-12)
    FleetPoints = int.from_bytes(ProfileMM.read(4),sys.byteorder)

    ProfileMM.seek(0)

    print("Campaign Properties:\n")
    print("(Faction):",Faction)
    print("(Difficulty):",Difficulty)
    print("(Level):",Level)
    print("Renown:",Renown)
    print("Leadership:",Leadership)
    print("FleetPoints:",FleetPoints)
    print("Income:",Income)
    print("Back: Go Back")
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
    elif (EditProperty == "Back"):
      break
    else:
      print("Invalid Selection - Try Again\n")
      continue

  ProfileMM.flush()
  return

if __name__ == "__main__":
    Main()