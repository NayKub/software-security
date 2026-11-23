# Week 3 — Cryptography Used Correctly (and Misused)

**OWASP 2025:** A04 Cryptographic Failures · **CWE:** CWE-327, CWE-916, CWE-330, CWE-321 (key case of CWE-798)

## Class and assessment contract

**Contact time: 150 minutes** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Build the lab image and pull the Week 2 scanner images before class. In class you do Tasks 0–6; Task 7 is optional homework.

**This week everyone does everything.** Complete the common practical 60 points plus **both** written sections, 40 points in total: **Conventional** = Part 2 written questions + Part 4 reflection, and **AIR-Sec** = Audit-the-AI + Explain-in-Plain-English + Prompt Problem. There is no odd/even split this week; the worksheet totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write which AI tool you used, if any, on the answer sheet.

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); keep the Week 2 scanner images (`semgrep/semgrep`, `zricethezav/gitleaks`) and run `docker compose build` in this lab while online. The built `kosen-swsec-week03:local` image contains the pinned Python packages, so class tasks can run without a PyPI download. Skim last week's recap.
2. **Slides, then class** — prepare the concepts before class. The 150-minute slot includes quiz/review 10, a brief/demo 15, the common practical core 100, debrief 20 and evidence/exit 5.
3. **Lab (in class)** — complete the bounded common practical core. Baseline behavior (5), scanner observations (10), code review (15), token predictability (10), key-handling analysis (10), student rehash-on-login (30), fixed control checks (20). Then complete both written parts (Conventional and AIR-Sec, 40 points in total), after class if needed.
4. **Submit before the next class** (homework included) — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link on branch `wk03`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: the class contract above and [Week 3 worksheet](worksheet.md). Grading: see the worksheet rubric.*

## Objectives
- Find crypto misuse in application code — with a scanner first, then by reading the code — and know why tools miss some of it.
- Store passwords with a vetted KDF (argon2id), and move legacy MD5 records to it with rehash-on-login.
- Keep keys out of source code, and use a CSPRNG for tokens.

How the primitives themselves work and break (cracking hashes, cipher modes, MACs, TLS) is taught in
Cryptography and Network Security (02005104). This week stays on the application-code side.

## 🔎 Signature game — "Misuse Hunt"
1. **Scan:** run Semgrep and Gitleaks on `vulnerable_crypto.py` and note what they flag — and what they don't.
2. **Hunt:** read the code with the checklist (MD5/SHA-1, `MODE_ECB`, key literals, `random` for secrets) and find all four mistakes with their line numbers.
3. **Remediate:** finish the rehash-on-login in `migrate.py` until it prints `ALL PASS`, then run the fixed version (argon2id, AES-GCM, `secrets`, key from `ENC_KEY_HEX`).

## Deliverable
The mistake table (line, mistake, CWE, flagged by a tool or not) + before/after code + a short note on which CWE each change closes.

## References
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
