# Lamp Drill — Hardware: Reverse Engineering, 15 pts

## Objective
`lampDrill.svg` / `lampDrill.pdf`: a grid of boxes, each holding two dots (filled ● / hollow ○),
with a legend row on top. "Warm-up. No spaces." Flag: `CSSCTF{...}`.

## Concepts
- The legend is a **truth table** for a logic gate. With **● = 1, ○ = 0**:
  `●●→●, ●○→○, ○●→○, ○○→○` = **AND** (only `1 AND 1 = 1`).
- Each box's two dots → one **bit** via AND. Read rows left-to-right as bytes → ASCII.

## Steps
Render the SVG (`rsvg-convert`) and read the dots (or parse the SVG fills: black `#1c1915`,
hollow `#f7f4ee`). Apply AND per box:
- Row 1 → `01100011` = `0x63` = `c`
- Row 2 → `01110011` = `0x73` = `s`
- Row 3 → `01110011` = `0x73` = `s`

3 rows × 8 boxes = `css`. The flag is **lowercase**, submitted as-is.

## Flag
```
CSSCTF{css}
```

## Takeaway
Dots-in-boxes + a two-input legend = a **logic-gate decode**. Map filled/hollow to 1/0, read the
legend as the truth table (AND/OR/XOR/NAND), reduce each cell, then bits → ASCII. Sample the image
pixels rather than eyeballing when boxes get dense.
