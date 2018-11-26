from bibliopixel import builder

b = builder.Builder('jumbo-12k.yml', threaded=True)
b.start(True)
# print(b.is_running)

b.pixel[0, 0] = 'blue'
b.pixel[1, 0] = 'green'
b.pixel[0, 1] = 'white'
b.pixel[1, 1] = 'yellow'

import time
time.sleep(10)

colors = 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'black'

for y in range(96):
    # print(y)
    for x in range(128):
        b.pixel[x, y] = colors[x % 8]
        if x % 32:
            time.sleep(0.01)
