# [lazy-rsa] Writeup
日付: 2026-07-07 
カテゴリ: [Crypto]

---

##  問題概要
今日の問題は [crypto] の問題で、  
[RSAをデコードして平文を入手] を達成することがゴールだった。

問題文は公開しないが、与えられた情報は以下のような内容だった：

- [RSA の公開鍵の元となる素数p, qはgetPrime(512)で 与えられる]
- [RSA の鍵の値 n, また、e = 65537]
- [暗号文 c]
- [特殊なヒント hint = 12345*p + 6789*q ]

---

##  解法の方針
この問題は以下の観点から攻略した：

1. **[ヒントを利用する]**  
   - hint = 12345*p + 6789*qからpまたはqの素数を求める
   - p * q = nの値が出力させているので、鍵の元の素数がわかる。
   - 鍵の元が分かれば、平文がわかる。

2. **[デコードする]**  
   - phi = (p-1)*(q-1)を計算
   - d = e^-1mod(phi)を計算
   - 平文 = c^dmod(N)を計算



##  実装（自分で書いたコード）
今回使用したコードの抜粋：

```python
# 変数
p, q = symbols('p q', integer=True)

# 連立方程式
eq1 = Eq(p*q, n)
eq2 = Eq(a*p + b*q, hint)

# 解く
sol = solve((eq1, eq2), (p, q))
for P, Q in sol:
    if P > 0 and n % P == 0:#解が二つ返すことがあるので、nを約数に持っている方を採用する
        p, q = P, Q
        break
        
phi = (p-1)*(q-1)
d = pow(e, -1, int(phi))
answer = long_to_bytes(pow(c, d, n))
print(f"answer = {answer}")
```


