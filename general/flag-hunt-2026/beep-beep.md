# Beep beep — General, 50 pts

## Objective
"An old signal from a ship at sea" — a string of dots and dashes. Decode and wrap in flag format
(lowercase, underscores for spaces).

## Concepts
- Dots/dashes + "signal"/"beep"/"ship at sea" = **Morse code**.
- Space between groups = **letter** gap. ` / ` = **word** gap.
- Two `/` in the message → three words → `_` between them.

## Steps
- **CyberChef:** paste the morse → recipe **From Morse Code** (letter delimiter = Space, word
  delimiter = Slash).
- **By hand:** match each group with the table:
  ```
  A .-   B -... C -.-. D -..  E .    F ..-. G --.  H .... I ..   J .---
  K -.-  L .-.. M --   N -.   O ---  P .--. Q --.- R .-.  S ...  T -
  U ..-  V ...- W .--  X -..- Y -.-- Z --..
  ```
- Then: lowercase, spaces → `_`, wrap in `CTF{}`.

## Flag
```
CTF{...}   <!-- your decoded morse -->
```

## Takeaway
Recognise Morse instantly: only two symbols, groups by spaces, words by `/`.
One wrong dot/dash flips a letter (`.-`=A vs `.-.`=R), so type carefully.
