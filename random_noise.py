import random
import numpy as np
from noise import pnoise1


seed = 

for i in range(20):
    x = seed + i * .3
    noise = pnoise1(x)
    if (noise > -1 and
        noise < -0.1):
        adjusted_noise = -1
    elif (noise > -0.1 and
        noise < 0.1):
        adjusted_noise = 0
    elif (noise > 0.1 and
          noise < 1):
        adjusted_noise = 1
    else:
        print("ERROR")
        exit()
    print(f"NOISE BEFFORE: {noise}")
    print(f"NOISE AFTER: {adjusted_noise} \n")





# output = []
# patches = []

# random.seed()

# normal = np.random.normal(size = 1)
# print(normal)
# for i in range (0, 4):
#     output.append(0)
# for i in range(5,15):
#     output.append(random.randint(1,5))
# # for i in range(len(output) - 1):
# #     output[i] = min(output[i], output[i+1])
    

# print(output)