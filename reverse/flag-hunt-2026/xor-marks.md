# XOR marks — Reverse, 150 pts

## Objective
A checker accepts only the correct flag:
```js
const enc = [105,126,108,81,82,26,88,117,67,89,117,67,94,89,117,69,93,68,117,67,68,92,79,88,89,79,87];
if ((input.charCodeAt(i) ^ 42) !== enc[i]) return false;
```

## Concepts
- Reverse engineering: read the transform, invert it. Here `enc[i] = flagchar[i] ^ 42`.
- **XOR is its own inverse:** `(x ^ 42) ^ 42 = x`. So XOR `enc` with 42 again to recover the flag.

## Steps
```python
enc=[105,126,108,81,82,26,88,117,67,89,117,67,94,89,117,69,93,68,117,67,68,92,79,88,89,79,87]
print("".join(chr(b^42) for b in enc))     # CTF{x0r_is_its_own_inverse}
```
Sanity: `105 ^ 42 = 67 = 'C'`. CyberChef: recipe **XOR**, key `42` (Decimal).

## Flag
```
CTF{x0r_is_its_own_inverse}
```

## Takeaway
XOR encrypt = decrypt with the same key. Constant-XOR → XOR again to undo. No key? Single-byte
XOR has 256 keys → brute-force all, look for `CTF{`. Rev mindset: don't guess inputs forward —
**invert each transform in reverse order**.
