import requests
import yaml
import gzip
import json
import csv

def get_new_data():
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
    
    new_data = [['ncode', 'title', 'general_lastup', 'general_all_no']]

    for r in res:
        new_data.append([r['ncode'], r['title'], r['general_lastup'], str(r['general_all_no'])])

    return new_data

def read_data():
    f_data = "update.csv"
    with open(f_data, encoding="utf-8") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    #data: list(['ncode', 'title', 'general_lastup', 'general_all_no'])
    return data

def store_data(res):
    # res: list(['ncode', 'title', 'general_lastup', 'general_all_no'])
    output = "update.csv"
    with open(output, mode='w', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for d in res:
            writer.writerow([d[0], d[1], d[2], d[3]])

def post_ifttt(json):
    # json: {value1: " content "}
    url = (
        "https://maker.ifttt.com/trigger/"
        + # Applet Name
        + "/with/key/"
        + # Webhooks Key
    requests.post(url, json)

def check(prev_data, new_data):
    # prev_data: [[previous information of bookmark1], [previous information of bookmark2], ...]
    # new_data: [[new information of bookmark1], [new information of bookmark2], ...]
    isUpdated = 0
    for i in range(len(prev_data)):
        if(i==0):
            continue
        if(prev_data[i][0]==new_data[i][0] and prev_data[i][2]!=new_data[i][2]):
            message = '\"' + new_data[i][1] + '\"' +  'が更新されました！\n' + 'https://ncode.syosetu.com/' + new_data[i][0] + '/' + new_data[i][3] + '/'
            print(message)
            json = {'value1': message}
            post_ifttt(json)
    store_data(new_data)

prev_data = read_data()
new_data = get_new_data()
check(prev_data, new_data)
