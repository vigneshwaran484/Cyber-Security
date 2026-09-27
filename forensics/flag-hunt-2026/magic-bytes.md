# Magic bytes — Forensics, 75 pts

## Objective
A file lost its extension. Given its first bytes (hexdump), identify the type. Answer `CTF{extension}`.
```
00000000  25 50 44 46 2d 31 2e 37 0a 25 e2 e3 cf d3 0a 31
00000010  20 30 20 6f 62 6a 0a 3c 3c 2f 54 79 70 65 2f 43
00000020  61 74 61 6c 6f 67
```

## Concepts
- A file's real type is set by its first bytes (**magic number**), not its extension.
- Left column = offset; right = bytes. Convert hex → ASCII.

## Steps
```
25 50 44 46 2d 31 2e 37
 %  P  D  F  -  1  .  7
```
Also `6f 62 6a`=`obj`, `3c3c2f 54797065 2f 436174616c6f67`=`<</Type/Catalog` → PDF internals.
```bash
echo '255044462d312e37' | xxd -r -p     # -r -p = reverse a plain hex string
```

## Flag
```
CTF{pdf}
```

## Takeaway
First move on a mystery file: `file mystery`, then `xxd mystery | head`.
See the [magic-bytes cheatsheet](../../cheatsheets/magic-bytes.md). Note `PK` = ZIP = also
.docx/.xlsx/.apk.
