# prince walk — Reverse / Memory Editing, 123 pts

## Objective
`prince_walk`: a walking-simulator binary. Avatar starts at `(1, 1)`; the goal tile is
`(999999, 999999)`. Walking there by hand is impossible — reach it another way. Flag: `CSSCTF{...}`.

## Concepts
- **Live memory editing** (Cheat Engine / **PINCE** style): the player's coordinates are just two
  `Int32` values in the process's writable memory. Overwrite them to teleport.
- The binary itself hints it: `strings` shows references to **PINCE** and
  "a terminal sandbox for PINCE Int32 memory-editing practice".
- The flag isn't in the file — it's only printed once you're standing on the destination tile.

## Steps
```bash
file prince_walk     # stripped x86-64 PIE ELF
strings prince_walk  # game text + the PINCE / Int32 hint (no plaintext flag)
```
Classic **scan → change → re-scan** to isolate the coordinate pair:
1. Player X and Y are two **adjacent Int32** values, starting `(1, 1)`.
2. Press `d` once → pair becomes `(2, 1)`. Scan writable memory for that byte pattern.
3. Repeat move/scan until a single address pair is isolated (same loop as PINCE/Cheat Engine).
4. **Write `(999998, 999999)`** into the coordinate pair, then press `d` once so the step lands
   exactly on `(999999, 999999)`.
   - ⚠️ Writing `999999` directly then stepping overshoots to `X = 1000000`. Set X to `999998` and
     let the final move increment it.
5. "THE END OF THE WORLD" appears and asks how you got there; answering `1` or `2` both trigger the
   dev's "No you didn't" and reveal the flag under **MISSION COMPLETE**.

> No PINCE/gdb in the sandbox → ran the binary in a pty and wrote to `/proc/<pid>/mem` from Python.
> On your own machine, just attach with **PINCE**: scan Int32 `1` → move → scan `2` → isolate → set
> `X=999998, Y=999999` → step once.

## Flag
```
CSSCTF{P12INC3_0R_P1NC3?}
```

## Takeaway
When a game demands an "impossible" grind, the intended path is usually **runtime memory editing**,
not actually playing. Coordinates/scores/health are plain `Int32`s you find by the scan-move-rescan
loop. Tools: **PINCE** (Linux) or **Cheat Engine** (Windows); scriptable via `/proc/<pid>/mem`.
Watch off-by-ones (`999998` + a step, not `999999` + a step).
