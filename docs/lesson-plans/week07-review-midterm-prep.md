# Lesson Plan — Week 7: Reflection & Review (pre-Midterm)

| | |
|---|---|
| **Course** | Software Security 2 (02005094, KOSEN-KMITL) |
| **Week / date** | 7 · Tuesday 15 December 2026, 09:05–11:50 |
| **Contact time** | 150 min, one continuous block (`AGENDA.md`, *Review weeks 7 and 17*): cumulative quiz 30 + Jeopardy 20 + two practice checkpoints 70 (35 each) + debrief/logistics 25 + save evidence 5 |
| **Lab folder** | `labs/week07-review-midterm-prep` — `README.md`, `mock-ctf.md` |
| **Slides** | `slides/week07.md` |
| **Type** | Review — **no new content**. Consolidates Weeks 1–6 |
| **Standards consolidated** | OWASP 2025 **A01** Broken Access Control · **A02** Security Misconfiguration · **A04** Cryptographic Failures · **A05** Injection · **A06** Insecure Design · **A07** Authentication Failures · CWE-501, 798, 489, 327, 916, 330, 89, 78, 434, 79, 352, 1004, 639, 287, 347, 321 |
| **CLOs addressed** | **CLO1–CLO4** (course specification §6, week 7 row) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — Recall, without notes, the one-line core of each of Weeks 1–6 and name the CWE and OWASP 2025 category that goes with it.
- K2 — State which of the six half-term topics is rehearsed by each of today's two practice checkpoints, and which four (threat modelling, tooling, cryptography, XSS) are reached today only by Jeopardy and Quiz 1, not by a checkpoint.
- K3 — Describe the shape of both midterm papers — what the Week 8 written exam asks for and what the Week 9 practical asks for — well enough to plan revision time against it.

**Skills (P)**
- P1 — Re-implement the Week 4 and Week 6 student-patch fixes unaided, from a fresh untouched copy, under the same two-function shape the real exam rewards (parameterize/validate; verify-then-authorize) — in class for the 70-minute block.
- P2 — For each checkpoint, give the one-line root cause and fix, and name the CWE — exactly what `mock-ctf.md` asks for and what the Week 8/9 papers also reward.
- P3 — Produce a one-page cheat sheet that is their own compression of the half-term, not a transcription of the slides.
- P4 — Identify, honestly, which topics they cannot yet do unaided, and say so in the debrief.

**Attitude (A)**
- A1 — Work only against the supplied practice copies under [ETHICS.md](../../ETHICS.md) — this holds in a practice checkpoint exactly as it does in a graded one.
- A2 — Treat the checkpoints as calibration rather than performance: an unsolved checkpoint found today is worth more than a solved one copied from a neighbour.
- A3 — Practise writing the same fixes **by hand** as well — Week 9 is a paper exam with no computer.

## 2. Key ideas (the through-line)

Weeks 1–6 look like six separate topics and are really one question asked six times: *where does
untrusted data cross a boundary, and what does it get to control on the other side?* In Week 1 the
boundary is drawn on a diagram; in Week 4 the data crosses it into a SQL parser and a shell; in Week 5
into an HTML parser; in Week 6 into an authorisation decision; in Week 3 into a key or a hash; in
Week 2 a tool looks for the crossing on the developer's behalf and misses some of them. The review
week's job is to make that single question retrievable under time pressure, because the exam will
present it in an unfamiliar wrapper. The second job is calibration: students consistently over-rate
what they can reproduce without the worksheet open beside them, and today's two checkpoints are the
cheapest place to discover that.

## 3. Prior knowledge and preparation

- **Students, before class:** review Weeks 1–6 — slides, their own submitted worksheets, and the
  CWE/OWASP list (`labs/week07-review-midterm-prep/README.md`). Bring the machine they will sit
  Week 9 on, and confirm Docker still runs.
