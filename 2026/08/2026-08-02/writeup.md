# [Password, Please] Writeup
日付: 2026-08-02 
カテゴリ: Misc

---

##  問題概要
与えられたshファイルを実行すると、パスワードの入力が求められる。パスワードは${RANDOM}をいくつか使用して作成されているのでわからない。しかし、スクリプト内のパスワード判定はBashの`[[ ... ]]`におけるunquotedな ==  比較を使っており、これは“完全一致”ではなくglobパターンマッチになる。
そのため、見た目では「ランダムな長い数字を完全一致させる」ように見えるが、実際には もっと緩い条件で通ってしまう。

---

##  解法
1. 配布されたshファイルを読む
- catコマンドで中身を確認する
- ${RANDOM}では乱数を作っているのでsecretは数字のパスワードになっているはず
- readで読み込んだパスワードをそのままif文で比較していてquoteされていない

``` bash
secret="${RANDOM}${RANDOM}${RANDOM}${RANDOM}"

printf 'Password: '
read -r password

if [[ $secret == $password ]]; then
    cat /flag.txt
else
    echo 'Access denied'
fi
```
2. Bashにはワイルドカードが存在する
- アスタリスク(\*)は文字数の制限がなく、任意の文字列を表している
- 入力するパスワードにアスタリスクを入力するとif文がtrueになる

```
Password: *
Alpaca{REDACTED}
```

## まとめ
- Bash の `[[ ... ]]` は右辺が unquoted だと glob パターン比較になる
- ${RANDOM}${RANDOM}${RANDOM}${RANDOM}は毎回違うので完全一致は不可能
- しかし `*` は 任意の文字列にマッチするワイルドカード
- よって `*` を入力すれば必ず一致し、フラグが返る 
