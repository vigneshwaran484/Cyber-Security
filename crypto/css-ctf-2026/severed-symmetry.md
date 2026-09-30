# Severed Symmetry — Crypto (Multivariate), 488 pts, Expert

## Objective
A multivariate public-key scheme (`source.py`): public equations + ciphertext given, private key
withheld. Recover the plaintext (the flag). Params `p=17, n=32, m=34, t=16, s=4`. Flag: `CSSCTF{...}`.

## Concepts
- A **Rainbow/UOV-style multivariate trapdoor** with an extra "Q layer": public map
  `P = A1 ∘ F ∘ A2` (secret affine maps around a structured central map `F`).
- `F` has two layers:
  - **w-layer** (first `t=16` polys): `w_i = z_i − q_i(z[16:])` — **degree 2** in the input.
  - **U-layer** (next `18` polys): `U_j(w, z[16:])` — feeding the quadratic `w` into a quadratic
    makes these **degree 4** → the public key is degree-4 (hence the 31 MB `out.txt`).
- **"Severed Symmetry"** = the two layers can be *severed* by degree, then the UOV oil space peeled off.

## Attack
**1. Sever the quadratic layer by degree.** Only the 18 U-polys have degree-3/4 terms, so among the
34 public polynomials there is a **16-dim space of linear combinations whose degree-3 and degree-4
coefficients all vanish** — exactly the `w`-layer. (Confirmed: degree≥3 part has rank 18 → 16-dim
null space.) The same combination applied to the ciphertext entries gives each block's `w` values.

**2. The quadratic parts live in a small subspace.** In `w_i = z_i − q_i(z[16:])`, the quadratic
terms only involve the 16 linear forms `z[16:]`. The row space of the stacked quadratic-form matrices
is that **16-dim subspace** `V` (the kernel of one `w` form already gives it — dim 16).

**3. Parametrise preimages.** With `w` known, each candidate `x` is fixed by 16 coordinates
`u = z[16:]`. The remaining 18 equations become **quadratic in `u`** (recover them by interpolation).

**4. Recover the oil space (UOV).** The U layer has **12 oil + 4 vinegar** variables ⇒ each quadratic
form has **rank ≤ 8**, so its kernel (dim 8) lies inside the oil space; two kernels span all 12 oil
dimensions. (Confirmed: ranks all 8, kernels all 8, span dim 12.)

**5. Brute-force the vinegar.** Try all `17⁴` values of the 4 vinegar coordinates; solve the
resulting **linear** system for the oil part; rebuild `x`; check `public(x) == ciphertext`; decode the
length-prefixed base-17 frame. All blocks re-encrypt back to the ciphertext → recovery verified.

## Flag
```
CSSCTF{P35T0_5CH3M3_4TT4CK2026}
```

## Takeaway
Layered multivariate schemes leak through **structure, not brute force**. The killer observations:
(1) a degree gap between layers lets you isolate the low-degree layer with pure linear algebra
("severing"); (2) UOV/Rainbow oil-vinegar layers have **low-rank quadratic forms**, so kernels of the
public forms reveal the oil space (the classic MinRank/Kipnis–Shamir handle); (3) once the space is
recovered, the trapdoor collapses to small linear systems + a tiny vinegar brute-force.
Note: this "Pesto" scheme's own name is in the flag — `P35T0_5CH3M3_4TT4CK`.