- **Instructor, before class — the two checkpoint images.** The checkpoints need only the Week 4 and
  Week 6 images already built in those weeks (`week04-injection-injection-lab:latest`,
  `kosen-swsec-week06:local`) — no live server, no port, and no network access at class time; the
  checkers run entirely in-process (`docker run --network none ...`). If a student's machine lost the
  images, rebuilding is a single `docker compose build` in the real `labs/week04-injection` or
  `labs/week06-authn-authz` folder while online, which `mock-ctf.md` itself says to do if `docker run`
  reports the image missing.
- **Instructor, before class — the Jeopardy board.** No board file ships in the repo. The presenter
  note in `slides/week07.md` says to prepare it beforehand — 6 categories × 5 values, questions
  seeded from the exam item bank (the banks live in the git-ignored `instructor/` directory:
  `instructor/exams/item-bank.md`, `instructor/quizzes/review-quiz-item-bank.md`).
- **Instructor, before class — the quiz.** `README.md` and `slides/week07.md` both say the cumulative
  review quiz runs on `learn.zcr.ai/quiz`, the same portal as the weekly quizzes — **confirm the
  Week 7 assessment has actually been created there before class** (as of this check it had not yet
  been; other weeks' assessments are normally created well ahead of their class date). Decide whether
  the cheat sheet will be admitted to the Week 8 written exam; `slides/week07.md` asks for that
  decision to be **announced today**, because it changes how students build the sheet.
- **Prerequisite state:** the Week 3, 4, 5 and 6 labs have been completed and submitted. A student
  who never stood up the Week 4 or Week 6 target will lose checkpoint time to environment setup.

## 4. Consolidation plan — the six weeks under review

| Wk | Topic | Signature exercise | Must be retrievable cold | Re-tested today by |
|---:|---|---|---|---|
| 1 | Security mindset & threat modelling | Threat model + STRIDE on the sample app | STRIDE letters → property violated; what a trust boundary is; attack surface | Jeopardy (*Threat Modeling*); Quiz 1 Part B |
| 2 | Secure SDLC, tooling & fuzzing | Scanner/secret-finding triage | SAST vs DAST vs SCA vs fuzzing — what each sees, when it runs; true vs false positive | Jeopardy (*Tooling*); Quiz 1 Part A |
| 3 | Cryptography used correctly (and misused) | Legacy-password rehash-on-login (`migrate.py`) | hashing vs encryption vs encoding; why MD5 is wrong for passwords; salts; why ECB leaks | Jeopardy (*Crypto*); Quiz 1 Part B — **no checkpoint today** |
| 4 | Injection & input handling | SQLi + command-injection patch (`student_patch.py`) | data vs code; why a parameterised query wins and escaping does not; `shell=True` → CWE-78 | **Checkpoint 1**; Jeopardy (*Injection*); Quiz 1 Part C |
| 5 | XSS & client-side risks | Encoding + CSRF-token patch | reflected vs stored vs DOM; contextual output encoding; CSP; `HttpOnly`/`SameSite`/`Secure` | Jeopardy (*XSS*) — **no checkpoint today** |
| 6 | Authentication, sessions & access control | JWT verification + ownership patch (`student_patch.py`) | authentication ≠ authorisation; IDOR; `alg:none`; weak HMAC secret; `exp`/`aud` | **Checkpoint 2**; Jeopardy (*Auth & Access*); Quiz 1 Part C |

**Coverage gap to name out loud.** Today's two practice checkpoints are drawn from Weeks 4 and 6
only — the same two weeks whose student-patch shape the Week 9 practical's Stations C and D rehearse
directly. Weeks 1, 2, 3 and 5 are **not** re-tested by a checkpoint today; they are carried by
Jeopardy and Quiz 1, and Weeks 1, 2 and 3 are also examined directly in the **Week 9 practical**
(Stations A and B). A student who revises only from today's two checkpoints will walk into Week 9
having skipped two of its four stations.

## 5. Session run-sheet — 150 min

Timings are `AGENDA.md`'s review-week agenda (*Review weeks 7 and 17*). There is no break.

| Time | Block | What happens |
|---|---|---|
| 0:00–0:30 | **Cumulative review quiz** | Quiz 1 (`quizzes/quiz1.md`, 25 pts) on `learn.zcr.ai/quiz` |
| 0:30–0:50 | **Security Jeopardy** | Team quiz-show across the six topics |
| 0:50–2:00 | **Two practice checkpoints** | `labs/week07-review-midterm-prep/mock-ctf.md` — Checkpoint 1 (Week 4, 35 min) then Checkpoint 2 (Week 6, 35 min), entirely in class |
| 2:00–2:25 | **Debrief** | Common mistakes (§6) + midterm logistics (§7) |
| 2:25–2:30 | **Save evidence** | Personal revision list |

### 5.1 Cumulative review quiz — 0:00–0:30

| Field | Value |
|---|---|
| Instrument | `quizzes/quiz1.md` — "Quiz 1 — Foundations & Web Security (Weeks 1–6)" |
| Weight | 25 pts, 30 min |
| Blueprint | Part A multiple choice 10 × 1 pt · Part B short answer 3 × 3 pts · Part C spot-the-vulnerability 2 × 3 pts |
| Covers | Threat modeling · SDLC/tooling/fuzzing · Cryptography · Injection · XSS · Auth & access control |
| Conditions | Closed book unless the instructor states otherwise |
| Delivery | `learn.zcr.ai/quiz` — the same portal as the weekly quizzes, individual one-time code given in class. `quiz1.md` is the content reference and paper fallback |
| Where it counts | The 10% weekly-quizzes / participation component |

**Before this session:** confirm the Week 7 assessment exists on the portal — as of this check it
had not yet been created (other weeks' assessments are normally created well ahead of their own
class date, and Week 7's still had time before 15 Dec).

Weeks 7 and 17 deliberately have **no** `quizzes/weekly/weekNN.md` 6-question quiz — the cumulative
quiz *is* this week's retrieval practice.

**Cohort rotation.** `quiz1.md` is a static file reused every cohort, which is a leak risk. Swap two
or three MCQs and/or the Part B/C alternates from the review-quiz item bank into a cohort copy,
keeping the total at 25 pts (10 × 1 + 3 × 3 + 2 × 3).

### 5.2 Security Jeopardy — 0:30–0:50

- **Categories** — exactly the six in the lab README, one per week under review:
  *Threat Modeling · Tooling · Crypto · Injection · XSS · Auth & Access*.
- **Board** — 6 categories × 5 point values, plus a **Final Jeopardy wager** at the end
  (`slides/week07.md` presenter note). Prepare it before the session; nothing ships in the repo.
- **Fit** — the block is 20 minutes; size the board and the wager to fit that, not the longer round a
  full 6×5 board plus wager would normally want. Prefer fewer squares answered well over rushing the
  whole board.
- **Teams** — run by Houses (non-graded engagement layer, per course specification §7).
- **Rules** — the team picks a square and answers; a wrong answer *loses* the points. Keep it fast.
- **Points** — award them into the CTFd / Houses board if the scoreboard is running; the Awards
  mechanism for non-flag games is documented in `instructor/CTFd-SETUP.md` §6.
- **Purpose** — this is the main retrieval-practice slot for Weeks 1, 2, 3 and 5, which today's
  checkpoints do not reach. Weight the board accordingly rather than filling it with injection
  questions.

### 5.3 Two practice checkpoints — 0:50–2:00

**What it is.** `labs/week07-review-midterm-prep/mock-ctf.md`: students make a fresh, untouched
practice copy of the Week 4 and Week 6 lab folders (`git archive origin/main labs/week04-injection |
tar -x -C ~/practice`, same for `week06-authn-authz`) so their own graded `wk04`/`wk06` work is
untouched, then redo the same two student-patch fixes against that copy. **Nothing is submitted and
nothing is marked** — this is confirmed end-to-end: the untouched copy's checker fails by design, and
a correct patch passes cleanly, with no server, no port and no network access needed at any point.

| Checkpoint | Time | File | Task |
|---|---:|---|---|
| 1 | 35 min | `~/practice/labs/week04-injection/student_patch.py` | Complete `authenticate()` (bound SQL values) and `ping_argv()` (one parsed IPv4 argument list). Check: `docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 -v "$PWD:/exam:ro" -w /exam week04-injection-injection-lab:latest python3 student_checks.py` |
| 2 | 35 min | `~/practice/labs/week06-authn-authz/student_patch.py` | Complete `decode_identity()` (pinned HS256, required sub/aud/exp) and `owns_order()` (server-side ownership). Check: `docker run --rm --pull never --network none -e PYTHONDONTWRITEBYTECODE=1 -v "$PWD:/lab:ro" -w /lab kosen-swsec-week06:local python3 student_checks.py` |

Before either edit, the command prints `FAILED`; after a correct patch, `OK`. For each checkpoint a
student records: the diff, the exact command and result, the root cause (the trust boundary crossed),
one legitimate and one attack control, and one limit — the same shape of evidence Week 9 rewards.

**No infrastructure risk today.** Unlike a live-exploit lab, these checkpoints need no target server,
no published port and no network access, so there is no port clash to brief and no image to pre-pull
beyond what Weeks 4 and 6 already built. If a student's image is missing, `mock-ctf.md` itself gives
the one-line fix: rebuild in the real lab folder while online.

**If a checkpoint is solved early.** Point the student at writing the same fix again **on paper**,
without the computer — direct rehearsal for Week 9, which is a closed-book paper exam.

### 5.4 Debrief — 2:00–2:25, Save evidence — 2:25–2:30

Run §6's misconception list against the room ("hands up who is shaky on this one") and drill the two
or three that draw the most hands, then give the Week 8/9 logistics from §7. Close by collecting or
sighting the one-page cheat sheet, then let students note their own personal revision list in the
final 5 minutes.

## 6. Common misconceptions to re-test

The first four are the ones `slides/week07.md` names as the recurring point-losers. The rest are
drawn from the specific corrections carried in the Weeks 1–6 worksheets — every one of them exists
because the naive version was wrong under reproduction.

| # | Misconception | Where it comes from | How to re-test it today |
|---|---|---|---|
| 1 | Encoding, encryption and hashing are interchangeable | `slides/week07.md`; Week 3 lecture Q1 | Jeopardy *Crypto*; Quiz 1 Part B |
| 2 | "The input was validated, so it's safe" — validation substitutes for parameterisation | `slides/week07.md`; Week 4 lecture Q3 | Ask for the fix line, not just the payload, on Checkpoint 1 |
| 3 | Authentication implies authorisation | `slides/week07.md`; Week 6 lecture Q1 — `get_order` *calls* `current_user()` and then ignores the result (`vulnerable_app.py`) | Checkpoint 2, then "which line is missing?" |
| 4 | Client-side checks are a control | `slides/week07.md` | Jeopardy *Auth & Access* |
| 5 | `' OR '1'='1` alone bypasses the login | Week 4 worksheet Task 1 — the trailing `--` is required: without it SQL binds `AND` tighter than `OR`, so `... OR '1'='1' AND password='x'` matches no row | Have them state, from the resulting SQL, why the comment is load-bearing |
| 6 | The `<img>` XSS vector is the *shorter* payload | Week 5 worksheet Task 1 — `<img src=x onerror=alert(1)>` is actually longer than `<script>alert(1)</script>`; it earns its place when `<script>` specifically is filtered, not on length | Jeopardy *XSS*: "why would you ever reach for `onerror`?" |
| 7 | A CSRF token check and cookie hardening are the same fix | Week 5 worksheet Task 4 — the fixed app's CSRF defense is the server-checked token, not `SameSite`/`HttpOnly` alone; ports 8080/8081 are same-site, so `SameSite` does not by itself block the forged cross-origin POST | Jeopardy *XSS*: "why does the token matter even with the cookie hardened?" |
| 8 | An accepted upload is remote code execution | Week 4 worksheet Task 4 — `UPLOAD_DIR` is not web-served in this lab, so the honest answer is *the missing control*, not a claimed RCE | Ask what two properties the directory and filename would both need |
| 9 | Pinning the JWT algorithm alone secures the token | Week 6 lecture Q4 — the hardcoded HMAC secret `"secret"` is exploitable with `alg` pinned; the fix needs a strong random secret plus required `exp`/`aud` | Checkpoint 2 — make them explain the weak-secret path, not just `alg:none` |
| 10 | Scanner-clean means bug-free | Week 2 worksheet — a scanner exiting with a tool error is an incomplete check, not zero findings | Jeopardy *Tooling* |

## 7. Exam preparation

### 7.1 Week 8 — written, 165-minute slot, 8% of the course

Closed-book paper exam. Per `labs/week08-midterm-written/README.md`: **10 minutes** of
administration + **145 minutes** of working/checking + **10 minutes** of collection (165 minutes
total). The current specimen paper (`exam.md`) has **ten questions**, raw 100 split **Basic 50 /
Technical 50**, contributing 8% of the course. Scope: Weeks 1–6 — threat modeling, tooling,
application crypto misuse/migration, injection, XSS, and authentication/authorization. Bring a
student ID card and a pen; no notes, phone, calculator, computer or AI. The real paper is handed out
on the day; the specimen is practice only.

### 7.2 Week 9 — practical, 165-minute slot, 12% of the course

**Individual, closed-book paper exam** — not a computer exam and not a hosted CTF. Per
`labs/week09-midterm-practical/README.md`: **10 minutes** of instructions + **145 minutes** on four
stations (about 130 on the stations, 15 to check) + **10 minutes** of collection. **Four stations
(A–D), 25 points each, 100 raw = 12% of the course:**

| Station | Topic | Minutes |
|---|---|---:|
| A | Threat model and scanner triage (Weeks 1–2, plus the Week 6 ownership idea) | 35 |
| B | Moving old password records to Argon2id (Week 3) | 35 |
| C | Parameterized SQL / safe argv (Week 4) | 30 |
| D | Login token verification and object ownership (Week 6) | 30 |

Students get printed code, scanner results and test output, and write their analysis, their fix as
code, and their test results **by hand**. Week 5 is not on the practical.

### 7.3 What today's checkpoints do *not* cover — say this explicitly

Today's two checkpoints map directly onto Week 9's Stations **C** and **D** only — the same two
functions, the same shape of evidence. They do **not** touch Stations A or B at all.

| | Today's checkpoints | Week 9 |
|---|---|---|
| Stations covered | C (W4), D (W6) only | A (W1–2), B (W3), C (W4), D (W6) — all four |
| Medium | Computer, real Docker checker | Paper — write code and tests by hand, no computer |
| Targets | Your own practice copy, local Docker | Printed code, scanner results and test output |
| Working | Individual | Individual |
| Hints | None — same as the exam | None |
| Stakes | Ungraded, practice | 100 pts, 12% of the course |

Anyone who finishes both checkpoints early should revise Weeks 1, 2 and 3 for Stations A and B, which
nothing today rehearses directly.

### 7.4 Logistics to read out in the debrief

`slides/week07.md`'s closing note asks for the exam logistics to be stated in this session:

- Week 8 (written) — Tuesday 22 December 2026, 09:05–11:50, usual classroom.
- Week 9 (practical) — Tuesday 29 December 2026, 09:05–11:50, usual classroom.
- What to bring: student ID card, a pen (blue or black). No computer, phone, notes, calculator or AI.
- Whether the cheat sheet is admitted to the Week 8 written exam: the instructor's decision,
  announced today.

### 7.5 Deliverable — the one-page cheat sheet

Each student submits their own one-page cheat sheet. Building it *is* the studying — the compression
is the learning, which is why it must not be a shared file. Whether it may be carried into the
Week 8 written exam is the instructor's decision, announced today so students build the right
artefact.

## 8. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Cumulative review quiz — Quiz 1 (25 pts) | Quiz score | K1, K2 | Part of the 10% quizzes / participation component |
| Two practice checkpoints | Diff + command + result recorded per checkpoint | P1, P2, A1 | **Ungraded** — practice only |
| Security Jeopardy | Team points | K1 | Non-graded engagement (Houses); CTFd Awards if the scoreboard is running |
| One-page cheat sheet | The sheet | P3 | Not separately marked — a study aid |
| Debrief self-assessment | Named weak areas | P4, A2 | Formative — feeds the instructor's Week 8/9 support list |

There is **no worksheet** for Week 7: the lab folder holds `README.md` and `mock-ctf.md` only, and
the week carries none of the 12 graded worksheets. The graded midterm follows in Weeks 8–9 (20% of
the course mark, course specification §4).

## 9. Materials

- Lab: `labs/week07-review-midterm-prep/` — `README.md`, `mock-ctf.md`
- Quiz: `quizzes/quiz1.md` (25 pts, 30 min) · quiz mechanics: `quizzes/README.md`
- Slides: `slides/week07.md`
- Checkpoint targets: `labs/week04-injection` and `labs/week06-authn-authz` only (their already-built
  images: `week04-injection-injection-lab:latest`, `kosen-swsec-week06:local`)
- What comes next: `labs/week08-midterm-written/` · `labs/week09-midterm-practical/`
- Instructor-only (git-ignored): `instructor/CTFd-SETUP.md` (scoreboard, Houses, Awards),
  the item banks under `instructor/exams/` and `instructor/quizzes/`, and the formative key
  `instructor/exams/kosen-02005094/week07-review-key.md`
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md)

## 10. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **A student runs the checkpoint checker against their real `wk04`/`wk06` lab folder instead of a practice copy.** Their already-finished work would pass instantly, teaching nothing | Walk the room confirming students ran the `git archive ... ~/practice` step first; `mock-ctf.md` itself flags this ("if a check below passes before you have changed anything, ask your instructor") |
| **The Week 7 portal quiz assessment does not exist yet.** `README.md` and the slides both point students to `learn.zcr.ai/quiz` | Confirm it is created well before 15 December, the same lead time other weeks' assessments get |
| **The Jeopardy board does not exist until someone makes it.** Nothing ships in the repo; if it is not prepared, the 20-min Jeopardy block has no content | Build the 6 × 5 board plus the Final Jeopardy wager beforehand from the item banks in `instructor/`. Fallback if unprepared: run a cold-call recap of the revision map from `slides/week07.md` and extend the checkpoint block |
| **The CTFd scoreboard may not be up.** Jeopardy points have nowhere to land without it | Tally on the whiteboard and enter CTFd Awards afterwards (`instructor/CTFd-SETUP.md` §6). Nothing today is graded on those points, so a missing scoreboard costs energy, not marks |
| **A student's Week 4 or Week 6 image is missing or was pruned.** `docker run` then reports the image missing | `mock-ctf.md`'s own fallback: rebuild it in the real lab folder while online (`docker compose build` in `labs/week04-injection` or `labs/week06-authn-authz`) |
| **Quiz-item leakage between cohorts.** `quiz1.md` is a static file reused each term | Swap two or three MCQs and/or the Part B/C alternates from the review-quiz item bank into a cohort copy, holding the total at 10 × 1 + 3 × 3 + 2 × 3 = 25 |

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan): ⬚
- Did Quiz 1 fit its 30 min? Did Jeopardy fit 20 min? ⬚
- Where the class got stuck, and what unblocked them: ⬚
- How many students needed a rebuild of the Week 4 or Week 6 image: ⬚
- Misconceptions from §6 that actually surfaced in the debrief (and any new ones): ⬚
- Anything to change before this week runs again: ⬚
