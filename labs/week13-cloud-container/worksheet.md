# Worksheet 13 — Cloud & Container Security

> **Course:** Software Security (KOSEN69) · Week 13
> **Aligned to:** OWASP 2025 **A02 Security Misconfiguration** · **CWE-732** (incorrect permission assignment), **CWE-16** (configuration), **CWE-526** (secret exposed through an environment variable), plus CWE-798 (hard-coded credential — OWASP files this under **A07**), CWE-250, CWE-538, CWE-269, CWE-1104
> **Signature game:** 🔍 *Misconfig Hunt* (CloudGoat-style) — each misconfig you find **and** fix = a flag.

> ⚠️ **Ethics note:** All artifacts here are deliberately broken for teaching and are marked *"Sandbox/teaching only; for authorized lab use."* Scan, exploit, and harden **only** these lab files (or systems you own / are authorized to test). Never point Trivy or these techniques at third-party cloud accounts or images without written permission.

## Class and assessment contract

**Class: Tuesday 26 January 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Pull the Trivy image and build the insecure image before class (see below). In class you do the four **core tasks** in Part 3; the "Optional extension" adds no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10) and even student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 13 answer sheet for your format (odd ID: AIR-Sec file; even ID: Conventional file), and say there which AI tool you used, if any.

## Words you will see

| Word | Meaning |
| --- | --- |
| **Misconfiguration** | A setting that makes a system less safe than it should be, such as running as root or putting a password in a file. |
| **Trivy** | A free scanner. `trivy config` checks Dockerfiles for risky settings. It does **not** read AWS IAM policy files. |
| **Image / layer** | A Docker image is built in layers, one per Dockerfile line. Anyone with the image can read every layer, including old `ENV` values. |
| **IAM policy** | A JSON document that says who may do which actions on which cloud resources. |
| **Least privilege** | Give only the exact actions and resources a job needs, nothing more. |
| **Wildcard `*`** | "Everything". `"Action": "*"` means every action. |
| **Blast radius** | How much damage is possible if a key or account is stolen. |

---

## Part 1 — Student Information

Fill these in at the top of your answer sheet:

| Name | Student ID | Date | Code link (branch wk13) | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

---

## Part 2 — Lecture Questions

**Scope:** These exercises inspect local configuration; they do not prove effective permissions in a deployed AWS account.

Answer in your own words (2–4 sentences each). Everyone should read these to prepare; only Conventional answers them for marks.

1. Explain the **shared-responsibility model**. In `harden.md` it says "the cloud provider secures *of* the cloud; you secure what you put *in* it." Give one concrete example of each side for an S3-backed app.
2. `iam-policy-insecure.json` uses `"Action": "*"` and `"Resource": "*"`. Describe **why this violates least privilege** and map it to CWE-732 vs CWE-269 — what is the difference between the two CWEs here?
3. The insecure Dockerfile bakes `ENV API_TOKEN=sk_live_...`. Explain how an attacker recovers that secret from a shipped image (name the `docker` commands) and why this is **CWE-526 / CWE-798 / CWE-200**.
4. Why is `FROM python:latest` a reproducibility and review problem? What does pinning to an `@sha256:` digest guarantee, and what do vulnerability review, provenance checks and an update process still need to do? Is `latest` automatically an unmaintained component (CWE-1104)?
5. What does a **distroless** base image remove (relative to `python:3.11-slim`), and how does that shrink the attack surface for an RCE or container-escape attacker?

---

## Part 3 — Shared supervised practice (100 minutes)

**Core run sheet (100 minutes):** scan the Dockerfiles (20) · manual container and IAM review (20) · write your least-privilege policy (35) · allow/deny results and explanation (25).

**Prerequisites:** Docker and `python3`. On Windows, type every command in the Ubuntu app.

**Before class — while online, pull the scanner and build the insecure image** (the build downloads `python:latest`, so do it at home):
```bash
cd ~/software-security/labs/week13-cloud-container
docker pull aquasec/trivy:latest
docker build -f Dockerfile.insecure -t week13-insecure:lab .
```

Type every command below in this lab folder (`cd ~/software-security/labs/week13-cloud-container`).

**Core task 1 — Scan the Dockerfiles (20 min).** Run Trivy offline on this folder:
```bash
docker run --rm --network none --pull never -v "$PWD:/src:ro" aquasec/trivy:latest config --skip-check-update --severity MEDIUM,HIGH,CRITICAL /src
```
You should see a table with `Dockerfile.hardened` = 0 and `Dockerfile.insecure` = 4 failures: `DS-0001` (MEDIUM, `FROM python:latest`), `DS-0002` (HIGH, no `USER`, so it runs as root) and `DS-0031` (CRITICAL, twice: secrets in `ENV`). A warning about "embedded checks" is normal. Then open `Dockerfile.insecure` and read its six `# DEFECT:` comments: three match a Trivy rule, and three (`COPY . .`, `chmod -R 777`, unpinned `pip install`) are found only by reading. *Deliverable:* the scan output + a 6-row table: defect → CWE → Trivy rule and severity, or "manual review — no Trivy rule".

