from hashlib import sha256

N = 2_000_000

def H(x):
    return sha256(x).digest()[:5]

seen = {}

for i in range(N):
    a = f"user={i}".encode()
    seen[H(a)] = a

for j in range(N):
    b = f"admin={j}".encode()
    
    h = H(b)

    if h in seen:
        print(seen[h], b, h)
        break

