
# [private-method] Writeup
日付: 2026-07-09
カテゴリ: Misc

---

##  問題概要
今日の問題は Miscの問題で、  
Pythonのプライベートメゾットを呼び出す。
- codeにalpaca()と入力するとalpaca()関数が呼び出せる
- __flagはそのままでは呼び出せない
- 正規表現で英数字1文字以上と"("と")"が使用可能

```python
class Main:
    # public 
    def alpaca():
        return "🦙"
    # private
    def __flag():
        return "Alpaca{REDACTED}"
        
    if re.fullmatch(r"\w+\(\)", code):
    print(eval(f"Main.{code}"))
```

---

##  解法の方針
1. **[pythonではプライベートメゾットは"_クラス名__メゾット名"で扱われる]**  
   - dir()でメゾットの保存方法がわかる
   




