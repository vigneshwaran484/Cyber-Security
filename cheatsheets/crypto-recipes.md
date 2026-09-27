# Crypto recipes

## RSA
Given `(n, e, c)`:
```python
# 1. factor n  (small -> trial division; else factordb.com / yafu / sage)
# 2.
phi = (p-1)*(q-1)
d   = pow(e, -1, phi)
m   = pow(c, d, n)          # decrypt
# per-character: "".join(chr(pow(x,d,n)) for x in c_list)
```
Attacks by weakness:
| Clue | Attack |
|---|---|
| small `n` | factor it |
| small `e` (e=3) + small m | cube root of c (no mod) |
| two keys share a prime | `gcd(n1,n2)` = p |
| same `n`, two `e` coprime | common-modulus attack |
| very small `d` | Wiener's attack |
Tools: `RsaCtfTool`, SageMath, factordb.com.

## Vigenère
```python
def dec(ct,key):
    o=[];i=0
    for c in ct:
        if c.isalpha():
            s=ord(key[i%len(key)])-97
            o.append(chr((ord(c.lower())-97-s)%26+97)); i+=1
        else: o.append(c)
    return "".join(o)
```
No key: **Kasiski / index of coincidence** for key length, then per-column frequency.
Hint-based: brute-force a candidate keyword list, keep readable output.

## XOR
```python
# single-byte, known key
bytes(b ^ k for b in data)
# unknown single-byte key: brute all 256, look for CTF{
for k in range(256):
    out=bytes(b^k for b in data)
    if b"CTF{" in out: print(k, out)
```
XOR is its own inverse. Repeating-key XOR: find key length (Hamming distance), then per-position single-byte solve.

## Caesar / ROT
```bash
# brute all 25 shifts
python3 -c "s='...'; [print(i, ''.join(chr((ord(c)-65-i)%26+65) if c.isupper() else c for c in s)) for i in range(26)]"
```
ROT13 = shift 13. `tr 'A-Za-z' 'N-ZA-Mn-za-m'`.

## Classic tools
CyberChef **Magic** op auto-detects. dcode.fr for obscure ciphers.
