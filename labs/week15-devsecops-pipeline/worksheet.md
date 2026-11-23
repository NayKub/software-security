# Worksheet 15 — DevSecOps: Putting It Together

> **Course:** Software Security (KOSEN69) · Week 15
> **Aligned to:** OWASP 2025 **A09 Security Logging & Alerting Failures** · **A10 Mishandling of Exceptional Conditions** (scanners also cover A02/A03/A07) · **CWE-636** (fail open), CWE-532 (logging sensitive data), CWE-209, CWE-489, CWE-798
> **Signature game:** 🔴🔵 *Break the Build* (Red vs Blue) — Blue scores per catch, Red scores per bypass.

> ⚠️ **Ethics note:** The pipeline and `sample-service.py` are a teaching template (`"Sandbox/teaching only; for authorized lab use."`). Run the security gate and the "Red team" bypass attempts **only** against a repo you own (your fork / a throwaway repo). Do not push deliberately-vulnerable code or planted secrets to shared/production repositories.

## Class and assessment contract

**Class: Tuesday 9 February 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the lab image before class (see below). In class you do the four **core tasks** in Part 3, all on your own machine; the GitHub pipeline and the Red/Blue game are an optional extension with no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10) and even student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 15 answer sheet for your format (odd ID: AIR-Sec file; even ID: Conventional file), and say there which AI tool you used, if any.

## Words you will see

| Word | Meaning |
| --- | --- |
| **DevSecOps** | Building security checks into everyday development, so problems are caught automatically. |
| **CI pipeline** | Steps GitHub (or another service) runs on every push, such as tests and security scans. A failing step turns the build red. |
| **Fail-closed / fail-open** | When something goes wrong, fail-closed **denies** access; fail-open accidentally **allows** it. |
| **Exception** | An error in running code. `except Exception` catches almost any error. |
| **Security log** | A record of who tried what and whether it was allowed. It must never contain passwords or tokens. |
| **Red / green run** | A test run that fails (red) or passes (green). Here, red before your fix and green after. |

---

## Part 1 — Student Information

Fill these in at the top of your answer sheet:

| Name | Student ID | Date | Code link (branch wk15) | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

---

## Part 2 — Lecture Questions

Answer in your own words (2–4 sentences each). Everyone should read these to prepare; only Conventional answers them for marks.

1. `README-pipeline.md` says each tool runs **twice** (report step, then gate step). Explain what each step is for: why the report step never fails, why the upload step uses `if: always()`, why the Security tab can show findings that the gate lets through (hint: the severity filter), and which step turns the build red.
2. What is the difference between **fail-closed** and **fail-open**? In `sample-service.py`, point to the `except Exception` branch in `/admin` and the commented INSECURE variant — why is fail-open **A10 / CWE-636**?
3. The `permissions:` block in `security-ci.yml` is `contents: read`, `security-events: write`. Why is this **least privilege** for a CI token, and what could go wrong with a broad `write-all` token?
4. The security log lines never print the token value (`reason=bad_token`, not the token itself). Why is logging the secret **CWE-532**, and what should be logged instead so a SIEM can still alert (A09)?
5. Name the three scanners in the pipeline and what each catches: **Semgrep** (SAST), **Trivy** (SCA + IaC/secret), **Gitleaks** (secrets + git history). Which OWASP categories does each map to per the README table?

---

## Part 3 — Shared supervised practice (100 minutes)

**Core run sheet (100 minutes):** compare fail-open and fail-closed (20) · red run and reading the tests (30) · write your fix and get a green run (40) · limits (10). Everything runs on your own machine; no GitHub account, repository or pull request is needed for full marks.

**Prerequisites:** Docker, `curl` and `python3`. On Windows, type every command in the Ubuntu app.

**Before class — build the lab image once, while online:**
```bash
cd ~/software-security/labs/week15-devsecops-pipeline
docker compose build
```

**In class — start both services** in terminal window A (it keeps running and shows the logs; that is correct):
```bash
cd ~/software-security/labs/week15-devsecops-pipeline
docker compose up --no-build --pull never
```
The **insecure** service is on `http://localhost:8090` and the **secure** one on `http://localhost:8091`. Type the commands below in a second window, in the same folder.

**Core task 1 — Fail-open vs fail-closed (20 min).** Ask both services for the admin page with no login, then as a real admin:
```bash
curl -s localhost:8090/admin
curl -s localhost:8091/admin
curl -s localhost:8091/admin -H 'Authorization: alice-token'
```
You should see the insecure service answer `{"panel":"UNLOCKED","secret":"FLAG{...}"}` with **no** login (fail-open; the demo flag is the same for everyone and is the expected evidence, nothing goes to ctf.zcr.ai), the secure service answer `{"error":"forbidden"}`, and alice still get in. In window A, the secure service logs a line with `event=authz_failure` and `reason=unauthenticated`, but no token. *Deliverable:* the three responses, the log line, and the exact line in `insecure_service.py` that fails open (A10 / CWE-636).

