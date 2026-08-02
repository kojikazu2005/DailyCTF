from Crypto.Hash.Poly1305 import Poly1305_MAC

TARGET = b"admin=true"

# チャレンジ側で表示された値をそのまま入れる
s_hex   = input("s: ").strip()           # HINT! s: ...
mac_hex = input("mac(message): ").strip()# message に対する MAC
msg     = input("message: ").encode()    # 実際に入力した message

# --- PyCryptodome の実装に合わせた m の計算 ---
m_raw = int.from_bytes(msg, "little")
m     = m_raw + (1 << (8 * len(msg)))    # len(message) に応じて 2^(8*len) を足す

# --- tag と s を little-endian 整数として扱う ---
tag_int = int.from_bytes(bytes.fromhex(mac_hex), "little")
s_int   = int.from_bytes(bytes.fromhex(s_hex),   "little")

# h の下位 128bit
acc   = (tag_int - s_int) % (1 << 128)
mod_p = (1 << 130) - 5

s_bytes = bytes.fromhex(s_hex)

print("[*] candidates:")
for carry in range(4):                   # h の上位 2bit を総当たり
    h_full = acc + (carry << 128)       # 130bit の h 候補

    # r を逆算
    r_int = h_full * pow(m, -1, mod_p) % mod_p
    r_int &= (1 << 128) - 1             # 下位 128bit だけ使う

    r_bytes = r_int.to_bytes(16, "little")

    tag = Poly1305_MAC(r_bytes, s_bytes, TARGET).hexdigest()
    print(f"carry={carry}: tag={tag}")
