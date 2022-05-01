import time

# state variable
x = [None]*8

# counter variable
c = [None]*8

# counter carry bit
carry = 0

# copy of master state
x_copy = [None]*8
c_copy = [None]*8
carry_copy = 0

# aj constants
a = ["4D34D34D",
    "D34D34D3",
    "34D34D34",
    "4D34D34D",
    "D34D34D3",
    "34D34D34",
    "4D34D34D",
    "D34D34D3"]

# calculate g value
def calc_g(j):
    global x
    global c

    # (xij + cij)^2
    num1 = pow((x[j] + c[j]),2)
    num2 = num1 >> 32

    temp = num1 ^ num2
    result = temp % pow(2,32)

    return result

# counter system
def calc_c(j):
    global c
    global a
    global carry

    a_int = int(a[j],16)
    temp = c[j] + a_int + carry
    c[j] = temp % pow(2,32)

    # update carry
    if (temp>pow(2,32)):
        carry = 1
    else:
        carry = 0

# left rotate n bits
def leftRotate(x, n):
    return (x<<n)|(x>>(32-n))

# next state function
def next_state():
    global x

    g = [None]*8

    # calculate new counter variable
    for i in range(0,8):
        calc_c(i)

    # calculate value of g
    for i in range(0,8):
        g[i] = calc_g(i)

    pow32 = pow(2,32)

    # calculate new state variable
    x[0] = (g[0] + leftRotate(g[7],16) + leftRotate(g[6],16)) % pow32
    x[1] = (g[1] + leftRotate(g[0],8) + g[7]) % pow32
    x[2] = (g[2] + leftRotate(g[1],16) + leftRotate(g[0],16)) % pow32
    x[3] = (g[3] + leftRotate(g[2],8) + g[1]) % pow32
    x[4] = (g[4] + leftRotate(g[3],16) + leftRotate(g[2],16)) % pow32
    x[5] = (g[5] + leftRotate(g[4],8) + g[3]) % pow32
    x[6] = (g[6] + leftRotate(g[5],16) + leftRotate(g[4],16)) % pow32
    x[7] = (g[7] + leftRotate(g[6],8) + g[5]) % pow32

# key setup scheme
def key_setup(K):
    global x
    global c

    # convert key from hex to 128-bit binary
    dec = int(K,16)
    k_bin = '{:0128b}'.format(dec)

    # split to 8 subkeys
    k = [k_bin[i:i+16] for i in range(0, len(k_bin), 16)]

    # initialize state variable and counter variable
    for j in range(0,8):
        # even
        if(j%2==0):
            # state variable
            mod = (j+1) % 8
            tempx = k[mod] + k[j]

            # counter variable
            moda = (j+4) % 8
            modb = (j+5) % 8
            tempc = k[moda] + k[modb]

        #odd
        else:
            # state variable
            moda = (j+5) % 8
            modb = (j+4) % 8
            tempx = k[moda] + k[modb]

            #counter variable
            mod = (j+1) % 8
            tempc = k[j] + k[mod]

        x[j] = int(tempx,2)
        c[j] = int(tempc,2)

    # iterate the system 4 times using next state function
    for i in range(0,4):
        next_state()

    # reinitialize counter variable
    for i in range(0,8):
        this_mod = (i+4) % 8
        c[i] = c[i] ^ x[this_mod]

# iv setup scheme
def iv_setup(IV):
    global x
    global c
    global carry
    global x_copy
    global c_copy
    global carry_copy

    # copy the master state
    x_copy = x
    c_copy = c
    carry_copy = carry

    # convert iv from hex to 64-bit binary
    dec = int(IV,16)
    iv_bin = '{:064b}'.format(dec)

    # split to 8 subkeys
    iv = [iv_bin[i:i+16] for i in range(0, len(iv_bin), 16)]

    # iv[0:31]
    str_a = iv[0] + iv[1]

    # iv[32:63]
    str_b = iv[2] + iv[3]

    # iv[48:63] + iv[16:31]
    str_c = iv[3] + iv[1]

    #iv[32:47] + iv[0:15]
    str_d = iv[2] + iv[0]

    c[0] = c[0] ^ int(str_a,2)
    c[1] = c[1] ^ int(str_c,2)
    c[2] = c[2] ^ int(str_b,2)
    c[3] = c[3] ^ int(str_d,2)
    c[4] = c[4] ^ int(str_a,2)
    c[5] = c[5] ^ int(str_c,2)
    c[6] = c[6] ^ int(str_b,2)
    c[7] = c[7] ^ int(str_d,2)

    # iterate 4 times using next state function
    for i in range(0,4):
        next_state()

# initialize Rabbit
def initialize(K,IV):
    # key setup
    key_setup(K)

    # IV setup
    iv_setup(IV)

# generate keystream
def keygen(num):
    global x
    global c
    global carry
    global x_copy
    global c_copy
    global carry_copy

    # use back the master state
    x = x_copy
    c = c_copy
    carry = carry_copy

    s = [None]*8
    keystream = ""

    i = 0
    while (i<=num):
        next_state()

        x0_bin = '{:032b}'.format(x[0])
        x1_bin = '{:032b}'.format(x[1])
        x2_bin = '{:032b}'.format(x[2])
        x3_bin = '{:032b}'.format(x[3])
        x4_bin = '{:032b}'.format(x[4])
        x5_bin = '{:032b}'.format(x[5])
        x6_bin = '{:032b}'.format(x[6])
        x7_bin = '{:032b}'.format(x[7])

        s[0] = int((x0_bin[0:16]),2) ^ int((x5_bin[16:32]),2)
        s[1] = int((x0_bin[16:32]),2) ^ int((x3_bin[0:16]),2)
        s[2] = int((x2_bin[0:16]),2) ^ int((x7_bin[16:32]),2)
        s[3] = int((x2_bin[16:32]),2) ^ int((x5_bin[0:16]),2)
        s[4] = int((x4_bin[0:16]),2) ^ int((x1_bin[16:32]),2)
        s[5] = int((x4_bin[16:32]),2) ^ int((x7_bin[0:16]),2)
        s[6] = int((x6_bin[0:16]),2) ^ int((x3_bin[16:32]),2)
        s[7] = int((x6_bin[16:32]),2) ^ int((x1_bin[0:16]),2)

        for j in s:
            s_hex = '{:04X}'.format(j)
            keystream = keystream + s_hex

        i = i+1
            
    return keystream

def encrypt_decrypt(plain_text,display):
    start = time.time()

    # convert plain text to hex
    plainHex = plain_text.encode("utf-8").hex()

    # obtain number of bits required
    size = len(plainHex)
    num = int(size/32)

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