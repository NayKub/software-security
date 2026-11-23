---
marp: true
theme: default
paginate: true
header: "Software Security · Week 5"
---

# Week 5
## XSS and browser request controls
Software Security 2 · KOSEN69

<!-- 150 min: quiz/review 10; mechanism demo 15; practical 100; debrief 20; evidence exit 5. The 100-minute budget has not had a representative student pilot. -->

---

## Today

- Reflected and stored XSS: untrusted data becomes browser code
- HTML output encoding; CSP as a second layer
- Origin versus site; authenticated CSRF
- Student patch: safe rendering **and** token validation

---

## Browser boundary

- **Origin** = scheme + host + port. `localhost:8080` and `localhost:8081` are different origins.
- **Site** excludes port. Those two pages are the same site.
- Same-origin policy limits what an attacker page can **read**. An HTML form can still **submit** to another origin.
- Cookies are scoped by host/path and policy, **not by port**. SameSite controls cross-site attachment; it is not an origin check.

<!-- Demo with DevTools: the port-8081 request targets port 8080 and carries the localhost session cookie. -->

---

## XSS: output turns data into code

| Type | Payload source | This lab |
|---|---|---|
| Reflected | URL `name` echoed into `/hello` | Yes |
| Stored | Saved comment rendered on `/comments` | Yes |
| DOM | Client JS writes untrusted input into DOM | Optional separate target |

```python
html = "<h1>Hello, " + name + "!</h1>"  # vulnerable HTML text sink
html = "<h1>Hello, " + str(escape(name)) + "!</h1>"  # fixed
```

HTML text encoding makes `<script>` visible text. JavaScript strings, URLs and attributes need their **own context-specific controls**.

---

## XSS defense layers

1. Encode at the output sink; use framework autoescaping.
2. Set CSP to limit script execution if something still lands.
3. Set `HttpOnly` so injected JavaScript cannot read a session cookie.

`HttpOnly` does **not** stop page defacement. CSP does **not** replace encoding. In the fixed lab, encoding removes the payload before a CSP violation would fire.

**OWASP 2025 A05 Injection · CWE-79 XSS**

---

## CSRF: a valid cookie, forged intent

1. The victim visits `localhost:8080/` and receives `session=abc123`.
2. The victim opens the attacker page at `localhost:8081/csrf.html`.
3. Its form POSTs to `localhost:8080/comments`; the browser attaches the same-site session cookie.
4. The vulnerable handler checks the cookie but no token, so it accepts the forged comment.

In a fresh profile with no session, the same POST returns **401**. This control proves that the attack depends on the victim's session.

---

## SameSite is not the whole CSRF defense

- Ports 8080 and 8081 are different **origins** but the same **site**; even `SameSite=Strict` can accompany this request.
- The reference handler requires a server-generated CSRF token tied to the sandbox session.
- A normal form includes the token; the attacker's page cannot read it across origins.
- Missing or wrong token returns **403**. An `Origin` check can add another layer.

**OWASP 2025 A01 Broken Access Control · CWE-352 CSRF**

<!-- A file:// attacker page is cross-site and modern default-Lax behavior may block its cookie. Use the supplied port-8081 page for the graded demonstration. -->

---

## 100-minute practical

| Time | Task |
|---:|---|
| 5 min | Baseline: normal page, cookie, comment |
| 15 min | Reflected XSS and HTML sink |
| 15 min | Stored XSS and sandbox cookie |
| 20 min | Same-site, cross-origin forged POST + no-session control |
| 45 min | Student patch, controls, browser proof |

Prepare the Docker image **before class**. `docker compose up --no-build --pull never` needs no runtime package download.

---

## Student patch: prove normal and attack controls

Edit `student_patch.py`:

- `render_name` and `render_comment`: encode for an HTML text node.
- `allow_post`: require the sandbox session and a nonempty matching CSRF token.

Run `student_checks.py` and `student_app.py`. Verify: normal comment **works**; XSS is text; forged POST is **403**; missing session is **401**. Read `fixed_app.py` only after your own patch.

---

## Assessment and exit

- **Common practical 60:** XSS observations 20, CSRF with controls 15, student patch 25.
- **Assigned 40, this week:** odd student IDs do AIR-Sec (Audit the AI 20 + EiPE 10 + Prompt 10); even student IDs do Conventional questions. The mapping swaps every week.
- Save code, browser evidence, request headers and your own explanation. Due Mon 7 Dec 23:59 (late until 17 Dec, −10% per started day).

**Sources:** [OWASP XSS prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html); [OWASP CSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html); [OWASP Top 10:2025](https://top10.owasp.org/2025/).
