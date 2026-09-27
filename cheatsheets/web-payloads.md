# Web payloads & tricks

## Where to look first (every web challenge)
1. **Elements/DOM** — hidden HTML, comments, `data-*`
2. **Console** — `console.log` leaks
3. **Sources/Debugger** — read the site's JS (Ctrl+Shift+F to search all files)
4. **Network** — server responses, headers, API JSON
5. **Storage/Application** — cookies, localStorage, sessionStorage

## SQL injection (auth bypass)
```
admin'--          # comment out password check
admin'--          # trailing space (MySQL)
admin'#           # MySQL comment
' OR '1'='1       # always-true condition
' OR 1=1 LIMIT 1--
```
Fix: **parameterized queries**. Payload goes in the *input field*, not the JS console.

## JWT (eyJ...)
- Decode payload: it's public Base64 — `base64 -d`.
- **Forge if signature unchecked:**
  - `alg: none` attack — set header alg to `none`, strip signature.
  - Weak HMAC secret — crack with `hashcat -m 16500` or `jwt_tool`.
- Tool: `jwt_tool <token>`.

## Client-side trust
- `localStorage.setItem("role","admin")` then re-trigger the check.
- Edit cookies in Storage tab. Base64/JSON values: decode → edit → re-encode.

## Other classes to learn
| Class | Idea |
|---|---|
| **XSS** | inject `<script>` into reflected/stored input |
| **IDOR** | change an `id=` in the URL to access others' data |
| **SSRF** | make the server fetch a URL you control |
| **SSTI** | template injection: `{{7*7}}` → 49 |
| **Path traversal** | `../../etc/passwd` |

## Meta-rule
**Never trust the client.** Anything sent to the browser can be read & modified.
