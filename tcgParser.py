import requests
import datetime


update_datetime = datetime.time(20,0,0, tzinfo = datetime.timezone.utc)
current_datetime = datetime.datetime.now(tz = datetime.UTC).time()

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

def getProductInfo(product : dict) -> dict:
    productExt = product['extendedData']
    wantedInfo = {}
    wantedInfo['name'] = product['name']
    wantedInfo['productId'] = product['productId']
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

r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/groups")
all_groups = r.json()['results']

for group in all_groups:
    group_id = group['groupId']
    r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/{group_id}/products")
    products = r.json()['results']
    r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/{group_id}/prices")
    prices = r.json()['results']
    
    
    for product in products:
        print(getProductInfo(product))

    r = requests.get(f"https://tcgcsv.com/tcgplayer/{gundam_category}/{group_id}/prices")
    prices = r.json()['results']

