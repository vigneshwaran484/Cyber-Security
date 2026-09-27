# Many alphabets — Crypto, 150 pts

## Objective
Only the part inside braces is encrypted with a **Vigenère cipher**. Key = the city where the CTF
was built, lowercase. Underscores aren't encrypted and don't consume key letters.
Ciphertext: `rvplnlxjhfrgik_rvare`.

## Concepts
- "Many alphabets" = **poly-alphabetic** = Vigenère: a Caesar shift whose amount changes each
  letter following a repeating keyword.
- Decrypt: `plain = (cipher - key) mod 26`, key repeating.
- Unknown key but strong hint ("a city") → **brute-force a candidate list**, keep readable output.

## Steps
```python
def dec(ct, key):
    out=[]; ki=0
    for c in ct:
        s = ord(key[ki%len(key)]) - 97
        out.append(chr((ord(c)-97-s)%26+97)); ki+=1
    return "".join(out)

ct = "rvplnlxjhfrgikrvare"          # underscore stripped first
for k in ["chennai","coimbatore","madurai","mumbai","delhi", ...]:
    print(k, dec(ct, k))
# chennai -> polyalphabeticpower   <-- readable!
```
Put the `_` back at its original position (after 14 letters).
CyberChef: **Vigenère Decode**, key `chennai`, input `rvplnlxjhfrgik_rvare` (it leaves `_` alone).

## Flag
```
CTF{polyalphabetic_power}
```

## Takeaway
Vigenère tells: letters-only ciphertext + a keyword/passphrase hint. Known key → CyberChef.
No key, no hint → **Kasiski / index of coincidence** to recover key length, then frequency analysis.
