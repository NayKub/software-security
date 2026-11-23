---
marp: true
theme: default
paginate: true
header: "Software Security 2 · 02005094 · Week 10"
---

<!-- Current KOSEN class: 150 minutes = quiz/review10 + brief15 + shared practical100 + debrief20 + capture5. Full deck is pre-class/reference; select only the short live explanation. Both versions: common60 plus Conventional40 OR AIR20/10/10. Viva verifies existing work, no extra score or automatic-zero gate. -->


# Week 10
## API Security
Software Security 2 · Tuesday 5 January 2027, 09:05–11:50

<!-- Welcome back after midterm. Hook: change one number in an API URL and read a stranger's car location — that's the #1 API bug, and it's everywhere. Today: the OWASP API Top 10, hands-on. ~2 min. -->

---

## Today

- How an API differs from a web page
- OWASP **API Security Top 10**
- BOLA & mass assignment
- Rate limiting & resource consumption
- 🥷 Local API raid: BOLA, mass assignment, throttling and a student-authored fix

<!-- Roadmap, 1 min. The required lab uses the supplied local vulnerable and fixed APIs plus a student-authored control. crAPI is optional extension practice. -->

---

## Recap — Web half

- Injection, XSS, auth/IDOR
- APIs concentrate all of these — and add their own

