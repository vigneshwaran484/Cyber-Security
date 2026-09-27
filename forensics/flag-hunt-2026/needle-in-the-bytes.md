# Needle in the bytes — Forensics, 100 pts

## Objective
A hexdump of a corrupted image. Something readable is buried in it.
(First bytes `89 50 4e 47 0d 0a 1a 0a` = PNG signature.)

## Concepts
- Printable ASCII ≈ hex `20`–`7e`. Scan the dump for a run of those among the binary noise.
- The `strings` tool does this automatically: prints every run of readable text.

## Steps
Spotting it by hand at offsets 0x30–0x40:
```
43 54 46 7b 73 74 72 69 6e 67 73 5f 66 69 6e 64
 C  T  F  {  s  t  r  i  n  g  s  _  f  i  n  d
5f 65 76 65 72 79 74 68 69 6e 67 7d
 _  e  v  e  r  y  t  h  i  n  g  }
```
The intended tool:
```bash
strings image.png | grep -i ctf
```
- `strings` = pull readable text. `grep -i ctf` = keep lines with "ctf" (case-insensitive).

## Flag
```
CTF{strings_find_everything}
```

## Takeaway
**First move on any file challenge: `strings file | grep -i ctf`.** Free, fast, solves a huge
fraction of forensics. If empty, escalate: `xxd`, `binwalk`, `exiftool`, `zsteg`.
