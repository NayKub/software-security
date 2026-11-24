# Lesson Plan — Week 9: Midterm — Individual Practical (paper)

| | |
|---|---|
| **Course** | Software Security 2 (02005094, KOSEN-KMITL) |
| **Week / date** | 9 · Tuesday 29 December 2026, 09:05–11:50, the usual classroom |
| **Contact time** | 165 minutes: 10 minutes of instructions + 145 minutes of work and checking + 10 minutes to collect papers. No lecture, no lab |
| **Format** | Individual, **closed-book paper exam**. Printed code, scanner results and test output; students write analysis, fixes (as code) and tests by hand. No computer, phone, notes or AI |
| **Lab folder** | `labs/week09-midterm-practical` — `README.md` and `ctf.md` (the student brief; the file name is historical, there is no CTF) |
| **Slides** | `slides/week09.md` — proctor deck, not a teaching deck |
| **Covers** | Weeks 1–4 and 6. Week 5 is not examined |
| **CLOs addressed** | **CLO3** remediate (course specification §6, row 9) |

---

## 1. What is assessed

Four stations, 25 marks each, 100 in total (`ctf.md`). Suggested times add up to 130 minutes, which leaves 15 minutes to check inside the 145.

| Station | Topic | Source week | Suggested time |
|---|---|---|---:|
| A | Threat model and scanner triage; ownership check before data is read | W1–W2, W6 | 35 min |
| B | Moving old password records to Argon2id at login | W3 | 35 min |
| C | Parameterized SQL and a safe IPv4 argv | W4 | 30 min |
| D | Pinned JWT verification and object ownership | W6 | 30 min |

Each station is marked in two halves: Basic 12.5 (cause 5, mechanism and boundary 5, reading evidence and its limits 2.5) and Technical 12.5 (own fix as code 5, one positive and one negative test with expected results 5, reading a printed test output 2.5). Raw Basic 50 + Technical 50 becomes 6 + 6 course marks, 12% of the course (`syllabus.md` §6). A flag, a leaderboard or House points do not exist in this exam.

## 2. Preparation

- **Paper.** The instructor prints the private Form B paper (36 copies plus spares) and keeps the key separate. The paper is generated from the private source, so rebuild it after any edit. The printed test outputs in the paper were produced by running deliberately flawed fixes against the supplied checkers; re-run them if the checkers change.
- **Nothing to install.** No hosted platform, VPN, Docker image or starter file is needed on the day.
- **Students.** Revise Weeks 1–4 and 6; the Week 7 checkpoints are the warm-up, and students practise writing the fixes by hand (`labs/week07-review-midterm-prep/README.md`).
- **Room.** Seating that stops reading a neighbour's paper; blank sheets for extra space (name, student ID and question number on every sheet). Room and invigilator count: not recorded in this repository.
- **Check the notice.** The official midterm notice and the Classroom Week 09 text must say the same date, time and rules as `README.md` and `slides/week09.md`.

## 3. Run of show — the 165-minute slot

| Time | Block | Instructor | Students |
|---|---|---|---|
| 09:05–09:15 | Instructions (10) | Check student ID cards, hand out papers face down, state the rules, ask for name and ID on every page | Listen; no writing yet |
| 09:15–11:40 | Work and checking (145) | Invigilate; announce the time at 09:50, 10:25, 10:55 and 11:25 and at 11:35 (5 minutes left); answer only questions about wording | Four stations in any order; the last 15 minutes are for checking |
| 11:40–11:50 | Collection (10) | Collect and count papers; check names and IDs | Stop writing |

There is no extra writing time and no debrief inside the slot.

## 4. Scoring

| Step | Rule |
|---|---|
| Per station | 25 marks, Basic 12.5 + Technical 12.5, using the private key's per-question mark map |
| Partial credit | For each criterion shown; small syntax slips do not lose fix marks if the idea is clear |
| Fix marks | None for a character blacklist (for example filtering only `;`); full marks need the ownership decision made before the data is read |
| Paper total | 100 raw |
| Course mark | Basic ÷ 50 × 6 + Technical ÷ 50 × 6, at most 12 |

The key is private. Never copy any of it into this repository's public files.

## 5. Academic integrity

Individual work, closed book, one paper each. Controls: ID check, seating, no devices, names on every sheet, papers counted at collection. Questions are written so that reasoning matters more than memorised answers: students read printed output from someone else's fix and explain what it does and does not prove.

## 6. After the sitting

- Mark with the private key and enter the Basic and Technical raw scores.
- Note any question the class found unclear or very slow (the exam design has not had a timed student pilot).
- Week 10 opens with its weekly quiz and today's goal; results of this exam are released through the usual feedback route.

## 7. Materials

- Student brief: `labs/week09-midterm-practical/ctf.md`, `labs/week09-midterm-practical/README.md`
- Proctor deck: `slides/week09.md`
- Instructor-only (git-ignored): the private Form B paper, its printable PDF generator, and its key
- Archived plan for the earlier hosted-CTFd sitting: [week09-midterm-practical-hosted-ctf-archive.md](week09-midterm-practical-hosted-ctf-archive.md)

## 8. Risks

| Risk | Mitigation |
|---|---|
| Not enough time for 21 questions in 145 minutes | The design is not a timed pilot. Watch during the sitting for students stuck at Station A and tell them to move on |
| A student reads a printed `500` status as meaningful | It comes from the checker's mocked process call. Accept any correct reading of the output |
| Notice, Classroom and slides disagree | Check all three against `README.md` before the day |
| Papers printed from an old version | Rebuild the PDF after any edit and compare page count and date |

## 9. Post-teaching reflection

*Complete after the session.*

- Attendance / completion: ⬚
- Time actually taken per station (vs. plan): ⬚
- Where students got stuck: ⬚
- Question with the lowest marks, and what that says about the week it came from: ⬚
- Anything to change before this exam runs again: ⬚
