import os, sys, struct

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

def xor_cnes_line(l):
    return ''.join([chr(ord(c)^(210 if i%2 else 243)) for i,c in enumerate(l)])

def decode_cnes_data(data):
    result = ""
    offset = 0
    while offset+4 < len(data):
        size = struct.unpack('i',data[offset:offset+4])[0]
        result += xor_cnes_line(data[offset+4:offset+4+size])
        offset += 4+size
    return result.decode("utf-16le").encode("1251").replace("\r","\r\n")

def encode_cnes_data(data):
    result = ""
    for line in data.replace("\r\n","\r").splitlines(True):
        l = xor_cnes_line(line.decode("1251").encode("utf-16le"))
        result += struct.pack('i',len(l)) + l
    if  line[-1] == "\r":
        result += struct.pack('i',-16)
    return result

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
    if  not os.path.exists(folder):
        os.mkdir(folder)
    for n,d in datalist:
        with open(os.path.join(folder,n),"wb") as f:
            if  n[-4:] == ".SCN":
                d = recode_data(d,-1)
            elif  n[-4:] == ".tmp":
                d = recode_data(d,+1)
            f.write(d)

def usage():
    print "Usage: python " + sys.argv[0] + "(necro|cosmos|onegin) <path>"
    print "    extracts:"
    print "        necro  <pak-file> with packed pak data"
    print "        cosmos <pak-file> with packed pak data"
    print "        cosmos <sav-file> with packed sav data"
    print "        cosmos <scn-file> with encoded scripts/persistent"
    print "        onegin <cnes-file> with encoded scripts"
    print "    packs:"
    print "        necro  <folder> with unpacked pak data"
    print "        cosmos <folder> with unpacked pak/sav data"
    print "        cosmos <scene-file> with readable scripts/persistent"
    print "        onegin <nes-file> with readable scripts"

if  len(sys.argv) != 3 or sys.argv[1] not in ["necro","cosmos","onegin"]:
    usage()
    exit(-1)

game = sys.argv[1]
path = sys.argv[2]

if  os.path.isfile(path):
    data = open(path,"rb").read()

    if  game == "necro":
        if  path.lower().endswith(".pak"):
            write_files_data(path.split(".")[0],parse_files_data(data))
        else:
            usage()

    if  game == "cosmos":
        if  path.lower().endswith(".scn"):
            write_files_data(".",[(path[:-4]+".scene",recode_data(data,-1))])
        elif path.lower().endswith(".scene"):
            write_files_data(".",[(path[:-6]+".scn",recode_data(data,+1))])
        elif path.lower().endswith(".sav") or path.lower().endswith(".pak"):
            write_files_data(path.split(".")[0],parse_files_data(data))
        else:
            usage()

    if  game == "onegin":
        if  path.lower().endswith(".cnes"):
            write_files_data(".",[(path[:-5]+".nes",decode_cnes_data(data))])
        elif path.lower().endswith(".nes"):
            write_files_data(".",[(path[:-4]+".cnes",encode_cnes_data(data))])
        else:
            usage()

elif len(sys.argv) == 3 and os.path.isdir(path) and game in ["necro","cosmos"]:
    files_data = read_files_data(path)
    suffix = ".sav" if any([n=="temp_.tmp" for n,d in files_data]) else ".pak"
    write_files_data(".",[(path+suffix,create_files_data(files_data))])