**Core task 2 — Red run and the tests (30 min).** Run the checker before editing, and keep the result:
```bash
python3 check_student.py
```
You should see `FAILED (errors=4)`. That is expected: nothing is written yet. Open `check_student.py` and read the four tests: a real admin is allowed; missing, unknown and non-admin tokens are denied; a lookup **error** is denied; and the log record holds only the outcome and the error's type, never its message. *Deliverable:* the red result + one line per test saying what it checks.

**Core task 3 — Write your fix and get a green run (40 min) 🛡️.** Open `student_task.py` and complete both functions:
- `authorize(lookup_user, token, admins)`: return `True` only when the token is present, `lookup_user(token)` succeeds and returns a user, and that user is in `admins`. If `lookup_user` raises **any** error, return `False` (fail closed).
- `event_fields(allowed, error=None)`: return `{"outcome": "allow"}` when allowed; otherwise `{"outcome": "deny"}`, plus `"error_type"` set to the error's **class name** when an error is given. Never put the error message or a token in the record.

Run the same checker again. You should see `Ran 4 tests` and `OK`. *Deliverable:* your `student_task.py` commit link, the red (`FAILED`) and green (`OK`) results in one stamped screenshot, and which test each part of your code satisfies.

Submit your code link: commit `student_task.py` to branch `wk15` in your own fork and push (see [SUBMISSION.md](../../SUBMISSION.md); do not open a pull request).

**Core task 4 — Limits (10 min).** In 3–4 sentences: what does a green checker prove, what does it not prove, and why does a green CI run not mean every vulnerability is gone? *Deliverable:* your explanation.

Stop the services when you finish: press Ctrl+C in window A, then run `docker compose down`.

---

## Optional extension — not needed for full marks

The tasks below are the original, longer version of this lab: the full Semgrep/Trivy/Gitleaks pipeline in your own public repo and the Red/Blue "Break the Build" game. They need GitHub Actions and add no points.

> The task budgets below add up to 205 min. That is deliberate over-provisioning, not a schedule:
> Tasks 2–4 are dominated by Actions queue and scan wall-clock. Push the gate in class (Task 2);
> Tasks 3–5 wait on Actions runs and the Red/Blue results, so they are homework.
>

![Two panels: the CI gate in security-ci.yml, where a MEDIUM DS-0001 finding slips past the HIGH,CRITICAL threshold and the build goes green, and the /admin handler, where one except branch returns 200 with the flag while the other returns 403 and logs it.](img/fail-closed.svg)

**Learning goals:** wire tool-specific security CI gates (Semgrep selected rules, Trivy HIGH/CRITICAL, Gitleaks detected secrets), observe structured security logging + fail-closed handling locally, then play Break-the-Build.

**Prerequisites:** a **public** GitHub repo you own with Actions enabled — a throwaway repo holding only this lab folder works best (on a private repo the SARIF upload needs GitHub Code Security and fails, turning every job red; a fork of the course repo also scans every other week's deliberately vulnerable lab, so it cannot go green). Open your Task 4 PR inside **your own** repo, never against the course repo; `git`; Docker; Python + Flask for the local service.

### Environment setup (real commands)

**A) Wire the gate into a public repo you own.** Copy this lab folder's files to the ROOT of the new repo, then run these inside it. `git add .` adds the workflow AND the lab files it scans (adding only `.github/` would leave nothing to scan); the push runs the workflow:
```bash
mkdir -p .github/workflows
cp security-ci.yml .github/workflows/security-ci.yml
git add .
git commit -m "ci: add security gate (Semgrep + Trivy + Gitleaks)"
git push
```

**B) Run the sample service locally.** From this lab folder, make a virtual environment (plain `pip install flask` is refused on some systems), install Flask and start the service:
```bash
cd ~/software-security/labs/week15-devsecops-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python sample-service.py
```
In another window, expect 401 (`authn_failure`), 403 (`authz_failure`) and 200 (admin):
```bash
curl -s -X POST localhost:5001/login -H 'Content-Type: application/json' -d '{"token":"nope"}'
curl -s localhost:5001/admin -H 'Authorization: bob-token'
curl -s localhost:5001/admin -H 'Authorization: alice-token'
```

