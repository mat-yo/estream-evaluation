from ciphers import hc128,rabbit,salsa20,sosemanuk,grain_v1,mickey2,trivium,aes128

import psutil
import numpy as np
import matplotlib.pyplot as plt

# get size of string
def utf8len(s):
    return len(s.encode('utf-8'))

# key
k_128 = "0F62B5085BAE0154A7FA4DA0F34699EC"
k_80 = "0F62B5085BAE0154A7FA"

# iv
iv_128 = "288FF65DC42B92F960C72E95FC63CA31"
iv_64 = "288FF65DC42B92F9"

# load data
f = open('data/1kb.txt','r')
plain1 = f.read()
f.close()

f = open('data/2kb.txt','r')
plain2 = f.read()
f.close()

f = open('data/4kb.txt','r')
plain4 = f.read()
f.close()

f = open('data/8kb.txt','r')
plain8 = f.read()
f.close()

f = open('data/16kb.txt','r')
plain16 = f.read()
f.close()

print()
# cpu frequency
cpufreq = psutil.cpu_freq().current
freq = cpufreq/1000
print("CPU frequency = %.2f GHz " % freq)

print()
# evaluation
print("Evaluating AES-128...")
aes128_a = aes128.encrypt_decrypt(k_128, plain1, False)
aes128_b = aes128.encrypt_decrypt(k_128, plain2, False)
aes128_c = aes128.encrypt_decrypt(k_128, plain4, False)
aes128_d = aes128.encrypt_decrypt(k_128, plain8, False)
aes128_e = aes128.encrypt_decrypt(k_128, plain16, False)

print("Evaluating HC-128...")
hc128.initialize(k_128,iv_128)
hc128_a = hc128.encrypt_decrypt(plain1, False)
hc128_b = hc128.encrypt_decrypt(plain2, False)
hc128_c = hc128.encrypt_decrypt(plain4, False)
hc128_d = hc128.encrypt_decrypt(plain8, False)
hc128_e = hc128.encrypt_decrypt(plain16, False)

print("Evaluating Rabbit...")
rabbit.initialize(k_128,iv_64)
rabbit_a = rabbit.encrypt_decrypt(plain1, False)
rabbit_b = rabbit.encrypt_decrypt(plain2, False)
rabbit_c = rabbit.encrypt_decrypt(plain4, False)
rabbit_d = rabbit.encrypt_decrypt(plain8, False)
rabbit_e = rabbit.encrypt_decrypt(plain16, False)

print("Evaluating Salsa20/12...")
salsa20.initialize(k_128,iv_64)
salsa20_a = salsa20.encrypt_decrypt(plain1, False)
salsa20_b = salsa20.encrypt_decrypt(plain2, False)
salsa20_c = salsa20.encrypt_decrypt(plain4, False)
salsa20_d = salsa20.encrypt_decrypt(plain8, False)
salsa20_e = salsa20.encrypt_decrypt(plain16, False)

print("Evaluating Sosemanuk...")
sosemanuk.initialize(k_128,iv_128)
sosemanuk_a = sosemanuk.encrypt_decrypt(plain1, False)
sosemanuk_b = sosemanuk.encrypt_decrypt(plain2, False)
sosemanuk_c = sosemanuk.encrypt_decrypt(plain4, False)
sosemanuk_d = sosemanuk.encrypt_decrypt(plain8, False)
sosemanuk_e = sosemanuk.encrypt_decrypt(plain16, False)

print("Evaluating Grain v1...")
grain_v1.initialize(k_80,iv_64)
grain_a = grain_v1.encrypt_decrypt(plain1, False)
grain_b = grain_v1.encrypt_decrypt(plain2, False)
grain_c = grain_v1.encrypt_decrypt(plain4, False)
grain_d = grain_v1.encrypt_decrypt(plain8, False)
grain_e = grain_v1.encrypt_decrypt(plain16, False)

print("Evaluating Mickey 2.0...")
mickey2.initialize(k_80,iv_64)
mickey2_a = mickey2.encrypt_decrypt(plain1, False)
mickey2_b = mickey2.encrypt_decrypt(plain2, False)
mickey2_c = mickey2.encrypt_decrypt(plain4, False)
mickey2_d = mickey2.encrypt_decrypt(plain8, False)
mickey2_e = mickey2.encrypt_decrypt(plain16, False)

