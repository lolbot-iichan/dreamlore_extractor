import os, sys

def create_files_data(datalist):
    offset = 0
    data = "%04d" % len(datalist)
    for n,d in datalist:
        data += "%04d" % len(n)
        data += n
        data += "%010d" % len(d)
        data += "%010d" % offset
        offset += len(d)
    for n,d in datalist:
        data += d
    return data

def parse_files_data(data):
    flist = []
    i = 4
    for n in range(int(data[:4])):
        namelen  = int(data[i             :i+4])
        name     =     data[i+4           :i+4+namelen]
        size     = int(data[i+4+namelen   :i+4+namelen+10])
        offset   = int(data[i+4+namelen+10:i+4+namelen+20])
        flist.append((name,size,offset))
        i += namelen+24
    return [(n,data[i+o:i+o+s]) for n,s,o in flist]

def recode_data(data, delta):
    return ''.join([chr((ord(c)+delta)%256) for c in data])

def read_files_data(folder):
    datalist = []
    for n in os.listdir(folder):
        with open(os.path.join(folder,n),"rb") as f:
            d = f.read()
            if  n[-4:] == ".SCN":
                d = recode_data(d,+1)
            elif  n[-4:] == ".tmp":
                d = recode_data(d,-1)
            datalist.append((n,d))
    return datalist

def write_files_data(folder,datalist):
    for n,d in datalist:
        with open(os.path.join(folder,n),"wb") as f:
            if  n[-4:] == ".SCN":
                d = recode_data(d,-1)
            elif  n[-4:] == ".tmp":
                d = recode_data(d,+1)
            f.write(d)

if  len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
    data = open(sys.argv[1],"rb").read()
    if  sys.argv[1][-4:].lower() == ".scn":
        write_files_data(".",[(sys.argv[1]+".unpack",recode_data(data,-1))])
    elif sys.argv[1][-7:] == ".unpack":
        write_files_data(".",[(sys.argv[1][:-7],recode_data(data,+1))])
    else:
        folder = sys.argv[1].split(".")[0]
        if  not os.path.exists(folder):
            os.mkdir(folder)
        write_files_data(folder,parse_files_data(data))
elif len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
    files_data = read_files_data(sys.argv[1])
    suffix = ".sav" if any([n=="temp_.tmp" for n,d in files_data]) else ".pak"
    write_files_data(".",[(sys.argv[1]+suffix,create_files_data(files_data))])
else:
    print "Usage: python " + sys.argv[0] + " <path>"
    print "    extracts:"
    print "        <pak-file> of NecroBook or RedCosmos"
    print "        <sav-file> of RedCosmos"
    print "        <SCN-file> of RedCosmos (triggers.scn)"
    print "    packs:"
    print "        <folder> with pak or sav of NecroBook or RedCosmos"
    print "        <unpack-file> with triggers.scn or RedCosmos"
