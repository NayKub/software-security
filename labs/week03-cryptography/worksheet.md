# Worksheet 3 — Cryptography Used Correctly (and Misused)

> **Course:** Software Security (KOSEN69) · **Week 3**
> **Aligned to:** OWASP 2025 (A04 Cryptographic Failures [CWE-327, CWE-916, CWE-330, CWE-321], A07 Authentication Failures [CWE-798]) · CWE-327, CWE-916, CWE-330, CWE-321, CWE-798
> **Signature game:** "Misuse Hunt" (find four crypto mistakes in 26 lines of code — with scanners, then with your own eyes)

> **This week's angle.** *How* hashes, ciphers, MACs and TLS work and break is taught in
> **Cryptography and Network Security (02005104)**, where cracking weak hashes, cipher modes, AEAD and
> TLS each get a full lab. This course does not repeat those attacks. Here you work on the
> application side: **find** crypto misuse in code, see what tools miss, and **fix** it with the right
> library call.

> **Ethics note:** Scan and test only this lab's files and your own fork of the project.

## Class and assessment contract

**Contact time: 150 minutes** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Build the lab image and pull the Week 2 scanner images before class (see Environment setup below). In class you do Tasks 0–6; Task 7 is optional homework.

**This week everyone does everything.** Complete the common practical 60 points plus **both** written sections, 40 points in total: **Conventional** = Part 2 written questions + Part 4 reflection, and **AIR-Sec** = Audit-the-AI + Explain-in-Plain-English + Prompt Problem. There is no odd/even split this week; the worksheet totals 100. Only the named 100-minute core is assessed in the shared 60; other practical tasks are optional extension/reference unless explicitly used in the assigned written questions, and are not a prerequisite for full marks. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 3 answer sheet from Google Classroom, and say there which AI tool you used, if any.

## Part 1 — Student Information
Fill these in at the top of the answer sheet:

| Name | Student ID | Date | Code link | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

## Part 2 — Lecture Questions
Answer in your own words (2–4 sentences each), from this week's slides.
1. Hashing, encryption and encoding are three different tools. Which one does `store_password()` in `vulnerable_crypto.py` use, which one does `encrypt_ecb()` use, and why is Base64 never a way to protect a secret?
2. In Week 2, Semgrep flagged MD5. Give two reasons a pattern-matching scanner can miss a crypto mistake such as a weak reset token or a hardcoded key.
3. Why is an encryption key written in source code dangerous even in a private repository, and why does deleting it in a new commit not fix the leak?
4. An app has 10,000 users whose passwords are stored as unsalted MD5. Why can't you convert them all to argon2id tonight, and how does *rehash-on-login* solve it?
5. What's the difference between `random` and a CSPRNG (e.g. `secrets`), and where does it matter?

![Four paired rows showing that password storage, cipher mode, randomness and key source are four separate crypto decisions: MD5 (CWE-916/327) becomes argon2id, AES-ECB with a hardcoded key (CWE-327) becomes AES-GCM with a nonce and tag, a 6-digit random.choice token (CWE-330) becomes secrets.token_urlsafe, and HARDCODED_KEY (CWE-798) becomes a key injected from the environment — so naming AES answers none of the four questions.](img/crypto-misuse.svg)

## Part 3 — Shared practical core (100 min in class)

**100-minute core:** Baseline behavior (5), scanner observations (10), code review (15), token predictability (10), key-handling analysis (10), student rehash-on-login (30), fixed control checks (20).

The minutes are a pacing guide. This week everyone completes Part 2/Part 4 and Audit/EiPE/Prompt; together they make up the 40 written points.


**Learning goals:** find four crypto misuses in application code — first with scanners, then by reading the code — and fix them with the right library call: a vetted KDF with a migration path, authenticated encryption, a CSPRNG, and a key from the environment.
**Prerequisites:** Docker, the scanner images from Week 2 (`semgrep/semgrep`, `zricethezav/gitleaks`), and this lab's prepared `kosen-swsec-week03:local` image. Build the lab image while online before class; no new tool is needed during the practical.

