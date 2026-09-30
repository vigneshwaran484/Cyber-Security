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
| **Web** | DOM inspection, console logs, JWT decode, localStorage tampering, SQLi (auth bypass), GraphQL introspection / hidden fields | XSS, SSRF, IDOR, JWT forging (`alg:none`, weak HMAC), SSTI |
| **Crypto** | Base64, Caesar/ROT, Vigenère, XOR, MD5 brute-force, RSA (factor small n), periodic rotor keystream (known-plaintext), multivariate (UOV/Rainbow) layer-severing + MinRank oil-space | Padding oracle, AES modes, RSA (Wiener, common modulus), ECC, lattices |
| **Forensics** | Magic bytes, `strings`, hexdump, audio spectrogram stego, WAV/ID3 metadata, ext4 deleted-file recovery (Sleuth Kit `fls`/`icat`), polyglot carving (`binwalk`), log/timeline correlation + AES-GCM key derivation | PCAP/Wireshark, memory (Volatility) |
| **Steganography** | audio spectrogram, per-channel + bit-plane image stego (GIMP Decompose, PIL) | `zsteg`/StegSolve depth, DCT/JPEG stego, LSB matching |
| **Reverse** | inverting a JS checker, XOR self-inverse, x86-64 asm reading (objdump), reconstructing integer physics + PRNG (xorshift32), protocol RE + solver bot, live memory editing (PINCE / `/proc/pid/mem`) | Ghidra, gdb, packers, anti-debug |
| **Pwn** | format-string `%p` leak, off-by-one saved-RBP pivot, ret2win (No-PIE), use-after-free → function-pointer hijack | full buffer overflow, ROP, GOT overwrite, tcache/heap |
| **AI/ML Security** | LLM prompt injection / social engineering (authority+urgency, split-confirm, roleplay) | indirect/RAG injection, jailbreak chaining, model extraction |
| **OSINT** | git history / deleted files / unmerged branches (`git log --all -p`), social recon | metadata, geolocation, infra recon |

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

### CSS CTF 2026: Return of Nexus (USYD Cybersecurity Society, team CYBORK) — **full clear** 🏆

Points shown are final (dynamic scoring). Challenges I personally have writeups for are linked;
team-solved ones (no writeup) are noted.

| Category | Challenge | Pts | Technique | Writeup |
|---|---|---|---|---|
| Welcome | Welcome to Nexus | 10 | intro | team |
| OSINT | Dead Faction Servers | 10 | git history / deleted file + unmerged branch | [link](osint/css-ctf-2026/dead-faction-servers.md) |
| OSINT | Server Juice | 15 | social media recon (follow account) | team |
| OSINT | 2(-1) Senses | 59 | audio spectrogram + WAV/ID3 metadata (fill-in-blank) | [link](forensics/css-ctf-2026/2senses.md) |
| Hardware: RE | Lamp Drill | 15 | logic-gate (AND) bit decode | [link](hardware/css-ctf-2026/lamp-drill.md) |
| Hardware: RE | Silicon Snare | 250 | — | team |
| Web | Welcome to Star City | 15 | source review / base64+URL decode | [link](web/css-ctf-2026/welcome-to-star-city.md) |
| Web | Secret Supernovas | 50 | GraphQL introspection / hidden fields | [link](web/css-ctf-2026/secret-supernovas.md) |
| Misc | A Star Trail 1 | 20 | shortest path (Dijkstra/A*), waypoint-only flag | [link](misc/css-ctf-2026/a-star-trail-1.md) |
| Misc | A Star Trail 2 | 75 | shortest path (variant) | team |
| AI/ML Security | After hours... | 20 | LLM prompt injection / social engineering | [link](ai-ml/css-ctf-2026/after-hours.md) |
| Pwn | Dockside Ticket Office | 25 | use-after-free → function-pointer hijack | [link](pwn/css-ctf-2026/dockside-ticket-office.md) |
| Pwn | Maintenance Log | 62 | format-string leak + off-by-one RBP → ret2win | [link](pwn/css-ctf-2026/maintenance-log.md) |
| Crypto | Chrono I | 25 | time-based keystream (simpler) | team |
| Crypto | Chrono II | 100 | periodic rotor keystream (7×11 gears), known-plaintext | [link](crypto/css-ctf-2026/chrono-ii.md) |
| Crypto | Severed Symmetry | 247 | multivariate (UOV/Rainbow) layer-severing + oil-space + vinegar brute | [link](crypto/css-ctf-2026/severed-symmetry.md) |
| Forensics | Echoes of the Relay | 33 | ext4 deleted-file recovery + polyglot ZIP-in-PNG | [link](forensics/css-ctf-2026/echoes-of-the-relay.md) |
| Forensics | The False Timeline | 66 | log/timeline correlation + AES-GCM key derivation | [link](forensics/css-ctf-2026/the-false-timeline.md) |
| Forensics | Signal Fracture | 100 | — | team |
| Forensics | Ghost Frequency | 115 | — | team |
| Steganography | Colour Shift | 45 | red-channel bit-plane stego (Pink Floyd) | [link](steganography/css-ctf-2026/colour-shift.md) |
| Reverse | prince walk | 50 | live memory editing (PINCE / `/proc/pid/mem`) | [link](reverse/css-ctf-2026/prince-walk.md) |
| Reverse | FLAPPY BOARD | 183 | RE integer physics + xorshift32, beam-search bot vs server API | [link](reverse/css-ctf-2026/flappy-board.md) |

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
