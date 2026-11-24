# Lesson Plan — Week 16: Capstone Studio & CTF Warm-up

| | |
|---|---|
| **Course** | Software Security 2 (02005094, KOSEN-KMITL) |
| **Week / date** | 16 · Tuesday 16 February 2027, 09:05–11:50 |
| **Contact time** | 150 min (`AGENDA.md`, *Week 16: formative project studio*): brief 10 + build/test/peer-review 100 + instructor clarification 30 + record next actions 10 |
| **Lab folder** | `labs/week16-capstone` — `README.md`, `worksheet.md`, `scrimmage.md`; it ships no target of its own |
| **Slides** | `slides/week16.md` — studio deck, not a teaching deck |
| **Type** | **Capstone studio — no new content.** Project work-in-progress + optional CTF warm-up |
| **Targets** | The teams' own term-project builds (`project/README.md`, default `project/starter-app` — *NoteVault*); the optional scrimmage draws on the Week 17 mock (`labs/week17-review-final-prep/mock-ctf.md`) |
| **Standards** | `worksheet.md` header: "All prior weeks + OWASP Top 10 (2025) — https://owasp.org/Top10/2025/ ; CWE mapping required throughout". Week 16 introduces no ids of its own |
| **CLOs addressed** | **CLO1** model · **CLO3** remediate · **CLO5** evaluate & communicate (course specification §6, row 16) |

---

## 1. Session objectives

This is a studio, not a lecture. What the session is designed to produce:

**Knowledge (K)**
- K1 — State the team's project **top-3 risks** and the STRIDE/attack category each falls under (`worksheet.md` Part 2, Q1).
- K2 — Give the headline vulnerability's **CWE id** and **OWASP 2025** category, plus a one-sentence root cause (Part 2, Q2).
- K3 — Explain what the team's **SBOM** covers, how it was generated, and what they would do if a dependency in it got a new CVE next week (Part 2, Q3).
- K4 — Explain how the build artifact is **signed** and how a consumer verifies the signature (Part 2, Q4).
- K5 — Name which **Week 15 CI gate(s)** — Semgrep / Trivy / Gitleaks, fail-closed on HIGH/CRITICAL — the pipeline enforces, and describe what a failing build looks like (Part 2, Q5).

**Skills (P)**
- P1 — If giving the optional peer preview, follow the segment structure in `worksheet.md` §3B: Context (0:00–0:45) → Finding (0:45–1:45) → **Fix and verify** (1:45–3:30) → Delivery (3:30–4:30) → Limits (4:30–5:00), inside the 100-minute build/peer-review block.
- P2 — Re-run the team's own exploit against the patched build and show it blocked (§3B, 1:45–3:30).
- P3 — Peer-review another team against the seven criteria of `worksheet.md` §3C, scoring each 1–5.
- P4 — If attempting the optional scrimmage, work one bounded task from the Week 17 mock (`scrimmage.md`) and record the root cause, a tested correction, a legitimate positive control and a negative control.
- P5 — Say, out of the six deliverables in `worksheet.md` §3A, exactly which are done, which are partial, and who owns the remainder before Week 19.

**Attitude (A)**
- A1 — Demo the attack → root cause → fix **only** against the team's own term-project application or the provided practice-CTF targets (`worksheet.md` ethics note), under [ETHICS.md](../../ETHICS.md).
- A2 — Use only authorized targets and keep the actual patch, test output and commands (`worksheet.md`, *Evidence and integrity*) — no identity-stamped screenshot or external AI account is required for every checkpoint.
- A3 — Take peer criticism as useful, not a verdict to argue with; give criticism the same way.
- A4 — Treat an AI explanation as something to verify against evidence, not trust outright (`worksheet.md`, *Conventional / AIR-Sec practice*, AIR-Sec branch).

## 2. Key ideas (the through-line)

