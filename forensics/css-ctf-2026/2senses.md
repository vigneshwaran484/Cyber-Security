# 2(-1) Senses — Steganography, 92 pts

## Objective
`2senses_puzzle.wav` (mono 16-bit 44.1 kHz, 17 s), with a warning to turn the volume down.
Recover the flag. Format: `CSSCTF{...}`.

## Concepts
- **2(−1) = 1 sense**: stop *listening*, start *looking* → view the **spectrogram** (audio stego).
  "Turn down volume" = the audio is deliberately harsh; the payload is meant to be seen, not heard.
- The flag is **split across two channels** (a fill-in-the-blank):
  - a **template** hidden in the WAV **metadata** (RIFF `LIST/INFO` + ID3 tags),
  - the **blank's answer** drawn into the **spectrogram**.

## Steps
**1. Spectrogram** (no matplotlib needed — scipy + PIL):
```python
import numpy as np, wave
from scipy import signal
from PIL import Image
w=wave.open('2senses_puzzle.wav'); d=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)
f,t,Sxx=signal.spectrogram(d, fs=w.getframerate(), nperseg=2048, noverlap=1536)
S=10*np.log10(Sxx+1e-12); S=(S-S.min())/(S.max()-S.min())
Image.fromarray(np.flipud((S*255).astype('uint8'))).save('spec.png')
```
Low-frequency band spells **`chinaski`**; the loud blob on the right is a portrait
(Henry *Chinaski* = Charles Bukowski's literary alter ego).

**2. Metadata template** — grep found `CSSCTF` *inside* the file; parsing the chunks reveals it:
```bash
python3 - <<'EOF'
import struct; d=open('2senses_puzzle.wav','rb').read(); p=12
while p+8<=len(d):
    cid=d[p:p+4]; sz=struct.unpack('<I',d[p+4:p+8])[0]
    if cid!=b'data': print(cid, d[p+8:p+8+sz][:80])
    p+=8+sz+(sz&1)
EOF
```
- `LIST/INFO` → `IART = "CSSCTF{WHOS_THIS_FLUFFMASTER_MR..."`, `ICMT = "}"`
- `id3 ` → `TPE1 = "CSSCTF{WHOS_THIS_FLUFFMASTER_MR..."`, `COMM = "}"`

So the template is `CSSCTF{WHOS_THIS_FLUFFMASTER_MR...}` — the `}` is stashed in the comment field,
and `...` is the blank. Fill it with the spectrogram answer, Title-cased as a proper noun.

## Flag
```
CSSCTF{WHOS_THIS_FLUFFMASTER_MR_Chinaski}
```

## Takeaway
Audio challenge → **always render the spectrogram first**. Then **always dump file metadata**
(`exiftool`/manual RIFF+ID3 parse): flags love hiding in `IART`/`ICMT`/`TPE1`/`COMM` tags, and here
the `}` was split off into a separate comment field to break naive `strings | grep` reads.
The last mile was pure **format**: the answer was `chinaski` all along; only Title-case (`Chinaski`,
matching the proper noun) was accepted — when a flag keeps failing, brute the casing/joiners of the
one token you're sure of before doubting the whole solve.
