import time
# 288-bit initial state
s = [None]*288

# trivium initialization
def initialize(K,IV):
    global s

    # convert to binary
    k_dec = int(K,16)
    k_bin = '{:080b}'.format(k_dec)
    iv_dec = int(IV,16)
    iv_bin = '{:080b}'.format(iv_dec)

    # load key
    for i in range(0,93):
        if (i<80):
            s[i] = int(k_bin[i])
        else:
            s[i] = 0

    # load iv
    j = 0
    for i in range(93,177):
        if (j<80):
            s[i] = int(iv_bin[j])
        else:
            s[i] = 0
        j += 1

    for i in range(177,288):
        if (i<285):
            s[i] = 0
        else: 
            s[i] = 1
    
    # rotate 4 full cycles
    cycle4 = 4*288
    for i in range(0,cycle4):
        old_s = s

        t1 = s[65] ^ s[90] & s[91] ^ s[92] ^ s[170]
        t2 = s[161] ^ s[174] & s[175] + s[176] ^ s[263]
        t3 = s[242] ^ s[285] & s[286] ^ s[287] ^ s[68]

        for i in range(0,93):
            if (i==0):
                s[i] = t3
            else:
                s[i] = old_s[i-1]

        for i in range(93,177):
            if (i==93):
                s[i] = t1
            else:
                s[i] = old_s[i-1]

        for i in range(177,288):
            if (i==177):
                s[i] = t2
            else:
                s[i] = old_s[i-1]

# generate keystream
def keygen(num):
    global s

    old_s = s

    if (num > pow(2,64)):
        n = pow(2,64)
    else:
        n = num

    z=""

    count = 0
    while (count<n):
        t1 = s[65] ^ s[93]
        t2 = s[161] ^ s[176]
        t3 = s[242] ^ s[287]
    
        t123 = t1 ^ t2 ^ t3
        z += str(t123)
    
        t1 = t1 ^ s[90] & s[91] ^ s[171]
        t2 = t2 ^ s[174] & s[175] ^ s[263]
        t3 = t3 ^ s[285] & s[286] ^ s[68]

        for i in range(0,93):
            if (i==0):
                s[i] = t3
            else:
                s[i] = old_s[i-1]

        for i in range(93,177):
            if (i==93):
                s[i] = t1
            else:
                s[i] = old_s[i-1]

        for i in range(177,288):
            if (i==177):
                s[i] = t2
            else:
                s[i] = old_s[i-1]

        count+=1

    keystream_dec = int(z,2)
    keystream = '{:X}'.format(keystream_dec)

    return keystream

def encrypt_decrypt(plain_text,display):
    start = time.time()

    # convert plain text to hex
    plainHex = plain_text.encode("utf-8").hex()

    # convert to binary
    plainBin = ''.join(format(ord(i), '08b') for i in plain_text)

    # obtain number of bits required
    num = len(plainBin)

    # generate keystream
    keystream = keygen(num)

    plainInt = int(plainHex,16)
    keyInt = int(keystream,16)

    # xor plaintext and keystream
    result = plainInt ^ keyInt

    # ciphertext in hexadecimal
    cipherHex = '{:0X}'.format(result)

    cipherInt = int(cipherHex,16)

    # xor ciphertext and keystream
    result = cipherInt ^ keyInt
    recoverHex = '{:0X}'.format(result)

    recover_text = bytes.fromhex(recoverHex).decode('utf-8')

    end = time.time()

    # get time to encrypt and decrypt (ms)
    time_used = (end - start) * 1000
    result = format(time_used, '.5f')

    if (display):
        print("plain text    : " + plain_text)
        print("cipher text   : " + cipherHex)
        print("recovered text: " + recover_text)

    return result