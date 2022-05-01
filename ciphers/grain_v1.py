import time

nfsr = [None]*80
lfsr = [None]*80

# clock function
def clock():
    global lfsr
    global nfsr

    hx = 0
    fx = 0
    gx = 0

    # clock 160 times
    for i in range(0,160):
        fx = lfsr[62] ^ lfsr[51] ^ lfsr[38] ^ lfsr[23] ^ lfsr[13] ^ lfsr[0] ^ hx

        g = nfsr[63] ^ nfsr[60] ^ nfsr[52] ^ nfsr[45] ^ nfsr[37] ^ nfsr[33] ^ nfsr[28] \
            ^ nfsr[21] ^ nfsr[15] ^ nfsr[9] ^ nfsr[0] ^ (nfsr[63] & nfsr[60]) ^ (nfsr[37] & nfsr[33]) \
            ^ (nfsr[15] & nfsr[9]) ^ (nfsr[60] & nfsr[52] & nfsr[45]) ^ (nfsr[33] & nfsr[28] & nfsr[21]) \
            ^ (nfsr[63] & nfsr[45] & nfsr[28] & nfsr[9]) ^ (nfsr[60] & nfsr[52] & nfsr[37] & nfsr[33]) \
            ^ (nfsr[63] & nfsr[60] & nfsr[21] & nfsr[15]) ^ (nfsr[63] & nfsr[60] & nfsr[52] & nfsr[45] & nfsr[37]) \
            ^ (nfsr[33] & nfsr[28] & nfsr[21] & nfsr[15] & nfsr[9]) \
            ^ (nfsr[52] & nfsr[45] & nfsr[37] & nfsr[33] & nfsr[28] & nfsr[21])
        gx = hx ^ g

        x0 = nfsr[0]
        y3 = lfsr[3]
        y25 = lfsr[25]
        y46 = lfsr[46]
        y64 = lfsr[64]
        x63 = nfsr[63]

        # cipher output bit zt
        p = 1 ^ y64 ^ (y46 & (y3 ^ y25 ^ y64))
        q = y25 ^ ((y3 & y46) & (y25 ^ y64)) ^ (y64 & (y3 ^ y46))
        hx = x0 ^ (x63 & p) ^ q

        # shift 1 bit to left, load last bit with new value
        lfsr_0 = lfsr[0]
        lfsr[:-1] = lfsr[1:]
        lfsr[-1] = fx
        nfsr[:-1] = nfsr[1:]
        nfsr[-1] = gx ^ lfsr_0

# grain v1 initialization
def initialize(K,IV):
    global nfsr
    global lfsr

    # convert to binary
    k_dec = int(K,16)
    k_bin = '{:080b}'.format(k_dec)
    iv_dec = int(IV,16)
    iv_bin = '{:064b}'.format(iv_dec)

    # set bit 65-80 to 1
    for i in range(64,80):
        iv_bin += "1"

    # load key and iv
    for i in range (0,80):
        nfsr[i] = int(k_bin[i])
        lfsr[i] = int(iv_bin[i])

    # clock function
    clock()

# generate keystream
def keygen(num):
    global nfsr
    global lfsr

    keystream_bin = ""

    # generate keystrean bits
    count = 0
    while (count<num):
        hx = 0

        fx = lfsr[62] ^ lfsr[51] ^ lfsr[38] ^ lfsr[23] ^ lfsr[13] ^ lfsr[0]

        gx = nfsr[0] ^ nfsr[63] ^ nfsr[60] ^ nfsr[52] ^ nfsr[45] ^ nfsr[37] ^ nfsr[33] ^ nfsr[28] \
            ^ nfsr[21] ^ nfsr[15] ^ nfsr[9] ^ nfsr[0] ^ (nfsr[63] & nfsr[60]) ^ (nfsr[37] & nfsr[33]) \
            ^ (nfsr[15] & nfsr[9]) ^ (nfsr[60] & nfsr[52] & nfsr[45]) ^ (nfsr[33] & nfsr[28] & nfsr[21]) \
            ^ (nfsr[63] & nfsr[45] & nfsr[28] & nfsr[9]) ^ (nfsr[60] & nfsr[52] & nfsr[37] & nfsr[33]) \
            ^ (nfsr[63] & nfsr[60] & nfsr[21] & nfsr[15]) ^(nfsr[63] & nfsr[60] & nfsr[52] & nfsr[45] & nfsr[37]) \
            ^ (nfsr[33] & nfsr[28] & nfsr[21] & nfsr[15] & nfsr[9]) \
            ^ (nfsr[52] & nfsr[45] & nfsr[37] & nfsr[33] & nfsr[28] & nfsr[21])

        x0 = nfsr[0]
        y3 = lfsr[3]
        y25 = lfsr[25]
        y46 = lfsr[46]
        y64 = lfsr[64]
        x63 = nfsr[63]

        p = 1 ^ y64 ^ (y46 & (y3 ^ y25 ^ y64))
        q = y25 ^ ((y3 & y46) & (y25 ^ y64)) ^ (y64 & (y3 ^ y46))
        hx = x0 ^ (x63 & p) ^ q

        lfsr_0 = lfsr[0]
        lfsr[:-1] = lfsr[1:]
        lfsr[-1] = fx
        nfsr[:-1] = nfsr[1:]
        nfsr[-1] = gx ^ lfsr_0

        keystream_bin += str(hx)

        count+=1

    # convert keystream to hex
    keystream_dec = int(keystream_bin,2)
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