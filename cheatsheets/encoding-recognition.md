# Encoding recognition

How to tell what you're looking at, and how to decode it fast.

## Quick tells

| Looks like | It's probably | Decode |
|---|---|---|
| `eyJ...` | Base64 of JSON / **JWT** | `base64 -d`, or jwt.io / CyberChef JWT Decode |
| `A-Za-z0-9+/`, len ÷4, maybe `=` | **Base64** | `base64 -d` |
| `A-Za-z0-9_-`, no `+//=` | **Base64URL** | `base64 -d` after `tr '_-' '/+'` |
| only `0-9a-f`, even length | **Hex** | `xxd -r -p` |
| only `.` and `-`, `/` separators | **Morse** | CyberChef From Morse Code |
| only `0` and `1`, groups of 8 | **Binary** | CyberChef From Binary |
| shifted letters, readable structure | **Caesar/ROT** | brute all 25 shifts / ROT13 |
| letters-only + "keyword" hint | **Vigenère** | CyberChef Vigenère Decode |
| `=` heavy, uppercase+digits | **Base32** | `base32 -d` |

## Terminal one-liners
```bash
echo 'aGVsbG8=' | base64 -d                 # base64
echo '68656c6c6f' | xxd -r -p               # hex -> ascii
echo -n 'hello' | base64                    # encode
echo -n 'hello' | xxd -p                    # ascii -> hex
python3 -c "print(0b01001000)"              # binary -> int
```

## Rules of thumb
- **Onion / nested:** decode, look at output, decode again. Encodings stack.
- Try CyberChef's **Magic** operation — it auto-detects and chains common encodings.
- Base64 that starts with `eyJ` is *always* worth decoding — it's structured data.
