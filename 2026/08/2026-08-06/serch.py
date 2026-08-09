from pwn import *

charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"

r = remote("34.170.146.252", 57189)

r.recvuntil(b"iv(hex): ")
iv = bytes.fromhex(r.recvline().strip().decode())

r.recvuntil(b"ciphertext(hex): ")
target_ct = r.recvline().strip().decode()
count = 39#ここ変える
# C
target_block = target_ct[32*(count-1):32*count]

# Cbefore
c_before = bytes.fromhex(target_ct[32*(count-2):32*(count-1)])

known = b"lenge_is_puzzle"#ここも変える

for c in charset:

    guess = known + bytes([c])

    pt = xor(guess, c_before, iv)

    r.recvuntil(b"plaintext to encrypt (hex): ")
    r.sendline(pt.hex().encode())

    r.recvuntil(b"ciphertext(hex): ")
    ct = r.recvline().strip().decode()

    if ct[:32] == target_block:
        print("FOUND:", chr(c))
        break

r.close()
"""print(len(guess), guess)
print(target_block)
print(ct[:32])"""
