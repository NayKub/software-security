# Worksheet 12 — Software Supply-Chain Security

> **Course:** Software Security (KOSEN69) · Week 12
> **Aligned:** OWASP 2025 — A03 Software Supply Chain Failures · A08 Software or Data Integrity Failures · **CWE:** CWE-1104, CWE-829, CWE-1357, CWE-1395
> **Signature game:** 📦 Dependency Confusion Heist
>
> **Ethics note:** This lab has **no live private/public registry to attack** — the dependency-confusion exercise is a controlled walkthrough (`dependency-confusion.md`) plus the interactive resolver simulation in Task 2, not a real package pull. **Never** plant or publish look-alike packages on the real PyPI or npm — that is an attack on every downstream user, and nothing in this lab requires it.

## Class and assessment contract

**Class: Tuesday 19 January 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the checker image before class (see below). In class you do the five **core tasks** in Part 3; everything under "Optional extension" is extra practice and adds no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 12 answer sheet for your format (odd ID: Conventional file; even ID: AIR-Sec file), and say there which AI tool you used, if any.

## Words you will see

| Word | Meaning |
| --- | --- |
| **Dependency** | A package your code uses (here, the nine pinned in `requirements.txt`). |
| **SCA** | Software Composition Analysis: a tool that checks your dependencies against lists of known vulnerabilities. |
| **Dependency confusion** | An attacker publishes a public package with the same name as your private one but a higher version, hoping your installer picks theirs. |
| **Index** | A package server, such as PyPI or a company's private server. "Merged" means the installer looks at several at once. |
| **SBOM** | Software Bill of Materials: a list of the components in your software. A list, not a safety check. |
| **Hash (SHA-256)** | A fingerprint of a file. Change one byte and the fingerprint changes completely. |
| **Signature / public key** | A signature proves who signed a file, but only if you already trust that signer's public key. |
| **Trust pin (fingerprint)** | The SHA-256 of the public key you were told, separately, to trust. |

## Part 1 — Student Information

Fill these in at the top of your answer sheet:

| Name | Student ID | Date | Code link (branch wk12) | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

## Part 2 — Lecture Questions

Answer in 2–4 sentences each. Everyone should read these to prepare; only Conventional answers them for marks.

1. Explain **dependency confusion** (substitution). If a requirement admits both private `acme-internal-utils 1.4.0` and public `99.0.0`, why can a merged-index highest-version resolver choose the public candidate? Would an exact `==1.4.0` pin admit `99.0.0`?
2. How does **typosquatting** (`reqeusts`, `urlib3`) achieve code execution *at install time* before any of your code runs?
3. What does an **SBOM** (CycloneDX/SPDX) inventory, and how does it help incident response? How does it differ from SLSA build provenance? Is an SBOM required to produce SLSA provenance?
4. Sigstore **keyless** signing uses Fulcio (CA) + Rekor (transparency log) tied to an OIDC identity. What long-lived-key risk does this reduce, and which identity and build risks remain? Is every protected long-lived key an instance of CWE-321?
5. Summarize the **SLSA Build** levels for the version taught. Does "signed artifact + SBOM + provenance gate before deploy" alone establish any Build level? Identify the additional build-provenance evidence needed to justify a level.

![Six hops a dependency crosses from a public registry into production, each with its own attack and the control that answers it.](img/supply-chain.svg)

## Part 3 — Shared supervised practice (100 minutes)

**Core run sheet (100 minutes):** review the supplied SCA results (20) · resolver case (15) · read and generate the SBOM (20) · your key-pin control and signature checks (30) · hash and index control (15). Everything runs offline except the last `pip` step in core task 5, which downloads one package.

**Prerequisites:** Docker and `python3` on your machine. On Windows, type every command in the Ubuntu app. The signature checker runs in a small Docker image with OpenSSL, so nothing else is needed.

**Before class — build the checker image once, while online:**
```bash
cd ~/software-security/labs/week12-supply-chain
docker build -f Dockerfile.student -t softsec-student-checks:local .
```

Type every command below in this lab folder (`cd ~/software-security/labs/week12-supply-chain`).

**Core task 1 — Review the supplied SCA results (20 min).** List the pinned packages, then open the supplied scan:
```bash
cat requirements.txt
```
You should see nine pinned packages, each deliberately an old version. Open `sca-core.snapshot.json` in a text editor. It is a real pip-audit 2.10.1 run your instructor captured ahead of time (57 advisories across 5 packages): label it as supplied evidence, not your own scan. Pick three findings and record package, current version, advisory/CVE id and fixed version. *Deliverable:* the package list + your 3-row table + which OWASP/CWE this maps to (A03, CWE-1104/1395).

**Core task 2 — Resolver case (15 min).** Run the bounded resolver model three ways:
```bash
python3 resolver_core.py --mode merged
python3 resolver_core.py --mode single
python3 resolver_core.py --mode merged --private 100.0.0 --public 99.0.0
```
You should see `"selected_index": "public"` with `99.0.0`, then `"private"` with `1.4.0`, then `"private"` with `100.0.0`. The same idea is in the resolver simulation under Task 2 below. *Deliverable:* the three results + one sentence on why "keep my private version number higher" is not a real defense.