print("Evaluating Trivium...")
trivium.initialize(k_80,iv_64)
trivium_a = trivium.encrypt_decrypt(plain1, False)
trivium_b = trivium.encrypt_decrypt(plain2, False)
trivium_c = trivium.encrypt_decrypt(plain4, False)
trivium_d = trivium.encrypt_decrypt(plain8, False)
trivium_e = trivium.encrypt_decrypt(plain16, False)

# calculate the size of data
data_size = utf8len(plain1) + utf8len(plain2) + utf8len(plain4) + utf8len(plain8) + utf8len(plain16)

# (bytes/second) / (cycles/second) = bytes/cycle
# 1 / (bytes/cycle) => cycles/byte
# get byte/second
aes128_total = (float(aes128_a) + float(aes128_b) + float(aes128_c) + float(aes128_d) + float(aes128_e)) / 1000
aes128_bps =  data_size / aes128_total

hc128_total = (float(hc128_a) + float(hc128_b) + float(hc128_c) + float(hc128_d) + float(hc128_e)) / 1000
hc128_bps =  data_size / hc128_total

rabbit_total = (float(rabbit_a) + float(rabbit_b) + float(rabbit_c) + float(rabbit_d) + float(rabbit_e)) / 1000
rabbit_bps =  data_size / rabbit_total

salsa20_total = (float(salsa20_a) + float(salsa20_b) + float(salsa20_c) + float(salsa20_d) + float(salsa20_e)) / 1000
salsa20_bps =  data_size / salsa20_total

sosemanuk_total = (float(sosemanuk_a) + float(sosemanuk_b) + float(sosemanuk_c) + float(sosemanuk_d) + float(sosemanuk_e)) / 1000
sosemanuk_bps =  data_size / sosemanuk_total

grain_total = (float(grain_a) + float(grain_b) + float(grain_c) + float(grain_d) + float(grain_e)) / 1000
grain_bps =  data_size / grain_total

mickey2_total = (float(mickey2_a) + float(mickey2_b) + float(mickey2_c) + float(mickey2_d) + float(mickey2_e)) / 1000
mickey2_bps =  data_size / mickey2_total

trivium_total = (float(trivium_a) + float(trivium_b) + float(trivium_c) + float(trivium_d) + float(trivium_e)) / 1000
trivium_bps =  data_size / trivium_total

# get cycles/second
cps = int(cpufreq * 1000000)

# get cycles/byte
aes128_cpb = 1/(aes128_bps/cps)
hc128_cpb = 1/(hc128_bps/cps)
rabbit_cpb = 1/(rabbit_bps/cps)
salsa20_cpb = 1/(salsa20_bps/cps)
sosemanuk_cpb = 1/(sosemanuk_bps/cps)
grain_cpb = 1/(grain_bps/cps)
mickey2_cpb = 1/(mickey2_bps/cps)
trivium_cpb = 1/(trivium_bps/cps)

txt1  = "1kb  "
txt2  = "2kb  "
txt4  = "4kb  "
txt8  = "8kb  "
txt16 = "16kb "
txtBreak = "============"
print()
print("Cipher \ Time (ms) | %12s | %12s | %12s | %12s | %12s |" % (txt1,txt2,txt4,txt8,txt16))
print("================== | %12s | %12s | %12s | %12s | %12s |" % (txtBreak,txtBreak,txtBreak,txtBreak,txtBreak))
print("           AES-128 | %12s | %12s | %12s | %12s | %12s |" % (aes128_a,aes128_b,aes128_c,aes128_d,aes128_e))
print("            HC-128 | %12s | %12s | %12s | %12s | %12s |" % (hc128_a,hc128_b,hc128_c,hc128_d,hc128_e))
print("            Rabbit | %12s | %12s | %12s | %12s | %12s |" % (rabbit_a,rabbit_b,rabbit_c,rabbit_d,rabbit_e))
print("           Salsa20 | %12s | %12s | %12s | %12s | %12s |" % (salsa20_a,salsa20_b,salsa20_c,salsa20_d,salsa20_e))
print("         Sosemanuk | %12s | %12s | %12s | %12s | %12s |" % (sosemanuk_a,sosemanuk_b,sosemanuk_c,sosemanuk_d,sosemanuk_e))
print("          Grain v1 | %12s | %12s | %12s | %12s | %12s |" % (grain_a,grain_b,grain_c,grain_d,grain_e))
print("        Mickey 2.0 | %12s | %12s | %12s | %12s | %12s |" % (mickey2_a,mickey2_b,mickey2_c,mickey2_d,mickey2_e))
print("           Trivium | %12s | %12s | %12s | %12s | %12s |" % (trivium_a,trivium_b,trivium_c,trivium_d,trivium_e))

