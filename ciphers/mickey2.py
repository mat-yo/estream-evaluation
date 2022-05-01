import time

# initialize register to all 0
r =  [0]*100
s =  [0]*100

# clock register r
def clock_r(input_r, ctrl_r):
    global r

    rtaps = [
        0,1,3,4,5,6,9,12,13,16,19,20,21,22,25,28,37,38,41,42,45,46,50,52,54,56,58,
        60,61,63,64,65,66,67,71,72,79,80,81,82,87,88,89,90,91,92,94,95,96,97
    ]

    old_r = r

    feedback =  old_r[99] ^ input_r

    # 1<=i<=99
    for i in range(1,100):
        r[i] = old_r[i-1]
    r[0] = 0

    # 1<=i<=99
    for i in range(0,100):
        if i in rtaps:
            r[i] = r[i] ^ feedback

    if (ctrl_r == 1):
        for i in range(0,100):
            r[i] = r[i] ^ old_r[i]

# clock register s
def clock_s(input_s, ctrl_s):
    global s

    comp0 = [
        None, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0,
        0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1,
        0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, None
    ]

    comp1 = [
        None, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1,
        0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1,
        0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1,
        1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, None
    ]

    fb0 = [
        1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1,
        0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0
    ]

    fb1 = [
        1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0,
        0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0,
        0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1,
        0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1
    ]

    old_s = s
    s_intermediate = [0]*100

    feedback = s[99] ^ input_s

    # 1<=i<=98
    for i in range(1,98):
        s_intermediate[i] = old_s[i-1] ^ ((old_s[i] ^ comp0[i]) & (old_s[i+1] ^ comp1[i]))
    s_intermediate[0] = 0
    s_intermediate[99] = old_s[98]

    if (ctrl_s == 0):
        for i in range(0,100):
            s[i] = s_intermediate[i] ^ (fb0[i] & feedback)
    else:
        for i in range(0,100):
            s[i] = s_intermediate[i] ^ (fb1[i] & feedback)

# clock overall generator
def clock_kg(mixing, input):
    global r
    global s

    ctrl_r = s[34] ^ r[67]
    ctrl_s = s[67] ^ r[33]

    if (mixing):
        input_r = input ^ s[50]
    else:
        input_r = input

    input_s = input

    clock_r(input_r, ctrl_r)
    clock_s(input_s, ctrl_s)

# initialize mickey 2.0
def initialize(K, IV):
    global r
    global s

    k_dec = int(K,16)
    k_bin = '{:080b}'.format(k_dec)
    iv_dec = int(IV,16)
    iv_bin = '{:b}'.format(iv_dec)

    # load iv
    count = len(iv_bin) - 1
    for i in range(0,count):
        clock_kg(True, int(iv_bin[i]))

    # load k
    for i in range(0,80):
        clock_kg(True, int(k_bin[i]))

    # preclock
    for i in range (0,100):
        clock_kg(True, 0)

# generate keystream
def keygen(num):
    global r
    global s

    keystream_bin = ""

    count = 0
    while (count<num):
        keystream_bin += str(r[0] ^ s[0])
        clock_kg(False, 0)
        count += 1

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