# pip install pandas
import pandas as pd
import os

if not os.path.isfile('./Project Outputs/BOM/BOMtxt-BOM.txt'):
    print('BOM in TXT format NOT FOUND')
    raise Exception(f'BOM in TXT format NOT FOUND')

with open('./Project Outputs/BOM/BOMtxt-BOM.txt',mode="r",encoding="ISO-8859-1") as f:
    lines = f.readlines()
for i in range(lines.__len__()):
    lines[i] = lines[i].strip()
for i in range(lines.__len__()):
    lines[i] = lines[i].split('\t')

data = pd.DataFrame(lines[1:], columns=lines[0])
data = data.drop(0)

with open('./Project Outputs/Pick Place/Pick Place for PCB.txt',mode="r",encoding="ISO-8859-1") as f:
    lines = f.readlines()
for i in range(lines.__len__()):
    lines[i] = lines[i].strip()
lines = lines[12:]
for i in range(lines.__len__()):
    lines[i] = lines[i].split()
for i in range(lines.__len__()):
    lines[i][7] = ' '.join(lines[i][7:])
altium_data = pd.DataFrame(lines)
altium_data = altium_data.iloc[:,:8]
altium_data.columns = altium_data.iloc[0,:]
altium_data = altium_data.iloc[1:,:]

for i in ' '.join(list(data['Designator'])).replace('"','').replace(',','').split(): #list of designators
    if i in list(altium_data.Designator.astype('str')):
        print(i,True)
    else: 
        print(i)
        raise Exception(f'There is no {i} form BOM in Pick and Place')