---
marp: true
theme: default
paginate: true
header: "Software Security · Week 4"
---

# Week 4
## Injection & Input Handling
Software Security 2 · Nutthakorn Chalaemwongwan · Shinya Oyama

<!-- Hook: type one quote mark into a login box and become admin — promise that demo. Injection is the oldest trick that still works. Today they exploit it, then fix it for real. ~2 min. -->

---

## Today

**KOSEN class: 150 minutes.** Quiz/review 10 + brief/demo 15 + practical 100 + debrief 20 + capture 5. Full slide explanations are preparation/reference.

**Worksheet:** common practical 60 + assigned 40. **This week: odd student IDs do Conventional (Part 2 + Part 4), even student IDs do AIR-Sec (Audit 20 / EiPE 10 / Prompt 10); the mapping swaps every week.** Each totals 100. Your instructor may ask you to show or repeat a step. Extensions add no graded points.


- Why injection still matters
- The general injection pattern
- SQL injection — hands-on
- Command injection
- Defenses: parameterized queries + validation
- 🎮 Game: **SQLi Warm-up**

<!-- Roadmap, 1 min. Tell them the one big idea (data becomes code) unifies SQLi, command injection, and even XSS next week. Lab = exploit DVWA/Juice Shop then patch it. -->

---

## Recap — Week 3

- Crypto failures: ECB, weak hashes, hardcoded keys
- Hashing ≠ encryption ≠ encoding
- Use vetted KDFs (bcrypt/argon2) + authenticated encryption

<!-- 1-min bridge. Last week we protected data at rest; today the attacker sends malicious data IN. Cold-call: "how should we store passwords?" to check W3 stuck. -->

---

## The injection pattern (one idea)

> Untrusted **data** gets interpreted as **code/commands**.

- Attacker input crosses a trust boundary into an interpreter
- SQL, OS shell, LDAP, XPath, template engines, NoSQL…
- Maps to **OWASP A05:2025 Injection**

<!-- This is THE mental model for the whole week — say it twice. Every injection is the same shape: an interpreter can't tell your data from its own instructions. Ask the class to name interpreters in a typical app (DB, shell, template). ~5 min. -->

---

## SQL injection — how it works

```sql
-- vulnerable (this week's vulnerable_app.py, SQLite)
"SELECT * FROM users WHERE username = '" + input + "'"
```

- Input `' OR '1'='1` → always true
- **UNION-based** → read other tables in one shot (today's lab)
- Stacked queries (`'; DROP TABLE users; --`) are the textbook example, but **don't assume they work everywhere** — Python's `sqlite3` refuses multiple statements in one `execute()` call; this week's target raises an error instead

<!-- Walk the string-concatenation on the board: show how the quote in the input lands inside the SQL string and breaks out. This app is SQLite via Python's sqlite3 module — no stacked queries, no blind SQLi task this week (that's UNION-based, direct-output only). Don't promise a DROP TABLE demo works here; it doesn't. ~7 min. -->

---

## Try it — watch the parse tree change

Type an input. See exactly where the quote breaks out of the string.

```sim
sqli-parse
```

<!-- Live payoff for "the quote lands inside the string and breaks out" — the sim renders the actual token boundaries shifting as they type, so the break-out is something they watch happen, not a claim on a slide. ~4 min. -->

---

## Auth bypass — anatomy of one payload

Inject into the **username** field:

```text
alice'--
```

```sql
SELECT * FROM users WHERE username = 'alice'--' AND password = '...';
```

- `'` closes the string literal you're injected into
- `--` comments out everything after it, including the password check
- No trailing space, no `LIMIT` trick needed — this app is SQLite via `fetchone()`, not a MySQL row-count gate; **don't carry over MySQL-specific folklore** ("needs a space after `--`") — that's a different engine's quirk

<!-- The worked example — slow down here. Decompose the payload token by token; this is exactly the SQLi Warm-up's auth-bypass hit. A common wrong instinct is to add `OR 1=1` and a `LIMIT` clause copied from a MySQL tutorial — walk through why neither is needed against this SQLite app, and why the bare `'--` is what the worksheet actually uses. ~8 min. -->

---

## The fix: parameterize — data stays data

```python
# concatenation: DB gets ONE finished string, decides grammar AFTER
"...WHERE username = '" + user + "'"     # user = alice'--  ->  ' breaks out, code

# parameterized: structure parsed and LOCKED first, value bound AFTER
db.execute("...WHERE username = ? AND password = ?", (user, pw))
```

- `?` locks the query **structure before the input ever arrives**
- `alice'--` is then bound as a **value** — it can no longer become SQL grammar
- Escaping quotes patches symptoms; **this** is the actual fix for SQLi

<!-- THE slide that makes SQLi click — spend time here, it's the one students miss. Draw both on the board. Concatenation: the DB receives one already-joined string and only THEN parses which characters are grammar vs. value, so the user's ' can retroactively become a string-terminator (the break-out they saw in the sim). Parameterized: the driver sends the template WITH the ?-placeholders to the DB and the DB parses+plans the structure FIRST — 'there are exactly two values here' is decided before any user byte is seen — then the values are shipped separately and slotted in as pure data. Because parsing already finished, alice'-- is just a 9-char username that matches no row; the ' and -- are inert. Punch line: parameterization doesn't *clean* the input, it *removes the input's power to change the grammar*. That's why it beats escaping/block-lists, which only try to spot bad characters. ~7 min. -->

