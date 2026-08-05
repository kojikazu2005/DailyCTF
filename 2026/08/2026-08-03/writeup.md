
# [Long Long Flag Printer 2026] Writeup
日付: 2026-08-03  
カテゴリ: Misc

---

## 問題概要

Long Long Flag Printer 2026 は、フラグを1文字ずつ出力するサービスである。

配布された `server.py` を見ると、フラグの各文字を出力した後に `sleep` を実行していることが分かる。フラグ長は 1024 文字に設定されており、素直に最後まで待つと非常に長い時間がかかる。 

```python
import os
flag = "Alpaca{*** 省略 ***}"
assert len(flag) == 1024

for i, c in enumerate(flag):
    print(c, end="", flush=True)
    os.system(f"sleep {i}")
```

Dockerfile は以下のようになっていた。 

```dockerfile
FROM python:3.14.6-slim-trixie
WORKDIR /app
RUN apt-get update && apt-get install -yq socat
COPY server.py .

CMD ["socat", "-T5", "tcp-listen:1337,fork,reuseaddr", "exec:'python server.py'"]
```

`socat -T5` が指定されているため、5秒間通信がないと接続が切断される。

---

## 試行錯誤

最初に接続したところ、

```text
Alpaca{
```

まで表示された後に切断された。

コードを確認すると、

```
os.system(f"sleep {i}")
```

i 番目の文字列の後は i 秒待機という挙動になっている。 
そのため `{` が表示された後は 6 秒間待機することになり、5秒間送受信が止まってしまうことにより接続が切断されてしまう。

当初は以下のような方向で考察した。

- 定期的にデータを送信してタイムアウトを回避する
- 別の情報漏洩が存在する
- `socat` の設定を悪用する

しかし接続を維持できたとしても、

```python
sleep 0
sleep 1
sleep 2
...
sleep 1023
```

をすべて待つ必要がある。

待機時間は

\[
0 + 1 + 2 + \cdots + 1023
=
523776
\]

秒となり、およそ 6 日かかる。 

したがって単純な接続維持だけでは解決にならない。

その他にもos.systemを使用しているのでOSコマンドインジェクションなどを試したが、入力を受け付けていないためダメだった。
sleepを回避する方法としてCtrl-Cがあることはわかったが、OSコマンドと同様にシグナルを送ることができないと考え答えには辿り着くことはできなかった。

---

## 解法

最終的には他の Writeup を参考にして解法を理解した。

ポイントは

```python
os.system(f"sleep {i}")
```

の部分である。 

`sleep` 実行中に Ctrl-C を送ることで、`sleep` を中断できる。
自身はシグナルを送れないと考えていた。

Ctrl-C は ASCII では

```python
b"\x03"
```

で表現できる。

Pwntools では別スレッドで継続的に `0x03` を送り続けることで、各 `sleep` を強制終了させられる。

```python
from pwn import *

p = remote("34.170.146.252", 21066)

while True:
    try:
        d = p.recv(1, timeout=3)
        p.send(b"\x03")

        if d:
            print(d.decode(), end="", flush=True)
        else:
            p.send(b"a")

    except EOFError:
        print("\nEOF")
        break
```

処理の流れは以下の通り。

```text
文字出力
↓
sleep実行
↓
Ctrl-C送信
↓
sleep中断
↓
次の文字出力
```

本来であれば数日かかる出力を、一瞬で取得できるようになる。

---

## なぜ効くのか

通常は Ctrl-C を送ってもローカル側のプログラムが終了するだけという印象がある。

しかしこの問題では `socat` 経由で実行された `python server.py` が制御文字を受け取り、結果として実行中の`sleep` が中断される。

そのため

```python
os.system("sleep 100")
```

のような長時間の待機も即座に終了し、フラグの出力が継続される。

---

## 学んだこと

この問題の本質は単純なタイムアウト回避ではなく、

- `socat -T5` による接続切断
- `os.system("sleep")` による遅延
- Ctrl-C（SIGINT）による中断

を組み合わせて考えることだった。
また、自分は　PTY が無いのでシグナルは届かないだろうと決めつけてしまい、この発想に辿り着けなかった。
サービスの構成を見て可能性を早い段階で切り捨てるのではなく、実際に試してみることの重要性を学べた問題だった。
