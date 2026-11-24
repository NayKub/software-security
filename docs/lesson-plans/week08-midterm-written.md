# Lesson Plan — Week 8: Midterm written examination

| | |
|---|---|
| **Course** | Software Security 2 (02005094, KOSEN-KMITL) |
| **Week / date** | 8 · Tuesday 22 December 2026, 09:05–11:50 |
| **Contact time** | 165 min, one continuous written-exam block (`AGENDA.md`, *Exams: weeks 8, 9, 18 and 19*): 10 min administration + 145 min working/checking (12 min × 10 questions suggested pace + 25 min review) + 10 min collection |
| **Lab folder** | `labs/week08-midterm-written` — holds the public specimen paper, not a coding target |
| **Slides** | `slides/week08.md` — proctor deck, not a teaching deck |
| **Covers** | Weeks 1–6 |
| **Standards** | CWE-89 (B4, T1 — SQL injection) · CWE-78 (B4, T2 — OS command injection) · CWE-79 (B4, T3 — cross-site scripting) · CWE-347 (B4, T4 — disabled/forged signature verification) · CWE-639 / CWE-862 (B4 — missing object/function-level ownership check) · CWE-916 (T5 — password hash of insufficient computational effort). Taken from the exam's own worked-answer key, Item 4 (`instructor/exams/kosen-02005094/week08-written-specimen-A-key.md`) |
| **CLOs addressed** | **CLO1–CLO4, CLO6** (`docs/course-specification.md`, assessment table: "Midterm written / practical … CLO1–4,6"). CLO5 (evaluate/communicate AI claims) is deliberately absent from this paper — it is carried by the Assigned Conventional/AIR-Sec worksheet sections instead |

> **This plan quotes no exam question, no answer and no flag.** The public specimen paper is
> `labs/week08-midterm-written/exam.md`; the worked key, Form B and the item bank are
> instructor-only and are referenced here by path only.

---

## 1. What this paper evidences

This is an assessment week, so the objectives are stated as *what a script demonstrates about its
author*, not as what is taught. A student whose script scores well has shown that they can:

**Knowledge (K)**
- K1 — Identify trust boundaries in a browser → application → database flow and classify realistic
  threats by STRIDE class and confidentiality/integrity impact (B1, 10 pts).
- K2 — Choose the right class of tool — SAST, secret scanning or SCA — for a given finding, state
  each tool's blind spot, and tell a genuine tool error apart from a clean result (B2, 10 pts).
- K3 — Distinguish hashing, encryption and encoding; state why an unsalted fast hash is unsafe for
  password storage and when a successful legacy login should trigger a migration (B3, 10 pts).
- K4 — Classify a given defect to its CWE and name the security boundary it crosses, across four
  different defect types in one item (B4, 10 pts).
- K5 — Distinguish authentication from authorization and apply least privilege / fail closed to
  design one legitimate and one rejected test case for an owner-only endpoint (B5, 10 pts).

**Skills (P)**
- P1 — Reason, on paper and with no interpreter to test against, about a SQL boolean-bypass input
  against a concatenated query, then rewrite the query with placeholders and bound values (T1, 10 pts).
- P2 — Design a safe external-command call — argv list, no shell, address validation, timeout — and
  explain why filtering a single character (e.g. a semicolon) is not sufficient (T2, 10 pts).
- P3 — Correct an HTML-text-context injection and state precisely what an `HttpOnly` cookie does and
  does not defend against (T3, 10 pts).
- P4 — Specify correct JWT verification (pinned algorithm, required claims, audience/expiry) plus a
  server-side ownership check, and justify it with a legitimate-owner test and two rejection cases
  (T4, 10 pts).
- P5 — Design a safe staged password-hash migration — update only after a successful legacy check,
  never on a failed one — and explain why a failed login must not touch the stored record (T5, 10 pts).

**Attitude (A)**
- A1 — Answer in their own words, as the paper's own instruction line requires, rather than reciting
  memorized definitions.
