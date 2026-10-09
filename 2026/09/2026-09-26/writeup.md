
# [typhoon-pythoon] Writeup
日付: 2026-09-26  
カテゴリ: rev

---

## 問題概要
台風がプログラムを遠くへ飛ばしてしまいました。 どうやらフラグは台風の目の中にあるようです。

このファイルは Python 3.10 でコンパイルされています。import や実行には Python 3.10 を使用してください。

### ヒント
- .pyc ファイルにはコンパイル済みの Python バイトコードが含まれます。
- モジュールとして import し、dir() や dis.dis() で調べてみましょう。


---

## 試行錯誤
1. .pycファイルをインポートして、dir()とdis.dis()を実行してみる。
### dir()の結果
```
['EYE_DATA', 'Path', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'is_inside_the_typhoon_eye', 'main', 'reverse_the_wind']
```
### dis.dis()の結果
mainの内容を見ると`answer`の値と`reverse_the_wind(EYE_DATA)`が一致する必要があることが予想できる。
また、Hintが与えられていて、ファイルを台風の目に入れろという指示がある。
```
Disassembly of main:
 36           0 LOAD_GLOBAL              0 (is_inside_the_typhoon_eye)
              2 CALL_FUNCTION            0
              4 POP_JUMP_IF_TRUE         9 (to 18)

 37           6 LOAD_GLOBAL              1 (print)
              8 LOAD_CONST               1 ('Hint: Move this file into the eye of the typhoon.')
             10 CALL_FUNCTION            1
             12 POP_TOP

 38          14 LOAD_CONST               0 (None)
             16 RETURN_VALUE

 40     >>   18 LOAD_GLOBAL              2 (input)
             20 LOAD_CONST               2 ('What was inside the eye? > ')
             22 CALL_FUNCTION            1
             24 STORE_FAST               0 (answer)

 42          26 LOAD_FAST                0 (answer)
             28 LOAD_GLOBAL              3 (reverse_the_wind)
             30 LOAD_GLOBAL              4 (EYE_DATA)
             32 CALL_FUNCTION            1
             34 COMPARE_OP               2 (==)
             36 POP_JUMP_IF_FALSE       25 (to 50)

 43          38 LOAD_GLOBAL              1 (print)
             40 LOAD_CONST               3 ('The typhoon is gone. Correct!')
             42 CALL_FUNCTION            1
             44 POP_TOP
             46 LOAD_CONST               0 (None)
             48 RETURN_VALUE

 45     >>   50 LOAD_GLOBAL              1 (print)
             52 LOAD_CONST               4 ('The wind is still too strong...')
             54 CALL_FUNCTION            1
```
is_inside_the_typhoon_eyeを見てみるとfileのパスを取得していることがわかる。そして`current_place`と`required_place`で比較していることが読み取れる。required_placeを見てみると **(101,121,101)** の内容をデコードしている。ASCIIで調べてみると **eye** という文字になったので、eyeというディレクトリを作成し.pycファイルとその中に配置した。
```
Disassembly of is_inside_the_typhoon_eye:
 19           0 LOAD_GLOBAL              0 (Path)
              2 LOAD_GLOBAL              1 (__file__)
              4 CALL_FUNCTION            1
              6 LOAD_METHOD              2 (resolve)
              8 CALL_METHOD              0
             10 LOAD_ATTR                3 (parent)
             12 LOAD_ATTR                4 (name)
             14 STORE_FAST               0 (current_place)

 20          16 LOAD_GLOBAL              5 (bytes)
             18 BUILD_LIST               0
             20 LOAD_CONST               1 ((101, 121, 101))
             22 LIST_EXTEND              1
             24 CALL_FUNCTION            1
             26 LOAD_METHOD              6 (decode)
             28 CALL_METHOD              0
             30 STORE_FAST               1 (required_place)

 21          32 LOAD_FAST                0 (current_place)
             34 LOAD_FAST                1 (required_place)
             36 COMPARE_OP               2 (==)
             38 RETURN_VALUE
```


2. .pycのプログラムを実行してみる
python3.10で実行するとHintが表示されたが、入力は受け付けていなかった。なので、eyeという名前のディレクトリ上で実行するとWhat was inside the eye?と表示され、入力を受け付けている状態になった。


3. 正解となる入力を調べる
dis.dis()で内容を確認したときに、`answer`の値と`reverse_the_wind(EYE_DATA)`の値を比較していたので、`reverse_the_wind(EYE_DATA)`の値を入力する。
`reverse_the_wind`も`EYE_DATA`もdir()で表示されたので、そのまま利用する。
```
answer = server.reverse_the_wind(server.EYE_DATA)
if isinstance(answer, bytes):
    #answer が「バイナリデータ（bytes型）」の場合
    sys.stdout.buffer.write(answer)
    
else:
    #answer が「通常の文字列（str型）」の場合
    sys.stdout.write(str(answer))
```
実行してみると**The typhoon is gone. Correct!**と表示されたので成功したが、flagは表示されなかった。なので入力した文字を疑った。
しかし、入力した文字は可読できない状態であった。
```
^Ô¥^Å¶¯¬O0< ><]¥^×°º^Ø^Ò¦I^×-4=&49=
```

4. 入力の内容をデコードしてみる。
上記の文字化けしている文字をUTF-8やunicodeでデコードしたが、うまくいかなかった。
latin1でencode(0x00~0xFFなので)してから、UTF-8に変換をするとflagが表示された。
今回のプログラムでは数値の値を強制的にchar型に変えているため、latin1で数値に直す必要があった。
```
 python3.10 -c "import server; print(server.reverse_the_wind(server.EYE_DATA).encode('latin1').decode('utf-8', errors='ignore'))"

Alpaca{DUMMY}
```
## まとめ
今回は.pycファイルを調べて、flagを探した。
dir()やdis.dis()を使用して中身の処理や関数などの情報を調べ、解法を予想した。
プログラムを実行するディレクトリの名前をeyeに変更したり、reverse_the_wind(server.EYE_DATA)の値を送信したりして、答えに辿りついた。
flagが表示されなかったので、入力した文字を疑い、デコードすることでflagを入手した。
スタックの順序などに苦戦して時間がかかったが、スタックなどについて理解が深まった。
