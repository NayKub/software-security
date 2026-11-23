# Week 15 — DevSecOps: Putting It Together

## Class and assessment contract

**Class: Tuesday 9 February 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the lab image before class (see below). In class you do the four **core tasks** in Part 3, all on your own machine; the GitHub pipeline and the Red/Blue game are an optional extension with no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10) and even student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. The demo flag is the same for everyone and is the expected evidence; nothing is submitted on ctf.zcr.ai. Write which AI tool you used, if any, on the answer sheet.

**Due:** Monday 15 February 2027, 23:59 (Thai time).

**OWASP 2025:** A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); while online run `cd ~/software-security/labs/week15-devsecops-pipeline` then `docker compose build`. Skim last week's recap.
2. **Slides, then class** — read `slides/week15.md` and the worksheet's Part 2 to prepare. Class opens with the weekly quiz (10 min) and a short explanation and demo (15 min).
3. **Lab (in class)** — start both services with `docker compose up --no-build --pull never` (insecure fails OPEN on `:8090`, secure fails CLOSED and logs on `:8091`) and do the four core tasks in the worksheet's Part 3 on your own machine. Then do the written section for your student ID this week (odd: AIR-Sec 20/10/10; even: Conventional 40), after class if needed. The GitHub pipeline and Red/Blue game are optional.
4. **Submit by Monday 15 February 2027, 23:59** — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link to `student_task.py` on branch `wk15`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Add logging/monitoring/alerting and fail-safe error handling.
- Build a CI/CD pipeline that enforces security gates.
- Understand vulnerability management and coordinated disclosure, framed by **CISA "Secure by Design"**.

## 🔴🔵 Signature game — "Break the Build" (Red vs Blue)
Use this lab's own pipeline template as the starting point: [`security-ci.yml`](security-ci.yml) (wiring steps in [`README-pipeline.md`](README-pipeline.md)).
- **Blue team** builds the gate:
  1. Add **SAST** (Semgrep), **SCA + IaC** (Trivy), and **secret scanning** (Gitleaks) jobs.
  2. Configure Semgrep to fail on selected-rule findings, Trivy on HIGH/CRITICAL, and Gitleaks on detected secrets; upload SARIF to the GitHub Security tab. Gate-step scanner errors also fail.
  3. Add structured security logging + an alert on auth failures; ensure errors **fail closed**, not open.
- **Red team** submits PRs trying to sneak a vuln/secret past the gate.
- **Score:** Blue gets points for each catch, Red for each bypass.

## Hand-in and extended pipeline practice
Required core: the student function diff, local failing-then-passing checker output, the fail-open/fail-closed responses and log line, and your explanation. The full scanner PR exercise below is retained as extended project practice; its scoreboard does not add course points.

## References
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- https://docs.github.com/actions
