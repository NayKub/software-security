---
marp: true
theme: default
paginate: true
header: "Software Security · Week 3"
---

# Week 3
## Cryptography Used Correctly (and Misused)
Software Security 2 · Nutthakorn Chalaemwongwan · Shinya Oyama

<!-- Hook: put vulnerable_crypto.py on screen (26 lines) and ask "how many crypto mistakes?" Most people say one (MD5). There are four, and a scanner finds only some of them. Today is about finding crypto misuse in code and fixing it with the right library call; how the math works and breaks is the Cryptography course's job. ~2 min. -->

---

## Today

**KOSEN class: 150 minutes.** Quiz/review 10 + brief/demo 15 + practical 100 + debrief 20 + capture 5. Full slide explanations are preparation/reference.

**Worksheet:** common practical 60 + written 40. **This week everyone does both written parts:** Conventional (Part 2 + Part 4) **and** AIR-Sec (Audit the AI + Explain in Plain English + Prompt Problem), 40 points in total. The worksheet totals 100. Your instructor may ask you to show or repeat a step. Extensions add no graded points.


- Two courses, two angles: Cryptography explains *how it breaks*; we find *where it hides in code*
- What a scanner catches — and what it misses
- Passwords: argon2id + moving old MD5 records (rehash-on-login)
- Keys out of source · CSPRNG tokens
- 🔎 Game: **Misuse Hunt**

<!-- Roadmap, 1 min. Lab: scan, hunt the rest by reading, migrate MD5 to argon2id, run the fixed version. -->

---

## Recap — Week 2

- Semgrep flagged **MD5** as a bug pattern
- Today: the crypto mistakes a pattern **can't** see — and why

<!-- Bridge: in W2 a SAST tool flagged MD5. Today the same tool is run on a small crypto module; it finds one thing, the rest is code review. ~1 min. -->

---

## Two courses, two angles

- **Cryptography and Network Security (02005104):** how primitives work and break — cracking weak hashes, cipher modes, MACs, AEAD, TLS
- **This course:** where crypto misuse hides in *application code*, how to find it, which library call fixes it
- So no hash cracking or ECB attacks here — you do those in the Cryptography labs

<!-- All KOSEN students take both courses. Say it plainly: we do not repeat the attacks; we use what they learned there to review code. If they ask about cracking for the midterm practical, hashes.txt is in the lab folder as optional practice. ~2 min. -->

---

## Three things people confuse

- **Hashing** — one-way, fixed-size digest (integrity, passwords)
- **Encryption** — reversible *with a key* (confidentiality)
- **Encoding** — reversible *without a key* (Base64 ≠ security!)

<!-- The #1 source of crypto bugs is conceptual confusion. Demo: base64-decode a string live to show encoding gives no protection. Part 2 Q1 asks which one store_password() and encrypt_ecb() use. ~3 min. -->

---

## Password storage

