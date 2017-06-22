import requests
import json
import re

urlBase = "http://pathofexile.gamepedia.com/"
skillList = []

url='https://pathofexile.gamepedia.com/api.php?format=json&action=browsebysubject&subject=List%20of%20skill%20gems'
r = requests.get(url)


skills_obj = json.loads(r.text)
#print (skills_obj['query'])
for i in skills_obj['query']['sobj']:
    for j in i['data']:
        if j['property'] == '_ASKST':
            for r in j['dataitem']:
                # print(r['item'])
                skillList.append(r['item'])


def makeOrgLink (stringToBeReplaced):
    # +LINK: Spell_Echo_Support http://pathofexile.gamepedia.com/Spell_Echo_Support
    replaced = re.sub('[\][:]', '', stringToBeReplaced)
    replaced = re.sub('[\s]', '_', replaced)
    skillName = replaced
    replaced = re.sub('\'', '%27', replaced)
    replaced = re.sub('^', urlBase, replaced)
    replaced = re.sub('^', '#+LINK: '+skillName+' ', replaced)
    return replaced



for i,skill in enumerate(skillList):
    skillList[i] = makeOrgLink(skill)


def writeResultToFile(listToWrite):
    f = open('poeOrgResources', 'w')
    for stringToWrite in listToWrite:
        f.write(stringToWrite+'\n')  # python will convert \n to os.linesep

    f.close()  # you can omit in most cases as the destructor will call it


del skillList[0]; # Removing the first entry as it is not a skill
writeResultToFile(skillList)