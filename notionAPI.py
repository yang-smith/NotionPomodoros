import requests, json
import sys

token = 'secret_eu9NvaTv04r4xiNeAVVKcIxZ2voFEr6tnwDABfVKFx5'
databaseId = '5bb52448afc448c29085e98a7de3b46d'
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def readDatabase(databaseId = databaseId, headers = headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    #print(res.text)
    return data

def cleanData(data):
    baseDict = {}
    for i in data['results']:
        #print(i)
        name = i['properties']['Name']['title'][0]['plain_text']
        if i['properties']['done']['rich_text'] != [] :
            
            baseDict[name] = {"done": i['properties']['done']['rich_text'][0]['text']['content'],
                                                                           "total": i['properties']['total']['number'],
                                                                           "id": i['id']}
        else:
            baseDict[name] = {"done": "",
                                                                           "total": i['properties']['total']['number'],
                                                                           "id": i['id']} 
        
        if baseDict[name]['total'] == None:
            baseDict[name]['total'] = int(0)
        else:
            baseDict[name]['total'] = int(baseDict[name]['total'])           
    
    return baseDict

def addDatabase(databaseId = databaseId, headers = headers, body = None):
    readUrl = f"https://api.notion.com/v1/pages"

    res = requests.request("POST", readUrl, json=body, headers=headers)

    print(res.status_code)
    print(res.text)

def findPageId(name, databaseId = databaseId, headers = headers):
    data = readDatabase(databaseId, headers)
    for i in data['results']:
        if i['properties']['Name']['title'][0]['plain_text'] == name :
            return i['id']
        #print(i['properties']['Name']['title'][0]['plain_text'])
    print('not found id')

def updatePage(name, body, headers = headers):
    pageId = findPageId(name)
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"
    
    res = requests.request("PATCH", updateUrl, json=body, headers=headers)
    print(res.status_code)

def updateTomato(Dict, headers = headers):
    newBody = {
        "properties": {
            "done": {"rich_text": [{"text": {"content": "🍅🍅🍅"}}]},
            "total":{"number": 0},
        },
    }
    newBody['properties']['done']['rich_text'][0]['text']['content'] = Dict['done']
    newBody['properties']['total']['number'] = Dict['total']
    pageId = Dict['id']
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"
    res = requests.request("PATCH", updateUrl, json=newBody, headers=headers)
    print(res.status_code)
