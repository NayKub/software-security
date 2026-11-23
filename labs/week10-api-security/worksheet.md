# Worksheet 10 — API Security

> **Course:** Software Security (KOSEN69) · **Week 10**
> **Aligned:** OWASP API Security Top 10:2023 — **API1** BOLA (reading another user's objects) · **API3** Broken Object Property Level Authorization (mass assignment) · **API4** Unrestricted Resource Consumption (no rate limit)
> **Signature game:** 🥷 **Local API Raid** — read orders that aren't yours, make yourself admin, and hammer a login that never says stop.

> ⚠️ **Ethics note:** Attack only the two lab APIs on this machine (`http://localhost:8080` and `http://localhost:8081`) or your own OWASP crAPI copy. Doing this to any real service is unauthorized access.

## Class and assessment contract

**Class: Tuesday 5 January 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the lab image before class (see below). In class you do Tasks 0–3 and 5; Task 4 is optional.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 10 answer sheet for your format (odd ID: Conventional file; even ID: AIR-Sec file), and say there which AI tool you used, if any.

## Words you will see

| Word | Meaning |
| --- | --- |
| **API** | A web address that programs (not people) call, usually sending and receiving JSON. |
| **BOLA** | Broken Object Level Authorization: the server does not check that the object in the URL (here, a user's orders) belongs to the caller. |
| **Mass assignment** | The server copies every field from your request into its record, including fields like `is_admin` that only the server should set. |
| **Allow-list** | A fixed list of the only fields a client may set; everything else is ignored. |
| **Rate limit** | The server counts requests and refuses extra ones (HTTP `429`) inside a time window. |
| **`X-User-Id` header** | This lab's stand-in for "who is calling". Anyone can type any value into a header, so a real app would use a verified, signed token instead. |
| **401 / 403 / 429** | 401 = "who are you?" (no identity) · 403 = "you are known, but not allowed" · 429 = "too many requests". |

## Part 1 — Student Information

Fill these in at the top of your answer sheet:

| Name | Student ID | Date | Code link (branch wk10) | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

## Part 2 — Lecture Questions

Answer in 2–4 sentences each. (Everyone should read these to prepare; only Conventional answers them for marks.)

1. Define **BOLA (API1:2023)**. Why is it the #1 API risk, and why can't a WAF (web application firewall) reliably stop it?
2. What is **mass assignment / broken object property level authorization (API3:2023)**? Contrast a blocklist with an allow-list of fields a client may set.
3. **API4:2023** is unrestricted resource consumption. Give two different impacts (one security, one availability) of a `/api/login` with no rate limit.
4. The vulnerable `get_orders()` route in `vulnerable_api.py` does not call `current_user()` at all. The fixed route uses the `X-User-Id` header as a teaching stand-in for identity. Why is a header the client sets NOT authentication, and what must a real system use to identify the caller before checking ownership?
5. Why must object-level authorization be checked **on every request, for every object**, rather than once at login?

## Part 3 — Shared practical core (100 min in class)

**100-minute core:** probe BOLA, mass assignment and the rate limit (Tasks 0–3, 35) · write your two controls in `student_task.py` (35) · run the checker and show positive and negative results (20) · explain the limits (10).

The minute labels are time budgets, not points. Task 4 is optional home practice and adds no points. Complete Part 2/Part 4 only for the assigned Conventional 40, or Audit/EiPE/Prompt only for the assigned AIR-Sec 40.

**Learning goals:** see BOLA, mass assignment and a missing rate limit on a live local API, then write per-object authorization and allow-list binding in `student_task.py` and prove them with `check_student.py`. `solution_api.py` (the fixed API on port 8081) is a comparison reference.

**Prerequisites:** Docker + Docker Compose and `curl`. Working folder: `~/software-security/labs/week10-api-security/`. On Windows, type every command in the Ubuntu app. The prebuilt image supplies Python and Flask for both APIs and the checker. No host Python or Flask install is required.

**Before class — build once while online:**
```bash
cd ~/software-security/labs/week10-api-security
docker compose build
```
You should see the build finish with lines ending in `Built`.

### Environment setup

You need **two terminal windows**, both in the lab folder. In window A, start both APIs:
```bash
cd ~/software-security/labs/week10-api-security
docker compose up --no-build --pull never
```
This starts the **insecure** API (`vulnerable_api.py`) on `http://localhost:8080` and the **secure** reference API (`solution_api.py`) on `http://localhost:8081`. It keeps running and does not give you the prompt back: that is correct. If you see `No such image`, run `docker compose build` while online first. Type every command below in window B:
```bash
cd ~/software-security/labs/week10-api-security
```
Seeded users: **alice** (id 1), **bob** (id 2), **carol** (id 3, admin, balance 9999).

**What to submit per task:** the exact command, the response or HTTP status, a stamped screenshot, and a 2–3 sentence note naming the OWASP API id.

---

**Task 0 — Onboarding (part of the 35-minute probe).** Check both APIs answer:
```bash
curl http://localhost:8080/
curl http://localhost:8081/
```
You should see `Week 10 INSECURE API — see attack.md` from 8080 and `Week 10 SECURE API` from 8081. *Deliverable: both responses + the three seeded users.*

![One REST API with three flaws — reading another user's orders by id, smuggling an admin field into user creation, and an unthrottled login — each shown at the handler where it occurs, next to its one-line fix.](img/api-flaws.svg)

**Task 1 — BOLA: read another user's orders (API1).**
- *Goal:* read carol's (admin) orders without being carol.
- *Steps:* on the insecure API, ask for carol's and then bob's orders:
  ```bash
  curl http://localhost:8080/api/users/3/orders
  curl http://localhost:8080/api/users/2/orders
  ```
  You should see carol's `Server rack` order plus an item holding a demo `FLAG{...}`, then bob's order `[{"item":"Mouse","order_id":"B-1","total":15}]`. You never logged in. The demo flag is the same for everyone: paste it in the Task 1 box as evidence; nothing is submitted on ctf.zcr.ai.
- Now try the same idea on the secure API, three ways:
  ```bash
  curl -i http://localhost:8081/api/users/3/orders
  curl -i -H "X-User-Id: 1" http://localhost:8081/api/users/3/orders
  curl -i -H "X-User-Id: 1" http://localhost:8081/api/users/1/orders
  ```
  The first line of each answer shows `401` (no identity), `403` (alice may not read carol's orders), then `200` (alice reads her own).
- *Deliverable:* the leaked order JSON + the 401/403/200 results + a note mapping this to API1.

**Task 2 — Mass assignment: make yourself admin (API3).**
- *Goal:* sneak `is_admin` and `balance` into a new account.
- *Steps:* create a user on the insecure API, then send the same request to the secure API:
  ```bash
  curl -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"username":"mallory","password":"x","is_admin":true,"balance":1000000}'
  curl -X POST http://localhost:8081/api/users -H "Content-Type: application/json" -d '{"username":"mallory","password":"x","is_admin":true,"balance":1000000}'
  ```
  From 8080 you should see `"is_admin":true`, `"balance":1000000` and a `"flag"` field holding a demo `FLAG{...}` (the same for everyone). From 8081 you should see `"is_admin":false` and `"balance":0`: the extra fields were ignored.
- *Deliverable:* both responses side by side + a note mapping this to API3 (allow-list).

**Task 3 — No rate limit: guess passwords (API4).**
- *Goal:* show the insecure `/api/login` never slows you down, and the secure one does.
- *Steps:* four guesses on the insecure API (the last one is alice's real password):
  ```bash
  for pw in wrong1 wrong2 wrong3 alice123; do curl -s -X POST http://localhost:8080/api/login -H "Content-Type: application/json" -d "{\"username\":\"alice\",\"password\":\"$pw\"}"; echo; done
  ```
  You should see `{"ok":false}` three times, then `{"is_admin":false,"ok":true,"user_id":1}`. Now seven wrong guesses on the secure API:
  ```bash
  for i in $(seq 1 7); do curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8081/api/login -H "Content-Type: application/json" -d '{"username":"alice","password":"wrong"}'; done
  ```
  You should see seven lines: `401` five times, then `429` twice. If every line is `429`, you already ran it in the last minute: wait 60 seconds and run it again.
- *Deliverable:* the `401 401 401 401 401 429 429` result + a note mapping this to API4.

**Task 4 — Optional home practice: crAPI (no extra points).**
OWASP crAPI is a much larger vulnerable API you can run on your own machine (`git clone https://github.com/OWASP/crAPI.git`, then follow its own setup guide). Capture one BOLA or mass-assignment flag and note the endpoint and OWASP API id. Skip this if your laptop is short of disk space or memory.

**Task 5 — Write your controls (55 min, in class) 🛡️.**
- *Goal:* write the two decisions that close Tasks 1 and 2 in `student_task.py`: who may read which orders, and which fields a client may set.
- *Steps:*
  1. Run the checker before editing, and keep the result:
     ```bash
     docker run --rm --network none -v "$PWD:/work:ro" -w /work kosen-swsec-week10:local
     ```
     You should see `FAILED (failures=3, errors=1)`. That is expected: nothing is written yet.
  2. Open `student_task.py` (`code student_task.py`, or `nano student_task.py`; in nano save with Ctrl+O then Enter, exit with Ctrl+X).
  3. In `may_read_orders(caller_id, target_id, is_admin)`, replace the `raise NotImplementedError(...)` line with one `return` line that is `True` only when the caller is reading their own orders, or the caller is an admin.
  4. In `bind_creation_fields(body)`, replace the `raise` line with one `return` line that builds a new dictionary containing only `username` and `password` (when they are present in `body`), and nothing else.
  5. Save, then run the same checker command again. You should see `Ran 5 tests` and `OK`.
- *Deliverable:* your `student_task.py` commit link, the before (`FAILED`) and after (`OK`) results in one stamped screenshot, and the diff of your two lines.
- *Explain (10 min):* open `solution_api.py` and find the three `# --- FIX ...` blocks. For API1, API3 and API4, write which exploit from Tasks 1–3 each block stops and the new HTTP result you saw on port 8081. Then explain why a client-set `X-User-Id` header and an in-memory, per-IP limiter are not complete real-world controls.

Submit your code link: commit `student_task.py` to branch `wk10` in your own fork and push (see [SUBMISSION.md](../../SUBMISSION.md); do not open a pull request). The supplied `solution_api.py` is the complete reference; copying or running it does not demonstrate your own control.

## Part 4 — Reflection

1. **Mapping:** complete a table — finding | endpoint | OWASP API id | fix applied — for all three findings.
2. **Evidence-based case:** read the [OWASP API1 example scenarios](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/) or a primary report of a real API access-control incident. Say what the source actually shows, and label anything you are guessing. Explain whether the ownership check in `solution_api.py` would have helped, and why. Do not claim a named breach was BOLA unless the source says so.
3. **Best mitigation:** of object-level authorization, allow-list binding and rate limiting, which gives the most risk reduction for an API platform, and why?

## Grading rubric (100)

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Common practical: main task and observations | 20 | 20 |
| Common practical: your controls and positive/negative tests | 20 | 20 |
| Common practical: reproducible evidence, reasoning and limits | 20 | 20 |
| Assigned Conventional Part 2 written questions | 20 | — |
| Assigned Conventional Part 4 reflection | 20 | — |
| Assigned Audit-the-AI | — | 20 |
| Assigned Explain-in-Plain-English | — | 10 |
| Assigned Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

**Due:** Monday 11 January 2027, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Flags this week:** the local lab prints the same demo `FLAG{...}` values for everyone (one in Task 1, one in Task 2). They are the expected evidence: paste them in those boxes with your stamped screenshots, and leave the "Personalized flag" field blank. Nothing is submitted on ctf.zcr.ai. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

**The statement to audit (it is deliberately wrong):**

> "An API is secure once it requires an X-User-Id header; an allow-list can still copy is_admin because only administrators know that field name."

Find the substantive mistakes (8), check your criticism with your own results from Tasks 1–3 or a reliable source (8), and write a justified correction (4). Cover both the identity claim and the allow-list claim. You can earn the full 20 by auditing this statement, without an AI account.

Optional extra practice (no marks): ask an AI assistant to fix this week's vulnerability, quote any wrong or risky line, and verify your own correct version. A correct AI answer is allowed: verify it rather than inventing an error.

> Write which AI tool you used, if any, in the table at the top of your answer sheet. Conventional does not do this section for marks.

---

## 🧠 Comprehension & Prompt — assigned AIR-Sec section (10 + 10)

**A. Explain in Plain English (EiPE, 10).** In 2–3 sentences, in your own words, describe what this week's vulnerable endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem (10).** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Run it if you have an AI tool, then check the result with `check_student.py` or your Task 1–2 requests. If you have no AI tool, submit the final prompt, the tests it must pass, and your own verified implementation. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
