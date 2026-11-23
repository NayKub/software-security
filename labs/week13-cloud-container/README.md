# Week 13 — Cloud & Container Security

## Class and assessment contract

**Class: Tuesday 26 January 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Pull the Trivy image and build the insecure image before class (see below). In class you do the four **core tasks** in Part 3; the "Optional extension" adds no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10) and even student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write which AI tool you used, if any, on the answer sheet. There is no CTF flag this week.

**Due:** Monday 1 February 2027, 23:59 (Thai time).

## Before class and the core commands

While online, pull the scanner and build the insecure image:
```bash
cd ~/software-security/labs/week13-cloud-container
docker pull aquasec/trivy:latest
docker build -f Dockerfile.insecure -t week13-insecure:lab .
```
In class, the core uses the offline Trivy scan, a manual IAM review, `docker history` on the insecure image, and the policy checker (`python3 check_student.py`, before and after you complete `build_policy()` in `student_task.py`). The worksheet's Part 3 gives every command and what you should see.

**OWASP 2025:** A02 Security Misconfiguration · **CWE:** CWE-732, CWE-16

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); while online, pull Trivy and build the insecure image (above). Skim last week's recap.
2. **Slides, then class** — read `slides/week13.md` and the worksheet's Part 2 to prepare. Class opens with the weekly quiz (10 min) and a short explanation and demo (15 min).
3. **Lab (in class)** — do the four core tasks in the worksheet's Part 3: scan (20 min), manual review (20), your least-privilege policy (35), allow/deny explanation (25). Then do the written section for your student ID this week (odd: AIR-Sec 20/10/10; even: Conventional 40), after class if needed.
4. **Submit by Monday 1 February 2027, 23:59** — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link to `student_task.py` on branch `wk13`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Apply the shared-responsibility model and least privilege (IAM).
- Manage secrets safely; harden container images.
- Find and fix common cloud/container misconfigurations.

## 🔍 Signature game — "Misconfig Hunt" (CloudGoat-style)
Scavenger hunt: each misconfiguration you find **and** fix = one point ("flag") in the game — **9 in total, two categories**. These are not CTF flags.
The first command scans the Dockerfiles for misconfigurations; the second (optional, after building `week13-hardened:lab`) scans an image for CVEs:
```bash
docker run --rm -v "${PWD}:/src" aquasec/trivy:latest config --severity MEDIUM,HIGH,CRITICAL /src
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL week13-hardened:lab
```
1. **Container (6):** `:latest` tag, root user, secret-in-`ENV`, `COPY . .`, `chmod -R 777`, unpinned `pip install`. Only 3 of the 6 map to a Trivy rule — the rest need manual review.
2. **IAM (3):** given an over-permissive policy (`Action:"*"`, `Resource:"*"`), fix `Resource:"*"` (CWE-732), `Action:"*"` (CWE-269), and add a missing `Condition` scope. Trivy does not parse standalone IAM JSON — entirely manual review.

Use a minimal/distroless base, drop root, pin versions; re-scan to show fewer findings.

## Deliverable
For the bounded common practical: a real Trivy Dockerfile scan (or a clearly labelled instructor-supplied report), manual container/IAM findings, your `student_task.py` least-privilege policy diff, and allowed/denied control results from `check_student.py`. The full hardened Dockerfile rebuild and image CVE scan remain extension work.


## References
- https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- https://kubernetes.io/docs/concepts/security/

**Scanner preflight:** confirm that the tool ran and produced a report before interpreting a count. Reporting wrappers may continue after a tool error (`|| true`); missing output or a failed download is not evidence of zero findings. Instructor-provided reports must be labelled as supplied cases rather than claimed as a personal scan.
