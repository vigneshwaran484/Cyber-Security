# Welcome to Star City — Web, 46 pts

## Objective
A flashy animated landing page at `http://34.116.80.78:9981/`.
Hint: *"But is there more to be seen than meets the eye?"* Find the flag.
Flag format: `CSSCTF{...}`

## Concepts
- The **rendered page** ≠ the **source**. Anything sent to the browser is yours to read —
  HTML, linked CSS, JS, comments. CSS files can hold comments (`/* ... */`) the page never shows.
- "More than meets the *eye*" = look past what's painted on screen → read the raw assets.
- Flag was **base64**, then **URL-encoded** (`%7B` = `{`, `%7D` = `}`, `%7C` etc.).

## Steps
The HTML is tiny and just links a stylesheet:
```html
<link rel="stylesheet" href="style.css">
```
Pull the CSS directly (don't just eyeball the rendered page):
```bash
curl -s http://34.116.80.78:9981/style.css | tail -5
```
Last line, right after the final `@keyframes` block, is a lone comment:
```css
} /*Q1NTQ1RGJTdCd2VfQlUxTFRfdGhpc19jaXR5X2Zyb21fcjBja19hbmRfUjAxMSU3RA*/
```
Looks like base64 → decode, then URL-decode the result:
```bash
echo 'Q1NTQ1RGJTdCd2VfQlUxTFRfdGhpc19jaXR5X2Zyb21fcjBja19hbmRfUjAxMSU3RA' | base64 -d
# CSSCTF%7Bwe_BU1LT_this_city_from_r0ck_and_R011%7D
python3 -c "import urllib.parse;print(urllib.parse.unquote('CSSCTF%7Bwe_BU1LT_this_city_from_r0ck_and_R011%7D'))"
```
> In-browser: DevTools → **Sources/Debugger** → open `style.css` and scroll to the bottom,
> or just visit `http://34.116.80.78:9981/style.css` in the address bar.

## Flag
```
CSSCTF{we_BU1LT_this_city_from_r0ck_and_R011}
```

## Takeaway
First move on any web challenge: **read every asset the page loads**, not just the DOM.
`curl` the HTML, then every linked `.css`/`.js`, and grep for comments and base64-looking blobs.
Recognising the double-encoding (base64 → URL-encode) is the other half — decode in layers until
you see `CSSCTF{`. See [encoding-recognition cheatsheet](../../cheatsheets/encoding-recognition.md).