print()

print("speed (bytes per second):")
print("    AES-128 = %.2f" % aes128_bps)
print("     HC-128 = %.2f" % hc128_bps)
print("     Rabbit = %.2f" % rabbit_bps)
print("    Salsa20 = %.2f" % salsa20_bps)
print("  Sosemanuk = %.2f" % sosemanuk_bps)
print("   Grain v1 = %.2f" % grain_bps)
print(" Mickey 2.0 = %.2f" % mickey2_bps)
print("    Trivium = %.2f" % trivium_bps)

print()

print("speed (cycles per byte):")
print("    AES-128 = %.2f" % aes128_cpb)
print("     HC-128 = %.2f" % hc128_cpb)
print("     Rabbit = %.2f" % rabbit_cpb)
print("    Salsa20 = %.2f" % salsa20_cpb)
print("  Sosemanuk = %.2f" % sosemanuk_cpb)
print("   Grain v1 = %.2f" % grain_cpb)
print(" Mickey 2.0 = %.2f" % mickey2_cpb)
print("    Trivium = %.2f" % trivium_cpb)

print()

# x values
x = [1,2,4,8,16]

# y values
y_aes128 = [float(aes128_a), float(aes128_b), float(aes128_c), float(aes128_d), float(aes128_e)]
y_hc128 = [float(hc128_a), float(hc128_b), float(hc128_c), float(hc128_d), float(hc128_e)]
y_rabbit = [float(rabbit_a), float(rabbit_b), float(rabbit_c), float(rabbit_d), float(rabbit_e)]
y_salsa20 = [float(salsa20_a), float(salsa20_b), float(salsa20_c), float(salsa20_d), float(salsa20_e)]
y_sosemanuk = [float(sosemanuk_a), float(sosemanuk_b), float(sosemanuk_c), float(sosemanuk_d), float(sosemanuk_e)]
y_grain = [float(grain_a), float(grain_b), float(grain_c), float(grain_d), float(grain_e)]
y_mickey2 = [float(mickey2_a), float(mickey2_b), float(mickey2_c), float(mickey2_d), float(mickey2_e)]
y_trivium = [float(trivium_a), float(trivium_b), float(trivium_c), float(trivium_d), float(trivium_e)]

# lines
plt.plot(x, y_aes128, label = "AES-128")
plt.plot(x, y_hc128, label = "HC-128")
plt.plot(x, y_rabbit, label = "Rabbit")
plt.plot(x, y_salsa20, label = "Salsa20/12")
plt.plot(x, y_sosemanuk, label = "Sosemanuk")
plt.plot(x, y_grain, label = "Grain v1")
plt.plot(x, y_mickey2, label = "Mickey 2.0")
plt.plot(x, y_trivium, label = "Trivium")

# draw line graph
plt.xlabel('file size (kb)', fontweight ='bold', fontsize = 12)
plt.ylabel('time (ms)', fontweight ='bold', fontsize = 12)
plt.title('Time taken to encrypt and decrypt', fontweight ='bold', fontsize = 15)
plt.legend()
plt.show()

barWidth = 0.1
fig = plt.subplots(figsize =(12, 8))

br1 = np.arange(len(y_aes128))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]
br6 = [x + barWidth for x in br5]
br7 = [x + barWidth for x in br6]
br8 = [x + barWidth for x in br7]

plt.bar(br1, y_aes128, width = barWidth, label ='AES-128')
plt.bar(br2, y_hc128, width = barWidth, label ='HC-128')
plt.bar(br3, y_rabbit, width = barWidth, label ='Rabbit')
plt.bar(br4, y_salsa20, width = barWidth, label ='Salsa20/12')
plt.bar(br5, y_sosemanuk, width = barWidth, label ='Sosemanuk')
plt.bar(br6, y_grain, width = barWidth, label ='Grain v1')
plt.bar(br7, y_mickey2, width = barWidth, label ='Mickey 2.0')
plt.bar(br8, y_trivium, width = barWidth, label ='Triium')

# bar graph
plt.xlabel('File Size', fontweight ='bold', fontsize = 12)
plt.ylabel('Time (ms)', fontweight ='bold', fontsize = 12)
plt.xticks(
    [r + barWidth*3.5 for r in range(len(y_aes128))],
    ['1kb', '2kb', '4kb', '8kb', '16kb']
)
plt.title('Time taken to encrypt and decrypt', fontweight ='bold', fontsize = 15)
plt.legend()
plt.show()
