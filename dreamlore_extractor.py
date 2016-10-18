import os, sys, struct, zipfile    

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

onegin_zip_password = "putinissatan" #wtf, lol

def parse_zip_data(path):
    result = []
    with zipfile.ZipFile(path, "r") as zip:
        zip.setpassword(onegin_zip_password)
        for n in zip.namelist():
            if  n.endswith(".cnes"):
                result.append((n,zip.read(n)))
                result.append((n[:-5]+".nes",decode_cnes_data(zip.read(n))))
            else:
                result.append((n,zip.read(n)))
    return result

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

def decode_sys0dfn_data(data):
    result = ""
    offset = 4
    for i in range(struct.unpack('i',data[:4])[0]):
        size = struct.unpack('i',data[offset:offset+4])[0]
        name = data[offset+4:offset+4+size].decode("utf-16le")
        offset += 4 + size
        trig_type = struct.unpack('i',data[offset:offset+4])[0]
        trig_type = "sys" if trig_type == 1 else "gal"
        size = struct.unpack('i',data[offset+4:offset+8])[0]
        value = data[offset+8:offset+8+size].decode("utf-16le")
        offset += 8 + size
        result += trig_type + " " + name + "=" + value + "\n"
    return result

def encode_sys0dfn_data(data):
    lines = [l for l in data.split("\n") if l]
    result = struct.pack('i',len(lines))
    for line in lines:
        trig_type = 1 if line[:3] == "sys" else 2
        k,v = line[4:].split("=")
        k,v = k.encode("utf-16le"), v.encode("utf-16le")
        result += struct.pack('i',len(k)) + k
        result += struct.pack('i',trig_type)
        result += struct.pack('i',len(v)) + v
    return result

def encode_necro_save_data(data):
    result = ""
    data = dict([l.split("=") for l in data.split("\r\n") if "=" in l])
    if  data["directors_cut"] != "0":
        result += "D"
    return result + `int(data["script_line"])+1` + "\n"

def decode_necro_save_data(data):
    if  data[0] == "D":
        return "directors_cut=1\r\nscript_line=" + `int(data[1:])-1`
    return "directors_cut=0\r\nscript_line=" + `int(data)-1`

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
    print "    extracts/decodes:"
    print "        necro  <pak-file> with packed pak data"
    print "        necro  <sav-file> with packed sav data"
    print "        cosmos <pak-file> with packed pak data"
    print "        cosmos <sav-file> with packed sav data"
    print "        cosmos <scn-file> with encoded scripts/persistent"
    print "        onegin <cnes-file> with encoded scripts"
    print "        onegin <pak-file> with packed pak data (+cnes converted)"
    print "        onegin <sys0.dfn-file> with encoded persistent"
    print "    packs/encodes:"
    print "        necro  <folder> with unpacked pak data"
    print "        necro  <save-file> with readable sav data"
    print "        cosmos <folder> with unpacked pak/sav data"
    print "        cosmos <scene-file> with readable scripts/persistent"
    print "        onegin <nes-file> with readable scripts"
    print "        onegin <sys0.persistent-file> with readable persistent"

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
        elif path.lower().endswith(".sav"):
            write_files_data(".",[(path[:-4]+".save",decode_necro_save_data(data))])
        elif path.lower().endswith(".save"):
            write_files_data(".",[(path[:-5]+".sav",encode_necro_save_data(data))])
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
        elif path.lower().endswith(".pak"):
            write_files_data(path.split(".")[0],parse_zip_data(path))
        elif path.lower().endswith("sys0.dfn"):
            write_files_data(".",[(path[:-4]+".persistent",decode_sys0dfn_data(data))])
        elif path.lower().endswith("sys0.persistent"):
            write_files_data(".",[(path[:-11]+".dfn",encode_sys0dfn_data(data))])
        else:
            usage()

elif len(sys.argv) == 3 and os.path.isdir(path) and game in ["necro","cosmos"]:
    files_data = read_files_data(path)
    suffix = ".sav" if any([n=="temp_.tmp" for n,d in files_data]) else ".pak"
    write_files_data(".",[(path+suffix,create_files_data(files_data))])

else:
    usage()
