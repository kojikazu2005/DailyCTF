import os
import random
from base64 import b16encode, b32encode, b64encode

flag = os.environ.get("FLAG", "Alpaca{**** REDACTED ****}").encode()

for i in range(20):
    base = random.choice([16, 32, 64])
    if base == 16:
        flag = b16encode(flag)
    elif base == 32:
        flag = b32encode(flag)
    elif base == 64:
        flag = b64encode(flag)

flag = flag.decode()

print(flag)
