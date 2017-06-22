import requests
import json
import re

urlBase = "http://pathofexile.gamepedia.com/"
skillGemsList = []
uniqueAccessoriesList = []

urlSkillGems = 'https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20skill%20gems'
urlUniqueAccessories = "https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20unique%20accessories"

skillGemsRequest = requests.get(urlSkillGems)
uniqueAccessoriesRequest = requests.get(urlUniqueAccessories)



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

def listCleaner(listToBeCleaned):
    regex = "^\[\[\:"
    for i, name in enumerate(listToBeCleaned):
        # print(re.search(regex, name))
        if re.match(regex, name) is None:
            listToBeCleaned.remove(name)
    return listToBeCleaned

def makeOrgLinks (listToBeChanged):
    # +LINK: Spell_Echo_Support http://pathofexile.gamepedia.com/Spell_Echo_Support
    for i, name in enumerate(listToBeChanged):
        replaced = re.sub('[\][:]', '', name)
        replaced = re.sub('[\s]', '_', replaced)
        skillName = replaced
        replaced = re.sub('\'', '%27', replaced)
        replaced = re.sub('^', urlBase, replaced)
        replaced = re.sub('^', '#+LINK: '+skillName+' ', replaced)
        listToBeChanged[i] = replaced
    return listToBeChanged

def writeResultToFile(listToWrite):
    f = open('poeOrgResources', 'w')
    for stringToWrite in listToWrite:
        f.write(stringToWrite+'\n')  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it

# Prepare active and support skill gems
skillGemsList = getNamesFromJson(skillGemsRequest)
skillGemsList = listCleaner(skillGemsList)
skillGemsList = makeOrgLinks(skillGemsList)
print(skillGemsList)

# Prepare Unique accessores
uniqueAccessoriesList = getNamesFromJson(uniqueAccessoriesRequest)
uniqueAccessoriesList = listCleaner(uniqueAccessoriesList)
uniqueAccessoriesList = makeOrgLinks(uniqueAccessoriesList)
print(uniqueAccessoriesList)

mergedList = skillGemsList + uniqueAccessoriesList
writeResultToFile(mergedList)