**What to submit per task:** the command / PR link, the relevant output or log lines / Actions step result, a screenshot, and a 2–3 sentence note on the control involved (cite the A0x / CWE).

### Tasks

- **Task 0 — Onboarding (full reference exercise: 15 min).** Run the sample service; trigger the three curls above. **Deliverable:** screenshot of the structured `event=...` security log lines for authn_failure, authz_failure, and authz_success.

- **Task 1 — Logging & fail-closed (full reference exercise: 35 min, A09/A10).** *Goal:* prove fail-closed behavior. *Steps:* read `/admin` in `sample-service.py`; explain why the broad `except Exception` returns **403, not the secret**, and why `type(exc).__name__` (not the message) is logged (CWE-209). Identify the line that would make it fail *open* (the commented INSECURE variant). *Deliverable:* the log lines + a 2–3 sentence explanation of fail-closed vs fail-open.

- **Task 1b — Break the Build, live (full reference exercise: 25 min, A10 / CWE-636).** *Goal:* exploit a real fail-open, then prove the fix. *Steps:* from the current lab directory (Setup B already put you there — `cd labs/week15-devsecops-pipeline` again from inside it fails, "no such file or directory"), run `docker compose up -d --no-build --pull never` after the pre-class build (spawns the **insecure** service on `:8090` and the **secure** one on `:8091`). As **Red**, hit the insecure admin route with **no** Authorization header — the fail-open path leaks the admin panel *and* the flag (a local run returns the public demo flag; a personal flag applies only if the instructor has actually issued an instance):
  Expected: the first leaks `{"panel":"UNLOCKED","secret":"FLAG{...}"}` (fail OPEN); the second is `{"error":"forbidden"}` with 403 (fail CLOSED and logged); the third still unlocks for a real admin:
  ```bash
  curl -s localhost:8090/admin
  curl -s localhost:8091/admin
  curl -s localhost:8091/admin -H 'Authorization: alice-token'
  ```
  Submit the leaked `FLAG{...}`. *Deliverable:* the flag, the two contrasting `/admin` responses (`:8090` leak vs `:8091` deny), and the exact line in `insecure_service.py` that fails open. *The local checker tests rejection and legitimate admin behavior. Use a hosted verifier only when the instructor has actually issued that environment; this worksheet does not assert that one is configured.*

- **Task 2 — Stand up the gate (full reference exercise: 35 min).** *Goal:* get the workflow running. *Steps:* push `security-ci.yml`, open the Actions run, confirm the three jobs (`semgrep`, `trivy`, `gitleaks`) execute and SARIF appears in the Security tab. *Deliverable:* screenshot of the Actions run + the Code scanning alerts page.

- **Task 3 — Blue team: pass the gate (full reference exercise: 30 min).** *Goal:* a green build. *Steps:* ensure the protected repo has no HIGH/CRITICAL findings and no secrets; fix or justify-and-document any (no blanket-ignore, per README §4). Expect a red baseline before you change anything:
  - **Semgrep flags every `uses: …@vN` tag (pin it to a commit SHA).** `security-ci.yml`'s own `aquasecurity/trivy-action@ed142fd0...` lines are the worked example of the *result* — here's how to get there for `actions/checkout@v4` and `github/codeql-action/upload-sarif@v3`:
    Each command prints `<sha>  refs/tags/v4`; replace `uses: actions/checkout@v4` with `uses: actions/checkout@<that sha>` and keep a `# v4` comment:
    ```bash
    git ls-remote https://github.com/actions/checkout v4
    git ls-remote https://github.com/github/codeql-action v3
    ```
    Also fix `host="0.0.0.0"` (needed so Docker can publish the port — justify it with a `# nosemgrep` comment and a reason).
  - **Gitleaks flags the docs' own `-H 'Authorization: alice-token'` examples** (`curl-auth-header`, a false positive). The fingerprint is `<commit-sha>:<file>:<rule-id>:<line>` and the commit SHA is specific to **your** repo, so there is no value to copy here — get your real ones and add each as its own line in `.gitleaksignore` with a comment:
    Each finding prints a line like `Fingerprint: <sha>:README-pipeline.md:curl-auth-header:92`:
    ```bash
    docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest detect -s /repo -v
    ```
    ```
    # .gitleaksignore — false positives only, never a real secret (reviewed, see worksheet Task 3)
    <sha>:README-pipeline.md:curl-auth-header:92  # docs example token, not a real credential
    <sha>:worksheet.md:curl-auth-header:70         # same
    ```
    Re-run Gitleaks after adding it to confirm `no leaks found` and exit code `0`.
  *Deliverable:* link to the passing run, the two action SHAs you pinned, and your `.gitleaksignore` diff.

