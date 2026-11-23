<!-- Sandbox/teaching only; for authorized lab use. -->

# DevSecOps Pipeline — Wiring & Interpreting Results

## Bounded class check and full workflow extension

The current class uses `student_task.py` and `check_student.py` for a small, explainable fail-closed/logging change. Run `python3 check_student.py` on your own machine: an unfilled starter produces a red result; a correct student change produces green under the **same** checks. Keep both outputs and the code diff. (`student-check-ci.yml` is included if you want to try the same check in your own lab-only repository; it is optional and adds no points. It has read-only repository permission and uses no AI service or credentials.)

The full Semgrep/Trivy/Gitleaks workflow described below is retained as extended project practice. Its findings/thresholds are a different scope from the bounded student-control job; passing one does not prove that the other passed. Ranking/game points do not add to the worksheet's 100 points.


**OWASP 2025:** A09 Security Logging & Alerting Failures, A10 Mishandling of
Exceptional Conditions (plus the scanners cover A02/A03).

This folder is a **lab template**. The workflow does not run from here; you
copy it into a repo's `.github/workflows/` directory.

---

## 1. Wire it in

In a lab-only repository that holds this lab's files: `git add .` includes the workflow AND the lab source it scans, and the push runs the workflow:
```bash
mkdir -p .github/workflows
cp security-ci.yml .github/workflows/security-ci.yml
git add .
git commit -m "ci: add security gate (Semgrep + Trivy + Gitleaks)"
git push
```

No secrets are required: Semgrep, Trivy, and Gitleaks all run with the
free/public rule sets in this template.

---

## 2. What each job does

| Job | Tool | Scans for | Maps to |
|-----|------|-----------|---------|
| `semgrep`  | Semgrep  | Insecure code patterns (SAST) | OWASP Top 10 rules |
| `trivy`    | Trivy    | Vulnerable deps (SCA), IaC/Dockerfile misconfig, secrets | A03 / A02 |
| `gitleaks` | Gitleaks | Hard-coded secrets in code + git history | CWE-798 |

---

## 3. How the gate works (the important part)

Each tool runs **twice** on purpose:

1. **Report step** (`exit-code: 0` / `|| true`) — produces a SARIF file and
   uploads it to the GitHub **Security** tab. Uses `if: always()` so the
   SARIF uploads *even when the build is about to fail*.
2. **Gate step** (`exit-code: 1`, `--error`) — re-runs and **fails the build**:
   Semgrep on any selected-rule finding, Trivy on HIGH/CRITICAL findings,
   and Gitleaks on any detected secret. A scanner error at this step is not
   a clean pass; investigate false positives before a narrow documented exception.

This split is deliberate: the report step has no severity filter, so the
Security tab shows findings of every severity. The gate applies each tool's
configured failure condition above.
Report-then-gate gives you both the full picture *and* a red build.

> Why not just `|| true` everything? Because then the build never fails and
> the "gate" is decorative. Real gates must be able to say **no**.

---

## 4. Reading results

- **GitHub UI:** Security tab -> Code scanning alerts (from the SARIF uploads),
  and the Actions run log for the gate step that failed.
- **Severity:** the template gates on `HIGH,CRITICAL`. Tune in the workflow
  (`severity:` for Trivy, rulesets for Semgrep) as the class matures.
- **Triage:** fix, or document a justified, time-boxed exception. Do not
  blanket-ignore.

---

## 5. "Break the Build" game (see week15 README)

- **Blue:** keep the gate green by fixing findings.
- **Red:** open PRs that try to sneak past — e.g. add an old `urllib3` (Trivy
  SCA), a Dockerfile that runs as **root** — no `USER` line, or `USER root`
  (Trivy config, `DS-0002`, HIGH), or a hard-coded token (Gitleaks). One
  defect per PR. A correctly-built gate turns the PR red.
- Don't reach for `chmod 777` here: both gate steps filter to
  `--severity HIGH,CRITICAL` and Trivy's Dockerfile scanner has no `chmod`
  rule at all, so it returns nothing and the build stays green. That makes it
  a *Red point* under the worksheet's Task 5 scoring, not a failing-gate screenshot.

## 6. Run the sample service locally (logging + fail-closed demo)

From this lab folder (on Git Bash for Windows, activate with `source .venv/Scripts/activate`):
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install flask
python sample-service.py
```
In another window, expect 401 (`authn_failure`), 403 (`authz_failure`) and 200 (admin):
```bash
curl -s -X POST localhost:5001/login -H 'Content-Type: application/json' -d '{"token":"nope"}'
curl -s localhost:5001/admin -H 'Authorization: bob-token'
curl -s localhost:5001/admin -H 'Authorization: alice-token'
```
Watch the structured `event=...` security log lines — those are what a SIEM
would alert on (A09). Note that errors deny by default (A10, fail-closed).
