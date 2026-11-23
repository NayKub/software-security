# Worksheet 4 — Injection & Input Handling

> **Course:** Software Security (KOSEN69) · **Week 4**
> **Aligned:** OWASP 2025 **A05 Injection** · **CWE-89** (SQLi), **CWE-78** (OS command injection), **CWE-434** (unrestricted upload)
> **Signature game:** 🐉 **SQLi Warm-up** — each successful injection lands a "hit"; you clear it when you dump every credential and land an RCE.

> ⚠️ **Ethics note:** All payloads here are for the provided sandbox (`vulnerable_app.py`) and your own DVWA/Juice Shop containers **only**. Never test systems you do not own or have written permission to test. Unauthorized injection is a crime under most computer-misuse laws.

## Class and assessment contract

**Contact time: 150 minutes** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief/reasoning 20 + evidence/exit 5. Build the lab image before class (see Environment setup below). In class you do Tasks 0–3 and 5; Task 4 is optional.

**Both assigned versions include the same common practical 60 points.** Complete that core plus **one** assigned 40-point section (**this week: odd student IDs do Conventional, even student IDs do AIR-Sec; the mapping swaps every week**): **Conventional** = Part 2 written questions 20 + Part 4 reflection 20; **AIR-Sec** = Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10. Each version totals 100. The unassigned section is reference practice, not another required 40 points. Only the named 100-minute core is assessed in the shared 60; other practical tasks are optional extension/reference unless explicitly used in the assigned written questions, and are not a prerequisite for full marks. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. Write your answers on the Week 4 answer sheet from Google Classroom, and say there which AI tool you used, if any.

## Part 1 — Student Information

Fill these in at the top of the answer sheet:

| Name | Student ID | Date | Code link (branch wk04) | AI tool used (if any) |
|---|---|---|---|---|
| | | | | |

## Part 2 — Lecture Questions

Answer in 2–4 sentences each.

1. Why does a **parameterized query** (`execute(sql, (params,))`) defeat SQL injection, while string formatting (`"... '%s'" % user`) does not? Reference how the database treats data vs. code.
2. In the `/ping` endpoint, `subprocess.run("ping -c 1 " + host, shell=True)` is vulnerable. Explain how `shell=True` turns user input into **CWE-78**, and how an argument array (`["ping","-c","1",host]`) removes the shell.
3. Distinguish **input validation** (allow-list) from **output handling**. Why is validation alone insufficient defense for SQLi?
4. The `/upload` route saves any filename to disk (**CWE-434**). What two properties must a directory and a filename have for an upload to become remote code execution, and which does `solution_app.py` remove?
5. What is a **UNION-based** SQLi, and why must the injected `SELECT` return the same number of columns as the original query? Relate to `/search?q=' UNION SELECT username,password FROM users--`.

![Untrusted request data in the Week 4 lab reaches three security sinks: the SQL engine (CWE-89), the OS shell (CWE-78) and file storage (CWE-434). The corresponding controls are bound query parameters, an argument list without a shell, and safe non-executable storage with filename and type checks.](img/injection-sinks.svg)

## Part 3 — Shared practical core (100 min in class)

**100-minute core:** Baseline login (5), bounded login bypass (15), UNION observation (20), command-injection observation (20), student parameterization/input patch with controls (40).

The minutes are a pacing guide. This week odd student IDs complete Part 2/Part 4 (Conventional 40) and even student IDs complete Audit/EiPE/Prompt (AIR-Sec 40).


**Learning goals:** extract data via SQLi, achieve OS command injection, write and test your own bounded defense in `student_patch.py`, then compare the full `solution_app.py` reference (optional extension: unrestricted upload).

**Prerequisites:** Docker + Docker Compose, `curl`, a browser. Working folder: `~/software-security/labs/week04-injection/`. On Windows, type every command in the Ubuntu app.

**Before class, on home Wi-Fi:** run `docker compose build` once in this folder. The image installs `ping` and Flask, which Tasks 3 and 5 need. Build while online; classroom commands use the local image without downloading packages.

### Environment setup

```bash
cd ~/software-security/labs/week04-injection
docker compose up --no-build --pull never
```
This runs the prebuilt vulnerable app (service `injection-lab`) at `http://localhost:8080` without downloading anything. If you see `No such image`, you have not built it yet: run `docker compose build` while online. Run every command below from this folder.

Optional secondary targets (run one at a time; not graded): DVWA opens at `http://localhost`, Juice Shop at `http://localhost:3000`.
```bash
docker run --rm -it -p 127.0.0.1:80:80 vulnerables/web-dvwa
```
```bash
docker run --rm -p 127.0.0.1:3000:3000 bkimminich/juice-shop
```

**What to submit per task:** the exact **payload/command**, a **screenshot** of the response proving success, and a **2–3 sentence mitigation** in your own words.

---

**Task 0 — Onboarding (5 min, in class).** Browse to `http://localhost:8080/login?user=alice&pw=alicepw` and confirm `Welcome alice`. Note the seeded users (`alice`, `bob`). Screenshot the working app. *Deliverable: screenshot.*