**Core task 3 — Read and generate the SBOM (20 min).**
```bash
python3 sbom_core.py
```
You should see a CycloneDX 1.5 JSON document (the same content as the supplied `sbom-core.cdx.json`). Find Flask's entry (`pkg:pypi/flask@1.1.4`). *Deliverable:* Flask's entry + one sentence on the scope: it lists the nine declared packages only, not transitive dependencies, installed packages, CVEs or provenance.

**Core task 4 — Your key-pin control (30 min) 🛡️.** The packet in `signature-core/` has a real signed artifact, the trusted signer's public key, and a second, valid signature made with a *different* key. Your job is the one check that decides whether a public key can be trusted at all.
1. Run the checker before editing, and keep the result:
   ```bash
   docker run --rm --network none -v "$PWD:/work:ro" -w /work softsec-student-checks:local
   ```
   You should see `FAILED (errors=3)`. That is expected: nothing is written yet.
2. Open `student_task.py` and complete `trusted_key(public_key, expected_sha256)`: return `True` only when the SHA-256 of the public-key **file's bytes**, written as lowercase hex, equals `expected_sha256`. You need to import one standard Python module for SHA-256; `Path` is already imported.
3. Run the same checker command again. You should see `Ran 3 tests` and `OK`: the trusted signature passes, a tampered artifact fails, and a valid signature from the wrong key is rejected.
- *Deliverable:* your `student_task.py` commit link, the before (`FAILED`) and after (`OK`) results in one stamped screenshot, and one sentence on why a valid signature is not enough without a trusted key.

Submit your code link: commit `student_task.py` to branch `wk12` in your own fork and push (see [SUBMISSION.md](../../SUBMISSION.md); do not open a pull request).

**Core task 5 — Hash and index control (15 min).** Check the artifact against the issued manifest, then tamper with a copy:
```bash
shasum -a 256 signature-core/artifact.txt
cat signature-core/manifest.json
cp signature-core/artifact.txt /tmp/tampered.txt
echo "tampered" >> /tmp/tampered.txt
shasum -a 256 /tmp/tampered.txt
```
You should see that the first hash equals `artifact_sha256` in the manifest, and the tampered copy's hash is completely different. Then see pip enforce hashes (this one needs the internet):
```bash
docker run --rm -v "$PWD":/w -w /w python:3.9-slim pip install --require-hashes -r requirements.txt
```
You should see `ERROR: Hashes are required in --require-hashes mode` with the hash pip found for Flask. *Deliverable:* the matching and changed hashes, the pip refusal, and one sentence on why a single trusted index plus required hashes stops a dependency-confusion swap.

---

## Optional extension — not needed for full marks

The tasks below are the original, longer version of this lab. They need a live scanner, image builds or a browser login, so your instructor may demo them. Do them only if you have time; they add no points.

**Reference-bank goals:** Run SCA on intentionally-outdated dependencies, generate an image SBOM, sign/verify an image, and defend against dependency confusion. The required core above uses the offline declared-component SBOM and real key-based artifact verification; image/keyless signing below is a prepared extension.

