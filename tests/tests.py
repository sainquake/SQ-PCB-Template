import os
import openpyxl
import json

parameters = {}
failsList = []

def check(i,it, li):
    ex_ = 'OK' if it in li else 'FAIL'
    print(f'{i} "{it}" existance: {ex_}')
    if 'FAIL' in ex_:
        failsList = f' "{it}" existance: {ex_}'
    return ex_

ex = ''

l =  os.listdir(path='.')

PROJ_PCB_NAME = ''
for item in l:
    ex_ = 'OK' if '.PrjPcb'.lower() in item.lower() else 'FAIL'
    if '.PrjPcb'.lower() in item.lower():
        PROJ_PCB_NAME = item
        break

parameters['PROJ_PCB_NAME'] = PROJ_PCB_NAME

if item=='FAIL':
    raise Exception('.PrjPcb not found')

NAME = item.split('.')[0]
parameters['NAME'] = NAME

print(f"NAME={NAME} PROJ_PCB_NAME={PROJ_PCB_NAME}")

prj = open('./'+PROJ_PCB_NAME,mode="r",encoding="utf-8")

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

#print(parameters)
ex = check('parameter','Version',parameters)

#version in PRJ
vp_h = str(parameters['Version'].split('.')[0] )
vp_m = str(parameters['Version'].split('.')[1] if len(parameters['Version'].split('.'))>1 else 0)
vp_l = str(parameters['Version'].split('.')[2] if len(parameters['Version'].split('.'))>2 else 0)
vp = vp_h+'.'+vp_m+'.'+vp_l
parameters['Version_ex'] = vp

ex = check('folder','doc', l)
if 'doc' in l:
    doc = os.listdir(path='./doc')
    ex = check('file in doc/','doc.pdf', doc)
    ex = check('file in doc/','view.png', doc)
    ex = check('file in doc/',f'{NAME}.step', doc)

ex = check('file','DRW.PCBDwf', l)
ex = check('file','Output.OutJob', l)
ex = check('file','README.md', l)
ex = check('file','.gitignore', l)
ex = check('file','BOM.BomDoc', l)
ex = check('file','LICENSE', l)

for item in l:
    ex_ = 'OK' if 'Project Outputs' in item else 'FAIL'
    if 'Project Outputs' in item:
        break
print(f'folder "{item}" existance: {ex_}')
ex = ex_

parameters['Gerber'] = {}
parameters['Gerber']['Layers'] = 0
parameters['Gerber']['Cutout'] = False

