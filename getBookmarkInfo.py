import requests
import yaml
import time
import webbrowser
import datetime
import pprint
import gzip
import json
import csv

def getNewData():
    """
    payload : json params
    e.g.) payload = {'out': 'json', 'ncode':'n5455cx-n3125cg-n2267be-n4029bs', 'of':'t-gl', 'gzip':5}
    reference) https://dev.syosetu.com/man/api/
    """
    payload = {'out': 'json', 'ncode':'n5455cx-n3125cg-n2267be-n4029bs', 'of':'t-gl-n-ga', 'gzip':5}
    url = "https://api.syosetu.com/novelapi/api/"
    r_gzip = requests.get(url, params=payload)
    r = r_gzip.content
    r_gzip.encoding = 'gzip'
    res_content = gzip.decompress(r).decode("utf-8")
    res = json.loads(res_content)[1:]
    
    newData = [['ncode', 'title', 'general_lastup', 'general_all_no']]
    for r in res:
        newData.append([r['ncode'], r['title'], r['general_lastup'], r['general_all_no']])
    
    return newData

def readData():
    f_data = "update.csv"
    with open(f_data) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    #data: list(['ncode', 'title', 'general_lastup', 'general_all_no'])
    return data

def storeData(res):
    # res: list(['title', 'general_lastup', 'general_all_no'])
    output = "update.csv"
    with open(output, mode='w', newline="") as f:
        writer = csv.writer(f)
        for d in res:
            writer.writerow([d[0], d[1], d[2], d[3]])

def post_ifttt(json):
    # json: {value1: " content "}
    url = (
        "https://maker.ifttt.com/trigger/"
        + "isUpdated"
        + "/with/key/"
        + # your ifttt key
    )
    requests.post(url, json)

def check(prevData, newData):
    # prevData: [[previous information of bookmark1], [previous information of bookmark2], ...]
    # newData: [[new information of bookmark1], [new information of bookmark2], ...]
    isUpdated = 0
    for i in range(len(prevData)):
        if(i==0):
            continue
        if(prevData[i][0]==newData[i][0] and prevData[i][2]!=newData[i][2]):
            message = '\"' + newData[i][1] + '\"' +  'が更新されました！\n' + 'https://ncode.syosetu.com/' + newData[i][0] + '/' + newData[i][3] + '/'
            print(message)
            json = {'value1': message}
            post_ifttt(json)
    storeData(newData)

# Example
payload = {'out': 'json', 'ncode':'n5455cx-n3125cg-n2267be-n4029bs', 'of':'t-gl-n-ga', 'gzip':5}
prevData = readData()
newData = getNewData(payload)

check(prevData, newData)
