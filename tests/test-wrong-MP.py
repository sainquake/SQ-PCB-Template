import json
import os

def readData(name):
    if not os.path.isfile(name): 
        print("File path {} does not exist...".format(name))
        raise Exception("File path {} does not exist...".format(name))
    else:
        with open(name, 'r', encoding='utf8') as f: 
            j = json.load(f)
            f.close()
        return j

BOMList = readData('BOMList.json')

for item in BOMList:
    print(item['Designator'],item['Value'])
    
    if item['MP']!=None:
        if '502494-0670' in item['MP']:
            raise Exception(f'Molex connector is wrong, 502494, should be 502585-0670')

        if  ('TJA1042' in item['MP']) and ('TK/3' not in item['MP']):  
            raise Exception(f'TJA1042 is wrong MP, should be TJA1042TK/3')
