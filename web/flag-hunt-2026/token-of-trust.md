# Token of trust — Web, 100 pts

## Objective
Given an intercepted login token "the app thinks is secret." Read what's inside.

## Concepts
- A string starting with **`eyJ`** is Base64 of `{"` → almost always **JSON / a JWT**.
- A **JWT** has 3 dot-separated parts: `header.payload.signature`.
- A JWT is **signed, not encrypted**. The signature stops *modification*; it does **not** hide
  the contents. Header and payload are just Base64 — anyone can read them.

## Steps
```bash
# split the token
echo "$T" | cut -d. -f2        # the payload (field 2)

# decode it (JWTs strip Base64 padding, so add '=' back)
echo 'eyJ1c2VyIjoic3R1ZGVudC...In0=' | base64 -d
# {"user":"student","role":"guest","note":"CTF{jwt_payloads_are_public}"}
```
- `cut -d. -f2` → split on `.`, take field 2.
- `base64 -d` → decode. Append `=`/`==` to fix stripped padding.

## Flag
```
CTF{jwt_payloads_are_public}
```

## Takeaway
The JWT payload is **public**. Never store secrets in it. Next level: if the server doesn't verify
the signature properly, you can **forge** the payload — see `alg:none` and weak-HMAC attacks
in [web-payloads cheatsheet](../../cheatsheets/web-payloads.md).