**Words used below:** *KDF* = a slow password-hashing function such as argon2id. *CSPRNG* = a random-number generator that attackers cannot predict (Python's `secrets`). *Nonce* = a random number used once per encryption. *Literal* = a value typed directly into the code. *Brute-force* = trying every possible value until one works. *Pattern-matching scanner* = a tool like Semgrep that looks for known code shapes; it cannot understand what the code is for.

**Environment setup**
On Windows, type every command in the Ubuntu app.

```bash
cd ~/software-security/labs/week03-cryptography
docker compose build
docker compose up --no-build --pull never
```
Run `docker compose build` once before class, while online: it installs the pinned Python packages into the lab image. `docker compose up --no-build --pull never` then runs the program without downloading anything. If `cd` says "no such file or directory", you cloned the repository somewhere else: ask your instructor. Run every command below from this folder.

Targets: `vulnerable_crypto.py` (four crypto mistakes, not labelled), `migrate.py` (Task 5) and `solution_skeleton.py` (the fixed version).

**What to submit per task:** the command run + a screenshot of the result + the short answer the task asks for.

**Task 0 — Onboarding (5 min, in class)** · *Goal:* see what the code produces. *Steps:* run `docker compose up --no-build --pull never`. Every line starts with `crypto-lab-1 |`; ignore that part. Record the **first three** lines: `md5:`, `ecb:` and `token:` (a 6-digit number). The lines after the one starting `--- secure reference` come from the fixed version you check in Task 6, so you can ignore them now. *Deliverable:* screenshot of the program output.

**Task 1 — Let the tools look first (10 min, in class)** · *Goal:* see what a scanner finds on its own. *Steps:* from `labs/week03-cryptography`, run the two Week 2 tools on `vulnerable_crypto.py`:

```bash
docker run --rm -v "$PWD":/src -w /src semgrep/semgrep \
    semgrep scan --config p/python --metrics=off vulnerable_crypto.py
docker run --rm -v "$PWD":/src zricethezav/gitleaks:latest \
    detect --no-git --source /src/vulnerable_crypto.py --no-banner
```

If the Semgrep registry is unavailable, use the supplied narrow rule offline and label that result as the **local fallback**:

```bash
docker run --rm --network none -v "$PWD":/src -w /src semgrep/semgrep \
    semgrep scan --config semgrep-local.yml --metrics=off --disable-version-check vulnerable_crypto.py
```

*You should see:* Semgrep reports 1 finding, an MD5 rule on line 9. Gitleaks prints `no leaks found`: that is a real result, not an error. Write down every finding (rule name and line), or "no findings", and which ruleset you used. The local fallback checks MD5 calls only; it cannot establish that the other crypto decisions are safe. If the registry rule prints SHA-256/SHA-3 advice, judge whether that is the right fix **for storing passwords**. *Deliverable:* screenshot of both scanner outputs + your list of findings + one line judging the advice or the fallback rule's limit.

**Task 2 — Find the rest by reading (15 min, in class)** · *Goal:* do the review the tools could not. *Steps:* show the file with line numbers:

```bash
cat -n vulnerable_crypto.py
```

Read all 26 lines with the checklist from the slides: MD5/SHA-1 used for security, `MODE_ECB`, a key written as a literal, `random` used for something secret. Fill in one row per mistake:

| Line | What the code does | The mistake | CWE | Flagged by a tool in Task 1? |
|---|---|---|---|---|
| | | | | |

CWE numbers to choose from: **CWE-916** = a password hash that is too fast or weak; **CWE-327** = a broken or risky crypto algorithm or mode; **CWE-330** = randomness an attacker can predict; **CWE-798 / CWE-321** = a password or key written directly in the code. A mistake can fit more than one; pick the best one or write both.

Then, in the `ecb:` line from Task 0, mark the two identical 16-byte blocks (32 hex characters each): that repetition is what ECB leaks. The line is one 96-character string, so this command cuts it into 32-character pieces for you (wait 10–20 seconds):

```bash
docker compose up --no-build --pull never 2>&1 | grep "ecb:" | sed "s/.*ecb: //" | fold -w 32
```

*You should see:* 3 lines of 32 characters; the first two are exactly the same. Copy all 3 into your answer sheet and highlight the 2 matching lines. (*Why* ECB behaves like this is the Cryptography course's cipher-modes lab — here you only need to recognise `MODE_ECB` in code.) For each mistake no tool flagged, write one line on why a pattern-matching tool cannot be sure it is a bug. *Deliverable:* the four-row table + the marked `ecb:` line + the one-liners.

> **Cracking `hashes.txt`?** Not this week — that attack is the Cryptography course's hash lab. The
> file stays in this folder as optional practice for the midterm practical (no marks here).

**Task 3 — Predictable token (10 min, in class)** · *Goal:* show the reset token is guessable. *Steps:* from `labs/week03-cryptography`, print several `reset_token()` values with this one Docker command:

```bash
docker run --rm --network none -v "$PWD":/work -w /work kosen-swsec-week03:local \
    python -c 'import vulnerable_crypto as v; [print(v.reset_token()) for _ in range(5)]'
```

*You should see:* five 6-digit numbers (yours will be different). Explain why a 6-digit `random` token is easy to brute-force (CWE-330): there are only 10^6 = 1,000,000 possible tokens, and `random` is not a CSPRNG. Assume an attacker can try 100 guesses per second. *Deliverable:* sample tokens + a one-line attack estimate.

**Task 4 — Get the key out of the code (10 min, in class)** · *Goal:* fix the key-management mistake properly. *Steps:* find the key literal in `vulnerable_crypto.py`; explain why shipping a key in source is CWE-798 (its cryptographic-key case is CWE-321), and say where the key should come from instead. Then explain why removing the line in a new commit does **not** end the leak (think of what Gitleaks scanned in Week 2). *Deliverable:* the line + a 2-sentence mitigation + one line on git history.

**Task 5 — Rehash-on-login (30 min, in class, guided)** · *Goal:* upgrade old MD5 passwords to argon2id the way real apps do. *Steps:* run `migrate.py` once. The first run shows 2 `FAIL` lines and `Not done yet` — that is expected before your edit. Open `migrate.py` in an editor (for example `nano migrate.py`; save with Ctrl+O then Enter, exit with Ctrl+X), write your one line under the `TODO` comment in `login()`, save, and run it again until it prints `ALL PASS`:

```bash
docker run --rm --network none -v "$PWD":/work -w /work kosen-swsec-week03:local python migrate.py
```

The output already includes the wrong-password check (`a wrong password is refused`) and the second login, so one screenshot covers them. *Deliverable:* the line you wrote + a screenshot of `ALL PASS` + 2 sentences: why the upgrade can only happen at login, and why the MD5 check uses `hmac.compare_digest`.

**Task 6 — Defend / fix it (20 min, in class, guided)** · *Goal:* check the fixed version, with the key coming from the environment. *Steps:* run `solution_skeleton.py` with a fresh key in `ENC_KEY_HEX`:

```bash
export ENC_KEY_HEX=$(openssl rand -hex 32)
docker run --rm --network none -e ENC_KEY_HEX -v "$PWD":/work -w /work \
    kosen-swsec-week03:local python solution_skeleton.py
```

Never show your `ENC_KEY_HEX` value in a screenshot. *You should see:* `argon2 ok: True`, a `gcm:` line with three byte strings (nonce, ciphertext, tag) and a long random `token:`. Then open `solution_skeleton.py` and confirm `store_password`/`verify_password` use argon2id (auto-salted), `encrypt_gcm` uses a random 12-byte nonce + auth tag with the key from `ENC_KEY_HEX`, and `reset_token` uses `secrets`. Map each fix to the CWE it closes. *Deliverable:* before/after table (mistake → fix → CWE closed) + screenshot of the fixed script running.

**Task 7 — Your project: NoteVault (homework, optional extension; no extra graded points)** · *Goal:* find the same mistakes in your term project. *Steps:* scan the NoteVault starter app from inside its own folder (a scan started at the repo root finds nothing there, because the root `.semgrepignore` excludes it):

```bash
cd project/starter-app
docker run --rm -v "$PWD":/src -w /src semgrep/semgrep \
    semgrep scan --config p/python --metrics=off .
```

List the crypto-related findings (file:line + rule), say which of this week's four mistakes NoteVault repeats, and describe in 2–3 sentences how rehash-on-login would move NoteVault's users off MD5. *Deliverable:* the list + the sketch — record it as a finding for your project report (`project/REPORT-TEMPLATE.md` in the repo root).

**Supplied reference versus student code:** despite its name, `solution_skeleton.py` is already complete: it is the instructor's fixed version. Your required authored change is the rehash-on-login TODO in `migrate.py`. Add a wrong-password/no-migration case and a subsequent successful login to your evidence; do not claim that merely running the reference implements the migration. This week is software misuse review, not a repeat of the cryptography course's cracking/mode-attack lab.

## Part 4 — Reflection
1. Map each of the four mistakes to its CWE and OWASP category, in one line each: weak password hashing, ECB encryption and the random reset token are all **A04 Cryptographic Failures**; the hardcoded key is **A07 Authentication Failures** (see the "Aligned to" line at the top of this sheet).
2. Name a real-world breach caused by weak password hashing or hardcoded keys, and which fix here would have prevented it.
3. Which of the four mistakes did no tool flag, and what would you add to code review or CI so it is caught next time?

## Grading rubric (100)
| Criterion | Points |
|---|---:|
| Common practical: main task and observations | 20 |
| Common practical: student defense/control or design, tests and limitations | 20 |
| Common practical: reproducible evidence and reasoning | 20 |
| Written: Conventional Part 2 + Part 4 **and** AIR-Sec Audit-the-AI + Explain-in-Plain-English + Prompt Problem (everyone does both) | 40 |
| **Total** | **100** |

The optional project/upload extension adds no extra graded points to the common 60 or the written 40.

**Due:** Monday 23 November 2026, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Personalized flag:** none this week. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — AIR-Sec section (everyone this week)

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Audit a complete AI answer about this week's design, exploit or fix. If your instructor gives you an AI answer to audit, use it; otherwise ask an AI assistant to fix `vulnerable_crypto.py` and paste its full answer. A correct answer is allowed: verify its claims and state the remaining assumptions rather than inventing an error.
2. **Check what is correct, wrong, risky or conditional** — insecure code, an incomplete fix, a hallucinated API/function/CVE, an edge case or unsupported reasoning. Quote the exact line(s) and support the evaluation with evidence.
3. Supply a verified correction where needed; if the answer is correct, supply the verification and limits. Explain your conclusion in 2–3 sentences. Do not manufacture a defect to satisfy the task.

> Write which AI tool you used in the table at the top of your answer sheet. This week everyone completes this section as part of the 40 written points.

---

## 🧠 Comprehension & Prompt — AIR-Sec section (everyone this week)

**A. Explain in Plain English (EiPE).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem.** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Run it: does the mistake go away (for example, the Semgrep finding disappears, or `migrate.py` still prints `ALL PASS`)? If not, refine the prompt and try again. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
