---
marp: true
theme: default
paginate: true
header: "Software Security 2 · 02005094 · Week 9 · Midterm practical"
---

# Week 9 — Midterm individual practical
## Software Security 2 (02005094)
Paper exam · Tuesday 29 December 2026, 09:05–11:50 · our usual classroom

<!-- Instructor: print the paper version (instructor/exams/kosen-02005094/week09-paper-form-B.md) and use its matching key. No computers in this exam. -->

---

## Format and time

- **165 minutes in total:** 10 minutes instructions + 145 minutes on the tasks + 10 minutes to collect papers
- **Paper, closed book:** bring your student ID card and a pen; no computer, phone, notes or AI
- **Four stations × 25 points = 100 points**
- Each station is marked in two halves: **Basic 50 + Technical 50** in total
- The practical counts as **12%** of your course grade

---

## The four stations — 130 minutes, then 15 to check

- **A · 35 minutes · 25 points** — Threat model and scanner triage (Weeks 1–2)
- **B · 35 minutes · 25 points** — Move old password records to Argon2id at login (Week 3)
- **C · 30 minutes · 25 points** — Parameterized SQL and a safe IPv4 ping (Week 4)
- **D · 30 minutes · 25 points** — Check the login token and who owns the order (Week 6)

Practise writing these fixes by hand before the exam.

---

## What earns marks

- Find the problem and explain why it happens and where the trust boundary is
- Write your own fix as code (small syntax slips are fine if the idea is clear)
- Write one **positive test** (normal use still works) and one **negative test** (the attack is refused), with the result you expect
- Read a printed test output and say what it shows and what it cannot prove

Each station: **Basic 12.5** (finding, explanation, reading evidence) + **Technical 12.5** (your fix, your tests, reading test output). Basic 50 + Technical 50 → 6 + 6 course marks.

---

## On the day

- Bring your student ID card and a pen; write your name and student ID on the first page
- Individual work; no talking
- Stop writing after 145 minutes; papers are collected in the final 10 minutes

[Read the full practical brief](../labs/week09-midterm-practical/ctf.md)