**Core task 2 — Manual container and IAM review (20 min).** Trivy does not read IAM JSON, so you review it yourself, then see the leaked secrets:
```bash
cat iam-policy-insecure.json
docker history --no-trunc week13-insecure:lab
```
You should see one statement with `"Action": "*"`, `"Resource": "*"` and no `Condition`, then image layers that show `API_TOKEN=…` and `AWS_SECRET_ACCESS_KEY=…` in plain text. *Deliverable:* a 3-row table (problem → CWE → why), one sentence on the blast radius if these credentials leaked, and where the secrets should live instead.

**Core task 3 — Write your least-privilege policy (35 min) 🛡️.**
1. Run the checker before editing, and keep the result:
   ```bash
   python3 check_student.py
   ```
   You should see `FAILED (errors=3)`. That is expected: nothing is written yet.
2. Open `student_task.py` and complete `build_policy(bucket, prefix)`. Return a policy dictionary (`Version` plus a `Statement` list) with **two** Allow statements: one that allows `s3:ListBucket` on the bucket itself (`arn:aws:s3:::BUCKET`) **only** when the requested `s3:prefix` matches your prefix (a `Condition` with `StringLike`), and one that allows `s3:GetObject` only on objects under that prefix (`arn:aws:s3:::BUCKET/PREFIX*`). No other actions. Compare the shape with `iam-policy-leastpriv.json`, but build the strings from the `bucket` and `prefix` arguments.
3. Run the same checker again. You should see `Ran 3 tests` and `OK`.
- *Deliverable:* your `student_task.py` commit link, the before (`FAILED`) and after (`OK`) results in one stamped screenshot, and your policy.

Submit your code link: commit `student_task.py` to branch `wk13` in your own fork and push (see [SUBMISSION.md](../../SUBMISSION.md); do not open a pull request).

**Core task 4 — Allow/deny results and explanation (25 min).** The checker's three tests show what your policy allows (`GetObject` and `ListBucket` under `app/`) and denies (another prefix, another bucket, `DeleteObject`, `PutObject`). Explain each result in one line. Then explain the limits: this is a small local checker, not AWS IAM, and a clean Trivy result does not prove the IAM policy or the deployed workload is safe. *Deliverable:* the allow/deny list with one-line reasons + 2–3 sentences on the limits.

---

## Optional extension — not needed for full marks

The tasks below are the original, longer version of this lab (rebuilding the hardened image, CVE scans, the full Misconfig Hunt tally). Do them only if you have time; they add no points.

**Learning goals:** find cloud/container misconfigurations with Trivy, map each to a CWE, and rebuild the IAM policy + Dockerfile to least privilege / hardened so the findings drop.

**Prerequisites:** Docker installed and running; the `week13-cloud-container/` lab folder; internet access to pull `aquasec/trivy:latest`.

### Environment setup (real commands)

`bash scan.sh` is the provided wrapper (an online Trivy config scan of the Dockerfiles; IAM JSON is reviewed manually). The last two commands build the hardened image and scan it for CVEs (online):
```bash
cd ~/software-security/labs/week13-cloud-container
bash scan.sh
docker build -f Dockerfile.hardened -t week13-hardened:lab .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL week13-hardened:lab
```

**What to submit per task:** the command(s) you ran + the relevant output (finding count or the specific finding line), a screenshot of the Trivy/terminal result, and a 2–3 sentence mitigation explaining *why* the fix reduces risk (cite the CWE).

![The same app shipped as two stacked container images, Dockerfile.insecure beside Dockerfile.hardened, with each layer paired to its fix and its CWE, and only the unpinned :latest tag, the root user and the ENV secret marked as things trivy config actually flags.](img/container-hardening.svg)

### Tasks

- **Task 0 — Onboarding (full reference exercise: 15 min).** Confirm Docker works (`docker version`), run `bash scan.sh`, and record the **baseline finding count for the `Dockerfile.insecure` row** of its output table (`scan.sh` scans the whole folder in one pass and lists each Dockerfile's count separately — `Dockerfile.hardened`'s row is `0` in that same table; that's not today's baseline, Task 4 revisits it). Trivy's `config` scanner does not parse standalone IAM policy JSON, so `iam-policy-insecure.json` is reviewed manually instead — see Task 2. **Also build the insecure image now, before class** (Task 3 needs it, and the first build pulls all of `python:latest` and installs Flask — on this machine that took about 100 seconds with nothing cached yet; 36 people pulling it at once in class is worse):
  ```bash
  docker build -f Dockerfile.insecure -t week13-insecure:lab .
  ```
  **Deliverable:** screenshot of the baseline scan.

