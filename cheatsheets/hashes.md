# Hashes — identify & crack

## Identify by length (hex chars)
| Length | Hash |
|---|---|
| 32 | **MD5** |
| 40 | **SHA-1** |
| 64 | **SHA-256** |
| 128 | **SHA-512** |
| starts `$2a$`/`$2b$` | **bcrypt** |
| starts `$argon2` | **Argon2** |
| starts `$6$` | sha512crypt |

Tool: `hashid <hash>` or `hash-identifier`.

## Crack
```bash
# small keyspace (PIN, short word) -> brute force in Python
python3 -c '
import hashlib
t="88cf91a1aef212f3c2cd12406983427d"
for n in range(10000):
    p=f"{n:04d}"
    if hashlib.md5(p.encode()).hexdigest()==t: print(p)
'

# unknown hash + wordlist
john --format=raw-md5 --wordlist=rockyou.txt hashes.txt
hashcat -m 0 hashes.txt rockyou.txt        # -m 0 = MD5, 100 = SHA1, 1400 = SHA256
```
- `rockyou.txt` on BlackArch/Kali: `/usr/share/wordlists/rockyou.txt`
- Also just **Google the hash** — common ones are in online reverse-lookup DBs.

## Notes
- Hashes are one-way; you never "reverse" them, you **guess + hash + compare**.
- MD5/SHA1 are fast & broken for passwords. Real systems use slow, salted (bcrypt/argon2).
