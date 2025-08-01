import json
import requests
import datetime
import os
import ast

r = requests.get("https://tcgcsv.com/last-updated.txt")
utc = r.text
update_datetime = datetime.datetime.fromisoformat(utc)
current_datetime = datetime.datetime.now(tz = datetime.UTC)


gundam_category = '86'


# r = requests.get("https://tcgcsv.com/tcgplayer/86/24221/products")
# products = r.json()['results']
# product = products[5]
# productExt = product['extendedData']
# wantedInfo = {}
# wantedInfo['name'] = product['name']
# wantedInfo['productId'] = product['productId']
# for data in productExt:
#     name = data['name']
#     if name == 'Cost' or name == 'CardType' \
#     or name == 'Level' or name == 'Number' \
#     or name == 'Attack Points' or name == 'Hit Points':
#         wantedInfo[name] = data['value']
#     if 'Attack Points' not in wantedInfo:
#         wantedInfo['Attack Points'] = -1
#     if 'Hit Points' not in wantedInfo:
#         wantedInfo['Hit Points'] = -1
# print(wantedInfo)

def getProductInfo(product : dict) -> dict | None:
    productExt = product['extendedData']
    wantedInfo = {}
    wantedInfo['name'] = product['name']
    wantedInfo['productId'] = product['productId']
    if not productExt:
        return None
    for data in productExt:
        name = data['name']
        if name == 'Cost' or name == 'CardType' \
        or name == 'Level' or name == 'Number' \
        or name == 'Attack Points' or name == 'Hit Points':
            wantedInfo[name] = data['value']
        if 'Attack Points' not in wantedInfo:
            wantedInfo['Attack Points'] = -1
        if 'Hit Points' not in wantedInfo:
            wantedInfo['Hit Points'] = -1
    return wantedInfo

def getDataOnline():
    r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/groups")
    all_groups = r.json()['results']

    allData = []
    for group in all_groups:
        group_id = group['groupId']
        r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/{group_id}/products")
        products = r.json()['results']
        r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/{group_id}/prices")
        prices = r.json()['results']
        
        
        for product in products:
            data = getProductInfo(product)
            if data:
                allData.append(data)

        r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/{group_id}/prices")
        prices = r.json()['results']
    return allData

script_dir = os.path.dirname(os.path.abspath(__file__))

file_name = 'test.txt'
output_path = os.path.join(script_dir, file_name)

def save(data):
    with open(output_path, "w") as f:
        f.write(str(current_datetime) + '\n')
        for entry in data:
            f.write(str(entry) + '\n')

def readData(filepath):
    allData = []
    output_path = os.path.join(script_dir, file_name)
    with open(output_path, 'r') as f:
        time = datetime.datetime.fromisoformat(f.readline()[:-1])
        if time > update_datetime:
            print("up to date!")
            for line in f:
                allData.append(ast.literal_eval(f.readline()[:-1]))
        else:
            allData = getDataOnline()
    return allData


allData = readData('test.txt')
print(allData)