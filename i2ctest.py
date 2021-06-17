from smbus import SMBus
import time

i2c = SMBus(1)
count = 0
while True:
    L = i2c.read_i2c_block_data(0x44, 0x03, 6)
    print(count, L)
    if L[0] != 0:
        break
    count += 1

# we learned:
# i2c first byte reads as 128 sometimes, though arduino sends a 0
# happens after 1000+ transactions (not deterministic), even with a delay bw transactions

# if we ask for more bytes than the arduino sends back, everything else reads as 255
