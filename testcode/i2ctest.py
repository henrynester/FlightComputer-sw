from smbus import SMBus
import time

i2c = SMBus(1)
while True:
    t0 = time.time()
    L = None
    # try:
    L = i2c.read_i2c_block_data(0x44, 0x02, 6)
    # except OSError:
    # print('err')
    print(time.time()-t0, L)
    time.sleep(0.001)

# we learned:
# i2c first byte reads as 128 sometimes, though arduino sends a 0
# happens after 1000+ transactions (not deterministic), even with a delay bw transactions

# if we ask for more bytes than the arduino sends back, everything else reads as 255