Everything the term taught in isolated weeks now has to hold together in **one** application the
team owns. A finding is not finished when the exploit works; it is finished when the root cause is
named (CWE + OWASP 2025), the fix is in a commit, the original attack has been re-run and fails,
the dependency inventory that shipped alongside it is known (SBOM), the artifact is signed, and a
pipeline gate will fail the build if any of it regresses. That chain — *attack → root cause → fix →
prove → keep it fixed* — is what `worksheet.md` Part 2 and the optional §3B preview ask the team to
account for, and it is what the Week 19 rubric marks.

Today's second, optional job is calibration for Week 19. `scrimmage.md` has teams pick one bounded
task from the Week 17 mock (`labs/week17-review-final-prep/mock-ctf.md`) only if their checklist is
already ready and time remains in the 100-minute block — it previews the *shape* of the Week 19
submission (root cause, fix, a positive and a negative test), not a timed multi-target board. There
is no dedicated CTF slot today; a team that never touches the optional scrimmage still gets full
marks for the studio.

## 3. What teams bring in, and what they leave with

**Coming in — the six deliverables** (`README.md`, *Bring*; `worksheet.md` §3A). By the
`project/README.md` timeline these are all past due at Week 14, so today is a check, not a start:

| # | Deliverable | Evidence to show (`worksheet.md` §3A) | Timeline milestone (`project/README.md`) |
|---|---|---|---|
| 1 | **Threat model** | Data-flow diagram + trust boundaries; top risks ranked (STRIDE) | Week 7 |
| 2 | **Vulnerability report** | Each finding mapped to **CWE + OWASP 2025**, with severity and PoC | Week 11 (draft) |
| 3 | **Fixed code** | Before/after diff for each finding; root cause noted | Week 14 |
| 4 | **SBOM** | Machine-readable CycloneDX, with explicit component scope and known omissions | Week 14 |
| 5 | **Signed artifact** | Signature + the exact verification command a consumer runs | Week 14 |
| 6 | **CI pipeline** | Security gate that fails on configured findings, detected secrets or check errors; link to a run | — |

Plus, from `README.md`: **the project runnable** (work-in-progress). There is no required demo —
`worksheet.md` §3B's peer preview is explicitly optional and capped at 5 minutes.

**Leaving with** — artefacts produced during the session:

| Artefact | Produced in | Source |
|---|---|---|
| A **ticked §3A checklist** showing which of the six deliverables are real | Build/peer-review block | `worksheet.md` §3A |
| **Peer scores** — 7 criteria × 1–5, for any team that gave or received the optional preview | Build/peer-review block | `worksheet.md` §3C |
| A **Part 4 reflection**: lessons learned, what to harden next, the hardest Week 19 topic | Submitted after class | `worksheet.md` Part 4 |
| Optionally, a **worked scrimmage task** (root cause, fix, positive + negative test) | Build/peer-review block, leftover time only | `scrimmage.md` |

**Instructor, before class.** Have the Week 17 mock's two checkpoints (`labs/week17-review-final-prep/mock-ctf.md`)
available in case teams ask for the optional scrimmage pointer. No separate target needs pre-pulling
for this week — teams work against their own project build.

## 4. Studio timetable — 150 min

The four block boundaries below are `AGENDA.md`'s (*Week 16: formative project studio*), and are
identical across `AGENDA.md`, `README.md`, `worksheet.md` and `slides/week16.md`:

| Time | Block | What happens | Source |
|---|---|---|---|
| 0–10 | **Brief** | Each team identifies its remaining risks and chooses what to work on today | `AGENDA.md`, `README.md` |
| 10–110 | **Build, test and peer review** | Teams improve and test their own project. Any pair may take an **optional preview of at most 5 minutes** (`worksheet.md` §3B) and score each other on §3C. Teams with a ready checklist may spend leftover time on the optional scrimmage (`scrimmage.md`) | `AGENDA.md`, `README.md`, `worksheet.md` §3 |
| 110–140 | **Instructor project clarification** | Targeted feedback and short Q&A per team or per cluster — not a required serial presentation from every team | `AGENDA.md`, `README.md` |
| 140–150 | **Save evidence and next actions** | Each team records its remaining-work checklist and, if used, a scrimmage retro | `AGENDA.md`, `README.md` |

