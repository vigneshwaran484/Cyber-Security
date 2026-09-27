# Guest pass — Web, 150 pts

## Objective
A dashboard decides who you are from "a value stored in your browser." You're a guest; guests see nothing.

## Concepts
- Browser-side identity lives in **Cookies**, **Local Storage**, or **Session Storage** — all
  fully controlled by the user.
- If a value is stored client-side and trusted by the app, you can **edit it**.

## Steps
1. F12 → **Storage** (Firefox) / **Application** (Chrome).
2. Under **Local Storage** → the site origin, found:
   | Key | Value |
   |---|---|
   | `flaghunt-lab:role` | `guest`  ← target |
   | `flaghunt:code` | `"QQMMTC"` (team code — leave) |
   | `flaghunt:me` | `"Vigneshwaran C"` (leave) |
3. Double-click `guest` → change to `admin` → Enter.
   Value is stored *without quotes* (plain string), so write `admin` unquoted.
4. Click **Open dashboard** again — page re-reads the value.

   Console equivalent:
   ```js
   localStorage.setItem("flaghunt-lab:role", "admin")
   ```

## Flag
```
CTF{st0rage_is_user_c0ntr0lled}
```

## Takeaway
This is **broken access control / client-side trust**. Permissions stored in the browser are only
suggestions. The server must verify roles, never trust cookies/storage/hidden fields blindly.