if ex_=="OK":
    outputs = os.listdir(path='./'+item)
    #print(outputs)
    ex = check('folder',f'{item}/BOM', outputs)
    ex = check('folder',f'{item}/Gerber', outputs)
    if 'Gerber' in outputs:
        Gerber = os.listdir(path='./'+item+'/Gerber')
        print(Gerber)
        for iitem in Gerber:
            layer_ = iitem.split('.')[1]
            if ('GBL' in layer_) or ('GTL' in layer_) or ('G1' in layer_) or ('G2' in layer_):
                parameters['Gerber']['Layers'] += 1
            if ('GM2' in layer_):
                parameters['Gerber']['Cutout'] = True
            #parameters['Gerber'].append( layer_ )
    
    ex = check('folder',f'{item}/NC Drill', outputs)
    ex = check('folder',f'{item}/Pick Place', outputs) 

    ex_ = 'OK' if os.path.isfile('./'+item+'/BOM/Bill of Materials-BOM.xlsx') else 'FAIL'
    print(f'file "{item}/Bill of Materials-BOM.xlsx" existance: {ex_}')
    ex = ex_
    
    print (' ')
    if os.path.isfile('./'+item+'/BOM/Bill of Materials-BOM.xlsx'):
        Rv1, Rv2, line_num, count, total_qty, smd_qty, smt_qty, none_qty = 0,0,0,0,0,0,0,0

        wb_obj = openpyxl.load_workbook('./'+item+'/BOM/Bill of Materials-BOM.xlsx') 
        wb_obj.template = False
        sheet = wb_obj.active
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            #print(i,row)
            if i>0:
                if 'Rv1' in row[0]:
                    Rv1 = row[4]
                    print(f'Rv1: {Rv1}')
                    parameters['Rv1'] = Rv1
                if 'Rv2' in row[0]:
                    Rv2 = row[4]
                    print(f'Rv2: {Rv2}')
                    parameters['Rv2'] = Rv2
                #print(row[3])
                DNP = (type(row[7]) is str) and ('DNP' in row[7])
                Test_Point = (type(row[7]) is str) and ('Test point' in row[7])
                Type = 'NONE'

                if (type(row[8]) is str) and ('SMD' in row[8]):
                    Type = 'SMD'
                if (type(row[8]) is str) and ('SMT' in row[8]):
                    Type = 'SMT'

                if (type(row[3]) is str) and ( len(row[3])<1 ):
                    if (not DNP) and (not Test_Point):
                        print( f'MP in line {line_num+1} not filled: FAIL',row  )
                        ex = "FAIL"
                        raise Exception(ex)
                    else:
                        print( f'MP in line {line_num+1} not filled but its OK' )
                
                # TJA1042 problem check
                if (type(row[3]) is str) and ('TJA1042' in row[3]):
                    ex_ = 'OK' if 'TJA1042TK/3' in row[3] else 'FAIL'
                    print(f'TJA1042 without TK/3: {ex_}')
                    ex = ex_

                # 502494-0670
                if (type(row[3]) is str) and ('502494-0670' in row[3]):
                    print(f'502494-0670: FAIL')
                    ex = "FAIL"
                    raise Exception(ex)


                if (not DNP) and ('NONE' in Type):
                    print(f' {line_num+1} {row[0]} has NONE type: FIX IT!')
                    none_qty += 1
                if (not DNP) and ('SMD' in Type):
                    smd_qty += int(row[1])
                if (not DNP) and ('SMT' in Type):
                    smt_qty += int(row[1])
                if not DNP:
                    count+=1
                if not DNP:
                    total_qty += int(row[1])
            line_num += 1
        
        print(f"line_num = {line_num}, total_qty={total_qty}, none_qty={none_qty}")
        print(f"Number of Unique Parts: {count}")
        print(f"Number of SMD Parts: {smd_qty}")
        print(f"Number of BGA/QFP Parts: {0}")
        print(f"Number of Through-Hole Parts: {smt_qty}")
        parameters["Number of Unique Parts"] = count
        parameters["Number of SMD Parts"] = smd_qty
        parameters["Number of BGA/QFP Parts"] = 0
        parameters["Number of Through-Hole Parts"] = smt_qty
    else :
        print( '/BOM/Bill of Materials-BOM.xlsx does not exists: FAIL' )
        ex = "FAIL"
        raise Exception(ex)

print("")


Rv2 = Rv1 = 0
if ('Rv2' in parameters) and ('Rv1' in parameters):  
    Rv2 = float(parameters['Rv2'].replace('k','').replace('M','')) * (1000 if 'k' in parameters['Rv2'] else 1) * (1000000 if 'M' in parameters['Rv2'] else 1)
    Rv1 = float(parameters['Rv1'].replace('k','').replace('M','')) * (1000 if 'k' in parameters['Rv1'] else 1) * (1000000 if 'M' in parameters['Rv1'] else 1)
    print('Rv2/(Rv1+Rv2)=',round(4095*Rv2/(Rv1+Rv2)))
    parameters['ADC'] = round(4095*Rv2/(Rv1+Rv2))
else:
    print('No Rv1 Rv2 for version control')


print('checking existed_boards.md ')
parameters['existed_boards'] = {}
print(NAME,Rv1,Rv2,parameters['Version'])
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
            if (r1 == Rv1) and (r2 == Rv2) and (parameters['Version_ex'] == v):
                print(name,r1,r2,v,'match!')
                match = True
                parameters['existed_boards']['r1']=r1
                parameters['existed_boards']['r2']=r2
                parameters['existed_boards']['v']=v
            else:
                print(name,r1,r2,v)