- **Task 1 — Misconfig Hunt: container image (full reference exercise: 40 min).** *Goal:* find every defect in `Dockerfile.insecure`. *Steps:* read each `# DEFECT:` comment, then locate the matching Trivy finding where one exists — only 3 of the 6 (unpinned `:latest`, runs as root, secrets in `ENV`) map to a Trivy config rule (`DS-0001`, `DS-0002`, `DS-0031`); `COPY . .`, `chmod -R 777`, and unpinned `pip install` are instruction-level RUN/COPY semantics Trivy's Dockerfile scanner doesn't check, so identify those 3 by code review instead. Build a table: defect → CWE → Trivy rule/severity (write "manual review — no Trivy rule" where none exists). *Deliverable:* completed table (6 rows) using the IDs from `harden.md`.

- **Task 2 — Misconfig Hunt: IAM (full reference exercise: 30 min).** *Goal:* document why `iam-policy-insecure.json` is full-admin. *Steps:* identify the `Action:*` / `Resource:*` / no-`Condition` problems; map to CWE-269 / CWE-732. *Deliverable:* 3-row table + one sentence on the blast radius if these creds leak.

- **Task 3 — Secrets & storage (full reference exercise: 25 min).** *Goal:* show secrets must not live in the image. *Steps:* explain how `ENV API_TOKEN` / `AWS_SECRET_ACCESS_KEY` are exposed via `docker history --no-trunc week13-insecure:lab` (or `docker inspect`); propose where they belong instead (secrets manager / mounted secret / orchestrator secret per `harden.md`). *Deliverable:* 2–3 sentence remediation + the `.dockerignore` entries you would add to stop `COPY . .` leaking `.git`/`.env` (CWE-538).

- **Task 4 — Hardened-Dockerfile + least-priv-IAM defense (full reference exercise: 50 min).** *Goal:* prove the "after" is clean. *Steps:* (a) **`bash scan.sh` scans the whole folder every time, so re-running it gives the identical combined table — nothing to compare against itself.** Read the `Dockerfile.hardened` row from that same table (it's `0`), or scan each file on its own to see the drop directly:
  The first line gives Task 0's baseline on its own; the second gives today's reduced count:
  ```bash
  docker run --rm -v "$PWD":/src aquasec/trivy:latest config --severity MEDIUM,HIGH,CRITICAL /src/Dockerfile.insecure
  docker run --rm -v "$PWD":/src aquasec/trivy:latest config --severity MEDIUM,HIGH,CRITICAL /src/Dockerfile.hardened
  ```
  (`scan.sh`'s own argument only selects an *image* for step 2's optional CVE scan — `bash scan.sh Dockerfile.hardened` does not make step 1 scan just that file, and running the image-scan step with that argument looks for a nonexistent image literally named `Dockerfile.hardened`.) Confirm the IAM fix manually per Task 2 by diffing `iam-policy-leastpriv.json` against the insecure policy; (b) for the Dockerfile, point to the fix for each Task-1 defect (digest pin, multi-stage venv, distroless runtime, `USER 65532:65532`, no secrets in `ENV`, copy only `app.py`); (c) for IAM, confirm the rewrite scopes `s3:GetObject` to `arn:aws:s3:::lab-app-bucket/app/*` and adds the `s3:prefix` `Condition`; (d) list the extra runtime flags from `harden.md` (`--read-only`, `--cap-drop ALL`, `--security-opt no-new-privileges`). *Deliverable:* before/after finding counts, the defect→fix mapping, and the diffed policy/Dockerfile with one sentence per fix.

- **Task 5 — Flag tally (full reference exercise: 20 min).** *Goal:* score the hunt. *Steps:* one flag per misconfig found **and** fixed (6 container + 3 IAM = 9). *Deliverable:* flag count + the single biggest-risk misconfig and why.

---

## Part 4 — Reflection

1. **Mapping.** For three findings, write the line of the artifact → CWE → OWASP 2025 A02, and the one-line fix.
2. **Real incident.** Briefly describe a real breach caused by a cloud/container misconfiguration (e.g., a public S3 bucket leak, or an over-permissive IAM role). What single control from this lab would have prevented it?
3. **Best mitigation.** Of everything you did, which control gives the most risk reduction per unit of effort, and why? Argue for least-privilege IAM vs. distroless+non-root.

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

**Due:** Monday 1 February 2027, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **No CTF flag this week:** the "flags" in the Misconfig Hunt are just points in the game; nothing is submitted on ctf.zcr.ai. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

**Scored exhibit supplied for this assignment (deliberately incorrect):**

> "A zero-result Trivy scan proves the IAM policy is least privilege and the workload is secure in AWS."

Identify the substantive mistakes (8), verify your criticism with relevant observations/tests or primary sources (8), and provide a justified correction (4). State exactly which file/scanner was checked, which IAM claims require manual review, and which deployment controls were not exercised.

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

**Scanner preflight:** confirm that the tool ran and produced a report before interpreting a count. Reporting wrappers may continue after a tool error (`|| true`); missing output or a failed download is not evidence of zero findings. Instructor-provided reports must be labelled as supplied cases rather than claimed as a personal scan.
