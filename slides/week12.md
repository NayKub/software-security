---
marp: true
theme: default
paginate: true
header: "Software Security 2 · 02005094 · Week 12"
---

<!-- Current KOSEN class: 150 minutes = quiz/review10 + brief15 + shared practical100 + debrief20 + capture5. Full deck is pre-class/reference; select only the short live explanation. Both versions: common60 plus Conventional40 OR AIR20/10/10. Viva verifies existing work, no extra score or automatic-zero gate. -->


# Week 12
## Software Supply-Chain Security
Software Security 2 · Tuesday 19 January 2027, 09:05–11:50

<!-- Hook: ask how many lines of code they wrote in their last project vs how many they shipped. The gap is dependencies — and that's the attack surface this week. One poisoned package = thousands of victims. ~2 min. -->

---

## Today

- Why the supply chain is now top-tier
- Dependency confusion & typosquatting
- SBOMs, SLSA provenance
- Signing with Sigstore/Cosign
- 🎮 Game: **Dependency Confusion Heist**

<!-- Roadmap, 1 min. Three verbs to remember all week: KNOW your ingredients (SBOM), PROVE your build (SLSA), SIGN your artifacts (Cosign). -->

---

## The new #1 design risk

- Your code is ~10% yours, ~90% dependencies
- One bad package → thousands of victims (xz, event-stream, SolarWinds)
- **OWASP A03:2025 Software Supply Chain Failures**

<!-- New in OWASP 2025 — promoted to A03, reflecting reality. The 10/90 ratio shocks students. You can write perfect code and still be owned through a dependency you never read. ~4 min. -->

---

## Most of your attack surface is other people's code

![Why the supply chain is now the top-tier risk: you write about 10% of what you ship and dependencies are the other ~90%, so every bug in that 90% ships under your name; one poisoned package fans out to thousands of downstream victims (xz-utils 2024, event-stream 2018, SolarWinds 2020); and OWASP promoted this up the list to A03:2025 Software Supply Chain Failures. You can write perfect code and still be owned through a dependency you never read.](img/supply-chain-design-risk.svg)

<!-- The 10/90 ratio made visual — land it hard, then the blast radius (one publish → thousands), then the A03:2025 promotion. The closing line is the week's thesis. ~2 min. -->

---

## Real supply-chain attacks

| Case | What happened |
|---|---|
| **SolarWinds** (2020) | trojanized vendor update → 18k orgs |
| **Log4Shell** (2021) | RCE in a ubiquitous logging dep |
| **event-stream** (npm) | malicious dep stole crypto-wallet keys |
| **XZ Utils** (2024) | backdoor planted in `liblzma` upstream |
| **CircleCI** (2023) | stolen CI tokens → customer secrets |

> Attacks are shifting **upstream**: registry → maintainer → CI/CD.

<!-- Spend time on xz (2024): a patient attacker became a trusted maintainer over years, then planted a backdoor caught only by luck (a 0.5s SSH delay). The lesson: trust in maintainers is itself attackable. ~5 min. -->

---

## Attack vectors

- **Typosquatting** — `reqeusts` vs `requests`; the malicious package's `setup.py` runs **at install time**, before any of your code runs — you don't have to import it to be owned
- **Dependency confusion** (**CWE-1357**) — public pkg shadows internal name
- **Malicious updates** — compromised maintainer
- **Transitive risk** — deps of deps you never chose