> Worksheet 16 has no separate assessed slot of its own — `AGENDA.md`'s per-week table lists Week 16's
> homework as "project", so Part 2's lecture questions and Part 4's reflection are completable inside
> the 100-minute block or afterwards as the team's own project work.

### 4.1 Running the build/peer-review block

There is no fixed station rotation and no mandatory per-team presentation slot this week — that is
the main difference from the format this course used to run (paired 15-minute demo stations with a
graded-shape CTF board). Instead:

- Teams work on their own project for the full 100 minutes; the optional 5-minute peer preview is
  something a pair arranges between themselves when both are ready, not a scheduled station.
- Pairing for the optional preview is left to teams — within a House if convenient, since reviewers
  already know each other and cross-House copying is not being invited.
- A team that skips the optional preview entirely still completes the block by working its own
  checklist and, time permitting, the optional scrimmage.

### 4.2 Instructor circulation

With no fixed stations, circulation is informal: walk the room, prioritising the teams likeliest to
be behind (§7's Amber/Red tiers). At each team visited, ask one unscripted follow-up in the
`project/README.md` deliverable-6 style — *"why this fix and not X?"* — the same spot-check spirit as
the Week 19 viva on flagged teams. Collect each team's §3A checklist progress before the 110-minute
mark, since the 110–140 clarification block is built around it.

## 5. The work-in-progress review

### 5.1 What is checked

Two instruments, both already in `worksheet.md`:

**(a) The six-deliverable checklist — §3A.** Binary, per deliverable, and checked against the
*evidence*, not the claim. "We have an SBOM" is not a tick; a machine-readable CycloneDX file
covering all dependencies, with explicit scope and known omissions, shown on screen, is. Likewise
deliverable 5 is not ticked without **the exact verification command a consumer runs**, and
deliverable 6 is not ticked without **a link to a run** where the gate failed on a configured
finding, a detected secret or a check error.

**(b) The peer-review rubric — §3C**, scored 1–5 on each of seven criteria, used only by pairs who
take the optional preview:

| Criterion | 1 (weak) → 5 (strong) |
|---|---|
| Threat model completeness | Missing boundaries → thorough, ranked, realistic |
| Vulnerability mapped to CWE/OWASP | Vague → precise id + accurate severity |
| Exploit clarity | Hand-wavy → clear, reproducible PoC |
| Remediation quality | Superficial → root-cause fix, re-tested |
| SBOM + signing | Absent → complete + verifiable |
| Pipeline / fail-closed | None → gate fails closed on HIGH/CRITICAL |
| Demo & Q&A | Unclear → confident, handles tough questions |

The four rubric criteria that most often score low without the team noticing are the last four —
they are exactly the deliverables due at Week 14 and the ones a short preview can talk around.
Encourage teams who do take the preview to *show* the **Fix and verify** segment (§3B, 1:45–3:30),
not just describe it: patch on screen, attack re-run, failure visible.

### 5.2 Feedback is informal this week

`worksheet.md` §3C is feedback between peers, not a formal deliverable collected by the instructor.
Teams are not required to produce a written punch-list for Week 16; the §3A checklist and the Part 4
reflection are what carries forward into each team's own remaining-work plan for Week 19.

## 6. The optional CTF warm-up

`scrimmage.md` is optional, ungraded, needs no flags, and is explicitly scoped to **leftover time
inside the 100-minute build/peer-review block**, only once a team's own checklist is ready. It is not
a separate timetabled block, and it is not the detailed multi-target board this course used to run —
it now points at the Week 17 mock (`labs/week17-review-final-prep/mock-ctf.md`), which has two
practice checkpoints (redoing the Week 10 API-authorization task and the Week 14 output-handling task
from fresh, untouched copies), plus a short debrief on Weeks 11, 12 and 15.

For each task attempted, `scrimmage.md` asks for: the root cause, a tested correction, one legitimate
positive control, one negative control, and remaining limits — the same shape of evidence the Week 19
final asks for, not a flag. `scrimmage.md`'s own framing: "Four grouped stations, not fourteen
mandatory flags, define the current Week 19 practical" — so today's warm-up is deliberately scoped
down to match.

### 6.1 Running it, if a team opts in

- Point the team at `labs/week17-review-final-prep/mock-ctf.md` directly; it is self-contained
  (practice-copy instructions, the two checkpoints, and the checker commands).
- Any leaderboard is informal and for fun only — `scrimmage.md`: "Any leaderboard is just for fun and
  gives no marks." Nothing here feeds the Houses engagement layer or CTFd.
- A binary offset or address in any practice material depends on the supplied build; `scrimmage.md`
  explicitly warns not to assume a fixed offset.

### 6.2 If a team asks about Week 19

Tell them what changes there: it is graded, it runs the full 150-minute slot as a team practical with
its own station structure (`labs/week19-final-ctf-capstone/ctf.md`), and the project demo (if any) is
scored separately under the project rubric, not the Week 19 practical rubric.

## 7. Support for teams that are behind

"Behind" has a repo definition today — the `project/README.md` milestone table. Triage while
circulating during the 100-minute build/peer-review block (§4.2) and assign a tier.

| Tier | Definition (`project/README.md` milestones) | What they do today |
|---|---|---|
| **Green** | All six §3A deliverables present | Keep building; use the clarification block (110–140) for polish questions (severity accuracy, report clarity) |
| **Amber** | Threat model (W7) and vuln report draft (W11) exist; the W14 group — remediation, SBOM, signed artifact — is partial or missing | Spend the block building the missing W14-group deliverables. SBOM and signing are the two most recoverable in a session: `docker run --rm -v "$PWD:/src" aquasec/trivy image --format cyclonedx -o /src/sbom.json myapp:lab` then `cosign sign` / `cosign verify` (`labs/week12-supply-chain/README.md`, `labs/week12-supply-chain/sign.sh`) |
| **Red** | No working exploit against their own app, or the app will not run | Reset them onto the default target: `cd project/starter-app && export TEAM_ID=<your-team-name> && docker compose up`. Point them at `project/starter-app/README.md`'s *Suggested attack surface* — login, register, note, search, admin and export endpoints; the session cookie; `requirements.txt`; the `Dockerfile` — with seeded logins `alice / alicepw` and `admin / admin123`. One reproducible finding with a CWE/OWASP mapping by the end of the block is the target |

Two further supports, both cheap:

- **The pipeline is the smallest deliverable.** `labs/week15-devsecops-pipeline/security-ci.yml` is a
  working starting point for §3A deliverable 6; a team with nothing there can have a gate running
  before the end of the day.
- **Milestone dates are not the mark.** `project/README.md`'s rubric scores the artefacts, not their
  punctuality; the Week 19 demo/report is the graded event. Tell Amber and Red teams that, then hold
  them to closing the gap before Week 19.

**Peer-contribution fairness.** If circulation exposes a team where one member is carrying
everything, note it now — `project/README.md` scales each member's mark by the private
peer-contribution rating (typically ×0.8–1.1), and an unjustified low score is discussed before it
is applied. Raising it in Week 16 gives the team five weeks to fix the split; raising it at the
Week 19 submission does not.

## 8. Assessment for this week

Two things run today and they must not be blended.

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 16 (Parts 1–4 + the Conventional/AIR-Sec practice) | Part 2 answers, the §3A checklist, any §3C peer scores taken, Part 4 reflection | K1–K5, P3, P5, A2, A4 | Formative. `worksheet.md`: "no separate worksheet marks, no due date and no late penalty for this sheet" |
| Term project (graded at Week 19) | The six deliverables + the graded demo/report | CLO1, CLO3, CLO4, CLO5, CLO6 (course specification §4, term-project row) | 15% of the final mark, scored on `project/README.md`'s own 100-point rubric, with each member's mark scaled by peer contribution |

The optional scrimmage (§6) carries no weight at all — it is a calibration exercise, not an
instrument.

Two separate 100-point rubrics exist and grade different things — keep them apart:

| Rubric | Lives in | Weighting |
|---|---|---|
| **Worksheet 16 (formative feedback checklist)** | `labs/week16-capstone/worksheet.md` | Mirrors the project rubric 1:1 for feedback purposes: threat model 20 · vulnerability findings 25 · remediation 25 · supply-chain hardening 15 · CI pipeline 10 · presentation & report clarity 5 |
| **Term project (graded)** | `project/README.md` | Threat model 20 · Vulnerability findings 25 · Remediation 25 · Supply-chain hardening 15 · CI pipeline 10 · Presentation & report 5 |

No weekly quiz this week — `AGENDA.md`'s per-week table gives Week 16 a quiz column of "—", and the
retrieval quizzes belong to teaching weeks.

## 9. Materials

- Lab: `labs/week16-capstone/` — `README.md`, `worksheet.md`, `scrimmage.md`
- Slides: `slides/week16.md`
- Project: `project/README.md` · `project/REPORT-TEMPLATE.md` · `project/starter-app/` (*NoteVault*)
- Optional scrimmage target: `labs/week17-review-final-prep/mock-ctf.md` (practice copies of the
  Week 10 and Week 14 student tasks)
- Week 15 pipeline reference for §3A deliverable 6: `labs/week15-devsecops-pipeline/security-ci.yml`
  and `README-pipeline.md`
- Week 12 signing reference for §3A deliverable 5: `labs/week12-supply-chain/sign.sh`,
  `labs/week12-supply-chain/README.md`
- Forward pointer: `labs/week19-final-ctf-capstone/ctf.md` — the graded team practical this course
  builds toward
- Printing list for the session: §3C rubric, for any pair that wants to take the optional preview
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement: [ETHICS.md](../../ETHICS.md)

## 10. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **A team treats the optional peer preview or scrimmage as mandatory and loses build time to it.** Both are explicitly optional and time-boxed to leftover time | State plainly at the 0–10 brief: the 100-minute block is for the team's own project first; the preview and scrimmage are only for a team that is already on track |
| **Cosign is not installed, or keyless signing needs network + OIDC.** `project/README.md` deliverable 4 requires the release artifact signed with Cosign, and `worksheet.md` §3A deliverable 5 wants the exact verification command — an Amber team trying to close that gap in-session hits an install and an interactive browser sign-in | Check `cosign version` on a representative machine beforehand. If keyless is not workable in the room, a team may show a key-pair signature plus the verification command; what §3A actually asks for is a signature and the command a consumer runs. `labs/week12-supply-chain/sign.sh` is the reference |
| **A team's own project app will not run at all in the room** | Reset them onto the default target (`project/starter-app`, §7 Red tier) rather than letting the block end with nothing to show |
| **A team demos against something that is not theirs.** `worksheet.md`'s ethics note limits today's work to the team's own term-project application or the provided practice-CTF targets | State the boundary at the 0–10 brief. Anything outside it stops there and is handled under [ETHICS.md](../../ETHICS.md) |
| **Peer review (for pairs who take the optional preview) degenerates into praise.** Ungraded feedback between friendly teams tends to score 5s | Encourage a genuine number on all seven §3C criteria; treat an all-5s score as a sign the pair did not look closely |
| **The Week 17 mock's practice copies collide with a team's real Week 10/14 branches.** The mock instructs a separate `~/practice17` copy specifically to avoid this | Remind teams who try the optional scrimmage to use the practice-copy commands in `mock-ctf.md`, not their real lab folders |

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan): ⬚
- How many teams took the optional peer preview, and how many attempted the optional scrimmage: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Teams triaged Amber/Red, and whether they closed the gap by the end of the block: ⬚
- Anything to change before this week runs again: ⬚
