# CTF Writeups & Cheatsheets

Personal writeups, organized by **category → event**, plus reusable **cheatsheets**.
Format follows my [Bandit repo](https://github.com/vigneshwaran484/bandit):
each writeup has **Objective → Concepts → Steps (command + why) → Takeaway**.

> Only tested on systems I own or platforms built for hacking (CTFs, HTB, THM, picoCTF).
> Using these techniques without permission is a crime.

---

## Layout

```
cyber/
├── web/        crypto/     forensics/
├── reverse/    pwn/        osint/       general/
│   └── <event>/<challenge>.md
└── cheatsheets/            ← reusable weapons (start here mid-CTF)
```

---

## Skills matrix

Techniques I've actually used, by category. Grows every event.

| Category | Techniques used | Still to learn |
|---|---|---|
| **Web** | DOM inspection, console logs, JWT decode, localStorage tampering, SQLi (auth bypass) | XSS, SSRF, IDOR, JWT forging (`alg:none`, weak HMAC), SSTI |
| **Crypto** | Base64, Caesar/ROT, Vigenère, XOR, MD5 brute-force, RSA (factor small n) | Padding oracle, AES modes, RSA (Wiener, common modulus), ECC |
| **Forensics** | Magic bytes, `strings`, hexdump reading | steganography, PCAP/Wireshark, memory (Volatility), `binwalk` |
| **Reverse** | inverting a JS checker, XOR self-inverse | x86/ARM asm, Ghidra, gdb, packers, anti-debug |
| **Pwn** | — | buffer overflow, ROP, format string, heap |
| **OSINT** | (team-solved) | metadata, geolocation, infra recon |

---

## Events

### Flag Hunt 2026 (team CYBORK) — full clear, 6/6 categories

Challenges I personally solved are linked. Team-solved ones are noted.

| Category | Challenge | Pts | Technique | Writeup |
|---|---|---|---|---|
| General | Sanity check | 10 | intro | team |
| General | Hex marks the spot | 50 | hex decode | team |
| General | Ones and zeros | 50 | binary decode | team |
| General | Beep beep | 50 | Morse code | [link](general/flag-hunt-2026/beep-beep.md) |
| General | Onion | 200 | nested encodings | team |
| Web | Look closer | 50 | DOM / hidden HTML | [link](web/flag-hunt-2026/look-closer.md) |
| Web | Dev notes | 75 | console.log | [link](web/flag-hunt-2026/dev-notes.md) |
| Web | Token of trust | 100 | JWT decode | [link](web/flag-hunt-2026/token-of-trust.md) |
| Web | Client-side login | 100 | client-side secret | [link](web/flag-hunt-2026/client-side-login.md) |
| Web | Guest pass | 150 | localStorage tamper | [link](web/flag-hunt-2026/guest-pass.md) |
| Web | Bobby Tables | 250 | SQL injection | [link](web/flag-hunt-2026/bobby-tables.md) |
| Crypto | Not so secret | 50 | base64 | team |
| Crypto | Rotate it | 50 | ROT/Caesar | team |
| Crypto | Et tu, Brute? | 100 | Caesar brute | team |
| Crypto | Many alphabets | 150 | Vigenère | [link](crypto/flag-hunt-2026/many-alphabets.md) |
| Crypto | Four digits | 150 | MD5 brute-force | [link](crypto/flag-hunt-2026/four-digits.md) |
| Crypto | Tiny RSA | 200 | RSA factor small n | [link](crypto/flag-hunt-2026/tiny-rsa.md) |
| Crypto | Known plaintext | 250 | XOR known-plaintext | team |
| Crypto | Too small to hide | 300 | small-key crypto | team |
| Forensics | Magic bytes | 75 | file signatures | [link](forensics/flag-hunt-2026/magic-bytes.md) |
| Forensics | Needle in the bytes | 100 | `strings` | [link](forensics/flag-hunt-2026/needle-in-the-bytes.md) |
| Forensics | Two in one | 250 | file carving | team |
| Reverse | XOR marks | 150 | XOR self-inverse | [link](reverse/flag-hunt-2026/xor-marks.md) |
| Reverse | Keygen | 250 | keygen logic | team |
| OSINT | Where was this taken? | 100 | image geolocation | team |
| OSINT | Leaky repo | 150 | git secrets | team |

---

## Cheatsheets

- [Encoding recognition](cheatsheets/encoding-recognition.md) — is it base64? hex? morse?
- [Magic bytes](cheatsheets/magic-bytes.md) — file signature table
- [Hashes](cheatsheets/hashes.md) — identify & crack
- [Web payloads](cheatsheets/web-payloads.md) — SQLi, JWT, storage
- [Crypto recipes](cheatsheets/crypto-recipes.md) — RSA, Vigenère, XOR

---

## Roadmap

1. **picoCTF** — General + Web tracks
2. **CryptoHack.org** — best crypto trainer
3. **PortSwigger Web Security Academy** — best web trainer
4. **HackTheBox** — realistic machines
5. **CTFtime.org** — live CTFs with the team

Focus categories: **Web + Crypto** first. Add **Reverse/Pwn** later.
