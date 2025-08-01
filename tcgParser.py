import json
import requests
import datetime
import os
import ast
import pandas as pd



class GTCGParser:
    
    def __init__(self, initData : pd.DataFrame = pd.DataFrame()):
        self.data = initData


    def setSaveFile(fileName) -> str:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, fileName)

    def getLastUpdated() -> datetime.datetime:
        r = requests.get("https://tcgcsv.com/last-updated.txt")
        update_datetime = datetime.datetime.fromisoformat(r.text)
        return update_datetime
    """
    Parses wanted data for card
    """
    def getProductInfo(product : dict) -> dict | None:
        productExt = product['extendedData']
        wantedInfo = {}
        wantedInfo['Name'] = product['name']
        wantedInfo['ProductId'] = product['productId']
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

    def getProductPrice(price : dict) -> dict | None:
        wantedInfo = {}
        wantedInfo['ProductId'] = price['productId']
        wantedInfo['Market Price'] = price['marketPrice']
        return wantedInfo

        """
        Returns a pandas DataFrame that contains the following information:
        Name,ProductId,Attack Points,Hit Points, Number (Position in Set), Level, Cost, CardType, Market Price
        """
    def getDataOnline(self) -> pd.DataFrame:
        r = requests.get(f"https://tcgcsv.com/tcgplayer/86/groups")
        all_groups = r.json()['results']

        allProducts = []
        allPrices = []
        for group in all_groups:
            group_id = group['groupId']
            r = requests.get(f"https://tcgcsv.com/tcgplayer/86/{group_id}/products")
            products = r.json()['results']
            r = requests.get(f"https://tcgcsv.com/tcgplayer/86/{group_id}/prices")
            prices = r.json()['results']
            
            for product in products:
                data = GTCGParser.getProductInfo(product) 
                if data: # If product is not a booster, box, case, etc. add it to the list
                    allProducts.append(data)

            for price in prices:
                data = GTCGParser.getProductPrice(price)
                allPrices.append(data)
            
            prodDF = pd.DataFrame(allProducts)
            priceDF = pd.DataFrame(allPrices)
            allData = pd.merge(prodDF, priceDF, on = "ProductId", how = "left")
        self.data = allData
        return allData

    def save(self, filepath):
        filepath = GTCGParser.setSaveFile(filepath)
        with open(filepath, "w") as f:
            f.write(str(datetime.datetime.now(tz = datetime.UTC)) + '\n')
            f.write(self.data.to_json(orient = 'records', lines = True))

        """
        Reads local data if the data is up to date and file exists, 
        otherwise collects data then parses it in
        """
    def readData(self, filepath):
        allData = []
        output_path = GTCGParser.setSaveFile(filepath)
        try:
            with open(output_path, 'r') as f:
                time = datetime.datetime.fromisoformat(f.readline()[:-1])
                if time > GTCGParser.getLastUpdated():
                    print("up to date!")
                    for line in f:
                        allData.append(json.loads(line))
                else:
                    allData = GTCGParser.getDataOnline()
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found, creating new data")
            allData = GTCGParser.getDataOnline()
            self.save(allData, filepath)
        self.data = pd.DataFrame(allData)
        return self.data


testParser = GTCGParser()
testDF = testParser.readData('test.txt')
testParser.save('test.txt')