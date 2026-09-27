# Dev notes — Web, 75 pts

## Objective
"A developer left a debug message that prints every time this challenge opens. Users never see it. You can."

## Concepts
- "Prints" in a web page almost always means **`console.log()`**.
- Console output does not appear on the page — it goes to DevTools → **Console**, which normal users never open.
- `console.debug` messages can be hidden unless the **Debug/Verbose** log level is enabled.

## Steps
1. F12 → **Console** tab.
2. If nothing is there, **close and reopen the challenge popup** with the Console visible (the log fires *on open*).
3. Ensure log-level filters **Logs** and **Debug** are enabled.
4. Filter box: type `CTF{`.

## Flag
```
CTF{c0ns0le_d0t_l0g}
```

## Takeaway
The Console is a first-class hiding spot. Also note: this site shipped the **entire challenge
list in a JS array** in the page source — a real "client-side secret" leak. Anything sent to the
browser can be read by the user.
