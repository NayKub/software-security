# Week 12 — Software Supply-Chain Security

## Class and assessment contract

**Class: Tuesday 19 January 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the checker image before class. In class you do the five core tasks in the worksheet's Part 3; the optional extension adds no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. There is no flag this week. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write which AI tool you used, if any, on the answer sheet.

**Due:** Monday 25 January 2027, 23:59 (Thai time).

*(Merges the former Dependencies and Integrity/Provenance weeks into one.)*

**OWASP 2025:** A03 Software Supply Chain Failures, A08 Software or Data Integrity Failures · **CWE:** CWE-1104, CWE-829



## Before class and the core commands

Build the checker image once, while online:
```bash
cd ~/software-security/labs/week12-supply-chain
docker build -f Dockerfile.student -t softsec-student-checks:local .
```

In class, in this lab folder, the core uses these offline commands (the worksheet's Part 3 says what to look for in each):
```bash
python3 resolver_core.py --mode merged
python3 resolver_core.py --mode single
python3 sbom_core.py
docker run --rm --network none -v "$PWD:/work:ro" -w /work softsec-student-checks:local
```
The last command runs the signature checker: it fails before you complete `trusted_key()` in `student_task.py` and passes after. `sca-core.snapshot.json` is a supplied pip-audit result to read, not a scan you run.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); while online, build the checker image (above). Skim last week's recap.
2. **Slides, then class** — read `slides/week12.md` and the worksheet's Part 2 to prepare. Class opens with the weekly quiz (10 min) and a short explanation and demo (15 min).
3. **Lab (in class)** — do the five core tasks in the worksheet's Part 3: supplied SCA results (20 min), resolver case (15), SBOM (20), your key-pin control (30) and hash/index control (15). Then do the written section for your student ID this week (odd: Conventional 40; even: AIR-Sec 20/10/10), after class if needed. `bash sca_scan.sh` and `sign.sh` are optional extensions.
4. **Submit by Monday 25 January 2027, 23:59** — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link to `student_task.py` on branch `wk12`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Explain why the supply chain is now a top-tier risk; recognize dependency confusion, typosquatting, malicious packages, transitive risk.
- Interpret the supplied, dated SCA results; run a fresh scan only when the scanner images and advisory databases are prepared.
- Generate/read an SBOM (CycloneDX/SPDX); explain SLSA provenance levels.
- Verify a real artifact signature against the issued trusted key; distinguish integrity, trusted signer identity and provenance. Retain Sigstore/Cosign keyless/OIDC signing as prepared extension practice.

## 📦 Resolver case and prepared keyless-signing extension
**Round 1 — Attack:** no live registry ships with this lab — walk the resolver's own "highest version wins" rule via `dependency-confusion.md` and the embedded resolver simulation (Worksheet 12 Task 2) and watch the wrong package win the version comparison.
Optional live SCA (this is a Python lab, so no npm audit): `sca_scan.sh` runs trivy on `requirements.txt`, then pip-audit:
```bash
bash sca_scan.sh
```
**Prepared extension — real keyless signing:** pin versions / add a lockfile and registry scoping. Run the following only when the instructor has preflighted registry, digest, networking and OIDC access; the offline signature core above earns the required control marks:
`sign.sh` pushes to a throwaway local registry, makes the SBOM, then signs and verifies with cosign:
```bash
docker build -t week12-supplychain:lab .
bash sign.sh week12-supplychain:lab
```
- Produce an SBOM and identify the component inventory.
- Show a tampered/unsigned image **fails** verification.
- Add a provenance/attestation gate before a simulated deploy.

## Deliverable
Required core: SCA/SBOM observations, resolver/hash-index analysis, the student key-pin diff and the real-signature positive/tamper/wrong-signer transcript. A prepared keyless-signing transcript and SLSA self-assessment are extension material; distinguish component inventory, signature integrity and provenance claims.

## References
- https://slsa.dev/  ·  https://www.sigstore.dev/  ·  https://cyclonedx.org/
- https://owasp.org/www-project-dependency-check/

**Scanner preflight:** confirm that the tool ran and produced a report before interpreting a count. Reporting wrappers may continue after a tool error (`|| true`); missing output or a failed download is not evidence of zero findings. Instructor-provided reports must be labelled as supplied cases rather than claimed as a personal scan.