---

## SQLi in one picture — break-out vs. bound value

![Three SQL login queries stacked: normal input sits inside the string as data; the injected username alice'-- makes the user's quote close the string and -- comment out the password check so it logs in with no password; and the parameterised version binds alice'-- into a ? placeholder as pure data so the quote and dashes are inert and login fails.](img/sqli-parse-breakout.svg)

<!-- The consolidation slide — leave it up while students work Task 1. It shows all three states at once (normal / injected / parameterised) with the token colours: blue = value/data, orange = attacker chars that became code, struck-through grey = the check that no longer runs. Point at the orange ' in row 2 — 'that one character is the whole bug' — then the ? in row 3 — 'the value can't reach the grammar'. Same picture the sqli-parse sim animates live. ~3 min. -->

---

## Real-world impact

- **Equifax (2017):** unvalidated HTTP header → Struts RCE (CVE-2017-5638); 147M people, ~$700M settlement
- **Heartland (2008):** SQLi into payment systems → 130M+ cards
- Bulgaria: data on *almost all adults* leaked via SQLi
- Impact: data leak/modification, full DB control, DoS, reputation

<!-- Make it real — these are careers ended and companies fined. Equifax = a single unpatched input parser. Tie back: every breach here started as "untrusted data interpreted as code". ~4 min. -->

---

## Validate: allow-list, not block-list

- **Allow-list (preferred):** accept only known-good (e.g. `0–9` for a phone)
- **Block-list:** ban known-bad → bypassed by new payloads
- Validate **type · length · range · format**
- Client-side for UX, **server-side for security**

<!-- Key principle that recurs all term. Block-lists always lose (attackers invent new payloads); allow-lists define what's acceptable. Emphasize: validation is defense-in-depth, NOT the primary SQLi fix (that's parameterization — next). ~4 min. -->

---

## Demo / attack surface

- Login forms, search boxes, URL params, JSON fields, headers
- Error messages leak schema → enumeration
- Today's lab: raw payloads via browser/curl against `vulnerable_app.py` — no scanner needed to see the mechanism
- Burp Suite / `sqlmap` are real-world tools worth knowing (sandbox-only, ethically) — not required for this week's tasks

<!-- Point out injection isn't just login boxes — any input reaching an interpreter. Note verbose DB errors are a gift to attackers (schema leakage). Be clear Burp/sqlmap are industry-awareness, not something this week's worksheet has them install — every task here is a plain URL/curl payload. ~3 min. -->

---

## Command injection

```php
system("ping -c 1 " . $_GET['host']);   // vulnerable
// host = 8.8.8.8; cat /etc/passwd
```

- Shell metacharacters: `; | & $() \` >`
- Leads to RCE — full server compromise

<!-- Same pattern, deadlier outcome (RCE = own the server, not just the DB). Walk the metacharacters: `;` chains a second command. Ask: "what does `8.8.8.8; cat /etc/passwd` run?" ~5 min. -->

---

## The fix: no shell — pass an argument vector

```python
# vulnerable: shell=True -> the OS shell parses the whole string
subprocess.run("ping -c 1 " + host, shell=True)     # host = 8.8.8.8;cat /flag.txt

# fixed: shell=False + argument array -> no shell, no metacharacters
subprocess.run(["ping", "-c", "1", host], shell=False)   # + allow-list host
```

- `shell=True` hands your string to `/bin/sh`, which reads `;` `|` `$()` as **syntax**
- An **arg vector** runs `ping` directly — `host` is one literal argument, never parsed
- `8.8.8.8;cat /flag.txt` becomes one impossible "hostname"; the `;` is **inert**

<!-- Same shape as the SQLi fix — separate command from data. shell=True actually spawns `/bin/sh -c "ping -c 1 <yourstring>"`, so sh does the parsing and every metacharacter (; | & $() backtick > <) is live -> command injection. With an argv list there is NO shell in the picture: execve runs the ping binary with argv = ["ping","-c","1",host], the kernel hands ping exactly four arguments, and host is a single opaque string -> ping tries to resolve "8.8.8.8;cat /flag.txt" as a hostname, fails, done. Nothing ever parses the ;. Exact parallel to parameterized queries: the structure (command + fixed flags) is fixed in code, the data (host) rides in a separate slot no interpreter re-parses. Add an allow-list on host as defense in depth. Punch line: you don't sanitize the metacharacters — you remove the shell that would interpret them. ~6 min. -->

---

## Upload → RCE (a classic chain)

The classic *chain*, attacker uploads `shell.php`:

```php
<?php system($_GET['cmd']); ?>
```

