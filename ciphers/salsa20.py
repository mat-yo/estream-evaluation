import time

# key
k = [None]*8

# nonce
n = [None]*2

# block counter 
count = 0
bc = [None]*2

# state
s = [None]*16

# convert to little-endian format
def littleendian(hex):
    b = [None]*4

    b[0] = int(hex[0:2],16)
    b[1] = int(hex[2:4],16)
    b[2] = int(hex[4:6],16)
    b[3] = int(hex[6:8],16)

    result = b[0] + pow(2,8)*b[1] + pow(2,16)*b[2] + pow(2,24)*b[3]

    return result

# block counter
def block_counter():
    global count
    global bc

    count_hex = '{:016X}'.format(count)
    temp = [count_hex[i:i+8] for i in range(0, len(count_hex), 8)]

    hex_str = ""

    for i in range(0,2):
        bc[i] = littleendian(temp[i])
        bc_hex = '{:08X}'.format(bc[i])
        hex_str = hex_str + bc_hex
    
    count = (int(hex_str,16) + 1) % pow(2,64)

# left rotate n bits
def leftRotate(x, n):
    return (x<<n)|(x>>(32-n))

# quarter round function
def quarter_round(y):
    z = [None]*4

    c = (y[0]+y[3]) % pow(2,32)
    d = (y[0]+y[3]) % pow(2,32)
    
    a = (y[0]+y[3]) % pow(2,32)
    z[1] = (y[1] ^ leftRotate(a, 7)) % pow(2,32)

    
    b = (z[1]+y[0]) % pow(2,32)
    z[2] = (y[2] ^ leftRotate(b, 9)) % pow(2,32)

    c = (z[2]+z[1]) % pow(2,32)
    z[3] = (y[3] ^ leftRotate(c, 13)) % pow(2,32)

    d = (z[3]+z[2]) % pow(2,32)
    z[0] = (y[0] ^ leftRotate(d, 18)) % pow(2,32)

    return z

# column round function
def column_round():
    global s

    col1 = [s[0],s[4],s[8],s[12]]
    col2 = [s[5],s[9],s[13],s[1]]
    col3 = [s[10],s[14],s[2],s[6]]
    col4 = [s[15],s[3],s[7],s[11]]

    new_col1 = quarter_round(col1)
    new_col2 = quarter_round(col2)
    new_col3 = quarter_round(col3)
    new_col4 = quarter_round(col4)

    s[0] = new_col1[0]
    s[4] = new_col1[1]
    s[8] = new_col1[2]
    s[12] = new_col1[3]

    s[5] = new_col2[0]
    s[9] = new_col2[1]
    s[13] = new_col2[2]
    s[1] = new_col2[3]

    s[10] = new_col3[0]
    s[14] = new_col3[1]
    s[2] = new_col3[2]
    s[6] = new_col3[3]

    s[15] = new_col4[0]
    s[3] = new_col4[1]
    s[7] = new_col4[2]
    s[11] = new_col4[3]

# row round function
def row_round():
    row1 = [s[0],s[1],s[2],s[3]]
    row2 = [s[4],s[5],s[6],s[7]]
    row3 = [s[8],s[9],s[10],s[11]]
    row4 = [s[12],s[13],s[14],s[15]]

    new_row1 = quarter_round(row1)
    new_row2 = quarter_round(row2)
    new_row3 = quarter_round(row3)
    new_row4 = quarter_round(row4)

    s[0] = new_row1[0]
    s[1] = new_row1[1]
    s[2] = new_row1[2]
    s[3] = new_row1[3]

    s[4] = new_row2[0]
    s[6] = new_row2[1]
    s[7] = new_row2[2]
    s[3] = new_row2[3]

    s[8] = new_row3[0]
    s[9] = new_row3[1]
    s[10] = new_row3[2]
    s[11] = new_row3[3]

    s[12] = new_row4[0]
    s[13] = new_row4[1]
    s[14] = new_row4[2]
    s[15] = new_row4[3]

# double round function
def double_round():
    column_round()
    row_round()

# expand key to 64 byte
def key_setup(K):
    global k

    # 64-byte key
    if(len(K)==64):
        temp = [K[i:i+8] for i in range(0, len(K), 8)]

        for i in range(0,8):
            k[i] = littleendian(temp[i])
    # 32-byte key
    elif (len(K)==32):
        temp = [K[i:i+8] for i in range(0, len(K), 8)]

        for i in range(0,8):
            mod = i % 4
            k[i] = littleendian(temp[mod])
    
def iv_setup(IV):
    global n

    temp = [IV[i:i+8] for i in range(0, len(IV), 8)]

    for i in range(0,2):
        n[i] = littleendian(temp[i])

# expansion function
def initialize(K,IV):
    # expand key
    key_setup(K)

    # expand nonce/iv
    iv_setup(IV)

    # block counter
    block_counter()

# generate keystream
def keygen(size):
    global s
    global k
    global n
    global bc

    # define constant
    c_hex = ["61707865", "3320646e", "79622d32", "6b206574"]
    c = [0]*4
    j = 0
    for i in c_hex:
        c_int = int(i,16)
        c[j] = c_int
        j = j+1

    keystream = ""
    tempkey = ""

    s = [
        c[0],c[1],c[2],c[3],
        k[0],k[1],k[2],k[3],
        k[4],k[5],k[6],k[7],
        bc[0],bc[1],n[0],n[1]
    ]

    round = 20

    num = int(size/64)
    count = 0

    # generate enough keystream bytes
    while (count<=num):
        # number of double rounds required
        num_double = int(round/2)

        for i in range(0,num_double):
            double_round()

        for i in s:
            hex_str = '{:08X}'.format(i)
            tempkey += hex_str

        count += 1

    keystream = tempkey[:size]
    return keystream

def encrypt_decrypt(plain_text, display):
    start = time.time()

    # convert plain text to hex
    plainHex = plain_text.encode("utf-8").hex()

    # obtain number of bytes required
    size = len(plainHex)
    
    # generate keystream
    keystream = keygen(size)
    
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