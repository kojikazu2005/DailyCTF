
# [AESAESAESAESAESAES] Writeup
日付: 2026-08-06  
カテゴリ: Crypto

---

## 問題概要
ncコマンドで接続を行うと、AESのCBCモードの初期ベクトルが与えられる。
また、Flagの先頭に**"FLAG IS:"**を付与した文字列を16回繰り返した平文の暗号文が与えられる。
- Flagの長さは31ということがわかっており、Flagは`Alpaca{`から始まり、`}`で終わる。
- Flagに使用されている文字列は`"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"`のみである。

さらに、その後は16進数で**16 bytes **の入力が可能で、同じ初期ベクトルで暗号化した暗号文が返ってくる。

```python
msg = b"FLAG IS:" + flag
msg_16 = msg * 16

ciphertext = cipher.encrypt(msg_16)
print(f"iv(hex): {cipher.iv.hex()}")
print(f"ciphertext(hex): {ciphertext.hex()}")

while True:
    user_input = bytes.fromhex(input("plaintext to encrypt (hex): "))

    if len(user_input) != 16:
        print("Input must be 16 bytes (32 hex characters).")
        continue

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(user_input)
    print(f"iv(hex): {cipher.iv.hex()}")
    print(f"ciphertext(hex): {ciphertext.hex()}")
```


---

## 試行錯誤
1, さまざまな平文を入力して平文と暗号文から鍵を予測しようとした。
- 総当たりやランダムで試してみたが、鍵の情報は得ることができなかった。
- さまざまな復号化ツールや解析ツールを探したが、見つからなかった。
- 調べてみるとAESの特徴から、鍵の予測は不可能だと知り断念。

2, 1ブロック目は「既知15文字＋未知1文字」であると考えた。
AESのブロックサイズは16 bytesである。
FLAG IS:Alpaca{ の長さは15 bytesであるため、1ブロック目は
 `FLAG IS:Alpaca{? `
の形になる。
未知なのは最後の1 byteのみなので、55通りの総当たりで求められると考えた。
16 bytes目だけを変更して、総当たりで入力を行い、ciphertext(hex)の初めの16 bytesが一致するか調べた。
Flagの先頭1文字が分かった。

```python
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
```

3, 2ブロック目も総当たりで調べようとした。
2ブロック目は16文字すべてが未知である。
使用可能文字数は55種類なので、
`55 ** 16`
通り存在する。これは約`7.0 × 10^27`通りとなり、現実的な時間では総当たり不可能だった。

4, msg `*` 16 に注目した。
通常であれば1回暗号化すれば十分である。
そのため、
`msg * 16`
という処理には何らかの意図があると考えた。
平文の長さは`"FLAG IS:"` + Flag(31bytes) = 39 bytesでブロックのサイズと異なるのでそれぞれのブロックごとの平文は異なるのではないかと考えた。

5, それぞれのブロックの開始位置を調べた。
何番目のブロックは平文の何bytes目から始まっているのかを調べた。

```python
while True:
    print(row, " :",count)
    count += 16
    now += 16
    row +=1 #行数を加算
    if now > max:#msg * 16の長さまで調べる
        break
    if count > 39:#msgの長さを超えた場合
        count = count % 39
```
プログラム実行結果をみると、ブロック開始位置は
`(16 * n) % 39`
で変化していた。
39 と 16 は互いに素であるため、最終的に平文中のすべての位置がブロック先頭として現れることが分かった。
下記の実行結果から1行目は平文の0番目から始まっていて、2行目は16番目、3行目は32番目から始まっていることが読み取れる。

```
1  : 0
2  : 16
3  : 32
4  : 9
5  : 25
6  : 2
7  : 18
8  : 34
```
6, CBCの暗号モードについて
CBCモードでは、

```
C1 = E(P1 ⊕ IV)

Ci = E(Pi ⊕ C(i-1))
```
となる。
一方、今回のプログラムは常に
`E(X ⊕ IV)`
を計算してくれる。
そこで、
```
X ⊕ IV = Pi ⊕ C(i-1)
```
となるように
```
X = Pi ⊕ C(i-1) ⊕ IV
```
を入力する。すると、

```
E(X ⊕ IV)
=
E(Pi ⊕ C(i-1))
=
Ci
```
となり、対象ブロックの暗号文を再現できる。

7,「既知15文字＋未知1文字」を探した
ブロック開始位置がずれていくため、`LAG IS:Alpaca{A?`のような「既知15文字＋未知1文字」のブロックが現れる。
このブロックを対象にすれば、再び55通りの総当たりで未知文字を求められる。
未知の1文字を調べることができると、1文字ずらし、次の未知の1文字を探すことを繰り返す。

```python
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
```

## まとめ
AESの鍵そのものを推測することは現実的に不可能だった。
また、ブロックのbytes列の総当たりも16bytesであり、総当たりは現実的ではなかった。
msg * 16 によってブロック境界がずれていることに着目した。
その結果、「既知15文字＋未知1文字」になるブロックを探し出し、CBC の性質を利用して対象ブロックを再現することで、1文字ずつ Flag を復元できた。
この問題の本質は AES の解読ではなく、固定 IV の CBC 暗号化オラクルと、39 bytes 周期で繰り返される平文によるブロック境界のずれを利用し、未知文字を1文字ずつ回収することであった。