if not match:
    print('No mached line in existed_boards.md: FAIL')
    ex = "FAIL"

section = ''
rdme = []

parameters['readme'] = {}
# README.md checks
print( ' ' )
print( 'README.md checks' )
readme = open('./README.md',mode="r",encoding="utf-8")
line = readme.readline()
while line:
    line = line.strip()
    if '#' in line:
        #print(line.strip())
        section = line
    if ('- ' in line) and (line[0]=='-'):
        rdme.append( line )
        #print(line)
        if (len(line.split(':'))>1) and (len(line.split(':')[1].strip())>0):
            if 'Size (single)' in line:
                parameters['readme']['size'] = line.split(':')[1].replace('mm','').strip()
                parameters['readme']['x'] = float(parameters['readme']['size'].split('x')[0].strip())
                parameters['readme']['y'] = float(parameters['readme']['size'].split('x')[1].strip())
            if 'Layers' in line:
                parameters['readme']['Layers'] = int(line.split(':')[1].strip())
            parameters['readme']['Number of Unique Parts'] = int(line.split(':')[1].strip()) if ('Number of Unique Parts' in line) else 0   
            parameters['readme']['Number of SMD Parts'] = int(line.split(':')[1].strip()) if 'Number of SMD Parts' in line else 0   
            parameters['readme']['Number of BGA/QFP Parts'] = int(line.split(':')[1].strip()) if 'Number of BGA/QFP Parts' in line else 0   
            parameters['readme']['Number of Through-Hole Parts'] = int(line.split(':')[1].strip()) if 'Number of Through-Hole Parts' in line else 0   
    line = readme.readline()
readme.close()



try:
    # pip install steputils
    from steputils import p21
    file = p21.readfile(f'doc/{NAME}.step')

    points = [
        file.data[0].instances[x].entity.params[1] for x in [                      # 4 get point by id
            entry.entity.params[1] for entry in                                    # 3 get vertex point id
            sum([list(section.instances.values()) for section in file.data], [])   # 1 gather all sections
            if hasattr(entry, 'entity') and entry.entity.name == 'VERTEX_POINT'    # 2 filter all vertices
        ]
    ]

    min_x = min(points, key=lambda x: x[0])[0]
    max_x = max(points, key=lambda x: x[0])[0]

    min_y = min(points, key=lambda x: x[1])[1]
    max_y = max(points, key=lambda x: x[1])[1]

    min_z = min(points, key=lambda x: x[2])[2]
    max_z = max(points, key=lambda x: x[2])[2]

    bbox = (
        (min_x, min_y, min_z),
        (max_x, max_y, max_z)
    )

    dim = (
        max_x - min_x,
        max_y - min_y,
        max_z - min_z
    )

    #print(bbox)
    print(dim)
    parameters['x'] = round(dim[0]*10)/10.0
    parameters['y'] = round(dim[1]*10)/10.0
    parameters['z'] = round(dim[2]*10)/10.0

    #check
    x_check = (parameters['x']-0.1 < parameters['readme']['x']) and (parameters['readme']['x'] < parameters['x']+0.1)
    y_check = (parameters['y']-0.1 < parameters['readme']['y']) and (parameters['readme']['y'] < parameters['y']+0.1)

    x_check2 = (parameters['x']-0.1 < parameters['readme']['y']) and (parameters['readme']['y'] < parameters['x']+0.1)
    y_check2 = (parameters['y']-0.1 < parameters['readme']['x']) and (parameters['readme']['x'] < parameters['y']+0.1)

    print('Check dimensions', (x_check and y_check) or (x_check2 and x_check2) )
except:
    print("An exception occurred pip install steputils not installed")



#new_file.write(f"| xx | {NAME} | {parameters['Rv1']}   | {parameters['Rv2']}  | {parameters['Version']} |\n")
#new_file.close()  

       
#if not os.path.isfile(name): 
#    print("File path {} does not exist...".format(name))
#else:
# print('OK')

print(' ')
print(json.dumps(parameters, indent=4))

if 'FAIL' in ex:
    raise Exception(ex)