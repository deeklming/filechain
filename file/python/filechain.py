import os
import sys
import timeit
import time
from hashlib import blake2b
from datetime import datetime

def err(s):
    print(s)
    sys.exit()

def helpcheck(s):
    print(s+"\nYou can [FileChain Program] [help]\n")
    sys.exit()

def allDFfind(dirLocation):
    dfinfo=[]
    for root, _, files in os.walk(dirLocation):
        for s in files:
                dfinfo.append(root+'\\'+s)
        dfinfo.append(root)
        print(root)
    return dfinfo

def fchainew(path):
    dfli = allDFfind(path)
    dflen = len(dfli)
    finalhash=bytes(0b10000000)
    for s in dfli:
        dfstr=""
        if os.path.isfile(s):
            if dflen>10 and s[-10:]==".filechain":
                err("<fchainew> Remove *.filechain file plz")
            dfstr=f"{os.path.basename(s)}{os.path.getsize(s)}{datetime.fromtimestamp(os.path.getmtime(s)).isoformat(sep=' ', timespec='seconds')}"
        else:
            dfstr=f"{os.path.basename(s)}"
        hash = blake2b(dfstr.encode('utf-8'))
        hash = hash.digest()+bytes(0b1000000)
        finalhash = bytes([a^b for a,b in zip(finalhash, hash)])
    return finalhash

def fchainud(path):
    dfli = allDFfind(path)
    dflen = len(dfli)
    finalhash=bytes(0b10000000)
    check=0
    alldfstr=[]
    for s in dfli:
        dfstr=""
        if os.path.isfile(s):
            if dflen>10 and s[-10:]==".filechain":
                check+=1
                with open(s,"rb") as f:
                    finalhash = f.read()
                continue
            dfstr=f"{os.path.basename(s)}{os.path.getsize(s)}{datetime.fromtimestamp(os.path.getmtime(s)).isoformat(sep=' ', timespec='seconds')}"
            alldfstr.append(dfstr)
        else:
            dfstr=f"{os.path.basename(s)}"
            alldfstr.append(dfstr)
    if check>1:
        err("<fchainud> Why are there more than 2 *.filechain?")
    elif check==1:
        tmpt=finalhash[:64]
        finalhash = finalhash[:64]+tmpt
        for j in alldfstr:
            hash = blake2b(j.encode('utf-8'))
            hash = hash.digest()+bytes(0b1000000)
            finalhash = bytes([a^b for a,b in zip(finalhash, hash)])
    else:
        err("<fchainud> Where is *.filechain?")
    return finalhash

def fchainvf(path):
    dfli = allDFfind(path)
    dflen = len(dfli)
    finalhash=bytes(0b10000000)
    check=0
    alldfstr=[]
    for s in dfli:
        dfstr=""
        if os.path.isfile(s):
            if dflen>10 and s[-10:]==".filechain":
                check+=1
                with open(s,"rb") as f:
                    finalhash = f.read()
                continue
            dfstr=f"{os.path.basename(s)}{os.path.getsize(s)}{datetime.fromtimestamp(os.path.getmtime(s)).isoformat(sep=' ', timespec='seconds')}"
            alldfstr.append(dfstr)
        else:
            dfstr=f"{os.path.basename(s)}"
            alldfstr.append(dfstr)
    if check>1:
        err("<fchainud> Why are there more than 2 *.filechain?")
    elif check==1:
        for j in alldfstr:
            hash = blake2b(j.encode('utf-8'))
            hash = hash.digest()+bytes(0b1000000)
            finalhash = bytes([a^b for a,b in zip(finalhash, hash)])
        truecheck=True
        for t in range(64):
            if finalhash[t] != finalhash[t+64]:
                truecheck=False
                print("[verify] -> Flase")
                break
        if truecheck:
            print("[verify] -> True")
    else:
        err("<fchainud> Where is *.filechain?")

if __name__=="__main__":
    starttime = timeit.default_timer()
    print("\n\t\t\t!!!HashFileChain!!!\n")

    if len(sys.argv)==1:
        helpcheck("<args check> No option! [FileChain Program] [Option] [Just one folder Path to hash]")
    elif len(sys.argv)==2:
        if sys.argv[1]=="help":
            print("help)\n[FileChain Program] [Option] [Just one folder Path to hash]")
            print("[Option]\n\tnew: 현제 폴더 새로운 해시 생성\n\tupdate: 해시 업데이트")
            print("\tverify: 검증\n\thelp: 사용법\n")
            sys.exit()
        elif sys.argv[1]=="new" or sys.argv[1]=="update" or sys.argv[1]=="verify":
            print("<args check> More Path [FileChain Program] [Option] [Just one folder Path to hash]\n")
            sys.exit()
        else:
            helpcheck("<args check> No option! [FileChain Program] [Option] [Just one folder Path to hash]")
    elif len(sys.argv)==3:
        if sys.argv[1]=="new" or sys.argv[1]=="update" or sys.argv[1]=="verify":
            pass
        elif sys.argv[1]=="help":
            helpcheck("help doesn't need a path.")
        else:
            helpcheck("Plz check option")
        if os.path.isdir(sys.argv[2]):
            print(f"OK, Selected! [Option]->{sys.argv[1]} [Path]->{sys.argv[2]}\n")
        else:
            helpcheck("<path check> Can't open folder")
    else:
        helpcheck("<args check> Over Args [FileChain Program] [Option] [Just one folder Path to hash]")
    path=sys.argv[2]
    if sys.argv[1]=="new":
        f1 = fchainew(path)
        with open(path+"\\b.filechain","wb") as f:
            f.write(f1)
    elif sys.argv[1]=="update":
        f2 = fchainud(path)
        with open(path+"\\b.filechain","wb") as f:
            f.write(f2)
    elif sys.argv[1]=="verify":
        fchainvf(sys.argv[2])

    endtime = timeit.default_timer()
    print(f"실행시간: {endtime-starttime}sec")
    