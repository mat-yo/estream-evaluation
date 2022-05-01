import time

# 2 tables with 512 32-bit elements
P = [None]*512
Q = [None]*512

# convert hexadecimal to binary
def hex_to_bin(hex):
    # convert hex to decimal
    dec = int(hex,16)

    # convert decimal to 128-bit binary
    binary = '{:0128b}'.format(dec)
    
    return binary

# get 32 least significant bits
def int32(x):
    return x % pow(2,32)

# get mod 512
def mod512(x):
    return x%512

# right rotate n bits
def rotateRight(x,n):
    result = int32(x >> n) ^ int32(x << (32-n))
    return result

# left rotate n bits
def rotateLeft(x,n):
    result = int32(x << n) ^ int32(x >> (32-n))
    return result
    
# f(1) function
def f1(x):
    result = rotateRight(x,7) ^ rotateRight(x,18) ^ (x>>3)
    return result

# f(2) function
def f2(x):
    result = rotateRight(x,17) ^ rotateRight(x,19) ^ (x>>10)
    return result

# g(1) function
def g1(x,y,z):
    result = int32((rotateRight(x,10) ^ rotateRight(z,23)) + rotateRight(y,8))
    return result

# g(2) function
def g2(x,y,z):
    result = int32((rotateLeft(x,10) ^ rotateLeft(z,23)) + rotateLeft(y,8))
    return result

# h1 function
def h1(x):
    binary = '{:032b}'.format(x)

    # split binary to 4 bytes
    arr = [binary[i:i+8] for i in range(0, len(binary), 8)]
    
    n0 = int(arr[0],2)
    n2 = int(arr[2],2)

    result = int32(Q[n0] + Q[256 + n2])

    return result

# h2 function
def h2(x):
    binary = '{:032b}'.format(x)

    # split binary to 4 bytes
    arr = [binary[i:i+8] for i in range(0, len(binary), 8)]
    
    n0 = int(arr[0],2)
    n2 = int(arr[2],2)

    result = int32(P[n0] + P[256 + n2])

    return result

# hc-128 initialization process
def initialize(K,IV):
    global P
    global Q

    #convert key and iv form hex to binary
    k_bin = hex_to_bin(K)
    iv_bin = hex_to_bin(IV)

    # split to 4 32-bit number
    k = [k_bin[i:i+32] for i in range(0, len(k_bin), 32)]
    iv = [iv_bin[i:i+32] for i in range(0, len(iv_bin), 32)]

    # initialize array w
    W = [None] * 1280

    # W[i] = K[i] where 0<=i<=7
    for i in range(0,8):
        mod = i%4
        W[i] = int(k[mod])

    # W[i] = IV[i] where 8<=i<=15
    for i in range(8,16):
        mod = i%4
        W[i] = int(iv[mod])
    
    for i in range(16,1280):
        W[i] = int32(f2(W[i-2]) + W[i-7] + f1(W[i-15]) + W[i-16] + i)
    
    # update table P and Q
    for i in range(0,512):
        P[i] = W[i+256]
        Q[i] = W[i+768]

    for i in range(0,512):
        P[i] = int32(P[i] + g1(P[mod512(i-3)], P[mod512(i-10)], P[mod512(i-511)]) ^ h1(P[mod512(i-12)]))
    for i in range(0,512):
        Q[i] = int32(Q[i] + g2(Q[mod512(i-3)], Q[mod512(i-10)], Q[mod512(i-511)]) ^ h2(Q[mod512(i-12)]))

# generate keystream
def keygen(num):
    global P
    global Q

    keystream = ""

    count = 0
    while (count<=num):
        j = mod512(count)
        key_int = None
        
        if (count % 1024) < 512:
            P[j] = int32(P[j] + g1(P[mod512(j-3)], P[mod512(j-10)], P[mod512(j-511)]))
            key_int = h1(P[mod512(j-12)]) ^ P[j]
        else:
            Q[j] = int32(Q[j] + g2(Q[mod512(j-3)], Q[mod512(j-10)], Q[mod512(j-511)]))
            key_int = h2(Q[mod512(j-12)]) ^ Q[j]
        
        # append keystream
        key_hex = '{:08X}'.format(key_int)
        keystream += key_hex

        count += 1

    return keystream

def encrypt_decrypt(plain_text,display):
    start = time.time()

    # convert plain text to hex
    plainHex = plain_text.encode("utf-8").hex()

    # obtain number of bits required
    size = len(plainHex)
    num = int(size/8)

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