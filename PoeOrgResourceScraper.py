import requests
import json
import re

urlBase = "http://pathofexile.gamepedia.com/"

skillGemsList = []
uniqueAccessoriesList = []
uniqueArmoursList = []
uniqueWeaponsList = []
uniqueFlasksList = []
uniqueJewelsList = []

essencesList = []

############################### JSON URL LIST ##############################################
urlSkillGems = 'https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20skill%20gems'
urlUniqueAccessories = "https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20unique%20accessories"
urlUniqueArmours = "https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20unique%20armour"
urlUniqueWeapons = "https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20unique%20weapons"
urlUniqueFlasks = "https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20unique%20flasks"
urlUniqueJewels = "https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20unique%20jewels"

urlEssences = ""

# Returns a list with relevant data values(names) from json 
def getNamesFromJson(urlRequestResult):
    tempList = []
    jsonObj = json.loads(urlRequestResult.text)
    # print (skills_obj['query'])
    for i in jsonObj['query']['sobj']:
        for j in i['data']:
            if j['property'] == '_ASKST':
                for name in j['dataitem']:
                    # print(r['item'])
                    tempList.append(name['item'])
    return tempList

# Cleans the entries not wanted in the end result
def listCleaner(listToBeCleaned):
    regex = "^\[\[\:"
    for i, name in enumerate(listToBeCleaned):
        # print(re.search(regex, name))
        if re.match(regex, name) is None:
            listToBeCleaned.remove(name)
    return listToBeCleaned

# Writes list to a file
def writeResultToFile(listToWrite, fileName):
    f = open(fileName, 'w')
    for stringToWrite in listToWrite:
        f.write(stringToWrite+'\n')  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

# Generates the final list and removies unwanted characters.
def makeNameList(listToBeChanged, poeRequest):
    listToBeChanged = getNamesFromJson(poeRequest)
    listToBeChanged = listCleaner(listToBeChanged)
    for i, name in enumerate(listToBeChanged):
        replaced = re.sub('[\][:]', '', name)
        listToBeChanged[i] = replaced
    return listToBeChanged
    

############################## Get json ##############################################
skillGemsRequest = requests.get(urlSkillGems)
uniqueAccessoriesRequest = requests.get(urlUniqueAccessories)
uniqueArmoursRequest = requests.get(urlUniqueArmours)
uniqueWeaponsRequest = requests.get(urlUniqueWeapons)
uniqueFlasksRequest = requests.get(urlUniqueFlasks)
uniqueJewelsRequest = requests.get(urlUniqueJewels)


################## Clean and generate lists of gems, items and jewels  ###############
skillGemsList = makeNameList(skillGemsList, skillGemsRequest)
uniqueAccessoriesList = makeNameList(uniqueAccessoriesList, uniqueAccessoriesRequest)
uniqueArmoursList = makeNameList(uniqueArmoursList, uniqueArmoursRequest)
uniqueWeaponsList = makeNameList(uniqueWeaponsList, uniqueWeaponsRequest)
uniqueFlasksList = makeNameList(uniqueFlasksList, uniqueFlasksRequest)
uniqueJewelsList = makeNameList(uniqueJewelsList, uniqueJewelsRequest)

########################## Merge all lists into one and write to file ################
mergedListOfNames = skillGemsList + uniqueAccessoriesList + uniqueArmoursList + uniqueWeaponsList + uniqueFlasksList + uniqueJewelsList

writeResultToFile(mergedListOfNames, 'listOfLinkNames')





####################### Old Approach ##############################
# def doListStuff(listPrep, poeRequest):
#     listPrep = getNamesFromJson(poeRequest)
#     listPrep = listCleaner(listPrep)
#     listPrep = makeOrgLinks(listPrep)
#     return listPrep

# def makeOrgLinks (listToBeChanged):
#     # +LINK: Spell_Echo_Support http://pathofexile.gamepedia.com/Spell_Echo_Support
#     for i, name in enumerate(listToBeChanged):
#         replaced = re.sub('[\][:]', '', name)
#         replaced = re.sub('[\s]', '_', replaced)
#         skillName = replaced
#         replaced = re.sub('\'', '%27', replaced)
#         replaced = re.sub('^', urlBase, replaced)
#         replaced = re.sub('^', '#+LINK: '+skillName+' ', replaced)
#         listToBeChanged[i] = replaced
#     return listToBeChanged

#skillGemsList = doListStuff(skillGemsList, skillGemsRequest)
#print(skillGemsList)

#uniqueAccessoriesList = doListStuff(uniqueAccessoriesList, uniqueAccessoriesRequest)
#print(uniqueAccessoriesList)

#uniqueArmoursList = doListStuff(uniqueArmoursList, uniqueArmoursRequest)
#print(uniqueArmoursList)


#mergedList = skillGemsList + uniqueAccessoriesList + uniqueArmoursList
#writeResultToFile(mergedList, 'poeOrgResources')
