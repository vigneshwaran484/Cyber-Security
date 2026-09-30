# The False Timeline — Forensics, 66 pts

## Objective
An incident set: logs, an SQLite `metadata.db`, an `audit.log`, and AES-GCM `.ekey-cache` files.
The logs blame user **KAI-7**, but the timeline was tampered. Find who really did it (and decrypt the
key). Flag: `CSSCTF{...}`.

## Concepts
- **Timeline / log forensics**: cross-check multiple sources — an attacker can edit one log but not
  all of them (session records, audit trail, file mtimes).
- **AES-GCM key derivation**: the decryption key is `SHA256(machine_id | session_uuid | event_epoch)`;
  the forged story points at the wrong session, so using the *real* actor's session recovers the key.

## Steps
1. **The false story** — `relay.log` says an export request was accepted for principal **KAI-7** at
   **03:17:03** (2101). But that timestamp is the fake.
2. **KAI-7's real activity** — `metadata.db` shows KAI-7's SSH session ran **02:52:05 → 03:05:41** and
   ended *before* 03:17. KAI-7 couldn't have triggered the 03:17 export → framed.
3. **The real actor** — at **03:10:02** `root` ran `su` to become **`sve-relay`**, and that second
   session launched the `emergency_export` job (epoch **4157543568**), per `audit.log`.
4. **The cover-up** — the last audit entry shows **uid 998** running `touch -r ... .ekey-cache` to
   back-date the cache and match the fabricated 03:17 story. `.ekey-cache` is owned by uid 998 =
   sve-relay.
5. **Decrypt** — rebuild the key with the **real** actor: `exporter.py` computes
   `SHA256(machine_id | session_uuid | event_epoch)`. Using sve-relay's real session (not KAI-7's
   forged one) decrypts the `.ekey-cache` and yields the flag.

Verdict: **KAI-7 was framed** by sve-relay (uid 998), who back-dated the evidence.

## Flag
```
CSSCTF{kai_did_not_do_it}
```

## Takeaway
Never trust a single log. **Correlate** session records, audit trails, and file timestamps — the
attacker edits the story in one place (`relay.log`) but the session DB and audit log betray the real
actor and a `touch -r` back-dating. When a key is derived from event metadata
(`machine_id|session|epoch`), the *forensic* answer (who/when) is literally what unlocks the crypto.
