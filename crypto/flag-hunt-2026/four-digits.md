# Four digits — Crypto, 150 pts

## Objective
A locker stores the **MD5 hash** of a 4-digit PIN: `88cf91a1aef212f3c2cd12406983427d`.
Find the PIN. Format `CTF{pin_XXXX}`.

## Concepts
- 32 hex chars = **MD5** (SHA-1 = 40, SHA-256 = 64).
- Hashes are **one-way** — can't be reversed mathematically.
- But a 4-digit PIN is only **10,000 possibilities** → **brute force**: hash every candidate,
  compare. Works because the keyspace is tiny.

## Steps
```python
import hashlib
target = "88cf91a1aef212f3c2cd12406983427d"
for n in range(10000):
    pin = f"{n:04d}"                      # 0000..9999, keep leading zeros
    if hashlib.md5(pin.encode()).hexdigest() == target:
        print(pin); break                 # -> 7391
```
Verify:
```bash
echo -n '7391' | md5sum        # -n = no trailing newline
```

## Flag
```
CTF{pin_7391}
```

## Takeaway
Identify a hash by **length**. **Small keyspace → brute force.** For unknown hashes use
**hashcat / John** + wordlists (`rockyou.txt`), or Google the hash. MD5 is unfit for
passwords/PINs (fast, unsalted).
