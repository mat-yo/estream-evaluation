from ciphers import hc128,rabbit,salsa20,sosemanuk,grain_v1,mickey2,trivium,aes128

# key
k_128 = "0F62B5085BAE0154A7FA4DA0F34699EC"
k_80 = "0F62B5085BAE0154A7FA"

# iv
iv_128 = "288FF65DC42B92F960C72E95FC63CA31"
iv_64 = "288FF65DC42B92F9"

# test texts
txt_hc128 = "This is a message for HC-128 encryption!!!"
txt_rabbit = "This is a message for Rabbit encryption!!!"
txt_salsa20 = "This is a message for Salsa20/12 encryption!!!"
txt_sosemanuk = "This is a message for Sosemanuk encryption!!!"
txt_grainv1 = "This is a message for Grain v1 encryption!!!"
txt_mickey2 = "This is a message for Mickey 2.0 encryption!!!"
txt_trivium = "This is a message for Trivium encryption!!!"
txt_aes128 = "This is a message for AES-128 encryption!!!"

# display output
print()
print("Encrypting and decrypting AES-128...")
print()
aes128_a = aes128.encrypt_decrypt(k_128, txt_aes128, True)
print()
print("==================================================")


print()
print("Initializing HC-128...")
hc128.initialize(k_128,iv_128)
print("HC-128 initialized!!!")
print("Encrypting and decrypting HC-128...")
print()
hc128_a = hc128.encrypt_decrypt(txt_hc128, True)
print()
print("==================================================")


print()
print("Initializing Rabbit...")
rabbit.initialize(k_128,iv_64)
print("Rabbit initialized!!!")
print("Encrypting and decrypting Rabbit...")
print()
rabbit_a = rabbit.encrypt_decrypt(txt_rabbit, True)
print()
print("==================================================")

print()
print("Initializing Salsa20/12...")
salsa20.initialize(k_128,iv_64)
print("Salsa20/12 initialized!!!")
print("Encrypting and decrypting Salsa20/12...")
print()
salsa20_a = salsa20.encrypt_decrypt(txt_salsa20, True)
print()
print("==================================================")

print()
print("Initializing Sosemanuk...")
sosemanuk.initialize(k_128,iv_128)
print("Sosemanuk initialized!!!")
print("Encrypting and decrypting Sosemanuk...")
print()
sosemanuk_a = sosemanuk.encrypt_decrypt(txt_sosemanuk, True)
print()
print("==================================================")

print()
print("Initializing Grain v1...")
grain_v1.initialize(k_128,iv_128)
print("Grain v1 initialized!!!")
print("Encrypting and decrypting Grain v1...")
print()
grainv1_a = grain_v1.encrypt_decrypt(txt_grainv1, True)
print()
print("==================================================")

print()
print("Initializing Mickey 2.0...")
mickey2.initialize(k_128,iv_128)
print("Mickey 2.0 initialized!!!")
print("Encrypting and decrypting Mickey 2.0...")
print()
mickey2_a = mickey2.encrypt_decrypt(txt_mickey2, True)
print()
print("==================================================")

print()
print("Initializing Trivium...")
trivium.initialize(k_128,iv_128)
print("Trivium initialized!!!")
print("Encrypting and decrypting Trivium...")
print()
trivium_a = trivium.encrypt_decrypt(txt_trivium, True)
print()
print("==================================================")
