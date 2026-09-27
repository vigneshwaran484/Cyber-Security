# Tiny RSA — Crypto, 200 pts

## Objective
Each character encrypted separately with RSA using tiny numbers:
```
n = 3233   e = 17
c = [2412,1230,1632,119,3179,1230,119,2271,1632,884,2170]
```
Decrypt each number to an ASCII char.

## Concepts
- RSA public = `(n, e)`. Encryption `c = m^e mod n`. Decryption `m = c^d mod n`.
- Security rests on **n being hard to factor**. Here `n = 3233` is 4 digits → factor instantly.
- Once you have primes `p, q`: `phi=(p-1)(q-1)`, `d = e^-1 mod phi`.

## Steps
```python
n=3233; e=17
c=[2412,1230,1632,119,3179,1230,119,2271,1632,884,2170]
p,q = 61,53                       # factor n (trial division)
phi = (p-1)*(q-1)                 # 3120
d = pow(e,-1,phi)                 # 2753  (modular inverse of e)
print("".join(chr(pow(x,d,n)) for x in c))   # rsa_is_math
```
- `pow(e,-1,phi)` = modular inverse (Python 3.8+).
- `pow(x,d,n)` = fast `x^d mod n`.

## Flag
```
CTF{rsa_is_math}
```

## Takeaway
RSA in a CTF → first question: **can I factor n?** Small → do it; bigger → **factordb.com**,
`yafu`, SageMath. Recipe once you have p,q: `phi → d=inverse(e,phi) → m=pow(c,d,n)`.
Other RSA attacks: small e (cube root), shared/common primes, Wiener (small d).
See [crypto-recipes cheatsheet](../../cheatsheets/crypto-recipes.md).
