import base64
import string

# 1. ファイルを読み込んで文字列として取得
with open("output.txt", "r", encoding="utf-8") as f:
    flag_str = f.read().strip()  # 余計な改行や空白を削除

# --- 判定用リストの定義 ---
# Base64にしか含まれない文字（小文字の英字 a-z, +, /）
list_b64 = list(string.ascii_lowercase) + ["+", "/"]

# Base32にしか含まれない文字（G以上の大文字 G-Z）
list_b32 = list("GHIJKLMNOPQRSTUVWXYZ")

# 2. 20回のループで自動判定してデコードする
for i in range(20):
    # 文字列に含まれる文字の種類を重複なく抽出
    current_chars = set(flag_str)

    # リストb64の文字が1つでも含まれているか判定
    if any(char in current_chars for char in list_b64):
        flag_bytes = base64.b64decode(flag_str)
        print(f"Loop {i+1}: Base64でデコードしました")

    # リストb32の文字が1つでも含まれているか判定
    elif any(char in current_chars for char in list_b32):
        flag_bytes = base64.b32decode(flag_str, casefold=True)
        print(f"Loop {i+1}: Base32でデコードしました")

    # どちらのリストの文字もなければ Base16 (0-9, A-F) と判定
    else:
        flag_bytes = base64.b16decode(flag_str, casefold=True)
        print(f"Loop {i+1}: Base16でデコードしました")
    
    # 次のループのために、デコードしたバイト列を文字列に戻す
    # （バイナリデータ等でエラーが出ないよう errors='ignore' を指定）
    flag_str = flag_bytes.decode('utf-8', errors='ignore')

# 3. 最終結果を表示
print("\n--- 最終結果 ---")
print(flag_str)
