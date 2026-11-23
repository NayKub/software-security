---
marp: true
theme: default
paginate: true
header: "Software Security 2 · KOSEN 02005094 · Week 16"
---

# Week 16 · Formative capstone studio
## Tuesday 16 February 2027, 09:05–11:50 · teams 2–3

No separate worksheet marks. This supports the existing 15% project; it is not a thirteenth Lab.

---

## Today: 10 + 100 + 30 + 10 = 150 minutes

- 0–10: brief and select remaining risks
- 10–110: build, test and peer review
- 110–140: instructor project clarification
- 140–150: save evidence and next actions

Optional peer preview of at most 5 minutes inside the 100-minute block; teams do not each need a 15-minute presentation.

---

## A convincing project chain

Threat model → authorized finding → root cause → student fix → negative and legitimate positive controls.

SBOM scope; trusted signing identity and cryptographic verification; CI red/green evidence. A signature plus SBOM does not automatically establish a SLSA level.

---

## Map the whole course

![OWASP/category map linking course topics to their labs; assessment rules follow the current project guide.](img/owasp-map.svg)

---

## Peer feedback

- Does the model cover actual boundaries and risks?
- Are findings precise, ethical and reproducible?
- Does the patch close the cause while preserving intended behavior?
- Does the CI gate fail safely, with useful secret-free logs?

Feedback stays formative. Optional scrimmage work uses remaining time only.

---

## Project deadline: Sunday 28 February 2027

Submit the project report + code + a recorded video of **at most 5 minutes** by 23:59 on learn.zcr.ai/submit (one report PDF per team, with the code and video links inside).

Project questions: Weeks 16 and 20. Week 19 is the separate 150-minute team practical (four stations, 100 points); no project questions take exam time.

The project mark (after peer adjustment) is out of 100 and counts 15% of the course.

[Current checklist](../labs/week16-capstone/worksheet.md)
