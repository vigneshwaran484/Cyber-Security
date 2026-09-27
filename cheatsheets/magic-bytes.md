# Magic bytes (file signatures)

First bytes identify the real file type regardless of extension.

| Hex | ASCII | Type |
|---|---|---|
| `25 50 44 46` | `%PDF` | PDF |
| `FF D8 FF` | `ÿØÿ` | JPEG |
| `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` | PNG |
| `47 49 46 38` | `GIF8` | GIF |
| `50 4B 03 04` | `PK..` | ZIP → also **.docx .xlsx .pptx .jar .apk .epub** |
| `52 61 72 21` | `Rar!` | RAR |
| `1F 8B` | | GZIP |
| `42 5A 68` | `BZh` | BZIP2 |
| `37 7A BC AF` | `7z..` | 7-Zip |
| `7F 45 4C 46` | `.ELF` | Linux executable |
| `4D 5A` | `MZ` | Windows PE (.exe/.dll) |
| `49 44 33` | `ID3` | MP3 |
| `00 00 00 .. 66 74 79 70` | `ftyp` | MP4/MOV |
| `CA FE BA BE` | | Java class |

## Workflow
```bash
file mystery              # identify by signature
xxd mystery | head        # look at first bytes yourself
binwalk mystery           # find EMBEDDED files (a PNG hiding a ZIP, etc.)
binwalk -e mystery        # extract them
```

## Traps
- Wrong/missing extension → trust `file`, not the name.
- `PK` header = a ZIP: unzip office docs to read raw XML / find hidden files.
- A valid header can hide a second file appended after it → `binwalk`.