**Prerequisites:** Docker; the lab folder (`requirements.txt`, `Dockerfile`, `app.py`, `sca_scan.sh`, `sign.sh`). `cosign` is **not** installed on your host — every `cosign` command in this worksheet runs inside a container, same as `sign.sh` does. For the sign step itself: a browser for the OIDC flow (your GitHub or Google login) — in class this is a guided demo one person drives, not something everyone repeats (see `sign.sh`'s header).

**Extension setup:** `bash sca_scan.sh` runs a live trivy + pip-audit scan of `requirements.txt`; `docker build -t week12-supplychain:lab .` builds the image; `bash sign.sh week12-supplychain:lab` makes a CycloneDX SBOM and signs and verifies the image with cosign (it needs a browser login):
```bash
cd ~/software-security/labs/week12-supply-chain
bash sca_scan.sh
docker build -t week12-supplychain:lab .
bash sign.sh week12-supplychain:lab
```

**What to submit per task:** the exact command(s) + output, a screenshot, and a 2–3 sentence remediation note mapping the finding to A03/A08 or the CWE.

### Task 0 — Onboarding (full reference exercise: 15 min)
Read `requirements.txt` and list the pinned packages with their versions. Note why they are intentionally outdated (each is deliberately an old release so SCA tools flag its known CVEs).
**Deliverable:** the package/version table + which OWASP/CWE this maps to.

### Task 1 — SCA scan: build the remediation worklist (full reference exercise: 35 min)
**Goal:** Flag the known-vulnerable dependencies — A03.
**Steps:**
1. `bash sca_scan.sh` — read the `trivy fs` table (CVE, installed vs. fixed version) and the `pip-audit` advisory IDs (GHSA-/PYSEC-).
2. Pick three findings; record CVE/advisory id, severity, and the fixed version.
**Deliverable:** the SCA output + a 3-row remediation table (package → current → fixed).

### Task 2 — Dependency Confusion Heist (full reference exercise: 35 min)
**Goal:** Watch the wrong package win — A03 / CWE-1357.

**Reality check:** this lab does **not** stand up a live private/public registry. `acme-internal-utils` is
a worked example, not an installable package — there is nothing to actually `pip install` here (the name
doesn't exist on real PyPI either, so don't expect that to work as a shortcut). Task 2 is a controlled
walkthrough of the resolver's own rule, using the simulation below, which computes the real
"highest version wins" logic live instead of just asserting the outcome.

```sim
resolver-confusion
```

**Steps:**
1. Read `dependency-confusion.md`'s "Dependency confusion (substitution)" section for the mechanism.
2. In the simulation, load the **"the attack"** preset (private `1.4.0`, public `99.0.0`, merged /
   `--extra-index-url` mode) and record which index the resolver picks and why.
3. Keep the same version numbers and switch to the **single-index** (`--index-url`) mode; record how the
   verdict changes — this is the resolver behavior Task 4's "single trusted index" defense relies on.
4. Try the **"win the race"** preset (private version numerically higher than public) and note why the
   sim's own explanation calls that "not a defense."

**Deliverable:** a screenshot of the simulation's verdict in both index modes (merged vs. single) for the
same version pair, plus one sentence on why an attacker defeats the "keep my internal version number high"
idea.

### Task 3 — SBOM + signing/verification (full reference exercise: 30 min)
**Goal:** Produce a component inventory and prove integrity — A08.
**Steps:**
1. After `bash sign.sh week12-supplychain:lab`, open `sbom.cdx.json` and find Flask's entry.
2. Read the `cosign verify` PASS for the signed image.
3. Negative test on an unsigned image (it **must** fail) — `cosign` isn't on your host, so this runs in the
   same container `sign.sh` uses:
   ```bash
   docker run --rm --network host gcr.io/projectsigstore/cosign:latest verify \
       --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' python:3.9-slim
   ```
   → `Error: no signatures found`. (Both `--certificate-identity*` flags are required in keyless mode; without
   them cosign stops at `Error: --certificate-identity or --certificate-identity-regexp is required` — a usage
   error, which is *not* the same thing as proving the image is unsigned.) This step needs no OIDC login —
   you can run it yourself even if someone else drove the sign step in Task 3.1.
**Deliverable:** the SBOM Flask component entry + the verify PASS + the negative-test failure.

### Task 4 — Defend / fix it (full reference exercise: 35 min)
**Goal:** Stop dependency confusion and lock integrity — defenses from `dependency-confusion.md` + `sign.sh`.
**Steps:**
1. **Pin + hashes:** run this inside the provided Python container (your host's `pip`, if it has one, may be
   a different version or an "externally managed environment" that refuses `pip install` outright — this
   stays reproducible for everyone):
   ```bash
   docker run --rm -v "$PWD":/w -w /w python:3.9-slim pip install --require-hashes -r requirements.txt
   ```
   against this lab's own `requirements.txt` (it has no hashes yet) and record pip's refusal — `ERROR: Hashes
   are required in --require-hashes mode...` plus the `--hash=sha256:…` line pip prints for you. That refusal
   is the same mechanism that would block a real confusion substitution: once hashes are required, a package
   that doesn't match — from *either* index — cannot install silently.
2. **Single trusted index:** use one `--index-url` instead of `--extra-index-url`; explain why the resolver stops shopping around (tie this back to Task 2's single-index verdict).
3. **Namespace scoping:** describe reserving/namespacing the internal package name.
4. **Provenance gate:** state how the `cosign verify` from `sign.sh` becomes a gate before a simulated deploy —
   and note that `sign.sh`'s `--certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*'` are
   **demo wildcards** (any keyless signer passes); a real gate pins both flags to the one CI identity/issuer
   you trust, so an attacker who signs their own malicious image is still rejected.
**Deliverable:** the `--require-hashes` refusal output (step 1) + the simulation's before/after verdict for merged vs. single index (from Task 2) + the one defense you found most effective and why.

## Part 4 — Reflection

1. **Mapping:** table — finding | tool (`sca_scan.sh` / `sign.sh`) | OWASP 2025 id | CWE | fix.
2. **Real breach:** analyze the **XZ Utils backdoor (CVE-2024-3094)**. Which OWASP/CWE applies, and would an SBOM + signing + provenance gate have caught a maliciously-modified upstream dependency? (Compare with SolarWinds or Log4Shell if useful.)
3. **Best mitigation + SLSA self-assessment:** one paragraph — which SLSA level your defenses reach and why, and the single highest-leverage control for your team.

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

**Due:** Monday 25 January 2027, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **No flag this week:** everything is offline evidence and your own control; there is nothing to submit on ctf.zcr.ai. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

**Scored exhibit supplied for this assignment (deliberately incorrect):**

> "Any mathematically valid signature proves that our trusted publisher produced the artifact, so verifying against whichever public key arrives beside it is sufficient."

Identify the substantive mistakes (8), verify your criticism with relevant observations/tests or primary sources (8), and provide a justified correction (4). Use both the correct-key and independently signed wrong-key packets. Explain why signature validity and trust in the signer are separate checks.

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
