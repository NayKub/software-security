# Week 17 — Two practice checkpoints

**02005094 · practice only · 70 minutes of the 150-minute review class (Tuesday 23 February 2027, 09:05–11:50).** You redo the Week 10 and Week 14 student tasks from a fresh, untouched copy. Nothing is submitted and nothing is marked. Your own Week 10 and Week 14 work stays exactly as it is.

## Before you start: make a practice copy

You already finished these files in Weeks 10 and 14, so their checks would pass straight away. Make a separate practice copy of the untouched starters instead. This does not change your real lab folders or your `wk10`/`wk14` branches. On Windows, type these in the Ubuntu app:

```bash
cd ~/software-security
mkdir -p ~/practice17
git archive origin/main labs/week10-api-security | tar -x -C ~/practice17
git archive origin/main labs/week14-ai-llm-security | tar -x -C ~/practice17
```

You now have `~/practice17/labs/week10-api-security` and `~/practice17/labs/week14-ai-llm-security`. Edit the `student_task.py` files there. If a check below passes before you have changed anything, ask your instructor.

## Checkpoint 1 — Who may read what, and which fields a client may set (35 minutes)

**File:** `~/practice17/labs/week10-api-security/student_task.py`. Complete `may_read_orders()` and `bind_creation_fields()`. Run the provided checks:

```bash
cd ~/practice17/labs/week10-api-security
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/work:ro" -w /work kosen-swsec-week10:local \
  python3 check_student.py
```

Before your edit you should see `FAILED (failures=3, errors=1)`; after a correct edit, `OK`. Record:

- a user reading their own orders, and an admin (whose role comes from the server's own user record, not from the request) reading any orders: both allowed;
- one user reading another user's orders: denied;
- an account-creation request that sends `"is_admin": true`: the field is ignored or rejected.

In one sentence, explain why the `X-User-Id` header in this lab is only a stand-in for "who is logged in" and is not real authentication. The checker does not open a port or use the network.

## Checkpoint 2 — Treat model output as untrusted text (35 minutes)

**File:** `~/practice17/labs/week14-ai-llm-security/student_task.py`. Complete `render_model_output()`: first remove the exact secret value you were given, then HTML-escape the text so a web page shows it as plain text instead of running it. Run the provided checks:

```bash
cd ~/practice17/labs/week14-ai-llm-security
docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$PWD:/lab:ro" -w /lab kosen-swsec-week14:local \
  python3 check_student.py
```

Before your edit you should see `FAILED (errors=4)`; after a correct edit, `OK`. Record:

- ordinary text that still reads normally;
- HTML markup (for example a `<script>` or `<img>` tag) that is shown as text and does not run;
- the secret text that no longer appears.

In one sentence, explain why passing this small local test cannot prove that a real online AI model, or the tools it is allowed to call, is safe.

## Debrief (minutes 120–145)

These are talk-through questions, not extra coding tasks:

- [Week 11 Rust counter](../week11-memory-safety-exploitation/student_safe.rs): how does the number of bytes differ from the number of Unicode characters, and what should happen with broken UTF-8 input?
- [Week 12 signature example](../week12-supply-chain/signature-core/manifest.json): why must a signature fail when it is valid but made with a key you do not trust?
- [Week 15 checker](../week15-devsecops-pipeline/check_student.py): when the lookup throws an error, why should the code deny access and log only the error type, never the token text?

For each checkpoint keep: your diff, the exact command and what it printed, the root cause (which trust boundary was crossed), one allowed and one denied example, and one limit. The final practical has its own pack. [Review schedule](README.md) · [Final practical overview](../week19-final-ctf-capstone/ctf.md).
