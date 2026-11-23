# Week 10 — API Security

**OWASP API Security Top 10:2023:** API1 BOLA (reading another user's objects) · API3 broken object property level authorization (mass assignment) · API4 unrestricted resource consumption (no rate limit)

## Class and assessment contract

**Class: Tuesday 5 January 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the lab image before class. In class you do Tasks 0–3 and 5; Task 4 is optional.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. The shared local demo flags are the expected evidence; nothing is submitted on ctf.zcr.ai. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write which AI tool you used, if any, on the answer sheet.

**Due:** Monday 11 January 2027, 23:59 (Thai time).

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); while online run `docker compose build` in this lab folder. It makes the `kosen-swsec-week10:local` image with Flask for both APIs and the checker. Skim last week's recap.
2. **Slides, then class** — read `slides/week10.md` and the worksheet's Part 2 to prepare. Class opens with the weekly quiz (10 min) and a short explanation and demo (15 min).
3. **Lab (in class)** — follow the worksheet's Part 3: probe the three bugs on ports 8080 and 8081 (35 min), write your two controls in `student_task.py` (35), run the checker (20) and explain the limits (10). Then do the written section for your student ID this week (odd: Conventional 40; even: AIR-Sec 20/10/10), after class if needed.
4. **Submit by Monday 11 January 2027, 23:59** — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link on branch `wk10`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Explain why an API must check the caller and the requested object on every request.
- Exploit BOLA and mass assignment, and see a missing rate limit.
- Write per-object authorization and allow-list binding in `student_task.py`; explain the reference API's rate limiter and why the `X-User-Id` header is not real authentication.

## 🥷 Signature game — "Local API Raid"
Target: **the two local APIs below** (the graded lab).
1. **BOLA:** read another user's orders by changing the id (`/api/users/<id>/orders`).
2. **Mass assignment:** sneak `is_admin` and `balance` into `POST /api/users`.
3. **No rate limit:** hammer `/api/login`; the secure API answers `401` five times, then `429`.
4. **Fix:** write the two controls in `student_task.py`, then find the matching fix in `solution_api.py`.

> **Optional home practice (no marks): crAPI** — OWASP's own, much larger vulnerable API. Run it only on your own machine: `git clone https://github.com/OWASP/crAPI.git`, then follow its setup guide.

## Run the local target

Once, while online:
```bash
cd ~/software-security/labs/week10-api-security
docker compose build
```
Then, in class:
```bash
docker compose up --no-build --pull never
```
This keeps running: the insecure `vulnerable_api.py` is on `http://localhost:8080` and the secure `solution_api.py` is on `http://localhost:8081`. Use a second terminal for the curl commands.

## Student task and checker

Complete the two functions in `student_task.py`, then run the checker from this lab folder (no network or port is used):
```bash
docker run --rm --network none -v "$PWD:/work:ro" -w /work kosen-swsec-week10:local
```
The untouched starter fails by design (`FAILED (failures=3, errors=1)`); after your edit it should say `OK`. Keep both results. `python3 check_student.py` runs the same checks if Flask is installed on your machine.

## Deliverable
Findings with their OWASP API ids, your `student_task.py` commit link and before/after checker results, and a short explanation. `solution_api.py` is comparison material; running or copying it does not replace your own control.

## References
- https://owasp.org/API-Security/  ·  https://github.com/OWASP/crAPI
