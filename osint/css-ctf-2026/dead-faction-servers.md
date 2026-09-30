# Dead Faction Servers — OSINT / Git Forensics

## Objective
Find a developer's leaked key across their public GitHub. Handle: **`bobdev508`**, with repos
`decoy-project` and `dashboard-app`. Flag format: `CSSCTF{...}`.

## Concepts
- **Decoys**: planted fake flags use the *wrong* prefix `CTF{...}` (e.g. `CTF{th1s_1s_n0t_th3_r34l_fl4g}`)
  instead of `CSSCTF{...}` — an instant tell to ignore them.
- **Git remembers everything**: deleted files still live in commit history; unmerged branches carry
  content the default branch never shows. `git log --all -p` surfaces both.
- The real key is **split across two hidden places** in `dashboard-app`.

## Steps
```bash
git clone https://github.com/bobdev508/dashboard-app
cd dashboard-app
git log --all -p          # every commit on every branch, with diffs
git branch -a             # list remote branches too
```
**Part 1 — deleted file in history.** Commit `be82c69` added `.env.local`; commit `99291d3`
("Remove committed secrets, oops") deleted it. The diff shows:
```
SECRET_PART=Q1NTQ1RGe3VfZzA=
```
```bash
echo 'Q1NTQ1RGe3VfZzA=' | base64 -d   # -> CSSCTF{u_g0
```
**Part 2 — unmerged branch.** `origin/experimental/auth-rework` contains `auth_notes.md`:
```
bypass_suffix = "t_130d_508}"
```
```bash
git show origin/experimental/auth-rework:auth_notes.md
```
Join the two halves.

## Flag
```
CSSCTF{u_g0t_130d_508}
```

## Takeaway
On any git-based OSINT: never trust the current checkout. `git log --all -p` (deleted files, all
branches), `git branch -a` / `git show <branch>:<file>` for unmerged work, and treat wrong-prefix
"flags" as decoys. Secrets "removed, oops" are still one command away.
See [web-payloads / recon notes](../../cheatsheets/web-payloads.md).
