from pwn import *

charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"

r = remote("34.170.146.252", 57189)
r.recvuntil(b"ciphertext(hex): ")
flag = b"FLAG IS:Alpaca{"
target_ct = r.recvline().strip().decode()
target_block = target_ct[:32]

for c in charset:
    pt = flag + bytes([c])
    r.recvuntil(b"plaintext to encrypt (hex): ")
    r.sendline(pt.hex().encode())
    r.recvuntil(b"ciphertext(hex): ")
    ct = r.recvline().strip().decode()
    if ct[:32] == target_block:
        print("FOUND:", chr(c))
        break
""" 
[+] Opening connection to 34.170.146.252 on port 57189: Done
 
FOUND: A
[*] Closed connection to 34.170.146.252 port 57189"""
