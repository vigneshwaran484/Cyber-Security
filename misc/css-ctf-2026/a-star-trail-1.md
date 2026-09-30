# A Star Trail 1 — Misc, 20 pts

## Objective
A "Polaris Logistics" star map (blueprint image) with planets/asteroids joined by dashed edges,
each labelled with a number of **days**. Deliver a package from **EARTH** to **LANCER-RXKRD**
in under 25 days, following the drawn paths.
Flag = first character of each **waypoint** on the route (start/end excluded), then `-` + total days
(1 dp). Example: `PAPA,OSCAR,SIERRA,TANGO,2025PLANET` over 5 days → `CSSCTF{POST2-5.0}`.

## Concepts
- The title is the hint: **"A Star" = A\***, i.e. **weighted shortest-path** on a graph.
- Bodies = nodes, dashed lines = edges, numbers = edge weights (days). Undirected.
- **The start (EARTH) and destination (LANCER-RXKRD) are NOT counted** in the letters — only the
  bodies you pass *through*. (This is the gotcha that cost several wrong submissions.)

## Steps
Transcribe the graph carefully (a single misread edge changes the answer — the trap here was a
non-existent direct `12-PUCK-8 → TAYLOR-3489` edge; the route must go via `JIP-REIA`).

Run Dijkstra from EARTH to LANCER-RXKRD. The shortest route is:
```
EARTH → PALLUS-XA → 12-PUCK-8 → JIP-REIA → TAYLOR-3489 → LANCER-RXKRD
 10.7      1.8         0.4         5.5          2.6         = 21.0 days
```
Now build the flag:
- Full node path initials: `E, P, 1, J, T, L`.
- **Drop the start and end** (E and L) → waypoints `P, 1, J, T` → `P1JT`.
- Total days: `21.0`.

## Flag
```
CSSCTF{P1JT-21.0}
```

## Takeaway
Labelled network + "reach X in under N" ⇒ **shortest path** (Dijkstra/A\*). Two lessons the hard way:
(1) transcribe the graph *exactly* — one imagined edge sent me to a bogus 18.3-day route; and
(2) read the flag-format wording precisely — here "each planet in your **path**" meant the
**intermediate waypoints only**, so the origin/destination initials are excluded.
Don't submit the prompt's worked example (`POST2-5.0`) — that's bait.