<!-- Define dependency confusion clearly (it's the game): if your internal pkg "acme-utils" isn't scoped, a public "acme-utils" with a higher version number can get pulled instead. Transitive = you vet your 10 deps, but they pull 800 you never saw. Stress the install-time-execution point — it's why "I never imported it" isn't a defense, and explain that this lab models index selection rather than installing a malicious package. ~5 min. -->

---

## Four ways a dependency turns malicious

![The four supply-chain attack vectors as a taxonomy: typosquatting (a malicious package named like one you use — reqeusts for requests — whose setup.py runs at install time, before any import, so a single typo is enough to be owned); dependency confusion (CWE-1357, a public package with a higher version shadows your internal name and is pulled instead); malicious updates (a hijacked or compromised maintainer ships a bad version of a package you already trust); and transitive risk (the dependencies of your dependencies, code you never chose or reviewed but still ship). The trust boundary is bigger than your requirements.txt.](img/supply-chain-attack-vectors.svg)

<!-- The four vectors as cards — the one to hammer is install-time execution (typosquat setup.py), because it kills the "I never imported it" defense but this lab does not install a malicious package or create a PWNED marker. Dependency confusion is the game. ~2 min. -->

---

## Try it — which package actually installs?

Set both versions and the index mode. This bounded single-package comparison demonstrates index selection; it is not pip's complete resolver.

```sim
resolver-confusion
```

<!-- Let them find the uncomfortable case themselves: merged mode with the private version numerically HIGHER also happens to be "safe" — but say explicitly that this is not a defense, just luck, since the attacker picks their own version number and will publish something higher. The only real fix in this sim is switching to single-index mode. Ties directly to Task 2 and Task 4's defense #2. ~4 min. -->

---

## SCA — find vulnerable deps

```bash
docker run --rm -v "$PWD:/src" aquasec/trivy fs /src   # this lab's Python deps
pip-audit                                                          # vs PyPI advisories
```

- Produces CVEs + fix versions
- CWE-1104 (unmaintained), CWE-829 (untrusted inclusion), **CWE-1395** (known-vulnerable 3rd-party dependency)

![Software Composition Analysis turns requirements.txt into a remediation worklist: the pinned-but-outdated deps (Flask 1.1.4, Werkzeug 1.0.1, urllib3 1.26.4, requests 2.25.1) feed two scanners — trivy fs (matches versions to the CVE database) and pip-audit (checks PyPI advisories) — neither of which reads your code, both read your dependency list. The output is one row per vulnerable package with the version that fixes it: Flask → 2.3.2 (CVE-2023-30861, HIGH), Werkzeug → 3.0.3 (CVE-2024-34069, HIGH), urllib3 → 1.26.17 (CVE-2023-43804, HIGH). The contrast: SAST reads the code you wrote and finds your bugs; SCA reads the versions you depend on and finds other people's known, already-patched bugs, so the fix is a version bump, not a code change.](img/sca-worklist.svg)

<!-- Hands-on tooling (ties to W2 SCA). This lab is pure Python — no npm project — so it's trivy fs + pip-audit, not npm audit/dependency-check. Run trivy live on the project — it lists CVEs + the fixed version. The diagram's one job: SCA ≠ SAST. SAST = your code, your bugs; SCA = your versions, other people's known bugs, fix = bump the pin. Don't read the worklist rows aloud — they'll run it live; point at the "→ FIXED IN" column and say "that's the whole remediation, a version number." ~4 min. -->

---

## Integrity: prove what you shipped

- **SBOM** (CycloneDX/SPDX) — ingredient list of the build
- **SLSA** — levels of build provenance & tamper-resistance
- **A08:2025** Software/Data Integrity Failures

<!-- SBOM = the food-label analogy: you can't manage what you can't list. When the next Log4Shell drops, an SBOM answers "are we affected?" in seconds. SLSA Build Track = levels L0–L3 of build provenance / tamper-resistance (L3 is the top; the old "1–4" numbering was v0.1 and is deprecated). ~5 min. -->

---

## Know what's in it, prove how it was built

![Two integrity controls side by side. Left, an SBOM (CycloneDX / SPDX): the build's itemized ingredient list — every component and version — so when the next Log4Shell drops you search it and answer "are we affected?" in seconds, not weeks. Right, SLSA: a ladder of build-provenance levels from L0 to L3 — L0 no guarantees, L1 provenance exists but is forgeable, L2 hosted build and signed (tamper-evident), L3 hardened builds whose provenance cannot be forged. SBOM knows what is in it; SLSA proves how it was built. Both map to OWASP A08:2025 Software or Data Integrity Failures.](img/sbom-slsa-integrity.svg)

<!-- SBOM = food label (know the ingredients, fast incident response); SLSA = the provenance ladder L0-L3 (prove how it was built). Two different questions, both integrity. Note the L0-L3 numbering replaces the deprecated 1-4. ~2 min. -->

---

## Signing with Cosign (keyless)

```bash
IMG=week12-supplychain:lab
docker run -d --rm --name reg -p 5500:5000 registry:2          # cosign signs a REGISTRY ref,
docker tag "$IMG" localhost:5500/$IMG && docker push localhost:5500/$IMG   # not a bare local tag
docker run --rm -v "$PWD:/src" -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image --format cyclonedx \
  --output /src/sbom.cdx.json "$IMG"                          # SBOM (reads the local image fine)
docker run --rm -it -e COSIGN_EXPERIMENTAL=1 --network host \
  gcr.io/projectsigstore/cosign:latest sign --yes localhost:5500/$IMG   # sign (OIDC)
docker run --rm -e COSIGN_EXPERIMENTAL=1 --network host \
  gcr.io/projectsigstore/cosign:latest verify \
  --certificate-identity-regexp ".*" \
  --certificate-oidc-issuer-regexp ".*" localhost:5500/$IMG            # verify
```

- Unsigned/tampered image → verification fails
- **`cosign sign`/`verify` need a registry reference** — mounting the docker socket only lets *trivy* read the local image; cosign has nowhere to attach a signature until the image is pushed somewhere, so `sign.sh` starts a throwaway local registry first
- **Every step needs the docker-socket mount** (trivy has to reach the local image, not just a local dir) — the SBOM step is a common copy-paste failure if it's dropped
- **`cosign verify` needs the two `--certificate-*-regexp` flags** in keyless mode — without them it errors, it doesn't just "fail closed"
- The demo's `".*"` identity/issuer patterns accept any signer. Pin the expected identity and issuer in a real admission policy; a mathematically valid signature alone is insufficient.
- Keyless signing uses **Fulcio** (short-lived certificate) + **Rekor** (transparency log) and avoids storing a long-lived signing key locally. **CWE-321 specifically means a hard-coded cryptographic key**, not every managed long-lived key.

<!-- Demo the sign→verify loop. sign.sh runs both tools dockerized — match that here, not a bare local binary. Keyless (Sigstore) = identity-based signing via OIDC through Fulcio, logged in Rekor, no key to leak — name both by name, worksheet Q4 grades on the vocabulary. The deploy gate: refuse any image that doesn't verify → a tampered artifact can't ship. This is the lab's defend step. ~4 min. -->

---

## Keyless signing — the flow

1. Authenticate the signer with OIDC; Fulcio binds an ephemeral public key to that identity in a short-lived certificate.
2. Cosign signs the artifact; Rekor records the signing event for transparency.
3. At deploy, verify the artifact signature **and the expected identity/issuer**. Reject unsigned, changed or wrong-signer artifacts.
4. The local Week 12 RSA fixture teaches this signer-trust decision without requiring a registry or OIDC login. Keyless signing reduces long-lived signing-key handling; it does not prove the build was trustworthy.

<!-- CWE-321 names a hard-coded cryptographic key, not every protected long-lived key. Use this text flow rather than the superseded sigstore-keyless.svg, which conflates those cases. Sigstore identity and Rekor evidence must be checked against an expected policy. -->

---

## Verify the signature — does it deploy?

Signed, unsigned, tampered, or signed by someone else. Run the gate and watch.

```sim
cosign-verify
```

<!-- The interactive companion to the keyless-signing diagram: it runs cosign's VERIFY logic in the page, so students drive the deploy gate themselves. Walk the four image states: unsigned → "no signatures found"; tampered → the signature no longer matches the digest; our CI → deploys; signed by another identity → blocked ONLY if the policy pins the expected signer. The move that lands the lesson: flip "pin the expected signer" OFF (the lab command's own '.*') and the attacker's validly-signed image deploys — a valid signature is not a signature you should trust. That's why the two --certificate-*-regexp flags from the previous slide must name YOUR identity, not '.*'. Ties to Task 3's verify-before-deploy gate and worksheet Q4. ~3 min. -->

---

## Tooling — GitHub Advanced Security (GHAS)

- **Secret scanning** + **push protection** — block secrets at push time (before they reach the remote)
- **CodeQL** code scanning — semantic SAST queries
- **Dependabot** — alerts + auto-PRs for vulnerable deps
- Native in the repo → results in the Security tab

<!-- The managed option students will meet in industry. Dependabot is the practical supply-chain workhorse: it opens PRs bumping vulnerable deps automatically. Push protection stops secrets at push time — local commits with a secret are allowed, the block fires on push to the remote (recall W2). ~3 min. -->

---

## Defenses

- **`pip install --require-hashes`** — a substituted package's hash won't match; install refuses
- **Single `--index-url`, not `--extra-index-url`** — one trusted index; the resolver won't "shop around" and pick a higher-versioned public package over your internal one
- Verify signatures before deploy (admission policy)
- Generate + store SBOMs per release
- 2FA/MFA on dev/CI/cloud accounts; least privilege
- Automate SCA in CI (next week)

<!-- The payoff checklist, now with the exact flags Task 4 grades. --require-hashes and single-index-url are what actually stops dependency confusion — "pin + scope" alone is too vague to reconstruct on the exam. Verify-before-deploy kills tampered artifacts; MFA on maintainer/CI accounts kills the xz/CircleCI vector. "Automate in CI" sets up W15. ~4 min. -->

---

## The whole journey, one dependency

![Six hops a dependency crosses from a public registry into production, each with its own attack and the control that answers it: registry (typosquatting → one trusted index), resolver (dependency confusion → scope the namespace), fetch (compromised maintainer → lockfile with hashes), build (stale pins → SCA in CI), image (no inventory → SBOM), deploy (unsigned image → Sigstore keyless gate). "We scanned our code" covers none of this — SAST reads the code you wrote, all six hops are code you didn't.](img/supply-chain.svg)

<!-- The synthesis slide — everything from the last five slides (SAST/SCA, SBOM, Cosign, the defenses checklist) is one column each in this diagram, chained in the order a real dependency actually travels. Walk it left to right ONE time, don't re-teach each hop — the point is showing they were never separate tools, they're six links in the same chain. Land on the closing line before moving to the game. ~5 min. -->

---

## 📦 Game — Dependency Confusion Heist

1. **Attack:** no live registry in this lab — use the resolver simulation to watch a higher-version public pkg beat the private one
2. **Required core:** declared-component SBOM, bounded resolver/hash controls and a real signature against the trusted key
3. **Prepared extension:** full image inventory, keyless Cosign and a provenance gate

<!-- Explain before lab — the resolver simulation stands in for a live registry (ethics: never publish a real typosquat). The bounded offline controls carry the shared practical points. Deeper SLSA analysis is reference/extension practice, or part of the assigned Conventional reflection. ~3 min. -->

---

## Deliverable

> 📋 **Worksheet 12** — `labs/week12-supply-chain/worksheet.md` · follow the 100-minute core run sheet.

- Supplied SCA snapshot analysis, or a clearly identified personal scan, plus remediation reasoning
- `python3 sbom_core.py` declared-component inventory and the two `resolver_core.py` index-mode results
- Your trusted-key pin diff and real signature positive/tamper/wrong-signer transcript
- Hash/index control and the distinction between component inventory, signature trust and build provenance
- **Assigned written version only:** Conventional Part 2/4 (20/20) or AIR Audit/EiPE/Prompt (20/10/10), after the shared practical 60.

<!-- The required core works without registry/OIDC. Full image SBOM, Cosign keyless signing and deeper SLSA self-assessment are prepared extension practice; signatures plus inventory do not automatically establish a SLSA level. -->

---

## Key takeaways

- Most of your attack surface is other people's code
- Know your ingredients (SBOM), prove your build (SLSA), sign your artifacts
- Verify before you trust

<!-- Recap with the three verbs. Cold-call: "the next Log4Shell drops at 2am — what artifact tells you if you're affected?" (the SBOM). ~2 min. -->

---

# Questions?
Next week: Cloud & container security

<!-- Cliffhanger: "Next week — where your code runs. We'll hunt cloud/container misconfigs, the #1 real-world breach cause." -->


---

## This week's hand-in

- **Class:** Tuesday 19 January 2027, 09:05–11:50 (150 minutes): quiz 10 + explanation/demo 15 + practical 100 + debrief 20 + evidence 5
- **Everyone (60 points):** the five core tasks: supplied SCA results, resolver case, SBOM, your `trusted_key()` control with the checker before (`FAILED`) and after (`OK`), and the hash/index control
- **This week odd ID = Conventional** (Part 2 + Part 4, 40) · **even ID = AIR-Sec** (Audit-the-AI 20 + EiPE 10 + Prompt 10)
- **Code link:** commit `student_task.py` to branch `wk12` in your fork
- **Due:** Monday 25 January 2027, 23:59 · worksheet PDF to learn.zcr.ai/submit
- Live scans and keyless signing (`sca_scan.sh`, `sign.sh`) are optional extensions; no flag this week
