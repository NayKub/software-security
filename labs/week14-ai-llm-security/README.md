# Week 14 — Security of AI / LLM-Powered Applications

## Class and assessment contract

**Class: Tuesday 2 February 2027, 09:05–11:50 (150 minutes)** = quiz/review 10 + explanation/demo 15 + supervised practical 100 + debrief 20 + evidence/exit 5. Build the lab image before class (see below). In class you do the five **core tasks** in Part 3; the "Optional extension" (including Agent Breaker) adds no points.

**Common practical 60 points + one assigned 40-point section.** This week odd student IDs do **Conventional** (Part 2 written questions 20 + Part 4 reflection 20) and even student IDs do **AIR-Sec** (Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10); the mapping swaps every week. Each version totals 100. Each of the twelve individual teaching worksheets contributes `score / 100 × 2.5` course points.

Your instructor may ask you to show or repeat any step. This only checks that the work is yours; it does not change the score. The demo flag is the same for everyone and is the expected evidence; nothing is submitted on ctf.zcr.ai. Write which AI tool you used, if any, on the answer sheet.

**Due:** Monday 8 February 2027, 23:59 (Thai time).

**OWASP Top 10 for LLM Applications (2025):** LLM01 Prompt Injection · LLM02 Sensitive Info Disclosure · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM08 Vector/Embedding Weaknesses · LLM10 Unbounded Consumption

## ✅ This week — what to do
1. **Before class** — Docker Desktop working (Week 1 *Lab 0*); while online run `cd ~/software-security/labs/week14-ai-llm-security` then `docker compose build`. Skim last week's recap.
2. **Slides, then class** — read `slides/week14.md` and the worksheet's Part 2 to prepare. Class opens with the weekly quiz (10 min) and a short explanation and demo (15 min).
3. **Lab (in class)** — start both bots with `docker compose up --no-build --pull never` (insecure on `:8082`, guarded on `:8083`) and do the five core tasks in the worksheet's Part 3. Then do the written section for your student ID this week (odd: Conventional 40; even: AIR-Sec 20/10/10), after class if needed.
4. **Submit by Monday 8 February 2027, 23:59** — worksheet PDF → `learn.zcr.ai/submit` · code → GitHub (commit link to `student_task.py` on branch `wk14`) · weekly quiz → `learn.zcr.ai/quiz`. (How: [SUBMISSION.md](../../SUBMISSION.md).)
5. **Project** — apply this week's lesson to your [NoteVault project](../../project/README.md) where it fits.

*Time breakdown: [AGENDA.md](../../AGENDA.md). Grading: see the worksheet rubric.*

## Objectives
- Explain the LLM Top 10 and where AI features add attack surface.
- Demonstrate direct-injection behavior in the deterministic mock; explain indirect-injection risks as a design case.
- Add guardrails: input/output validation, least-privilege tools, output handling.

## 🧙 Optional external game — "Gandalf Challenge"
External extension reference: Lakera Agent Breaker (https://play.lakera.ai/agent-breaker). Check its current access/rules before use. It is not required for the worksheet; external game points are engagement only.
1. **Direct prompt injection:** override the system prompt to reveal a hidden secret (required: local bots in Tasks 1–2; external levels are optional).
2. **Indirect injection (optional design case):** explain a malicious instruction in a retrieved document; the local mock has no RAG pipeline to trigger.
3. **Improper output handling:** show model output flowing unsanitized into a downstream action (XSS/command).
4. **Agentic-AI / MCP risks (current, post-Oct 2025, written-only):** this lab has no agent to attack — describe how **tool poisoning** and **excessive agency** would work in an agent with tools (e.g. an MCP server), where a malicious instruction makes the agent call a tool it shouldn't.
5. **Fix (round 2):** input/output guardrails, strict output schemas/validation, **least-privilege tool access**, human-in-the-loop for sensitive tools, and rate/consumption limits; re-test.

## Deliverable
Required core: local mock disclosure/output observations, the student output-control diff, legitimate/attack test results and an explanation of the mock's limits. The agent/MCP design and external game are reference/extension material; the assigned written section remains within its 40 points.

## References
- https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
- https://play.lakera.ai/agent-breaker — Lakera Agent Breaker (optional external reference; verify current access/rules)
- MITRE ATLAS (AI/agentic attack techniques) — https://atlas.mitre.org/
