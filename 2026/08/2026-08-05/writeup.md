
# [Happy Birthday] Writeup
日付: 2026-08-05  
カテゴリ: Crypto

---

## 問題概要

userとadminの16進数を入力して、SHA-256の先頭5バイト（40ビット）が一致するとFlagが出力されるプログラムである。
入力された16進数はバイト列に変換され、SHA-256でハッシュ化される。
ハッシュの先頭5バイトの一致以外にもそれぞれ "user=" と "admin="で始まる必要がある。

```python
def H(m):
    return sha256(m).digest()[:5]

a = bytes.fromhex(input("user hex > "))
b = bytes.fromhex(input("admin hex > "))

ok = (
    a != b
    and a.startswith(b"user=")
    and b.startswith(b"admin=")
    and H(a) == H(b)
)

print(FLAG if ok else "nope")
```


---

## 試行錯誤
1, a.startswith()の処理を理解するためにprintデバックを行った。
Cyberchefを用いてどのような入力なら `a.startswith` が Trueになるのか確かめた。
結果、先頭が()の中と一致しているならTrueになることがわかった。

2, user= や admin=を固定して = の後ろに数字を追加して一致するものを順番に調べた。
for文でカウンタを増やしていき、それぞれのハッシュを保存して一致しているのか確かめた。
初めはNの値を100000で実行したが一致しなかったので、Nの値を2000000に増やしてuser側のハッシュ値を辞書に保存してadmin側と比べることで一致しているかどうかを調べた。

``` python
from hashlib import sha256

N = 2_000_000

def H(x):
    return sha256(x).digest()[:5]

seen = {}

for i in range(N):
    a = f"user={i}".encode()
    seen[H(a)] = a

for j in range(N):
    b = f"admin={j}".encode()
    
    h = H(b)

    if h in seen:
        print(seen[h], b, h)
        break
```

実行すると以下のように出力された。
```
b'user=******' b'admin=****' b'\x**\x**\x***'
```
3, 得られた値をcyberchefで16進数に変換して入力するとFlagが得られた。

```
user hex > *****************
admin hex > ***************
Alpaca{DUMMY}
```
## まとめ

当初はSHA-256の先頭5文字が比較されていると思っていたが、
実際には digest()[:5] により先頭5バイト（40ビット）が比較されていた。
そのため、最初に試した N=100000 では衝突が見つからず、N=2000000 まで増やして探索を行った。
また、user側のハッシュ値を辞書に保存することで、効率的に衝突を探索できた。
