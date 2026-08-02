# Poly_MAC2 Writeup
日付: 2026-07-15  
カテゴリ: Crypto 

---

## 問題概要
Poly1305 風の MAC を使った認証付きチャレンジ。

与えられた情報はだいたいこんな構成だった：

- 秘密鍵として 16 バイトの `r`, `s` がランダム生成される
- `HINT! s: ...` が公開される（`s` はそのまま見える）
- ユーザが任意の `message` を送ると  
  `Poly1305_MAC(r, s, message)` が返ってくる
- 最後に `tag:` として  
  `Poly1305_MAC(r, s, TARGET)` を当てると FLAG が出る  
  （`TARGET = b"admin=true"`）

目的は：

> 1 回だけ好きな `message` を投げて得た MAC から  
> 内部の `r` を逆算し、`TARGET` の正しい tag を偽造すること。

---

## 解法方針

### 1. Poly1305 の数式を整理する
PyCryptodome の `Poly1305_MAC(r, s, msg)` はざっくりこういう式になっている：

- `r` は内部で clamp される
- `msg` は 16 バイト以下なら 1 ブロックとして処理される
- ブロック `m` は little-endian で整数化し、末尾に `0x01` を付ける  
  → 実装的には `m_raw + 2^(8 * len(msg))`
- 内部値 `h` は  
  

\[
  h = (m + 2^{8\cdot\text{len(msg)}}) \cdot r \mod (2^{130} - 5)
  \]


- 最終的なタグは  
  

\[
  \text{tag} = (h + s) \mod 2^{128}
  \]



ここから逆算の基本式が決まる。

---

### 2. 1 回の MAC から h を復元する
`message` に対する MAC（tag）が分かっているので、



\[
\text{tag}_m = (h_m + s) \mod 2^{128}
\]



より、



\[
h_m^{\text{low}} = \text{tag}_m - s \mod 2^{128}
\]



ただし Poly1305 の内部値 `h` は 130bit なので、  
上位 2bit が失われている。

そこで、



\[
h_m^{(c)} = h_m^{\text{low}} + c \cdot 2^{128},\quad c \in \{0,1,2,3\}
\]



と 4 通りの候補を総当たりする。

---

### 3. h から r を逆算する
各候補について、



\[
r = h_m^{(c)} \cdot (m + 2^{8\cdot\text{len(msg)}})^{-1} \mod (2^{130} - 5)
\]



を計算することで、clamp 済みの `r` を求めることができる。

---

### 4. 求めた r で TARGET の tag を偽造する
逆算した `r` と公開されている `s` を使って、

```python
Poly1305_MAC(r, s, TARGET)