**Before you start — see why concatenation is the flaw** 🔬 Type any input and watch which characters the database will parse as *SQL* rather than as a name. The point is not the payload; it is that with concatenation the input becomes syntax, and with a parameterised query it structurally cannot. You will be asked to state that difference in your own words in Task 5.

```sim
sqli-parse
```

**Task 1 — Auth bypass via SQLi (15 min, in class) 🐉 Hit #1.**
- *Goal:* log in as `alice` with **no valid password**.
- *Steps:* hit `/login?user=alice'--&pw=x`, then `/login?user=x' OR '1'='1'--&pw=x` (the trailing `--` is required: without it, SQL binds `AND` tighter than `OR`, so `... OR '1'='1' AND password='x'` matches no row). Observe the comment in the query at lines 61–63 of `vulnerable_app.py`.
- *Note — browser vs `curl`:* pasted into a **browser**, the space in `x' OR '1'='1'--` is encoded for you; with **`curl`** an unencoded space silently returns a **blank page (no error)**. Use `curl -G "http://localhost:8080/login" --data-urlencode "user=x' OR '1'='1'--" --data-urlencode "pw=x"` — same `-G --data-urlencode` form for Task 2's `q=`.
- *Deliverable:* both URLs + screenshot of `Welcome alice` + explain why `--` and `OR '1'='1` work.

**Task 2 — Credential dump via UNION SQLi (20 min, in class) 🐉 Hit #2.**
- *Goal:* exfiltrate every username **and password** from the `users` table.
- *Steps:* request `/search?q=' UNION SELECT username,password FROM users--`. Confirm `alice:alicepw` and `bob:bobpw` appear — plus a third `admin` row whose password field holds a `FLAG{...}` value. This local demo flag is the same for everyone: paste it in the Task 2 box of your answer sheet as evidence. There is nothing to submit on ctf.zcr.ai this week.
- *Deliverable:* payload + screenshot of the dumped credentials (including the `admin` flag row) + note on why column count must match.

**Task 3 — OS command injection (20 min, in class) 🐉 Hit #3.**
- *Goal:* run an arbitrary command through `/ping`, then read the lab's demo flag file with it (same for everyone; paste it in the Task 3 box).
- *Steps:* request `/ping?host=127.0.0.1;id` then `/ping?host=127.0.0.1;whoami` (URL-encode if needed). Capture the injected command's output. Then use the same injection to read the flag file the server keeps at `/flag.txt` (the space needs `--data-urlencode`, see the note on Task 1):
  ```bash
  curl -G "http://localhost:8080/ping" --data-urlencode "host=127.0.0.1;cat /flag.txt"
  ```
- *Deliverable:* the three payloads + screenshot of the `id`/`whoami` output **and** the `FLAG{...}` from `/flag.txt` + explanation of the `shell=True` flaw (CWE-78).

**Task 4 — Unrestricted upload (25 min, optional extension) 🐉 Hit #4.**
- *Goal:* show the upload accepts a dangerous file type with no checks (CWE-434).
- *Steps:* first make a small test file: `echo "print('hi')" > shell.py`. Then `GET /upload` (form) and upload `shell.py`. Confirm `saved to /tmp/uploads/shell.py`. Via the browser form this just works; via `curl` the file field is named **`f`**: `curl -F "f=@shell.py" "http://localhost:8080/upload"`. Discuss: if `UPLOAD_DIR` were web-served or executed, this is the RCE chain (here the dir is **not** served, so document the missing control rather than claiming auto-RCE).
- *Deliverable (optional, ungraded):* upload command/screenshot + 2–3 sentences on why extension allow-listing matters. You may also re-fire the upload against `solution_app.py` and show `file type not allowed` (fix lines L86–93). This extension adds no points.

**Task 5 — Defend / fix it (40 min, in class, guided) 🛡️ Warm-up cleared.**
- *Goal:* write the two bounded defenses in `student_patch.py` and prove normal behavior still works while the SQLi and command-injection payloads fail.
- *Steps:* complete the student patch and run its controls below, then compare the supplied `solution_app.py` for the `/search` fix and optional upload extension.
- *Deliverable:* your patch commit, passing normal/attack controls, explanation of each defense and its limits, plus reference comparison evidence for the original SQLi and command-injection payloads.

### Student patch — required common practical evidence

Before comparing the reference, complete the two TODO functions in `student_patch.py`: bind the login values as SQLite parameters, and accept a single IPv4 address as an argument list. The provided `student_app.py` executes that list with `shell=False`; do not change the harness to use a shell. This bounded target intentionally accepts IPv4 only, not arbitrary DNS names.

Run the in-process checks in the prebuilt lab image from this directory:

```bash
docker compose run --rm --no-deps --pull never injection-lab python student_checks.py
```

