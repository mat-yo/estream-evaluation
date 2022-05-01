from Crypto.Cipher import AES
import time

K = "0F62B5085BAE0154A7FA4DA0F34699EC"

# aes128 encryption
def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('ascii'))

    return nonce, ciphertext, tag

# aes128 decryption
def decrypt(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False

def encrypt_decrypt(k, plain_text, display):
    start = time.time()

    key = bytes.fromhex(k)
    nonce, ciphertext, tag = encrypt(key,plain_text)
    cipherHex = ciphertext.hex()
    recover_text = decrypt(key, nonce, ciphertext, tag)

    end = time.time()

    # get time to encrypt and decrypt (ms)
    time_used = (end - start) * 1000
    result = format(time_used, '.5f')


    if (display):
        print("plain text    : " + plain_text)
        print("cipher text   : " + cipherHex.upper())
        print("recovered text: " + recover_text)

    return result