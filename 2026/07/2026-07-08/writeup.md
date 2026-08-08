# [Let's Poly1305!] Writeup
日付: 2026-07-08 
カテゴリ: Crypto

---

##  問題概要
今日の問題は **crypto**　の問題で、  
**カギのもとを調べてMAC偽造** を達成することがゴールだった。

問題文は公開しないが、与えられた情報は以下のような内容だった：

- rの値は与えられるがsの値はわからない。
- 任意のメッセージを送信でき、メッセージから生成されたMACの値が返ってくる。
- TARGETから作成されたMACの値を入力できるとFlagが返ってくる。

```python
from Crypto.Hash.Poly1305 import Poly1305_MAC

TARGET = b"admin=true"
r, s = token_bytes(16), token_bytes(16)
print(f"HINT! r: {r.hex()}")

message = input("message: ").encode()
print(Poly1305_MAC(r, s, message).hexdigest())

if input("tag: ") == Poly1305_MAC(r, s, TARGET).hexdigest():
    print(FLAG)
```


---

##  解法の方針

### 1. r が公開される
サーバは MAC の鍵の一部である **r をそのまま表示する**。  
Poly1305 は線形構造を持つため、r が分かれば MAC の式を直接扱える。

---
### 2. 任意メッセージの MAC を 1 回取得する
TARGET（admin=true）は送れないが、任意の message を送ると以下の値が返る：


MAC(m) = r `*` acc(m) + s

ここで s は秘密。

---

### 3. Poly1305_MAC(r, 0, m) で r·acc(m) を計算する
以下を使うと、内部の acc(m) を r と掛けた値が得られる

```python
temp_tag = Poly1305_MAC(r, b'\x00'*16, message)
```
---
### 4. s の値を復元する
サーバから返ってきた **MAC(message)** を `num` とし、  
先ほど求めた **r·acc(message)** を `temp_tag` とすると、  
Poly1305 の基本式


MAC(m) = r `*` acc(m) + s


より、s は次のように求められる：


s = MAC(m) - r `*` acc(m)

 
実装では、MAC と temp_tag を整数化して差分を取る

```python
tag_int = int.from_bytes(num, 'little')
temp_tag_int = int.from_bytes(temp_tag, 'little')

s_int = (tag_int - temp_tag_int) % ((1 << 130) - 5)
s = s_int.to_bytes(16, 'little').hex()
```
---
### 5. TARGETに対してsとrを使用してMACの値を求める
復元した **s** と、問題で公開されている **r** を使えば、  
禁止されている TARGET（`admin=true`）の MAC を **正規の計算式どおりに再現できる**。

Poly1305 の MAC は次の式で定義されている：

MAC(m) = r `*` acc(m) + s


つまり、TARGET に対しても同じ式がそのまま使える。

---

###  なぜこれで偽造できるのか？
- acc(TARGET) は Poly1305 の内部処理で自動的に計算される  
- r は公開されている  
- s は前のステップで復元済み  

よって、サーバが本来計算するはずの **MAC(TARGET)** を完全に再現できる。

サーバ側は「MAC が一致するかどうか」しか見ていないため、  
この偽造 MAC を送ると **TARGET の正しい MAC と判断して FLAG を返す**。

---

###  実際の計算コード
```python
fake_tag = Poly1305_MAC(bytes.fromhex(r), bytes.fromhex(s), TARGET).hexdigest()
print(fake_tag)
```

##  実装（自分で書いたコード）

```python
from Crypto.Hash.Poly1305 import Poly1305_MAC

TARGET = b"admin=true"
r = input("r: ")
num = input("mac: ")

message = input("message: ").encode()

num = bytes.fromhex(num)

# r * acc(message) を計算
temp_tag = Poly1305_MAC(bytes.fromhex(r), b'\x00' * 16, message).hexdigest()
temp_tag = bytes.fromhex(temp_tag)

tag_int = int.from_bytes(num, 'little')
temp_tag_int = int.from_bytes(temp_tag, 'little')

# s を復元
s_int = (tag_int - temp_tag_int) % ((1 << 130)-5)
s = s_int.to_bytes(16, 'little').hex()
print(s)

# TARGET の MAC を偽造
print(Poly1305_MAC(bytes.fromhex(r), bytes.fromhex(s), TARGET).hexdigest())
```
