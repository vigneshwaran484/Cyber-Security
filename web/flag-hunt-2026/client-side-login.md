# Client-side login — Web, 100 pts

## Objective
An admin panel checks the password **in the browser**. The JS was shipped to the client:
```js
function login(pw) {
  if (btoa(pw) === "c3VwM3JfczNjcmV0") {
    const f = atob("fXR...RlRD");
    show(f.split("").reverse().join(""));
  }
}
```

## Concepts
- `btoa()` = **encode** to Base64. `atob()` = **decode** from Base64.
- Base64 is an **encoding, not encryption** — no key, fully reversible.
- The password and the flag are both sitting in client-side code.

## Steps
```bash
# recover the password: decode the compared Base64
echo 'c3VwM3JfczNjcmV0' | base64 -d          # -> sup3r_s3cret

# OR decode the flag directly (it's Base64 then reversed)
echo 'fXR...RlRD' | base64 -d | rev           # rev = .reverse()
```
- Path A: type the recovered password into the box, log in, read the flag.
- Path B: replicate the JS: `base64 -d | rev`.
- Browser console equivalent: `atob("...").split("").reverse().join("")`.

## Flag
```
CTF{never_trust_the_client}
```

## Takeaway
Any check done in the browser can be read and bypassed. **Real authentication must happen on
the server.** Recognise Base64: `A-Za-z0-9+/`, length multiple of 4, maybe `=` padding.
