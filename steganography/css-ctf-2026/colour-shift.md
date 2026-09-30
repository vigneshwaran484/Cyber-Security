# Colour Shift — Steganography, 45 pts

## Objective
`colorshiftctf.bmp` (also a `.jpg` variant): the Pink Floyd *Dark Side of the Moon* prism cover.
Title hint: "Colour Shift." Flag: `CSSCTF{...}`.

## Concepts
- Title + a colour image ⇒ **per-channel / bit-plane steganography**. The payload is hidden in one
  **colour channel**, at low intensity — invisible normally, revealed by isolating that channel.
- Use the **BMP** (lossless); the JPEG variant is a re-compressed decoy where LSB data is destroyed.

## Steps
1. **Recon**: `file`, `binwalk`, `exiftool`, `strings` → plain BMP, no appended data, no obvious tEXt.
2. **Bit-plane / channel sweep** — split R/G/B into 8 bit-planes each and save every plane as an image:
```python
from PIL import Image
import numpy as np
a = np.array(Image.open("colorshiftctf.bmp").convert("RGB"))
for c,name in enumerate("RGB"):
    for bit in range(8):
        plane = ((a[:,:,c] >> bit) & 1) * 255
        Image.fromarray(plane.astype('uint8')).save(f"{name}{bit}.png")
```
   The album art shows up on the high bits of every channel (normal). The hidden content is in the
   **red channel**, low intensity.
3. **Amplify the red channel** — high-pass / band-pass the red plane to remove the album art and boost
   faint marks. Text appears as a **line across the lower part of the image** (around y ≈ 420–440).
   In GIMP: `Colors → Components → Decompose` (RGB), keep the red layer, then
   `Colors → Curves`/`Levels` to boost — the string becomes readable.

The revealed text (a nod to Pink Floyd's *Shine On You Crazy Diamond*):

## Flag
```
CSSCTF{SHINE_ON}
```

## Takeaway
For colour-image stego: work on the **lossless** original, then go **channel-by-channel and
plane-by-plane** — data hidden in one channel's low bits (or as a faint low-amplitude overlay) is
invisible in the composite but obvious once you isolate and stretch that channel. Tools: PIL bit-plane
dump, GIMP Decompose + Curves, `zsteg` (PNG/BMP), StegSolve. Beware provided JPEG copies — they kill
LSB payloads; find/keep the BMP.
