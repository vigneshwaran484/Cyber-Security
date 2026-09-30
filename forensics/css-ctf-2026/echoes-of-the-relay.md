# Echoes of the Relay — Forensics, 33 pts

## Objective
`relay_backup.img` (~32 MB): a filesystem image. "Recovery beacon flickers... residual filesystem
entries detected." Recover the deleted evidence. Flag: `CSSCTF{...}` ("deleted doesn't mean gone").

## Concepts
- **Deleted-file recovery** on an **ext4** image: metadata (inodes) often survives deletion → carve
  it back with The Sleuth Kit (`fls` / `icat`).
- **Polyglot / appended archive**: a PNG can have a ZIP glued on after its `IEND` marker
  (`binwalk` / manual carve).
- Chained clues: recovered note → password → hidden ZIP → flag.

## Steps
1. **Identify & list** (visible files — logs, shift maps, `diagnostics.txt` — are decoys):
```bash
file relay_backup.img            # Linux ext4 filesystem
fls -r relay_backup.img          # recursive list; shows deleted entries with *
```
   A deleted entry appears: `operator/Documents/emergency_note.txt` (inode 25).
2. **Recover the deleted note**:
```bash
icat relay_backup.img 25 > emergency_note.txt
cat emergency_note.txt
```
   The note gives an **archive password** (`severance2101`) and a hint to *"look beyond attaching the
   recovery package"* / check the image viewer.
3. **Extract the visible PNG and carve the appended ZIP**:
```bash
icat relay_backup.img <inode_of_relay_status.png> > relay_status.png
binwalk relay_status.png         # PNG + ~560 bytes ZIP after IEND
binwalk -e relay_status.png      # or: dd the trailing ZIP out
```
4. **Open the password-protected ZIP** (`severance2101`) →
   `transmission/manifest.txt` + `transmission/core_recovery.txt` (holds the flag).
```bash
unzip -P severance2101 extracted.zip
cat transmission/core_recovery.txt
```

## Flag
```
CSSCTF{d3l3t3d_d0esnt_m34n_g0ne}
```

## Takeaway
A "filesystem image" ⇒ **The Sleuth Kit**: `fls -r` to spot deleted entries, `icat <inode>` to carve
them. Deletion clears the directory entry, not the inode/data. Then treat every recovered image as a
possible **polyglot** — `binwalk` for archives hidden after `IEND`/EOF. Notes-in-images that hand you
a password are a classic multi-stage forensics chain.