The untouched TODOs are expected to fail. Your completed code must preserve Alice/Bob's legitimate logins, refuse wrong passwords and SQL payloads, accept `127.0.0.1` for the ping command, and reject separators/options before a process starts. The checker mocks ping and opens no listener. To inspect the patched target in a browser, stop the other target and run:

```bash
docker compose run --rm --no-deps --pull never --service-ports injection-lab python student_app.py
```

Submit your `student_patch.py` commit link (commit it to branch `wk04` in your own fork and push; see [SUBMISSION.md](../../SUBMISSION.md); do not open a pull request), test output, one legitimate case and each rejected attack with your explanation. A successful check of the reference alone does not demonstrate your own patch.

### Compare the supplied reference

Stop the vulnerable container (`Ctrl-C`), then run the fixed reference on the same prebuilt image:

```bash
docker compose run --rm --no-deps --pull never --service-ports injection-lab python solution_app.py
```

Re-fire the Task 1–3 payloads. Expected: `Login failed`, no credential dump, and `invalid host` (400) on `127.0.0.1;id`. Name the parameterized login/search queries and the argument list with validation. The `/search` fix and optional upload extension are outside the two-function student harness; compare them here, but submit your authored patch as the primary Task 5 evidence.

## Part 4 — Reflection

1. **CWE/OWASP mapping:** map each of your core exploits to its CWE (89/78 — and 434 if you did the optional Task 4 extension) and to OWASP 2025 **A05 Injection**.
2. **Real breach:** the **2017 Equifax breach** exposed ~147M people after attackers exploited a known input-handling flaw (Apache Struts CVE-2017-5638). In 3–4 sentences, connect that failure to the lessons in this lab (untrusted input reaching a powerful interpreter; the cost of an unpatched/unvalidated input path).
3. **Best mitigation:** of parameterized queries, allow-list validation, least privilege, and avoiding `shell=True`, which single control would have prevented the most damage in this lab, and why?

## Grading rubric (100)

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Common practical: main task and observations | 20 | 20 |
| Common practical: student defense/control or design, tests and limitations | 20 | 20 |
| Common practical: reproducible evidence and reasoning | 20 | 20 |
| Assigned Conventional Part 2 written questions | 20 | — |
| Assigned Conventional Part 4 reflection | 20 | — |
| Assigned Audit-the-AI | — | 20 |
| Assigned Explain-in-Plain-English | — | 10 |
| Assigned Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

The optional project/upload extension adds no extra graded points to the common 60 or assigned 40.

**Due:** Monday 30 November 2026, 23:59 (Thai time); check learn.zcr.ai/submit for the exact time. **Late:** −10% per started day; 0 after 10 days.

---

## Evidence & Integrity — common to both versions

- **Identity proof:** every screenshot/diagram must show a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in the
  same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed evidence is not accepted.
- **Flags this week:** the local lab prints the same demo `FLAG{...}` values for everyone (Task 2 and Task 3). They are the expected evidence: paste them in the Task 2 and Task 3 boxes, with your stamped screenshots. Nothing is submitted on ctf.zcr.ai. Submit the worksheet PDF at **learn.zcr.ai/submit** (full guide: [SUBMISSION.md](../../SUBMISSION.md)).
- **Common practical reasoning** *(graded within the common 60, not as another EiPE score):*
  1. What did you do, and **why did the vulnerability work**?
  2. **Why does your fix actually stop it** — and what could still break it?

---

## 🤖 Audit the AI — assigned AIR-Sec section (20)

AI is a power tool you must **distrust** — you are graded on your *critique*, not the AI's answer.

1. Audit a complete AI answer about this week's design, exploit or fix. If your instructor gives you an AI answer to audit, use it; otherwise ask an AI assistant to fix `vulnerable_app.py` and paste its full answer. A correct answer is allowed: verify its claims and state the remaining assumptions rather than inventing an error.
2. **Check what is correct, wrong, risky or conditional** — insecure code, an incomplete fix, a hallucinated API/function/CVE, an edge case or unsupported reasoning. Quote the exact line(s) and support the evaluation with evidence.
3. Supply a verified correction where needed; if the answer is correct, supply the verification and limits. Explain your conclusion in 2–3 sentences. Do not manufacture a defect to satisfy the task.

> Write which AI tool you used in the table at the top of your answer sheet. This is the assigned AIR-Sec Audit component (20 points); it is not added to the common 60 or to the Conventional 40.

---

## 🧠 Comprehension & Prompt — assigned AIR-Sec section (10 + 10)

**A. Explain in Plain English (EiPE).** In 2–3 sentences, in your own words, describe what this week's vulnerable code/endpoint actually *does* and *why it is exploitable* — explain the mechanism, don't dump jargon.

**B. Prompt Problem.** Write a **single prompt** that makes an AI produce a *correct, secure* fix for one finding. Run it: does the exploit now fail? If not, refine the prompt and try again. Submit the **final prompt + the verified result**.
*Graded on the prompt's precision and your verification — this trains problem decomposition and AI literacy (Denny et al. 2024).*
