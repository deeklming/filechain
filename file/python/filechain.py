import os
import sys
import timeit
import json
import random
from hashlib import sha3_512
from hashlib import blake2b
from datetime import datetime
import traceback

def help_start():
    print("""
\n\t\t!!!Filechain!!!\n
[OPTION]
    init - make initialization hash.
    set - set file path, added and ignored.
    create - create filechain.
    update - filechain update.
    verify - filechain verify.

<START>""")

    if len(sys.argv)==1:
        raise Exception("Need option.")
    elif len(sys.argv)==2:
        opt = ["init", "set", "create", "update", "verify"]
        if sys.argv[1] in opt:
            print("Args OK.\n")
        else:
            raise Exception("No option.")
    else:
        raise Exception("Args failed.")
    
    return sys.argv[1]

def jsonprint(j):
    print('{')
    for i in j:
        print('  ',i,': ',j[i])
    print('}')

def init():
    init_json = {
        "programname": "",
        "version": "",
        "targetpath": "",
        "savepath": "",
        "initialvalue": "",
        "addfile": [],
        "ignorefile": []
    }
    init_json["programname"] = input("<init - start>\nprogram name: ")
    init_json["version"] = input("program version: ")
    init_json["targetpath"] = input("program target path(only directory): ")
    init_json["savepath"] = input("init json and filechain file path(only directory): ")

    with open(init_json["savepath"]+"\\FilechainInit.json", "w") as f:
        json.dump(init_json, f, indent=2)
    with open(init_json["savepath"]+"\\FilechainAdd.txt", "w") as f:
        pass
    with open(init_json["savepath"]+"\\FilechainIgnore.txt", "w") as f:
        pass
    
    jsonprint(init_json)
    print('<init - success>')

def set():
    json_path = input("<set - start>\nFilechainInit.json path(file): ")
    if json_path.split('\\')[-1] != "FilechainInit.json":
        raise Exception("This file is not FilechainInit.json!")

    init_hash_value = input("Initional hash value(string): ")
    if not init_hash_value:
        init_hash_value = str(random.random())

    with open(json_path, "r") as f:
        json_data = json.load(f)
        json_data["initialvalue"] = init_hash_value
        with open(json_data["savepath"]+"\\FilechainAdd.txt", "r") as adf:
            json_data["addfile"] = list(map(str.strip, adf.readlines()))
        with open(json_data["savepath"]+"\\FilechainIgnore.txt", "r") as igf:
            json_data["ignorefile"] = list(map(str.strip, igf.readlines()))
        json_data["ignorefile"].append(json_data["targetpath"]+f"\\{json_data['programname']}.filechain")#ignore filechain file
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=2)
    
    jsonprint(json_data)
    print('<set - success>')

def findDaF(dirLocation):#path list return
    dfInfo = []
    dfAppd = dfInfo.append#speed up
    for root, _, files in os.walk(dirLocation):
        for s in files:
            dfAppd(root+'\\'+s)
        dfAppd(root)
    return dfInfo

def create():
    json_path = input("<create - start>\nFilechainInit.json path(file): ")
    if json_path.split('\\')[-1] != "FilechainInit.json":
        raise Exception("This file is not FilechainInit.json!")

    with open(json_path, "r") as f:
        json_data = json.load(f)
        finalHash = sha3_512(json_data["initialvalue"].encode('utf-8')).digest()#Initional hash value
        finalHash += finalHash#make lash hash
        dfList = findDaF(json_data["targetpath"])#make target list, start
        addFiles = json_data["addfile"]
        if addFiles:
            for addFile in addFiles:
                if os.path.isfile(addFile):
                    dfList += addFile
                else:
                    dfList += findDaF(addFile)
        dfList = list(dict.fromkeys(dfList))#deduplication
        ignoreFiles = json_data["ignorefile"]
        if ignoreFiles:
            for ignoreFile in ignoreFiles:
                if os.path.isfile(ignoreFile):
                    dfList.remove(ignoreFile)
                else:
                    for tmp in findDaF(ignoreFile):
                        dfList.remove(tmp)#make target list, end
        
        for x in dfList:#make hash
            if os.path.isfile(x):
                dfStr=f"{os.path.basename(x)}{os.path.getsize(x)}{datetime.fromtimestamp(os.path.getmtime(x)).isoformat(sep=' ', timespec='seconds')}"
            else:
                dfStr=f"{os.path.basename(x)}"
            hash = blake2b(dfStr.encode('utf-8'))
            hash = hash.digest()+bytes(0b1000000)
            finalHash = bytes([a^b for a,b in zip(finalHash, hash)])
        
        with open(json_data["targetpath"]+f"\\{json_data['programname']}.filechain", "wb") as fc:
            fc.write(finalHash)
    print(finalHash)    
    print('<create - success>')

