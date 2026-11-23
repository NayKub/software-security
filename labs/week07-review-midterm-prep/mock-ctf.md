# Week 7 — Two practice checkpoints

**02005094 · practice only · 70 minutes of the 150-minute review class (Tuesday 15 December, 09:05–11:50).** You redo the Week 4 and Week 6 patch tasks from a fresh, untouched copy. Nothing is submitted and nothing is marked. Your own Week 4 and Week 6 work stays exactly as it is.

## Before you start: make a practice copy

You already finished these files in Weeks 4 and 6, so their checks would pass straight away. Make a separate practice copy of the untouched starters instead. This does not change your real lab folders or your `wk04`/`wk06` branches. On Windows, type these in the Ubuntu app:

```bash
cd ~/software-security
mkdir -p ~/practice
git archive origin/main labs/week04-injection | tar -x -C ~/practice
git archive origin/main labs/week06-authn-authz | tar -x -C ~/practice
```

You now have `~/practice/labs/week04-injection` and `~/practice/labs/week06-authn-authz`. Edit the `student_patch.py` files there. If a check below passes before you have changed anything, ask your instructor.

## Checkpoint 1 — Injection control, 35 minutes

**File:** `~/practice/labs/week04-injection/student_patch.py`. Complete `authenticate()` with bound SQL values and `ping_argv()` with one parsed IPv4 argument list. Run the provided checks:

```bash
cd ~/practice/labs/week04-injection
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/exam:ro" -w /exam week04-injection-injection-lab:latest \
  python3 student_checks.py
```

Before your edit you should see `FAILED`; after a correct patch, `OK`. Record an ordinary login and IPv4 request that still work, plus a SQL payload and a shell-metacharacter host that are denied. In one sentence, explain how parameter binding and `shell=False` keep data out of code. The checker only pretends to run ping; it does not contact a network target.

## Checkpoint 2 — Token and object boundary, 35 minutes

**File:** `~/practice/labs/week06-authn-authz/student_patch.py`. Complete the pinned JWT verification and the server-side order-owner decision. Run the provided checks:

```bash
cd ~/practice/labs/week06-authn-authz
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/lab:ro" -w /lab kosen-swsec-week06:local \
  python3 student_checks.py
```

Before your edit you should see `FAILED`; after a correct patch, `OK`. Record owner success, cross-user denial, and one unsigned or wrong-audience token denial. Explain why a valid identity alone does not authorize access to another person's order. The checker runs the app inside Python; it does not start a web server.

If `docker run` says the image is missing, build it in the real lab folder while online: `cd ~/software-security/labs/week04-injection && docker compose build` (or `week06-authn-authz`).

## Debrief, in the 120–145 minute block

Open your Week 3 `migrate.py` and explain why a wrong password leaves an old MD5 record unchanged, and why a correct login can upgrade it to Argon2id. Review one scanner error versus a clean result from Week 2. These are discussion prompts, not extra 35-minute code tasks. The Week 9 practical also has a threat-model/scanner station and a password-migration station, so revise Weeks 2 and 3 as well.

For each checkpoint keep: your diff, the exact command and result, the root cause (the trust boundary), the legitimate and attack controls, and one limit. The real midterm practical uses its own exam pack. [Review schedule](README.md) · [Practical blueprint](../week09-midterm-practical/ctf.md).
