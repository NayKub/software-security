---
marp: true
theme: default
paginate: true
header: "Software Security 2 · 02005094 · Week 11"
---

<!-- Current KOSEN class: 150 minutes = quiz/review10 + brief15 + shared practical100 + debrief20 + capture5. Full deck is pre-class/reference; select only the short live explanation. Both versions: common60 plus Conventional40 OR AIR20/10/10. Viva verifies existing work, no extra score or automatic-zero gate. -->


# Week 11
## Memory-Safety & Exploitation
Software Security 2 · Tuesday 12 January 2027, 09:05–11:50

<!-- Hook: feed random bytes to a C program until it crashes, then turn that crash into "execute my code." This week is the closest to classic hacking — and to why the world is moving to Rust. ~2 min. -->

---

## Today

- The C/C++ memory model & the stack
- Finding bugs with **fuzzing**
- Stack overflow → control hijack
- Mitigations + the **memory-safe language** shift
- 🎮 Game: **Fuzzing Race → Pwn the Binary**

<!-- Roadmap, 1 min. Arc of the week: find (fuzz) → understand (debug) → exploit (pwn) → defend (mitigations) → cure (Rust). Lab follows the same arc. -->

---

## Why this still matters

- C/C++ runs the world's critical infrastructure
- Memory bugs = ~70% of severe CVEs historically
- Now a national-policy issue (CISA/ONCD roadmaps)

<!-- Motivate hard. ~70% of Microsoft/Chrome severe CVEs are memory-safety bugs — that stat lands. It's now government policy (CISA Secure by Design, White House ONCD memory-safety report). This isn't legacy trivia; it's current. ~4 min. -->

---

## Why it still matters — in one picture