- A2 — Treat a catalogue identifier (a CWE number) as something to justify from the mechanism, not a
  slogan to recite — the paper states that precise mechanisms and tested-design reasoning matter more
  than memorized catalogue IDs (`exam.md`'s own closing framing).
- A3 — Sit an individual, closed-book written assessment under the same integrity conditions as every
  other graded instrument ([ETHICS.md](../../ETHICS.md)), carrying that standard into a paper sitting
  with no computer to check against.

## 2. Exam blueprint — what is assessed

Taken from the paper itself (`labs/week08-midterm-written/exam.md`) and its worked key
(`instructor/exams/kosen-02005094/week08-written-specimen-A-key.md`): **165-minute slot · ten
questions · 10 raw points each · 100 raw · closed book.** Kept at item-and-topic granularity so this
file can stay public.

| Item | Topic | Week(s) drawn on | Marks |
|---|---|---|---:|
| B1 | Trust boundaries & STRIDE classification | 1 | 10 |
| B2 | Scanner triage — SAST / secret scanning / SCA | 2 | 10 |
| B3 | Hashing vs encryption vs encoding; password storage | 3 | 10 |
| B4 | CWE classification across four defect types | 3, 4, 5, 6 | 10 |
| B5 | Authentication vs authorization; least privilege / fail closed | 6 | 10 |
| T1 | SQL injection — boolean bypass + parameterized fix | 4 | 10 |
| T2 | OS command injection — safe argv design | 4 | 10 |
| T3 | XSS — context-appropriate encoding; cookie-hardening limits | 5 | 10 |
| T4 | JWT verification + object ownership | 6 | 10 |
| T5 | Legacy-hash-to-Argon2id migration, staged safely | 3 | 10 |

**Raw 100 → course 8%,** split Basic 4% (B1–B5) + Technical 4% (T1–T5)
(`labs/week08-midterm-written/README.md`, `slides/week08.md`).

> **Known drift — do not use these as a source for this exam's current format.**
> `course-plan-19weeks.md` (around line 16 and 91–92) and `instructor/exams/item-bank.md`'s own
> "MIDTERM POOL (Weeks 1–6)" section still describe an entirely different, **obsolete four-section
> exam** (A-Concepts / B-Spot-the-Vulnerability / C-Applied-SQL-Injection / D-Defense-&-Design,
> 120 minutes) that has no counterpart in the current ten-item Basic/Technical paper. This is a
> separate, already-logged finding (`instructor/platform-build/deploy/GO-LIVE-CHECKLIST.md`, Week 8
> check, 2026-11-24) and is **not fixed by this rewrite** — it needs its own pass over those two
> files. Until then, treat `labs/week08-midterm-written/exam.md` and the current KOSEN instruments
> under `instructor/exams/kosen-02005094/` as the only authoritative description of this exam.

## 3. Preparation before the day

- **Students, before the exam:** revise Weeks 1–6 using the Week 7 consolidation — cumulative review
  quiz `quizzes/quiz1.md`, Security Jeopardy and the two practice checkpoints
  (`labs/week07-review-midterm-prep/mock-ctf.md`) — then read the public specimen
  (`labs/week08-midterm-written/exam.md`) for the current item shape. The specimen is practice only;
  the actual sitting paper is handed out on the day and is different.
- **Instructor, at the Week 7 debrief** (`docs/lesson-plans/week07-review-midterm-prep.md` §7.4):
  the closed/open-note decision — whether the Week 7 one-page cheat sheet is admitted — must already
  have been announced there, before students built the sheet. Confirm it was actually said.
- **Instructor, before the day:** decide which sitting form to use — see §5 — and confirm the
  matching key is the one that will actually be opened while marking. Produce the printed papers from
  the chosen form; proof-read one printed copy end to end, including the blueprint diagram
  (`img/exam-blueprint.svg`), to confirm nothing is cut off or illegible on a photocopy.
- **Instructor, before the day:** confirm the current KOSEN instrument index
  (`instructor/exams/kosen-02005094/README.md`) still points to the files actually being used — it is
  the live index for Form A/B, their keys and the printed-candidate hash.
- **No portal component this week.** Confirmed this is a paper exam with no `learn.zcr.ai`
  assignment or assessment row for Week 8 — nothing to create or check on the portal, unlike every
  ordinary teaching week.
- **⬚** Room, seating plan, number of sections/sittings, invigilator roster and printing arrangements
  are not recorded in this repository.

## 4. The 165-minute block — logistics

`AGENDA.md` (*Exams: weeks 8, 9, 18 and 19*) budgets the written sitting as **145 min task block +
20 min administration** inside the 09:05–11:50 slot; `exam.md`/`slides/week08.md` break the same slot
down as **10 + 145 + 10**. Order of business follows the proctor deck:

| Step | Action | Source |
|---|---|---|
| Before the clock | Seat the cohort; confirm which sitting form is being used; distribute papers | `slides/week08.md` |
| Before the clock | State the duration, the closed-book rule and the integrity policy (no phones, no AI) aloud | `slides/week08.md`, presenter note: "Owner decision 18 Nov 2026: closed book; bring student ID card and pen" |
| Before the clock | State the format: ten questions, five Basic + five Technical, 10 pts each, 100 raw, 8% of the course | `slides/week08.md`, slide *Format and time* |
| Before the clock | State what is assessed and the biggest score-saver — explain the mechanism and give the fix, not just name the bug | `slides/week08.md`, slide *What is assessed* |
| Clock starts | 145 min working/checking: suggested pace 12 min/question (120 min) + 25 min reserved to check all answers | `exam.md`; `slides/week08.md` |
| On the paper | Name, Student ID and Date fields are on the paper — check they are filled before collecting | `exam.md` header |
| At collection | Collect papers; remind the cohort that Week 9 (Tuesday 29 December) is the four-station practical — also a paper, closed-book sitting, no computer | `slides/week08.md`, closing note |

**Materials allowed.** Closed book throughout (`exam.md`: "This is a paper exam and closed book");
bring a student ID card and a pen, blue or black; no notes, phone, calculator, computer or AI
(`exam.md`, `slides/week08.md`). Whether the Week 7 one-page cheat sheet is admitted is the
instructor's decision, to be announced at the Week 7 debrief (§3) — confirm it actually was.

## 5. Forms A and B, and make-up sittings

| Form | Where it lives | Status | Use |
|---|---|---|---|
| **A (specimen)** | Public `labs/week08-midterm-written/exam.md`; worked key `instructor/exams/kosen-02005094/week08-written-specimen-A-key.md` | The public file is practice-only — the actual sitting paper is handed out on the day and differs from it | The default description of scope and workload; confirm the day's actual paper against the current key before using it as a sitting instrument |
| **B** | Private `instructor/exams/kosen-02005094/week08-written-form-B.md` / `-form-B-key.md`; a pre-formatted five-page printable candidate also exists, with its SHA-256 recorded in the exams index `README.md` | Instructor-only (git-ignored); same ten-item Basic/Technical shape as A, different case specifics | Use for a cohort that has already seen the public specimen, or for a make-up sitting |

- **Make-up sittings:** run the form the main cohort did *not* sit. Record which form the main sitting
  used, so this is not left to memory on the make-up day.
- **Do not confuse either current form with the obsolete top-level files**
  `instructor/exams/week08-midterm-written-{formB,formB-answers}.md` — these describe a completely
  different, old four-section exam (see §2's drift note) and are flagged for a separate fix, not for
  use at any sitting.
- **⬚** Make-up sitting date, eligibility rules and any cap on the make-up mark are institutional and
  not recorded in this repository.

## 6. Invigilation and academic integrity

Sourced from `instructor/anti-cheating.md` §C (*Written exams (W8/W18)*) and the `slides/week08.md`
presenter notes.

- In-class and **monitored** throughout.
- **Multiple versions / shuffled sections** where the room allows it, and **closed book** — or the
  one-page cheat sheet only, if admitted (§4).
- **No phones, no AI**, stated aloud before the clock starts.
- The paper is individual work; the instruction line on the paper requires answers in the student's
  own words, which is also the marking stance (§7).
- Identical wrong answers across adjacent scripts are the written-exam form of the red flag listed in
  `instructor/anti-cheating.md` §F. Keep the seating record so an adjacency claim can be checked later.
- **If copying is found:** follow `instructor/anti-cheating.md` §G — keep the evidence, apply the
  syllabus penalty consistently, and follow [ETHICS.md](../../ETHICS.md) plus **⬚** (institutional
  conduct process).

## 7. Marking

- **Who marks: ⬚.** The course specification names one instructor (plus a second named instructor at
  course level) and records no explicit co-marker or moderation arrangement for this paper. If more
  than one person marks, fix a split (one marker takes all Technical items across every script) so a
  judgement call is at least applied consistently.
- **The key.** Form A → `instructor/exams/kosen-02005094/week08-written-specimen-A-key.md`; Form B →
  `instructor/exams/kosen-02005094/week08-written-form-B-key.md`. **Never** the obsolete top-level
  `instructor/exams/week08-midterm-written-{answers,formB-answers}.md` (§2, §5) — those describe a
  different exam and would mis-grade every script if opened by mistake. Match the key to the form
  actually sat before the first script.
- **The key is already item-level.** Each of the ten items in the current key carries its own named
  mark split (e.g. B1 = boundaries 4 + STRIDE/CIA 6; T4 = crypto/claim validation 4 + ownership
  decision 3 + positive/negative controls 3) — apply those splits directly; there is no separate
  section-level rubric to reconcile against them.
- **Borderline answers.** Apply the course specification's rubric stance: credit a correct mechanism
  explained clearly even if a catalogue id is slightly off, or a parameterized-query answer has a
  minor syntax slip but the right bound-value idea. Decide each such class of answer **once**, write
  the ruling in the margin of your working copy of the key, and apply it to every script.
- **Score entry.** Enter the mark against **Midterm** in the gradebook; `instructor/GRADEBOOK.md`
  computes **Midterm % = average of W8 and W9**, so this paper is half of the 20% midterm component
  (`docs/course-specification.md`, assessment table: "Midterm written / practical | 8 / 12").
- **⬚** Grading scale / letter-grade boundaries (institutional).

## 8. After the exam — item analysis

The repository defines the *loop* but not the *statistics*. Everything below that is not sourced is
marked ⬚ rather than guessed.

1. **Mark, then look at the paper rather than the students.** For each item, note where the cohort
   clustered: near-universal correct (the item discriminated nothing), near-universal wrong (the item
   was mis-set, mis-worded, or the teaching week did not land), and split-with-good-students-wrong
   (the item is probably ambiguous).
2. **Separate a bad item from a real gap.** If B2 (tooling) failed cohort-wide, that is a Week 2
   signal, not a bad item — feed it to the Week 17 review rather than deleting the item.
3. **Rotate, don't patch, using the current instruments.** The current KOSEN exams index
   (`instructor/exams/kosen-02005094/README.md`) is where the live Form A/B instruments and their
   hashes are tracked — build next cohort's specimen or Form B candidate from there.
   `instructor/exams/item-bank.md`'s own "MIDTERM POOL" is **not** a reliable source today (§2) —
   do not rotate items from it until it is rebuilt against the current ten-item design.
   `instructor/anti-cheating.md` §E requires rotating the paper every cohort regardless of how the
   items performed, so this step is needed every time even if nothing below is a real gap.
4. **Write the ruling back.** Every borderline-answer ruling made in §7 is evidence that an item's
   wording could be sharper. Add it to the item's worked-answer note in the current key, or reword the
   item, before it is used again.
5. **Close the loop on the forms.** Record which form this cohort sat, so the next cohort's specimen
   is not the exact paper this cohort has already seen or photographed.

**⬚ Not defined anywhere in this repository, and deliberately not invented here:** which item
statistic is used (facility index, discrimination index, point-biserial or none), the threshold at
which an item counts as discriminating poorly, who reviews the analysis, when it is done, and where
it is recorded.

## 9. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Midterm written paper, items B1–B5 / T1–T5 | The script, 100 pts | K1–K5, P1–P5, A1–A2 | Half of the 20% midterm component (`instructor/GRADEBOOK.md`: Midterm % = average of W8, W9) |
| Invigilation record + seating record | Sitting conditions, form sat, incidents | A3 | Integrity control, not a mark |
| Item analysis (§8) | Per-item performance | Course-level, not student-level | Feeds the current KOSEN instruments and the Week 17 review |

No worksheet, no quiz and no portal component this week — nothing is submitted to Classroom,
`learn.zcr.ai` or GitHub.

## 10. Materials

- Public specimen (practice only): `labs/week08-midterm-written/exam.md`
- Week brief: `labs/week08-midterm-written/README.md`
- Exam blueprint diagram: `labs/week08-midterm-written/img/exam-blueprint.svg`
- Proctor deck: `slides/week08.md` (Marp)
- Instructor-only, **never published**: current KOSEN exams index
  `instructor/exams/kosen-02005094/README.md`; Form A worked key
  `week08-written-specimen-A-key.md`; Form B paper + key `week08-written-form-B.md` /
  `-form-B-key.md`; `instructor/GRADEBOOK.md`; `instructor/anti-cheating.md`
- What students revised from: `labs/week07-review-midterm-prep/` (`quizzes/quiz1.md`,
  `mock-ctf.md`), the Week 1–6 lab folders
- Rules of engagement: [ETHICS.md](../../ETHICS.md)
- **⬚** Printed papers, script booklets, room booking

## 11. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **The public specimen (`exam.md`) leaks between cohorts** — it is static and lives in the public repo, so a repeating student or a shared drive from last year may already have it | Decide Form A vs Form B *before* the sitting (§5); for a cohort that may hold the specimen, sit Form B instead |
| **The obsolete top-level files could be opened by mistake while marking** (`instructor/exams/week08-midterm-written-{answers,formB,formB-answers}.md`, §2, §5, §7) — they describe a different exam entirely | Mark only from the `instructor/exams/kosen-02005094/` paths named in §7; the obsolete files are logged for a separate fix/retirement (GO-LIVE-CHECKLIST.md, 2026-11-24) |
| **`course-plan-19weeks.md` and `instructor/exams/item-bank.md`'s MIDTERM POOL still describe the old four-section format** (§2) | Do not use either as a source for this exam's shape or for rotating items until they are fixed separately |
| **A Form B sitting marked against the Form A key** — the two share the same item shape, so the mismatch is not obvious until the marks look strange | Write the form letter on the board and on the script header; open only the deployed form's key while marking |
| **`instructor/` is git-ignored** — a colleague marking from a fresh clone of the public repo has **no key at all**, and no Form B | Transfer the key out-of-band before marking day; never "fix" this by committing it |
| **The cheat-sheet admit/no-admit decision is made at the Week 7 debrief, a week earlier** | Confirm it was actually announced there (`docs/lesson-plans/week07-review-midterm-prep.md` §7.4) before relying on it here |
| **Printing the blueprint diagram** — `img/exam-blueprint.svg` may not reproduce cleanly on a black-and-white photocopier | Print-proof one copy of the current paper and confirm the diagram is legible in greyscale before duplicating |
| **No lab block this week, so nothing is checked on a machine** — Week 9 is a 165-min paper practical and the first time anyone discovers a problem with the printed materials is at its start | Use the deck's closing note at collection: remind the cohort Week 9 is also closed-book and paper-based |
| **A student misses the sitting** | Run the other form (§5); eligibility and date are **⬚** (institutional) |
| **Multiple sections / multiple sittings of the same cohort** | The later sitting must not sit the same form as the earlier one; record which form each section sat |

## 12. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Form sat (A / B), and by which section: ⬚
- Time actually used by the cohort (did anyone need the full 145 min?): ⬚
- Item-by-item mark distribution, and which item was weakest: ⬚
- Items that discriminated poorly, and what replaced them: ⬚
- Borderline-answer rulings made during marking, and the item wording they imply: ⬚
- Integrity incidents, and how they were handled: ⬚
- Anything to change before this exam runs again: ⬚
