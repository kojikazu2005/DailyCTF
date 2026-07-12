
from secrets import token_bytes
from Crypto.Hash.Poly1305 import Poly1305_MAC
from cryptography.hazmat.primitives.poly1305 import Poly1305


# Poly1305_MAC clamps r internally

TARGET = b"admin=true"
r = input("r: ")
num =input("mac: ")

message = input("message: ").encode()
#num = Poly1305_MAC(r, s, message).hexdigest()
num = bytes.fromhex(num)
#num = int.from_bytes(num) - int.from_bytes(message) * int.from_bytes(bytes.fromhex(r.hex()))
temp_tag = Poly1305_MAC(bytes.fromhex(r), b'\x00' * 16, message).hexdigest()
temp_tag = bytes.fromhex(temp_tag)
tag_int = int.from_bytes(num, 'little')
temp_tag_int = int.from_bytes(temp_tag, 'little')

s_int = (tag_int - temp_tag_int) % ((1 << 130)-5)
s = s_int.to_bytes(16, 'little').hex()
print(s)

print(Poly1305_MAC(bytes.fromhex(r), bytes.fromhex(s), TARGET).hexdigest())
