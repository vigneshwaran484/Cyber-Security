# FLAPPY BOARD — Reverse Engineering, 244 pts

## Objective
A stripped 64-bit ELF (`flappy_board`): an X11 Flappy-Bird clone that talks to
`http://34.116.80.78:8765`. Beat **3 relay sectors** (rounds) within a 20-minute session
to recover the access key. Flag format: `CSSCTF{...}`.

## Concepts
- **Server-verified game**: the client plays locally but the *server re-simulates* your input
  (a list of "flap" ticks) and checks the score — so you can't fake it. You must submit a
  **physically valid flap sequence** for a server-chosen `seed`.
- **Reverse the physics + PRNG** from the binary, reproduce the pipe layout from `seed`, then
  **search** for flap timings that clear enough pipes.
- The controls-change gimmick (flap key remaps every pipe) is UI only — the API submits **tick
  numbers**, not keys, so it's irrelevant to the solve.

## Recon
```
strings → /api/attempt /api/practice /api/complete, "flag", "Authorization: Bearer %s"
objdump -d -M intel  → find the PRNG, physics_step, pipe init, POST builders
```
Protocol (all `application/x-www-form-urlencoded`, header `Authorization: Bearer <token>`):
- `POST /api/attempt` → `token, round, seed, target, wait_seconds` (r1 target=10)
- `POST /api/complete` `round&wait_ms&ticks&score&flaps=t0,t1,...` → next round's seed/target,
  or `flag=` after round 3.

## Reversed physics (all integer, fixed-point ×256 — fully deterministic)
```
PRNG  = xorshift32(13,17,5):  x^=x<<13; x^=x>>17; x^=x<<5
gap_center = rng()%231 + 125                 # pixels
pipes[5]:  x = (i*270 + 1040) << 8 ,  gap = gap_center
per tick:
  if flap: vel = -1724
  vel += 67 ; if vel > 2048: vel = 2048       # gravity + terminal
  bird_y += vel ; tick += 1  (max 36063)
  each pipe: x -= 717
  die if bird_y <= 3072 or bird_y > 119807
  collision when 30720 < pipe.x <= 54271:
     die if (bird_y-3071) <= (gap-87)<<8  or  (bird_y+3071) >= (gap+87)<<8
  score++ when a pipe reaches x <= 30719 (once) and alive
  recycle pipe when x < -17408: x = max_x + 69120, gap = rng()%231+125
init: bird_y = 61440 (240px), vel = 0
```

## Exploit
1. Re-implement the above in Python ([flappy-solver.py](flappy-solver.py)).
2. **Beam search** each round's seed for a flap-tick list that reaches `target` alive
   (keep alive states, rank by score then distance to the next gap center).
3. Submit each round via `/api/complete`. **The server does not enforce the real wait timers**
   (`wait_seconds` 180/360/600) — just claim `wait_ms = wait_seconds*1000 + buffer`.
4. Round 3's response contains `flag=`.

Full automation: [flappy-fullrun.py](flappy-fullrun.py). Clears all 3 rounds in ~190 s.

## Flag
```
CSSCTF{birdddd}
```

## Takeaway
When a client "plays" but a server verifies, the win condition is **reproduce the server's model
exactly**, not patch the client. The whole solve hinged on reading the *integer* physics precisely
(fixed-point `<<8`, exact constants) and the tiny PRNG. Two shortcuts mattered: (a) validating the
Python sim against the server on the real path (`/api/complete` round 1) before trusting it, and
(b) noticing the anti-cheat wait timers were never actually enforced.
Defence: enforce server-side timing, and rate-limit/replay-check submissions.
