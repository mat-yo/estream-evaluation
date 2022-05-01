import time

# s box
s_box = [
    [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
    [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
    [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
    [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
    [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
    [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
    [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
    [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6],
]

# 32-bit words
word32 = [None]*108

# subkeys
sub_key = [[0]*4 for i in range(0,25)]

# result
data = [0]*4

# state
s = [None]*10
r = [None]*2


# output
f = [None]*4


# get 32 least significant bits
def int32(x):
    return x % pow(2,32)

# left rotate n bits
def rotateLeft(x,n):
    result = int32(x << n) ^ int32(x >> (32-n))
    return result

# s-box application
def apply_sbox(index, temp):
    global s_box

    temp_bin = [None]*32
    result_bin = [""]*4
    result = [None]*4

    j = 0
    for i in temp:
        temp_bin[j] = '{:032b}'.format(i)
        j+=1

    for i in range(0,32):
        # get bitslice
        a = temp_bin[0][i]
        b = temp_bin[1][i]
        c = temp_bin[2][i]
        d = temp_bin[3][i]
        location = int((a+b+c+d),2)

        # get sbox output bits
        sbox_out = s_box[index][location]
        sbox_out_bin = '{:04b}'.format(sbox_out)

        # set corresponding bits
        result_bin[0] += sbox_out_bin[0]
        result_bin[1] += sbox_out_bin[1]
        result_bin[2] += sbox_out_bin[2]
        result_bin[3] += sbox_out_bin[3]

    j = 0
    for i in result_bin:
        result[j] = int(i,2)
        j+=1

    return result

# 1 round of serpend
def serpent1(round):
    global sub_key
    global data

    # subkey addition
    temp = [0]*4
    for i in range(0,4):
        temp[i] = sub_key[round][i] ^ data[i]

    # sbox application
    x = apply_sbox(round%8, temp)

    # linear bijective transformation
    x[0] = rotateLeft(x[0],13)
    x[2] = rotateLeft(x[2],3)
    x[1] = x[1] ^ x[0] ^ x[2]
    x[3] = x[3] ^ x[2] ^ rotateLeft(x[0],3)
    x[1] = rotateLeft(x[1],1)
    x[3] = rotateLeft(x[3],7)
    x[0] = x[0] ^ x[1] ^ x[3]
    x[2] = x[2] ^ x[3] ^ rotateLeft(x[1],7)
    x[0] = rotateLeft(x[0],5)
    x[2] = rotateLeft(x[2],22)

    data = x

# multiplexer
def mux(c,x,y):
    if(c==0):
        return x
    else:
        return y

def trans(z):
    # constant value m
    m_hex = "54655307"
    m = int(m_hex,16)

    temp = m * (z % pow(2,32))
    result = rotateLeft(temp,7)

    return result

# LFSR function
def lfsr():
    global s
    #print()

    old = s

    # alpha
    # xor with most significant bit
    alpha = int32(old[0] << 8) ^ (old[0] >> 24)

    # 1/alpha
    # xor with least significant bit
    alpha_inverse = int32(old[3] >> 8) ^ (old[3] & 254)

    s9 = old[9] ^ alpha_inverse ^ alpha

    # move 1 state ahead
    for i in range(1,10):
        s[i-1] = old[i]

    s[9] = s9

# FSM function
def fsm():
    global r
    global s

    r1_old = r[0]

    # least significant bit
    lsb = '{:032b}'.format(r[0])[-1]
    x = s[1]
    y = s[1] ^ s[8]

    r[0] = (r[1] + mux(lsb,x,y)) % pow(2,32)
    r[1] = trans(r1_old)

    temp = s[9] + (r[0] % pow(2,32))

    f = int32(temp) ^ r[1]

    return f

# key initialization using serpent key schedule
def key_init(K):
    global s_box
    global sub_key
    global word32

    # split key into words
    k = [K[i:i+8] for i in range(0, len(K), 8)]
    
    # little endian
    j = len(k) - 1
    for i in k:
        word32[j] = int(i,16)
        j-=1

    # if key less than 256 bit
    if len(k) < 8:
        for i in range(len(k),8):
            word32[i] = 0

    # create prekeys (100 32-bit words)
    for i in range(8,108):
        temp = word32[i-8] ^ word32[i-5] ^ word32[i-3] ^ word32[i-1] ^ 2654435769 ^ (i-8)
        word32[i] = rotateLeft(temp,11)
    
    # create 25 subkeys from the 100 32-bit words
    for i in range(0,25):
        index =  (24 + 3 - i) % 24
        for k in range(0,24):
            a = ((word32[4*i+0] >> k) & 1) << 0
            b = ((word32[4*i+1] >> k) & 1) << 1
            c = ((word32[4*i+2] >> k) & 1) << 2
            d = ((word32[4*i+3] >> k) & 1) << 3
            s = s_box[index%8][a|b|c|d]

            # each subkeys has 128-bit
            for j in range (0,4):
                temp = ((s >> j) & 1) << k

                sub_key[i][j] = sub_key[i][j] | temp

# iv injection
def iv_init(IV):
    global data
    # split iv into words
    iv_temp = [IV[i:i+8] for i in range(0, len(IV), 8)]
    iv = [0]*4

    # little endian
    j = len(iv_temp) - 1
    for i in iv_temp:
        iv[j] = int(i,16)
        j-=1

    data = iv

    # serpent round 1-12
    for i in range(0,12):
        serpent1(i)

    # store round 12th output
    s[9] = data[0]
    s[8] = data[1]
    s[7] = data[2]
    s[6] = data[3]

    # serpent round 13-18
    for i in range(12,18):
        serpent1(i)

    # store round 18th output
    r[0] = data[0]
    r[1] = data[2]
    s[5] = data[3]
    s[4] = data[1]

    # serpent round 19-24
    for i in range(18,24):
        serpent1(i)

    s[3] = data[0] ^ word32[104]
    s[2] = data[1] ^ word32[105]
    s[1] = data[2] ^ word32[106]
    s[0] = data[3] ^ word32[107]

# sosemanuk initialization
def initialize(K,IV):
    # key schedule
    key_init(K)

    # iv injection
    iv_init(IV)

# generate keystream
def keygen(num):
    count = 0
    z = [0]*4
    key = ""

    while (count<num):
        for i in range(0,4):
            f = fsm()
            lfsr()
            zi = f ^ s[i]
            z[i] = '{:08X}'.format(zi)
            key = key + z[i]
        count+=1

    return key

def encrypt_decrypt(plain_text,display):
    start = time.time()

    # convert plain text to hex
    plainHex = plain_text.encode("utf-8").hex()

    # obtain number of bits required
    size = len(plainHex)
    num = int(size/32)

    # generate keystreamte
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