- **Task 4 — Red team: Break the Build (full reference exercise: 40 min).** *Goal:* make the gate say **no**. *Steps:* on a branch/PR, inject *one* planted defect (per README §5), each aimed at a different gate step (a root Dockerfile also trips Semgrep, and a token also trips Trivy's secret scan): an outdated vulnerable dependency (e.g. an old `urllib3`) → Trivy SCA; a Dockerfile that runs as **root** — drop the `USER` line, or write `USER root` → Trivy config (`DS-0002`, HIGH); or a hard-coded token → Gitleaks. Open the PR and watch the matching gate step fail. *Deliverable:* screenshot of the **failing** gate step + which job caught it (Trivy SCA / Trivy config / Gitleaks) and which `exit-code: "1"` / `--error` step enforced it.
  > **Why root and not `chmod 777`.** Both gate steps filter to `--severity HIGH,CRITICAL`, and Trivy's Dockerfile scanner has no rule for `chmod` at all — it checks instruction-level `RUN`/`COPY` semantics, exactly as Week 13 Task 1 says. `chmod 777` therefore returns **nothing**, at any severity, and the build goes green: a defect that slips the gate is a Task 5 *Red point*, not a Task 4 screenshot. `:latest` is no good either — that is `DS-0001` and Trivy rates it MEDIUM, which this gate filters out. Running as root is `DS-0002` HIGH, so it fails the build for real.

- **Task 5 — Score Break-the-Build (full reference exercise: 25 min).** *Goal:* tally Red vs Blue. *Steps:* one Blue point per finding the gate caught, one Red point per finding that slipped through; for any bypass, propose the rule that would have caught it. *Deliverable:* scoreboard + one proposed gate improvement.

---

## Part 4 — Reflection

1. **Mapping.** For three controls you exercised, give: control → A09/A10 (or A02/A03 for a scanner) → CWE → one-line rationale.
2. **Real incident.** Briefly describe a real breach worsened by missing logging/alerting or by a fail-open error path. Which control here would have changed the outcome?
3. **Best mitigation.** Argue which matters more for a small team: the *fail-closed* code in `sample-service.py`, or the *CI gate* in `security-ci.yml` — and why both together beat either alone.

---

## Grading rubric (100)

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Common practical: main task and observations | 20 | 20 |
| Common practical: your control and positive/negative tests | 20 | 20 |
| Common practical: reproducible evidence, reasoning and limits | 20 | 20 |
| Assigned Conventional Part 2 written questions | 20 | — |
| Assigned Conventional Part 4 reflection | 20 | — |
| Assigned Audit-the-AI | — | 20 |
| Assigned Explain-in-Plain-English | — | 10 |
| Assigned Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

**Due:** Monday 15 February 2027, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Flags this week:** the insecure service leaks the same demo `FLAG{...}` for everyone in Core task 1. It is the expected evidence: paste it in that box with your stamped screenshot, and leave any "Personalized flag" field blank. Nothing is submitted on ctf.zcr.ai. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

**Scored exhibit supplied for this assignment (deliberately incorrect):**

> "A green Actions run proves every vulnerability is absent and guarantees that GitHub prevents merging a vulnerable pull request."

Identify the substantive mistakes (8), verify your criticism with relevant observations/tests or primary sources (8), and provide a justified correction (4). Distinguish the configured checks and thresholds from complete coverage, and workflow status from enforced repository rules.

The original open-ended AI exercise below is retained as optional extension practice. Do not assume a fresh AI answer must contain an error; a correctly supported answer may be accepted with tests. You can earn the full assigned 20 by auditing the supplied exhibit, without an external AI account.

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Ask an AI assistant to exploit **or** fix this week's vulnerability. Paste its full answer.
2. **Find what's wrong or risky** in it — insecure code, a subtly incomplete fix, a hallucinated API/function/CVE, a missed edge case, or wrong reasoning. Quote the exact line(s).
3. Produce the **correct, verified** version yourself and explain in 2–3 sentences why the AI's output was insufficient.

> Disclose any AI use beside your Part 1 details. The supplied exhibit is the scored AIR-Sec Audit-the-AI task (20); the open-ended ask-an-AI exercise above is optional extension practice. Conventional does not complete the AIR-Sec written section for marks.

---

## 🧠 Comprehension & Prompt — assigned AIR-Sec section (10 + 10)

**A. Explain in Plain English (EiPE, 10 points).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem (10 points).** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Use a local tool or an external AI if available, then verify the proposed change against the supplied tests. If no external model is available, submit the final prompt, the expected change/acceptance tests, and your own verified implementation. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
