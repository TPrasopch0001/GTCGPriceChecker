import json
import pandas as pd
import tcgParser as parser

current_deck = []

class GTCGDeckPricer:
    def __init__(self, deck = []):
        self.deck = deck
    def loadGundamDev(self,filepath : str) -> list[dict] | None:
        try:
            with open(filepath, 'r', encoding = 'utf-8') as f:
                for line in f:
                    if not(line[0] == '/' or line[0] == ' ' or line[0] == '\n'):
                        data = line.split()
                        entry = {}
                        entry['Number'] = data[1]
                        entry['Count'] = data[0]
                        entry['Name'] = " ".join(data[2:])
                        self.deck.append(entry)
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found")
            return None
        return self.deck

    def getDeckDetails(self, prod_DF : parser.GTCGParser) -> pd.DataFrame:
        deck = pd.DataFrame()
        for entry in self.deck:
            df_entry = prod_DF.getProductFromNumber(entry['Number'])
            deck = pd.concat([deck, df_entry])
        deck = deck.merge(pd.DataFrame(self.deck),on = 'Number', suffixes=('', '_y'))
        deck.drop(deck.filter(regex='_y$').columns, axis = 1, inplace = True)
        return deck
    
    def getDeckPrice(self, prod_DF : parser.GTCGParser):
        total = 0
        for entry in self.deck:
            df_entry = prod_DF.getProductFromNumber(entry['Number'])
            total += float(entry['Count']) * float(df_entry['Lowest Price'].iloc[0])
        return total


    def cleanDeck(self):
        self.deck = []

    def saveToExcel(self, prod_DF : parser.GTCGParser, filepath : str) -> bool:
        deck = self.getDeckDetails(prod_DF)
        print(deck)
        deck.to_excel(filepath, index=False)
        return True