- Never store plaintext or plain hashes
- Use a **slow, salted KDF**: **argon2id** (scrypt / bcrypt / PBKDF2 only where argon2id isn't available)
- Salt is per-user and random: identical passwords hash differently, so precomputed (rainbow) tables fail

```python
from argon2 import PasswordHasher
ph = PasswordHasher(); hash = ph.hash("correct horse battery staple")
```

<!-- They saw WHY fast unsalted hashes fall in the Cryptography hash lab; here the point is the library call. argon2-cffi picks the salt and parameters for you. ~3 min. -->

---

## Old MD5 records: rehash-on-login

```python
def login(user, pw):
    record = db[user]
    if is_legacy_md5(record):
        if not hmac.compare_digest(md5(pw), record):
            return False
        db[user] = ph.hash(pw)   # upgrade now: only at login do we hold pw
        return True
    return ph.verify(record, pw)
```

- You can't re-hash 10,000 MD5 records tonight: you never had the passwords
- Each user moves to argon2id at their next successful login — no reset email

<!-- This is Task 5 (migrate.py): students write the one marked line. compare_digest avoids a timing side channel on the old check. Users who never log in stay on MD5: say that after a deadline you force a reset for them. ~4 min. -->

---

## What the scanner sees

```bash
semgrep scan --config p/python vulnerable_crypto.py
# -> insecure-hash-algorithm-md5   line 9
#    "...Use SHA256 or SHA3 instead."
gitleaks detect --no-git --source vulnerable_crypto.py
# -> no leaks found
```

- It matches **API names** — it can't know a `random` value is a reset token
- A key like `b"0123456789abcdef"` doesn't look like a secret
- Its advice is for signatures: **SHA-256 is still wrong for passwords**

<!-- Run it live if the network allows; this is the output on the day the lab was written. Registry rules change, so students record whatever their own run shows. Key point: one finding out of four, and its suggested fix is the wrong one for passwords. ~4 min. -->

---

## Review checklist

- **MD5 / SHA-1** used for passwords or security
- **`MODE_ECB`** — identical blocks give identical ciphertext (CWE-327)
- **A key written as a literal** in source (CWE-321, a case of CWE-798)
- **`random`** used for anything secret (CWE-330)

<!-- Students use exactly this list in Task 2 to find the four mistakes by reading. ECB: recognise MODE_ECB and point at the repeated block in the ecb: line; the why is the Cryptography cipher-modes lab. ~3 min. -->

---

## Keys belong outside the code

- Load the key at runtime: environment variable or a secrets manager / KMS
- **Deleting the line in a new commit doesn't end the leak**: it stays in git history (Gitleaks scans history — Week 2)
- After a leak: rotate the key, then remove it

```bash
export ENC_KEY_HEX=$(openssl rand -hex 32)   # Task 6
```

<!-- Task 4 + Task 6. A private repo still gets cloned, forked, backed up and shared with contractors. ~3 min. -->

---

## Do this instead

- Passwords: **argon2id** via a library, never your own scheme
- Data: **authenticated encryption (AES-GCM)** — unlike ECB or plain CBC it detects a changed ciphertext
- Tokens: a CSPRNG — `secrets` (Python), `crypto.randomBytes` (Node)
- Keys: from the environment / KMS, never in code

<!-- The "right library call" slide. The Cryptography course shows the attacks behind each line; here students should leave able to pick the call. ~2 min. -->

---

## Four fixes — in the code

```python
# vulnerable_crypto.py                       ->  solution_skeleton.py
md5(pw).hexdigest()           # CWE-916      ->  argon2.PasswordHasher().hash(pw)
AES.new(key, AES.MODE_ECB)    # CWE-327      ->  AES.new(key, MODE_GCM, nonce=os.urandom(12))
HARDCODED_KEY = b"0123..."    # CWE-798      ->  bytes.fromhex(os.environ["ENC_KEY_HEX"])
random.choice("0123456789")   # CWE-330      ->  secrets.token_urlsafe(16)
```

- Four separate decisions — **KDF · cipher mode · key source · RNG** — not one "use better crypto"
- "Use AES" answers none of them: AES-GCM under a hardcoded key is still CWE-798

<!-- Task 6 (the fixed version). Walk the four rows; land on the closing line. ~3 min. -->

---

## 🔎 Game — Misuse Hunt

- **Round 1 (speedrun):** scan + read — first team to list all four mistakes with line numbers and CWE wins
- **Round 2:** rehash-on-login — first team whose `migrate.py` prints `ALL PASS`
- **Round 3 (defend):** run the fixed version with the key from `ENC_KEY_HEX`

<!-- Explain rounds before lab. Leaderboard on round 1; check line numbers, not just names. ~2 min. -->

---

## Lab 3 — deliverable

> 📋 **Worksheet 3** — `labs/week03-cryptography/worksheet.md` (Part 3) · **before class:** `docker compose build` while online and pre-pull both scanner images · **kickoff:** `docker compose up`

- Tool findings + your judgement of the tool's advice
- The four-mistake table (line · mistake · CWE · flagged by a tool?) + the repeated ECB block marked
- Token sample + estimate · key line + git-history point
- `migrate.py` → `ALL PASS` · fixed version + before/after table
- Every screenshot: **whoami + student ID + timestamp in-frame** · **Written 40, everyone does both: Conventional Part 2 + Part 4 and AIR-Sec Audit / EiPE / Prompt** (see worksheet)

<!-- Graded output. Optional extension (homework): scan NoteVault and record its crypto findings for the project report. -->

---

## Key takeaways

- Scanners find some crypto mistakes; code review finds the rest
- argon2id for passwords — and rehash-on-login to get there from MD5
- Keys outside the code · `secrets` for tokens

<!-- Recap. Cold-call: "Semgrep said use SHA-256 — why is that wrong here?" ~2 min. -->

---

# Questions?
Next week: Injection & input handling

<!-- Cliffhanger: "Next week — type one quote mark and log in as admin." -->
