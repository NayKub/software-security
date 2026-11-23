# Week 6 — Authentication, Sessions & Access Control

**OWASP 2025:** A01 Broken Access Control, A07 Authentication Failures · **CWE:** CWE-639 (IDOR), CWE-347 (improper signature verification), CWE-321 (weak hardcoded key)

## Class and assessment contract

**Contact time: 150 minutes** (09:05–11:50) = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Build the lab image before class. In class you do Tasks 0–3 and 5; Task 4 is optional.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. The shared local demo flags are the expected evidence; nothing is submitted on ctf.zcr.ai. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write which AI tool you used, if any, on the answer sheet.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); while online run `docker compose build` in this lab. Keep the resulting `kosen-swsec-week06:local` image for the class; it contains pinned Flask and PyJWT. Skim last week's recap.
2. **Slides, then class** — prepare the concepts before class. The 150-minute slot includes quiz/review 10, a brief/demo 15, the common practical core 100, debrief 20 and evidence/exit 5.
3. **Lab (in class)** — complete the bounded common practical core. Legitimate session (5), cross-user IDOR (20), unsigned JWT (15), weak-key JWT (15), student verification/ownership patch and controls (45). Then complete the written section for your student ID this week (odd: Conventional 40; even: AIR-Sec 20/10/10), after class if needed.
4. **Submit before the next class** (homework tasks included) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link on branch `wk06`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Distinguish authentication vs authorization.
- Exploit IDOR and broken access control.
- Identify JWT pitfalls (alg=none, weak secret) and fix token handling.

## 🗺️ Signature game — "IDOR Treasure Hunt + JWT Forgery"
Target: provided app with user objects and JWT auth (or Juice Shop).
1. **IDOR:** change an object/user id in a request to read another user's data.
2. **Privilege escalation:** use a forged token to become another regular user (e.g. impersonate "bob") — horizontal, not an admin-only function.
3. **JWT:** forge a token with `alg:none` or the exposed weak HMAC secret. The exercise demonstrates forgery; it does not ask students to brute-force an unknown key.
4. **Fix:** enforce a server-side ownership check on every object access (`order["owner"] != user`, not RBAC/ABAC), validate JWT alg + signature with a strong secret/key, and add deny-by-default checks.

## Run the local target

Once, before class, while online:
```bash
cd ~/software-security/labs/week06-authn-authz
docker compose build
```
Then, in class:
```bash
cd ~/software-security/labs/week06-authn-authz
docker compose up --no-build --pull never
```
This keeps running: the insecure `vulnerable_app.py` is on `http://localhost:8080`. Use a second terminal for the other commands. The fixed version is `solution_app.py`.

## Student-written patch and control checks

Complete the TODOs in `student_patch.py`, then run the checks in the prebuilt image from this lab directory:

```bash
docker run --rm --network none -v "$PWD":/lab -w /lab kosen-swsec-week06:local python student_checks.py
```

The untouched template fails by design. `student_app.py` is the provided harness; the worksheet names the exact edits, normal-operation controls and attack/limitation tests. Commit your authored patch and record the tests. The existing reference application stays available for comparison. Token-minting commands in the worksheet also use this image, so PyJWT is not required on the host.

## Deliverable
Exploits + your `student_patch.py` commit and positive/negative `student_checks.py` results, with a short explanation of JWT verification and object ownership. `solution_app.py` is comparison material; citing or running it does not replace the student-authored patch.


## References
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
