# Week 4 — Injection & Input Handling

**OWASP 2025:** A05 Injection · **CWE:** CWE-89 (SQLi), CWE-78 (command injection)

## Class and assessment contract

**Contact time: 150 minutes** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Build the lab image before class. In class you do Tasks 0–3 and 5; Task 4 is optional.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write which AI tool you used, if any, on the answer sheet.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (see Week 1 *Lab 0*); skim last week's recap.
2. **Slides, then class** — prepare the concepts before class. The 150-minute slot includes quiz/review 10, a brief/demo 15, the common practical core 100, debrief 20 and evidence/exit 5.
3. **Lab (in class)** — complete the bounded common practical core. Baseline login (5), bounded login bypass (15), UNION observation (20), command-injection observation (20), student parameterization/input patch with controls (40). Then complete the written section for your student ID this week (odd: Conventional 40; even: AIR-Sec 20/10/10), after class if needed.
4. **Submit before the next class** (homework tasks included) — worksheet PDF → `learn.zcr.ai/submit` · fixed code → GitHub (commit link on branch `wk04`) · weekly quiz → `learn.zcr.ai/quiz`. (How/where: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — add this week's finding + fix to your NoteVault report.

*Time breakdown and grading: [Week 4 worksheet](worksheet.md).*

## Objectives
- Exploit SQL and command injection.
- Explain why parameterized queries defeat injection.
- Apply input validation and output handling correctly.

## ⚔️ Signature game — "SQLi Warm-up"
Three core hits and one optional upload extension against this week's own app — no filters to bypass, the app has none:
1. **Hit #1 — Auth bypass** via SQLi (e.g. `alice'--`).
2. **Hit #2 — UNION dump:** steal every username and password.
3. **Hit #3 — Command injection** on `/ping`.
4. **Hit #4 — Unrestricted upload** with no type checks *(optional extension)*.
5. **Warm-up cleared:** write the assigned student patch and pass its normal/attack controls, then compare `solution_app.py` for the full reference (upload is an optional extension).

## Run the local target
```bash
docker compose build                       # once, before class, while online
docker compose up --no-build --pull never  # vulnerable_app.py at http://localhost:8080
```
The fixed version is `solution_app.py`.

## Student-written patch and control checks

Complete the TODOs in `student_patch.py`, then run `docker compose run --rm --no-deps --pull never injection-lab python student_checks.py` from this lab directory after building the image. The untouched template fails by design. `student_app.py` is the provided harness; the worksheet names the exact edits, normal-operation controls and attack/limitation tests. Commit your authored patch and record the tests. The existing reference application stays available for comparison.

## Deliverable
PoC payloads + the patched code + proof the fix blocks them.

## References
- https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
