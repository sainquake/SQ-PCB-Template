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
def writeData(name,data):
    if data!=None:
        if (len(name.split("/"))>1) and (not os.path.isdir(name.split("/")[0])):
            os.mkdir(name.split("/")[0])
        with open(name, 'w', encoding='utf8') as outfile: 
            json.dump(data, outfile, indent=4, ensure_ascii=False)
            outfile.close()
    else:
        print(f'Data for {name} is none ')    

paths = readData('paths.json')

PROJECT = ''
for item in paths:
    if 'PrjPcb' in item['key']:
        print(item['name'])
        PROJECT = item['name']
        break

if len(PROJECT)<1:
    print(f'PROJECT NAME NOT FOUND')
    raise Exception(f'PROJECT NAME NOT FOUND')

#EXTRACT VERSION FROM .PROJPCB FILE
print('EXTRACT VERSION FROM .PROJPCB FILE')

prj = open('./'+PROJECT,mode="r",encoding="utf-8")

parameters = {}

while prj:
    line = prj.readline()
    if '[Parameter' in line:
        n = prj.readline().split('=')[1].strip()
        v = prj.readline().split('=')[1].strip()
        parameters[n] = v
        print(n,v)
    if line == '':
        break
prj.close()

#version in PRJ
vp_h = str(parameters['Version'].split('.')[0] )
vp_m = str(parameters['Version'].split('.')[1] if len(parameters['Version'].split('.'))>1 else 0)
vp_l = str(parameters['Version'].split('.')[2] if len(parameters['Version'].split('.'))>2 else 0)
vp = vp_h+'.'+vp_m+'.'+vp_l
print(f'version from {PROJECT} file is ',vp)



#EXTRACT Rv1 and Rv2 from BOM
BOMList = readData('BOMList.json')

Rv1_str = '0'
Rv2_str = '0'

for item in BOMList:
    #print(item['Designator'],item['Value'])
    if 'Rv1'.lower() in item['Designator'].lower():
        Rv1_str = item['Value']
    if 'Rv2'.lower() in item['Designator'].lower():
        Rv2_str = item['Value']

Rv2 = float(Rv2_str.replace('k','').replace('M','')) * (1000 if 'k' in Rv2_str else 1) * (1000000 if 'M' in Rv2_str else 1)
Rv1 = float(Rv1_str.replace('k','').replace('M','')) * (1000 if 'k' in Rv1_str else 1) * (1000000 if 'M' in Rv1_str else 1)

print('EXTRACT Rv1 and Rv2 from BOM ',Rv1,Rv2)

if Rv1 == 0 and Rv2 == 0:
    print('no version control on PCB')
else:
    ADC = round(4095*Rv2/(Rv1+Rv2))

    print('ADC ',ADC)


    # EXTRACT version and Rv1 Rv2 from ./pcb-versions/existed_boards.md
    print('EXTRACT version and Rv1 Rv2 from ./pcb-versions/existed_boards.md')


    #print(BOMList)

    NAME = PROJECT.split('.')[0]
    match = False
    new_file=open("./pcb-versions/existed_boards.md",mode="r",encoding="utf-8")
    Lines = new_file.readlines()  
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        if count>2:
            s = line.strip().split('|')
            name = s[2].strip()
            r1 = float(s[3].strip() if len(s[3].strip())>1 else 0)
            r2 = float(s[4].strip() if len(s[4].strip())>1 else 0)
            #version in existed_boards
            v = str(s[5].strip()) 
            v_h = str(v.split('.')[0] if len(v.split('.'))>0 else 0)
            v_m = str(v.split('.')[1] if len(v.split('.'))>1 else 0)
            v_l = str(v.split('.')[2] if len(v.split('.'))>2 else 0)
            v = v_h+'.'+v_m+'.'+v_l

            if (NAME in name):
                if (r1 == Rv1) and (r2 == Rv2) and (vp == v):
                    print(name,r1,r2,v,'match!')
                    match = True
                else:
                    print(name,r1,r2,v)
    if not match:
        print('No mached line in existed_boards.md: FAIL')
        raise Exception(f'No mached line in existed_boards.md: FAIL')