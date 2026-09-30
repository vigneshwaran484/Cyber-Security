# Chrono II — Cryptography, 100 pts

## Objective
A time-based cipher feed: `feed.json` = 60 records `{timestamp, ciphertext}` (one per second), each
the **same flag** encrypted under a **different key every second**. Recover the flag. Format: `CSSCTF{...}`.

## Concepts
- **Known-plaintext + periodic keystream.** Every ciphertext has the same structure
  (`xxx_xxxxx_..._{...}`): letters shift, digits shift, and `{ } _` stay fixed. The known prefix
  **`CSSCTF`** gives 6 keystream values per row (A = 0).
- The per-second key is **not** simple Caesar/Vigenère. The page hints at "a few gears turning
  together" → a keystream of **N = 77 = 7 × 11** shift values (a 7-gear and an 11-gear), read with a
  per-second **stride C = 43**:  `k = K[(C·n + j) mod N]`, where `n` = seconds since the first record
  and `j` = character position (counting only stepping chars).
- **Stepping rule**: the key index advances on **letters and digits**, but **not** on `{ } _`.
  Letters shift mod 26; digits shift mod 10.

## Steps
**1. Recover the 77-value keystream** from the known `CSSCTF` prefix across all 60 rows. Each row
starts at a different index of the 77-cycle, so together the 60 rows cover essentially all of `K`
(`n=77/gcd`… — verified by cross-checks between rows, e.g. row `n=34` at index 76 matches row `n=27`).
```python
import json, datetime as dt
data = json.load(open("feed.json"))
known, N, C = "CSSCTF", 77, 43
secs = lambda ts: dt.datetime.fromisoformat(ts.replace("Z","+00:00")).timestamp()
t0 = secs(data[0]["timestamp"]); K = {}
for r in data:
    n = round(secs(r["timestamp"]) - t0)
    for j,p in enumerate(known):
        k = (ord(r["ciphertext"][j].lower()) - ord(p.lower())) % 26
        K[(C*n + j) % N] = k
```
**2. Decrypt any row** with the recovered key, honouring the stepping rule:
```python
def dec(ct, n):
    out, idx = [], 0
    for ch in ct:
        k = K[(C*n + idx) % N]
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            out.append(chr((ord(ch)-base-k) % 26 + base)); idx += 1
        elif ch.isdigit():
            out.append(str((int(ch)-k) % 10)); idx += 1
        else:
            out.append(ch)            # { } _  copied; key does NOT advance
    return "".join(out)
print(dec(data[0]["ciphertext"], 0))
```
All 60 rows now decrypt to the same plaintext → key fully recovered.

## Flag
```
CSSCTF{th3_c10ck_r3m3mb3rs_3very_s3c0nd}
```

## Takeaway
Same message under many keys + a **known prefix** = known-plaintext recovery of a keystream. The twist
was the key schedule: a **finite periodic keystream** (N = 7×11 "gears") indexed by `C·n + position`,
with the index **stepping only on encrypted chars** (letters/digits), not on the literal `{ } _`.
Collect enough windows of the cycle across timestamps and the whole key falls out. Watch the digit rule
(`mod 10`, not `mod 26`) and the non-advancing separators — the classic bug that makes the tails
garble.
