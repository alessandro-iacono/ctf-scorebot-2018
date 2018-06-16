import pwn, re, random, string

def set_flag(ip, port, flag):
    pwn.context(timeout=10)
    flag_id = "".join(random.choice(string.ascii_letters) for i in range(30))
    token = "".join(random.choice(string.ascii_letters) for i in range(30))
    r = pwn.remote(ip, port)
    if not r.recvline() == 'Welcome to the NADMOZG translator service!\n':
        raise RuntimeError("Wrong banner")
    r.send("dict {}\n".format(flag_id))
    info = r.recvline()
    m = re.match("Please enter your alphanumeric password xored with byte 0x([0-9A-F]{2}) and hex encoded:\n", info)
    if not m:
        raise RuntimeError("Wrong password request")
    byte = int(m.group(1), 16)
    r.send(''.join(chr(ord(c) ^ byte) for c in token).encode('hex') + '\n')
    if not r.recvline() == "Dictionary created\n":
        raise RuntimeError("Can't create dictionary")
    r.send("add secretik {}\n".format(flag))
    if not r.recvline() == "Word saved!\n":
        raise RuntimeError("Can't store word")
    r.send("quit\n")
    if not r.recvall() == "Good bye!\n":
        raise RuntimeError("Wrong goodbye")
    return {"flag_id" : flag_id, "token" : token}

def get_flag(ip, port, flag_id, token):
    pwn.context(timeout=10)
    r = pwn.remote(ip, port)
    if not r.recvline() == 'Welcome to the NADMOZG translator service!\n':
        raise RuntimeError("Wrong banner")
    r.send("dict {}\n".format(flag_id))
    info = r.recvline()
    m = re.match("Please enter your alphanumeric password xored with byte 0x([0-9A-F]{2}) and hex encoded:\n", info)
    if not m:
        raise RuntimeError("Wrong password request")
    byte = int(m.group(1), 16)
    r.send(''.join(chr(ord(c) ^ byte) for c in token).encode('hex') + '\n')
    if not r.recvline() == 'Password ok!\n':
        raise RuntimeError("Can't load dictionary")
    if not r.recvline() == 'Dictionary loaded\n':
        raise RuntimeError("Can't load dictionary")
    r.send("translate secretik\n")
    flag = r.recvline().strip()
    if not flag != "secretik":
        raise RuntimeError("Flag not present or deleted")
    r.send("quit\n")
    if not r.recvall() == "Good bye!\n":
        raise RuntimeError("Wrong goodbye")
    return flag