![Why memory safety still matters: C/C++ runs the world's critical infrastructure (OS kernels, browsers, embedded, network stacks); memory bugs are about 70% of severe CVEs historically (Microsoft, Chrome and Android all agree); and it is now a national-policy issue (CISA Secure by Design, ONCD memory-safe roadmap, NSA guidance). Memory safety is not a legacy footnote — it is still the dominant source of serious vulnerabilities, which is why this week ends at "rewrite it in a memory-safe language".](img/why-memory-safety-matters.svg)

<!-- The visual for the motivation — point at the ~70%, say "C/C++ is everywhere AND it's where most severe bugs live," then the policy response. Sets up why the week ends with the Rust rewrite. ~1 min. -->

---

## The stack frame

- `gets`/`strcpy`/unchecked `memcpy` → overflow
- Overwrite return address → redirect execution

```sim
stack-frame
```

<!-- The worked example — the sim IS the board drawing, live. A local buffer sits BELOW the saved return address; writing past the buffer marches upward into the return address. Control the return address = control where the CPU jumps next. This is THE concept of the week. ~8 min. -->

---

## Bug classes

- **CWE-121** stack overflow · **CWE-787** OOB write
- **CWE-134** format string · **CWE-242** dangerous function (`gets()`)
- *(this week's binary: no UAF, no off-by-one — those are real bug classes but not in this lab's code)*

<!-- Map the family — these four are what's actually in vuln.c/fuzz_harness.c, verified against the source. UAF and off-by-one are legitimate classes worth mentioning exist, but don't cite them as "this week's bug classes" — nothing here demonstrates them. CWE-121 (this week's actual bug) ranks #14 in the 2025 CWE Top 25 — a stronger, on-topic stat than the old CWE-787-was-#1 line, which is now #5. ~3 min. -->

---

## The four bug classes, side by side

![The four memory-safety weakness classes present in this week's vuln.c, as a classification (not an exploitation guide): CWE-121 stack-based buffer overflow (writing past a fixed char buffer overruns adjacent stack memory), CWE-787 out-of-bounds write (the umbrella class, of which CWE-121 is the stack case), CWE-134 use of an externally-controlled format string (printf(user) instead of printf("%s", user) lets input read or corrupt memory), and CWE-242 use of an inherently dangerous function (gets(), which cannot be used safely and was removed from C11). Footnote: this binary has no use-after-free and no off-by-one — real classes, just not in this code.](img/memory-bug-classes.svg)

<!-- The four classes as cards — each is a weakness definition (what it IS), not a how-to. Point out CWE-121 is the stack case of the CWE-787 umbrella, and that gets() (CWE-242) is so unsafe it was removed from the C standard. Keep the UAF/off-by-one footnote honest — those aren't in this binary. ~1 min. -->

---

## Fuzzing — how bugs are found today

```bash
clang -g -fsanitize=address,fuzzer fuzz_harness.c -o fuzz && ./fuzz   # libFuzzer
```

- Coverage-guided mutation finds crashes fast
- Pair with sanitizers (ASan) for root cause
- The toolbox has libFuzzer, not AFL++ — one fuzzer is plenty for this lab

![Coverage-guided fuzzing as a feedback loop. The top row runs seed corpus → mutate (flip/splice bytes) → run target → "what happened?", which asks two questions. First: did the input reach NEW code? If yes it's kept and added to the corpus, and a dashed arrow feeds back to mutate — this is the coverage-guided loop that lets the fuzzer learn its way to deep bugs instead of guessing blindly. Second: did it crash? If yes, AddressSanitizer turns a silent memory corruption into a precise report naming the faulting line, and the crashing input is minimized and saved as crash-<hash>. Two notes: coverage guidance reaches bugs a random generator never would, and ASan turns a mystery segfault into an actionable root cause. This is round 1 of the lab — finding the crash, not exploiting it.](img/fuzz-loop.svg)

<!-- Connect to W2 fuzzing (now hands-on). Coverage-guided = the fuzzer mutates inputs and keeps the ones that reach NEW code, so it "learns" its way to deep bugs. ASan turns a silent corruption into a precise crash report. This is round 1 of the game. ~6 min. -->

---

## Exploiting a stack overflow

1. Measure the return-address offset in the issued binary: use a **cyclic pattern** with a working debugger, or disassembly plus a successful exploit control if ptrace fails under emulation. Do not assume 72 bytes applies to another build.
2. Overwrite RA → jump to `win()`
3. Format string: `%x%x%x` leak, `%n` write

<!-- Walk the exploit method. Cyclic pattern (De Bruijn) tells you exactly how many bytes for THIS specific build — stress that 72 is a fact about the unhardened binary, not a fact about the bug; the sim/exploit-chain diagram shows this shift explicitly. Then overwrite it with the address of win(). Format string: %x leaks stack, %n writes — a primitive most students haven't seen. This is round 2 (pwn). ~6 min. -->

---

## Mitigations raise the bar

- **FORTIFY_SOURCE** — checks the copy itself, at call time (`__stpcpy_chk` or `__strcpy_chk`, depending on the compiler)
- **Stack canaries** — detect overwrite at function return, *after* the copy already happened
- **ASLR** / **PIE** — randomize addresses
- **NX/DEP** — blocks executing shellcode planted *on the stack* — irrelevant to this exploit, which returns into existing code (`win()`), never injects shellcode
- On **this lab's hardened build, FORTIFY fires first** — `*** buffer overflow detected ***: terminated`. The canary never gets a chance to run. Check this yourself in Task 3: it is FORTIFY, not the canary, that stops the payload.

<!-- THE key correction this slide needed: FORTIFY_SOURCE checks at the copy call, before the function even returns — so on the hardened build it always wins the race against the canary, which only checks at return time. This lab's own interactive sim literally calls "the canary detects it" the week's most reliable wrong answer — don't teach it. NX is a real mitigation but not for THIS exploit (ret2win, no injected shellcode) — say so explicitly rather than implying all four defenses equally harden the one attack just demonstrated. Worksheet Q4 grades naming all four (canary/PIE/NX/FORTIFY) + what each defeats — FORTIFY must be on this slide. ~5 min. -->

---

## From strcpy to shell — where each mitigation cuts the chain

![A vertical attack chain from fuzzing finding the crash, to the unchecked strcpy overflow, to the overwritten return address, to a ret2win shell. Three mitigations cut this chain at different links: FORTIFY_SOURCE aborts at copy time, before any overwrite — this hardened build traps here, which students often misread as the canary. The stack canary only detects the smash at return, after the copy already happened. ASLR/PIE randomizes addresses so the fixed win() address is wrong. NX/DEP stops the OTHER exploitation path (injected shellcode), not this one.](img/exploit-chain.svg)

<!-- Walk it top to bottom exactly once — this is the whole week's argument as one picture: which mitigation actually stops THIS exploit, and in what order they'd fire if more than one were present. Land on the same correction as the last slide: FORTIFY wins the race against the canary, every time, on this build. ~4 min. -->

---

## The real fix: memory-safe languages

- Safe Rust and managed Go code prevent the unchecked memory writes shown here; unsafe/native boundaries need separate review
- CISA "Secure by Design" + ONCD: move off C/C++ for new code
- Rust borrow checking and bounds checks, or Go runtime checks, prevent this C-style unchecked buffer write

![Comparison of C/C++ unchecked memory operations with safe Rust and managed Go code. The C lab's unchecked copy can overwrite the stack; canaries, ASLR, PIE, NX and FORTIFY can detect or impede exploitation without removing that source bug. Safe Rust uses ownership and bounds checks; Go uses managed memory and bounds checks. These prevent the shown unchecked write in their safe-code scope. Unsafe Rust, native interfaces, logic flaws, panics and resource errors remain separate risks.](img/memory-safe-languages.svg)

<!-- The thesis of the week. Explain what safe Rust prevents in this counting task, then name the boundary: unsafe blocks, native interfaces and input/resource errors are not removed by choosing a language. Go has garbage collection and runtime bounds checks, not Rust's borrow checker. ~4 min. -->

---

## 💥 Game — Fuzzing Race → Pwn the Binary

1. **Round 1 (Fuzzing Race):** who crashes the target first? (everyone submits their own evidence)
2. **Round 2 (Pwn):** exploit the overflow / format string
3. **Round 3 (Defend):** test the supplied hardened build, then implement the bounded safe counting function in `student_safe.rs`; a full rewrite is extension practice

<!-- Explain the 3 rounds before lab. Round 1 = reproducible crash. Round 2 = measured ret2win in the isolated toolbox. Round 3 = hardened control plus student-authored Rust counting function. If ptrace fails under emulation, accept disassembly with the actual binary and exploit control. The weekly quiz runs before the lab; capture these results in the worksheet. ~3 min. -->

---

## Deliverable

> 📋 **Worksheet 11** — `labs/week11-memory-safety-exploitation/worksheet.md` · follow the 100-minute core run sheet.

- Seeded fuzz/replay and measured ret2win evidence from the issued isolated toolchain
- Hardened-build control and its actual observed failure mode
- Your `student_safe.rs` counting change plus `python3 check_student.py` controls; state memory-safety/input-error limitations
- **Assigned written version only:** Conventional Part 2/4 (20/20) or AIR Audit/EiPE/Prompt (20/10/10), after the shared practical 60.

<!-- No promise that safe Rust can never panic or reject input. Measure the actual architecture/build, and do not execute vulnerable binaries on the host. -->

---

## Key takeaways

- Fuzz to find, debug to understand, mitigate to slow attackers
- Mitigations raise exploit cost; safe memory handling removes this unchecked-write path
- This is where the industry is moving

<!-- Recap. Cold-call: "why aren't stack canaries enough?" (they detect, don't prevent; bypassable via leaks — the cure is memory safety). ~2 min. -->

---

# Questions?
Next week: Software supply-chain security

<!-- Cliffhanger: "Next week — one poisoned dependency owns thousands of victims; we'll replay xz and SolarWinds-style attacks." -->


---

## This week's hand-in

- **Class:** Tuesday 12 January 2027, 09:05–11:50 (150 minutes): quiz 10 + explanation/demo 15 + practical 100 + debrief 20 + evidence 5
- **Everyone (60 points):** fuzz and replay a crash, measure and try ret2win, run the hardened build, complete `count_chars()` in `student_safe.rs` and show the checker before and after, and explain the evidence
- **This week odd ID = AIR-Sec** (Audit-the-AI 20 + EiPE 10 + Prompt 10) · **even ID = Conventional** (Part 2 + Part 4, 40)
- **Code link:** commit `student_safe.rs` to branch `wk11` in your fork
- **Due:** Monday 18 January 2027, 23:59 · worksheet PDF to learn.zcr.ai/submit
- Run the C programs only inside the toolbox container; the demo `FLAG{...}` is the same for everyone and nothing goes to ctf.zcr.ai
