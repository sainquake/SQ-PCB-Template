import os
import json

def writeData(name,data):
    if data!=None:
        if (len(name.split("/"))>1) and (not os.path.isdir(name.split("/")[0])):
            os.mkdir(name.split("/")[0])
        with open(name, 'w', encoding='utf8') as outfile: 
            json.dump(data, outfile, indent=4, ensure_ascii=False)
            outfile.close()
    else:
        print(f'Data for {name} is none ')

paths = []

shouldBe = []
shouldBe.append( {'root':'.','files':['.PrjPcb','.SchDoc','.BomDoc','.PCBDwf','LICENSE','.OutJob','.PcbDoc','.md','.gitignore'],'ok':False} )
shouldBe.append( {'root':'doc','files':['.step','.pdf','view-bottom.png', 'view-top.png', 'view.png'],'ok':False} )
shouldBe.append( {'root':'Outputs','files':['.Cam'],'ok':False} )
shouldBe.append( {'root':'BOM','files':['BOM.xlsx'],'ok':False} )
shouldBe.append( {'root':'Gerber','files':['.GB','.GT'],'ok':False} )
shouldBe.append( {'root':'NC Drill','files':['.'],'ok':False} )
shouldBe.append( {'root':'Pick Place','files':['.'],'ok':False} )

for root, subdirs, files in os.walk('.'):
    if ('.git' not in root) and ('History' not in root):
        #print(root, subdirs, files)
        for item in shouldBe:
            if (not item['ok']) and (item['root'] in root):
                #print(files,item['files'])
                for j in item['files']:
                    found = False
                    for k in files:
                        if j.lower() in k.lower():
                            found = True
                            print(root,k,j)
                            paths.append( {'root':item['root'],'key':j,'path':root,'name':k} )
                            break 
                    if not found:
                        print(f'FILE {j} in {root} folder NOT FOUND')
                        raise Exception(f'FILE {j} in {root} folder NOT FOUND')
                item['ok'] = True
                
                break

for item in shouldBe:
    if not item['ok']:
        print(f'FOLDER { item["root"] }  NOT FOUND')
        raise Exception(f'FOLDER { item["root"] }  NOT FOUND')

print(paths)
writeData('paths.json',paths)

'''

rootFiles = []
rootDirs = []

i=0
for root, subdirs, files in os.walk('.'):
    if '.git' not in root:
        print(root, subdirs, files)
        if i==0:
            rootFiles = files
            rootDirs = subdirs
            break
        i += 1

#l =  os.listdir(path='.')

# CHECK THAT FILES EXISTS
print('CHECK THAT FILES EXISTS')

shouldBeInRepo = ['.PrjPcb','.SchDoc','.BomDoc','.PCBDwf','LICENSE','.OutJob','.PcbDoc','.md','.gitignore']
shouldBeInRepoResult = []

ok = True
for item in shouldBeInRepo:
    shouldBeInRepoResult.append( [item,False] )
    for it in rootFiles:
        if item.lower() in it.lower():
            shouldBeInRepoResult[-1][0] = it
            shouldBeInRepoResult[-1][1] = True
            break
    if not shouldBeInRepoResult[-1][1]:
        ok = False

for item in shouldBeInRepoResult:
    print(f' file {item[0]} \texists =  \t{str(item[1])} ')

if not ok:
    raise Exception('some of the FILES not found')

# CHECK THAT FOLDERS EXISTS
print('CHECK THAT FOLDERS EXISTS')

souldBeInRepoFolders = ['doc','Outputs']
souldBeInRepoFoldersResult = []

ok = True
for item in souldBeInRepoFolders:
    souldBeInRepoFoldersResult.append( [item,False] )
    for it in rootDirs:
        if item.lower() in it.lower():
            souldBeInRepoFoldersResult[-1][0] = it
            souldBeInRepoFoldersResult[-1][1] = True
            break
    if not souldBeInRepoFoldersResult[-1][1]:
        ok = False

for item in souldBeInRepoFoldersResult:
    print(f' folder {item[0]} \texists =  \t{str(item[1])} ')

if not ok:
    raise Exception('some of the FOLDERS not found')

# CHECK THAT FILES IN doc EXISTS
print('CHECK THAT FILES IN doc EXISTS')

l =  os.listdir(path=f'./{souldBeInRepoFoldersResult[0][0]}')

shouldBeInDoc = ['.step','.pdf','view-bottom.png', 'view-top.png', 'view.png']
shouldBeInDocResult = []

ok = True
for item in shouldBeInDoc:
    shouldBeInDocResult.append( [item,False] )
    for it in l:
        if item.lower() in it.lower():
            shouldBeInDocResult[-1][0] = it
            shouldBeInDocResult[-1][1] = True
            break
    if not shouldBeInDocResult[-1][1]:
        ok = False

for item in shouldBeInDocResult:
    print(f' file {item[0]} \texists =  \t{str(item[1])} ')

if not ok:
    raise Exception('some of the FILES not found in folder ./doc')

# CHECK THAT FILES IN Outputs EXISTS
print('CHECK THAT FILES IN Outputs EXISTS')

shouldBeInOutputs = ['BOM', '.Cam', 'Gerber', 'NC Drill', 'Pick Place']


l =  os.listdir(path=f'./{souldBeInRepoFoldersResult[1][0]}')
print( l )

for item in shouldBeInOutputs:
    for it in l:
        if 

    

#os.path.isdir(directory)

'''