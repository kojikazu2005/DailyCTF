# [Redirecting to Login Page] Writeup
日付: 2026-07-11
カテゴリ: web

---

## 問題概要

Webサイトに接続するとログインフォームが表示される。ユーザ名:alpaca、パスワード:pacapacaと入力するとログインできるが、他のことはできず、flagは入手できない。配布されたプログラムファイルはlogin.phpとlogout.phpの他、ログイン成功後のページのcontent.phpとflagのページのindex.phpがある。

## 解答の方針

### 1. index.phpにflagがあることがわかっているので、urlから直接index.phpにアクセスする
- http://localhost:3000/index.php と入力することでindex.phpにアクセスできると考えた。
- しかし、http://localhost:3000/login.php にリダイレクトされてしまった。
- 原因はindex.phpにリダイレクトのhttpヘッダが記述されているためである。

```php
header("Location: login.php");
```

### 2. index.phpにアクセスするとリダイレクトされるので**crulコマンド**でリダイレクトなしでアクセスする
- curl http://localhost:3000/login.php でアクセスすることでリダイレクトが起こらず、flagを取得することができる。
- -vオプションを追加することでヘッダやレスポンスの内容を見ることができる。