- **If** the upload dir is web-served and PHP-executable: `.../uploads/shell.php?cmd=ls%20-l` → RCE
- **This week's lab stops one step earlier:** CWE-434 unrestricted upload — the app accepts any file type/extension, but the upload directory is **not** served or executed. Your task: explain *which missing control* would complete the chain (type check, extension allow-list, storage outside web root, no-exec) — not demonstrate a live shell
- **Fix:** check type using controls appropriate to the app, allow-list extensions, store uploads outside web root, disable execution

<!-- Connects to W1's /upload threat model. Be precise: this app does NOT give you a working webshell today — Task 4 is a documentation exercise ("what's missing, and why does that stop RCE?"), not a live exploit. Don't imply students will pop a shell; they'll reason about the one control standing between this bug and that outcome. ~5 min. -->

---

## CWE mapping

- **CWE-89** — SQL injection
- **CWE-78** — OS command injection (CWE-77 is its general parent — cite CWE-78, the specific one)
- **CWE-434** — unrestricted upload of a dangerous file type

<!-- They map every lab finding to a CWE id — these three are what this week's worksheet actually grades. CWE-434 remains an optional upload extension; keep its mechanism in the reference list without assigning it extra required core points. ~1 min. -->

---

## Defenses that actually work

- **Parameterized queries / prepared statements** (the fix for SQLi)
- ORM with bound parameters
- **Allow-list** input validation (type, length, format)
- Avoid shells: use exec APIs with arg arrays, not string concat
- Least-privilege DB accounts

<!-- The payoff. #1 message: parameterization makes data STAY data — the DB never parses it as SQL. For shells, pass an argv array, not a string. Least-privilege limits blast radius if they still get in. ~5 min. -->

---

## One request, three security sinks

![Untrusted request data reaches three security sinks: SQL (CWE-89, controlled with bound parameters), the OS shell (CWE-78, avoided with an argument list and shell=False), and file storage (CWE-434, constrained with a safe filename, allowed type and non-executable storage). Each sink needs its own control.](img/injection-sinks.svg)

- **SQL** (`WHERE username = <in>`) → parameterized query — bind the value
- **Shell** (`ping … <in>`) → argument vector + `shell=False` — no shell to parse it
- **Filesystem** (`save(<in>)`) → extension allow-list + store outside web root
- Each sink needs its own control.

<!-- Synthesis slide — the SAME untrusted value from request.args/request.files is what feeds all three attacks just covered. Land on the closing line: escaping quotes does nothing to a semicolon in a shell, and a safe filename does nothing to SQL. Sets up "Defenses" as three separate fixes, not one. ~4 min. -->

---

## ⚔️ Game — SQLi Warm-up

Three core hits and one optional upload extension against this week's own app — no filters to bypass, the app has none:

1. Auth bypass (`alice'--`)
2. UNION dump (steal all credentials)
3. Command injection
4. Unrestricted upload *(optional extension)*
5. **Warm-up cleared:** write `student_patch.py`, pass normal/attack controls, then compare `solution_app.py`

<!-- Explain before lab: three attacks against the supplied app, then the student-authored patch and its controls. Upload is an optional extension. No filter exists in the vulnerable app to bypass. DVWA/Juice Shop are optional secondary targets. ~3 min. -->

---

## Lab steps

> 📋 **Worksheet 4** — `labs/week04-injection/worksheet.md` (Part 3) · **prebuild while online:** `docker compose build` · **kickoff:** `docker compose up --no-build --pull never` → http://localhost:8080

```bash
docker run --rm -p 127.0.0.1:80:80 vulnerables/web-dvwa
```

1. Find an injectable parameter, bypass auth
2. Extract data (UNION dump)
3. Achieve command injection
4. Write the bounded login/ping patch and run its controls
5. Compare the full reference; probe upload only as an optional extension

<!-- Logistics. Circulate with TAs. The student-authored patch and its normal/attack controls are graded, along with the core observations and reasoning. Also kick off the NoteVault project injection task. -->

---

## Deliverable

- Findings: each injection point + payload + impact (CWE-mapped)
- The **fixed** code (prepared statements / validation)
- Proof the payload no longer works
- **This week: odd student IDs do Conventional written 40; even student IDs do AIR-Sec 40 (Audit / EiPE / Prompt)** (see worksheet)

<!-- Set expectations: before AND after code + proof. Only the assigned AIR-Sec 40 uses Audit/EiPE/Prompt; Conventional students submit their written 40. The weekly quiz no longer asks for their payload/flag (that question was dropped — quiz runs before the lab, so it couldn't be answered) — the payload + flag are required in the worksheet's Task 1 and Evidence & Integrity section instead. -->

---

## Key takeaways

- Never build interpreter strings from untrusted input
- Parameterize first; validate as defense-in-depth
- Injection = data treated as code

<!-- Recap in 3 lines. Cold-call: "what's the ONE fix for SQLi?" (parameterized queries). ~2 min. -->

---

# Questions?
Next week: XSS & client-side risks

<!-- Cliffhanger: "Next week the same trick runs in the victim's browser — and skims credit cards." Remind DVWA/Juice Shop ready in their VM. -->

<!-- Current authored work: student_patch.py plus student_checks.py, positive and negative controls, and an explanation. Reference-only output does not demonstrate the student patch. -->
