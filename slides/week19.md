---
marp: true
theme: default
paginate: true
header: "Software Security 2 · KOSEN 02005094 · Week 19 · Final team practical"
---

# Week 19 — Final team practical
## KOSEN 02005094
Paper exam · your project team of 2–3 · whole term, mostly Weeks 10–15

Date, time and room: announced by your instructor (final exam period 8–16 March 2027).

<!-- Instructor: print the paper version (instructor/exams/kosen-02005094/week19-paper-form-B.md) and use its matching key. No computers in this exam. -->

---

## Format and time

- **150 minutes:** instructions 10 + four stations 130 + collecting papers 10
- **Paper, closed book:** no computer, phone, notes or AI; one answer booklet per team
- **Four stations × 25 marks = 100**
- All 100 marks are Technical; they count **15%** of the course

---

## Four stations — 130 minutes

- **A: 30 minutes, 25 marks** — who may read which orders, and which fields a client may set (practice: Week 10)
- **B: 35 minutes, 25 marks** — explain a given memory crash; write the Rust character counter (practice: Week 11)
- **C: 30 minutes, 25 marks** — trusted signing key and a small S3 policy fix (practice: Weeks 12–13)
- **D: 35 minutes, 25 marks** — clean up AI output and deny access on errors (practice: Weeks 14–15)

Practise writing these fixes by hand before the exam.

---

## Splitting the work

- Your team may split the stations between members
- Every member must be able to explain **any** station if asked
- Write on the first page who wrote which station

---

## What earns marks

- Find the problem; explain why it happens and where the trust boundary is
- Write your own fix as code (small syntax slips are fine if the idea is clear)
- One example that should work and one that should be refused, with the result you expect
- Read a printed test output: what it shows and one thing it cannot prove

Each station: root cause 5 + fix 10 + examples 7 + evidence and limits 3 = 25 Technical. 100 marks = 15 course points.

---

## On the day, and the project

- Write every member's name, student ID and stations on the first page
- Stop writing after 130 minutes; papers are collected in the last 10 minutes
- Project report, code and a **video of at most 5 minutes** were due **Sunday 28 February 2027, 23:59**, marked separately (15%)
- No project questions during the 130 minutes; ask them in Weeks 16 and 20

[The four stations](../labs/week19-final-ctf-capstone/ctf.md)