def update():
    json_path = input("<update - start>\nFilechainInit.json path(file): ")
    if json_path.split('\\')[-1] != "FilechainInit.json":
        raise Exception("This file is not FilechainInit.json!")
    
    with open(json_path, "r") as f:
        json_data = json.load(f)
        dfList = findDaF(json_data["targetpath"])#make target list, start
        addFiles = json_data["addfile"]
        if addFiles:
            for addFile in addFiles:
                if os.path.isfile(addFile):
                    dfList += addFile
                else:
                    dfList += findDaF(addFile)
        dfList = list(dict.fromkeys(dfList))#deduplication
        ignoreFiles = json_data["ignorefile"]
        if ignoreFiles:
            for ignoreFile in ignoreFiles:
                if os.path.isfile(ignoreFile):
                    dfList.remove(ignoreFile)
                else:
                    for tmp in findDaF(ignoreFile):
                        dfList.remove(tmp)#make target list, end
        
        with open(json_data["targetpath"]+f"\\{json_data['programname']}.filechain", "rb+") as fc:
            finalHashOriginal = fc.read()
            finalHash = finalHashOriginal[:64]+finalHashOriginal[:64]#nowhash to lasthash
            for x in dfList:
                if os.path.isfile(x):
                    dfStr=f"{os.path.basename(x)}{os.path.getsize(x)}{datetime.fromtimestamp(os.path.getmtime(x)).isoformat(sep=' ', timespec='seconds')}"
                else:
                    dfStr=f"{os.path.basename(x)}"
                hash = blake2b(dfStr.encode('utf-8'))
                hash = hash.digest()+bytes(0b1000000)
                finalHash = bytes([a^b for a,b in zip(finalHash, hash)])
            if finalHashOriginal == finalHash[64:]+finalHash[:64]:#not change target file
                print('<verify - failure>')
                return False
            else:
                fc.seek(0)
                fc.write(finalHash)
                print('<update - success>')
                return True

def verify():
    json_path = input("<verify - start>\nFilechainInit.json path(file): ")
    if json_path.split('\\')[-1] != "FilechainInit.json":
        raise Exception("This file is not FilechainInit.json!")
    
    verifyCheck = True
    with open(json_path, "r") as f:
        json_data = json.load(f)
        dfList = findDaF(json_data["targetpath"])#make target list, start
        addFiles = json_data["addfile"]
        if addFiles:
            for addFile in addFiles:
                if os.path.isfile(addFile):
                    dfList += addFile
                else:
                    dfList += findDaF(addFile)
        dfList = list(dict.fromkeys(dfList))#deduplication
        ignoreFiles = json_data["ignorefile"]
        if ignoreFiles:
            for ignoreFile in ignoreFiles:
                if os.path.isfile(ignoreFile):
                    dfList.remove(ignoreFile)
                else:
                    for tmp in findDaF(ignoreFile):
                        dfList.remove(tmp)#make target list, end
        
        with open(json_data["targetpath"]+f"\\{json_data['programname']}.filechain", "rb") as fc:
            finalHash = fc.read()
            for x in dfList:
                if os.path.isfile(x):
                    dfStr=f"{os.path.basename(x)}{os.path.getsize(x)}{datetime.fromtimestamp(os.path.getmtime(x)).isoformat(sep=' ', timespec='seconds')}"
                else:
                    dfStr=f"{os.path.basename(x)}"
                hash = blake2b(dfStr.encode('utf-8'))
                hash = hash.digest()+bytes(0b1000000)
                finalHash = bytes([a^b for a,b in zip(finalHash, hash)])
            for p in range(64):#verify check
                if finalHash[p] != finalHash[p+64]:
                    verifyCheck = False
                    break
    if verifyCheck:
        print('<verify - success>')
        return True
    else:
        print('<verify - failure>')
        return False

if __name__=="__main__":
    starttime = timeit.default_timer()

    try:
        argv = help_start()
        if argv == "init":
            init()
        elif argv == "set":
            set()
        elif argv == "create":
            create()
        elif argv == "update":
            update()
        elif argv == "verify":
            verify()
    except Exception as e:
        print('<err>: ', e)
        print(traceback.format_exc())
    finally:
        print("\n<END>\nProgram exit.")

    endtime = timeit.default_timer()
    print(f"Running Time: {endtime-starttime}ms")