<!-- 1-min bridge from the web unit. The midterm tested W1-6; APIs reuse all of it. Ask: "what was IDOR?" — because BOLA (the #1 API risk) is literally IDOR at API scale. -->

---

## The web half, at API scale

![The web-half bugs reappearing at API scale: Injection/SQLi (W4), XSS (W5) and Auth/IDOR (W6) all return; IDOR becomes BOLA (API1); and APIs add their own — mass assignment (API3) and no rate limit (API4). The point: there is no browser to hide behind, so the API endpoint is the whole attack surface, every field attacker-chosen.](img/web-to-api-bridge.svg)

<!-- The visual bridge for the recap — walk left (the bugs they already know) to right (the same bugs at the endpoint + the three API-native ones). Browser controls do not authorize API object access; the server must check it on every request. ~1 min. -->

---

## Why APIs are different

- Machine-to-machine clients can call the endpoint without browser controls
- Object IDs everywhere → ripe for IDOR/BOLA
- Clients can send any field → mass assignment
- Maps to the **OWASP API Security Top 10:2023** edition used in this course

![A browser may enforce same-origin, SameSite cookies and CSP for browser interactions, while curl, scripts and modified apps can send requests directly to the API. Neither path establishes object authorization. An API must validate identity and authorize each requested object and bindable field on the server; object IDs need not be sequential for BOLA to occur.](img/browser-vs-api.svg)

<!-- Key framing. Browser protections address browser threats; they are not API authorization. Assume clients can choose request paths, IDs and fields. ~5 min. -->

---

## BOLA (API1) — the #1 API risk

```text
GET /api/users/2/orders   → bob's orders — while authenticated as alice
```

- Broken Object Level Authorization = IDOR, at API scale
- The vulnerable endpoint does not check ownership **at all**: it returns the orders for whatever `<id>` you ask for
- The `X-User-Id` header is this lab's stand-in for "who is calling", but this route never even reads it

![BOLA shown as insecure versus secure. On the insecure API (:8080), alice (authenticated) sends GET /api/users/2/orders — asking for id 2, not hers — and because the code never reads who is calling, there is no check to spoof and none runs, so the server returns bob's orders with 200 OK. On the secure API (:8081) one ownership check produces a three-rung ladder: no identity header → 401 Unauthorized; alice (X-User-Id 1) requesting carol's id 3 → 403 Forbidden (she's known, but the object isn't hers); alice requesting her own id 1 → 200 OK. The whole fix is one question asked every request — does the caller own this object? — not escaping or a WAF rule, since the JSON was always well formed.](img/bola-ladder.svg)

<!-- The worked example — this is today's local target (vulnerable_api.py), not crAPI's vehicle-location challenge (which uses GUID ids you can't just increment — don't reuse that worked example against this lab or the ids won't line up). Same root cause as W6 IDOR. Verify before teaching: `get_orders()` in vulnerable_api.py never calls current_user() — grep it live if you doubt this. Toggling X-User-Id (garbage value, wrong id, omitted) makes zero difference; only the URL's own id matters. Don't say "server trusts a client-set header" — that implies a check exists and is merely spoofable. It's simpler and worse than that: no check runs. The fix (solution_api.py) is what actually introduces the X-User-Id comparison — that's where "auth" first exists in this exercise, fake as it is. ~6 min. -->

---

## BOLA — change the id, watch it leak

Pick a login, request another user's `id`, flip the server. The ladder is live.

```sim
bola-view
```

<!-- The interactive companion to the BOLA ladder diagram. Re-implements both get_orders() paths from this week's real code — nothing is sent anywhere. Let them drive it: on :8080 any id returns, even with no login; switch to :8081 and the same request becomes 401 (no identity) / 403 (not owner) / 200 (own). The one move that matters: on the vulnerable server, changing only the URL id changes the data, which is the whole bug. Ties to Task 1 (the 401→403→200 ladder they'll reproduce against the container). ~3 min. -->

---

## Mass assignment (API3)

```json
POST /api/users  { "username":"x", "password":"y", "is_admin":true, "balance":9999 }
```

- Client sets fields the server blindly binds (`user.update(body)` — no allow-list)
- Privilege/balance escalation, right at account creation

```sim
mass-assign
```

<!-- Walk it: the server takes the whole JSON body and binds it to the model, including fields the UI never exposes (is_admin, balance). The sim runs both create_user() implementations for real — edit the body, flip the toggle, watch which fields survive. This is today's local target's mass-assignment bug and the weekly quiz Q6. Fix = allow-list the bindable fields (ALLOWED_CREATE_FIELDS in solution_api.py). ~5 min. -->

---

## More of the Top 10

- API2 — broken authentication *(this week's `X-User-Id` header trick is a live example)*
- **API4 — unrestricted resource consumption:** no rate limit on `/api/login` → today's third graded bug (5 failed attempts, then 429)
- API6 — unrestricted access to sensitive business flows
- Under **2023's** taxonomy, "excessive data exposure" isn't its own number — it's folded into **API3 BOPLA** alongside mass assignment (you may see it listed separately elsewhere, incl. crAPI's own docs — that's the older 2019 split)

<!-- Round out the list. API4 = no rate limit → today's lab actually grades this one (Task 3, 401×5 then 429×2). Flag the API3/"excessive data exposure" taxonomy note pre-emptively — a student cross-checking crAPI's challenge list will see it as separate and think the slide is wrong; it's OWASP's own edition difference. ~4 min. -->

---

## The whole map — API Top 10:2023

![The ten OWASP API Security Top 10:2023 categories as a single map, with API1 (BOLA), API3 (BOPLA / mass assignment) and API4 (unrestricted resource consumption) highlighted as this week's three graded bugs and the other seven shown as the rest of the map. Footnote: API3:2023 BOPLA folds in the old 2019 "excessive data exposure". The three we drill are authorization and design bugs, not input-validation bugs.](img/api-top10-map.svg)

<!-- The overview that frames the three graded bugs against the full ten. Don't read all ten aloud — point at the three orange ones and say "these are today; the other seven exist and you'll meet them in the CTF weeks." Reinforces the taxonomy note (API3 absorbs excessive data exposure). ~2 min. -->

---

## API4 — watch the lockout window

The fixed server allows **5 attempts per 60s per IP**, checked *before* the password. Hammer it; advance the clock; find the lockout.

```sim
rate-limit
```

<!-- The interactive companion to API4. Re-implements solution_api.py's rate_limited() exactly: it prunes to a 60s window, then the 6th attempt is 429 — and because the >= check returns BEFORE appending, a rejected 429 is NOT counted, so holding the button down never extends the lockout (students always assume it does). Two beats to land: (1) the limiter runs before the credential check, so a legit user with the RIGHT password is locked out too — that's the availability/DoS face, and the reason per-IP limits behind shared NAT are a real-world headache; (2) the vulnerable server has no limiter, so it's 401 forever — unlimited brute force. This is Task 3 (401×5 then 429×2). The clock control makes the sliding window visible: advance past a timestamp and a slot frees. ~4 min. -->

---

## Defenses

- **Object-level authorization** on every request (check ownership)
- **Allow-list** request schemas — bind only intended fields
- Rate limiting / quotas
- Return only needed fields (DTOs)
- Schema validation (OpenAPI / GraphQL types)

<!-- The payoff. #1: ownership check on every object access (kills BOLA). DTO/allow-list binding kills mass assignment AND excessive exposure in one move. Schema validation at the edge rejects junk early. ~5 min. -->

---

## Each defense, and the attack it kills

![Each Week 10 API defense mapped to the attack it stops: object-level authorization (an ownership check) kills BOLA (API1), allow-listing the request schema kills mass assignment (API3), rate limiting kills unrestricted resource consumption (API4), plus schema validation and response DTOs as defense-in-depth. These are authorization and design controls, not escaping or a WAF, because the JSON was always well formed — the bug was in what the server allowed, not how it was encoded.](img/api-defenses-map.svg)

<!-- The checklist as a map: each control points at the exact bug it closes. Land the closing line — none of today's bugs are input-validation problems, so "sanitize your inputs" doesn't apply; the fix is a missing check, not bad parsing. ~2 min. -->

---

## Complementary: black-box recon cheat-sheet

When you only have an IP/URL (Kali):

| Tool | What it finds |
| --- | --- |
| `netdiscover` | hosts on the network |
| `nmap -sV target` | open ports and services (80/443?) |
| `nikto -h http://target` | web server issues |
| `dirb http://target` | hidden paths |
| `wpscan --url http://target` | WordPress problems |
| `hydra` | password guessing (only on authorized targets) |

*General awareness — no worksheet task uses these against today's target; useful for the CTF weeks later in the term.*

<!-- Practical recon, but be upfront it's not homework this week. Emphasize ethics + scope: only against provided sandbox targets. This is the "map the attack surface" muscle from W1, applied live. ~4 min. -->

---

## Real-world: feature abused as backdoor

WordPress 404-template RCE → bind shell:

```text
Appearance → Theme Editor → 404 Template → insert exec(...)
# trigger by visiting any non-existent page
nc -lvp 34567 -e /bin/bash   # attacker gets a shell
```

> Legitimate admin features become RCE without strict authz + integrity checks.

<!-- Shows that "a feature" + missing authz = RCE. A legit admin editor, abused once an attacker has access. Ties to least-privilege: even admins shouldn't be able to inject executable code. ~3 min. -->

---

## That backdoor, step by step

![A five-step attack chain turning a legitimate WordPress admin feature into RCE: (1) the attacker already has wp-admin access, (2) opens Appearance → Theme Editor → 404.php, (3) pastes a PHP exec() payload saved straight to disk as part of the active theme, (4) visits any non-existent page so the 404 runs 404.php and the payload executes, (5) gets an nc bind shell as the web-server user. A legitimate admin feature becomes RCE without authorization and integrity checks — separate content editing from code editing, and version, sign and verify theme files.](img/wp-backdoor-flow.svg)

<!-- The chain the bash on the previous slide describes — walk it top to bottom once. The point is not WordPress specifics; it's that a legitimate, authenticated feature became RCE because nothing separated "edit content" from "edit code" and nothing verified integrity. ~2 min. -->

---

## One API, three flaws

![One REST API with three separate flaws, each in a different handler. GET /api/users/{id}/orders never compares owner to caller — API1 BOLA. POST /api/users splats the whole JSON body into the model — API3 mass assignment. POST /api/login has no counter or lockout — API4 unrestricted resource consumption. All three are authorization and design flaws, not input-validation flaws — the JSON is well formed, so no amount of escaping, encoding, or a WAF rule blocks any of them.](img/api-flaws.svg)

<!-- Synthesis slide — today's three graded bugs, each traced to its exact line and exact fix. Land on the closing line: nothing here is a malformed-input problem, which is why "sanitize your inputs" doesn't apply this week — these are missing checks, not bad parsing. ~4 min. -->

---

## 🥷 Today's raid — the graded target

Prebuild the image before class with `docker compose build`; run `docker compose up --no-build --pull never` → :8080 (vulnerable) / :8081 (fixed):

1. **BOLA:** `401 → 403 → 200` — probe with no token, get denied reading *another* user's orders, then read *your own* orders successfully
2. **Mass assignment:** smuggle `is_admin`/`balance` into account creation
3. **Resource consumption:** `401×5 → 429×2` on `/api/login`
4. **Defend:** author the two bounded policy functions in `student_task.py`, verify positive/negative controls; use `solution_api.py` only as comparison reference

> **Bonus (optional, ~20 min): crAPI** — OWASP's own intentionally-vulnerable API, real GUID-based BOLA, capture-only, no fix step, no separate grade

<!-- The shared practical is 60 points. All students author the bounded authorization/binding change and explain controls. crAPI remains optional with zero required grading weight. -->

---

## Deliverable

> 📋 **Worksheet 10** — `labs/week10-api-security/worksheet.md` · follow the 100-minute core run sheet.

- Local BOLA/mass-assignment/throttling observations, mapped to the API taxonomy
- Your `student_task.py` authorization/binding diff and `python3 check_student.py` results
- Legitimate requests still succeed; cross-user requests and sensitive binding fail
- **Assigned written version only:** Conventional Part 2/4 (20/20) or AIR Audit/EiPE/Prompt (20/10/10), after the shared practical 60.

<!-- The prebuilt solution is a comparison reference. Students author the bounded policy functions and retain red/green evidence. Public demo flags alone do not identify a student's work. -->

---

## Key takeaways

- BOLA/IDOR is the dominant API bug — check ownership
- Bind only fields you intend
- Validate and throttle everything

<!-- Recap. Cold-call: "what one check stops BOLA?" (per-object ownership authorization). ~2 min. -->

---

# Questions?
Next week: Memory-safety & exploitation

<!-- Cliffhanger: "Next week we leave the web — crash a C binary with a fuzzer and hijack its execution, then rewrite it in Rust." Remind crAPI pulled before next session. -->


---

## This week's hand-in

- **Class:** Tuesday 5 January 2027, 09:05–11:50 (150 minutes): quiz 10 + explanation/demo 15 + practical 100 + debrief 20 + evidence 5
- **Everyone (60 points):** Tasks 0–3 on ports 8080/8081, your two controls in `student_task.py`, the checker before (`FAILED`) and after (`OK`), and your explanation
- **This week odd ID = Conventional** (Part 2 + Part 4, 40) · **even ID = AIR-Sec** (Audit-the-AI 20 + EiPE 10 + Prompt 10)
- **Code link:** commit `student_task.py` to branch `wk10` in your fork
- **Due:** Monday 11 January 2027, 23:59 · worksheet PDF to learn.zcr.ai/submit
- The demo `FLAG{...}` values are the same for everyone: paste them as evidence; nothing goes to ctf.zcr.ai
- `X-User-Id` is a teaching stand-in for identity, not real authentication
