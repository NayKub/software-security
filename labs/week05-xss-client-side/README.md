# Week 5 — XSS and browser request controls

**OWASP 2025:** A05 Injection / CWE-79 (XSS); A01 Broken Access Control / CWE-352 (CSRF). [Worksheet 5](worksheet.md) is the student contract.

## Class flow

10-minute quiz/review + 15-minute mechanism demo + 100-minute common practical + 20-minute debrief + 5-minute evidence exit. The quiz covers contextual output encoding, CSP and SameSite. The practical is worth 60 points; each student completes one 40-point written format: **this week odd student IDs do AIR-Sec and even student IDs do Conventional** (the mapping swaps every week). Follow-up writing is outside the 100-minute core. Submit your `student_patch.py` commit link from branch `wk05` (see [SUBMISSION.md](../../SUBMISSION.md)). The minute budgets have not been validated with a representative student.

## Prepare once, then run offline

```bash
cd ~/software-security/labs/week05-xss-client-side
docker compose build
docker compose up --no-build --pull never
```

The image pins Flask 3.1.3. No runtime `pip install` or network access is needed after the image has been built. Open `http://localhost:8080/` before testing `/comments`. The service binds only to `127.0.0.1`. To host the supplied attack page on a different origin, start `python3 -m http.server 8081 --bind 127.0.0.1` from this directory and visit `http://localhost:8081/csrf.html`.

Two localhost ports are different **origins** but the same **site**. The vulnerable endpoint requires the session cookie but accepts a comment without a CSRF token. The reference `fixed_app.py` checks a server-generated token and escapes output. Students first fix the provided `student_patch.py` and run `student_checks.py`, then test `student_app.py` in the browser. See the worksheet for the exact commands and required normal/attack controls.

The sandbox session value is deliberately fixed. The reference is a teaching example, not a production authentication pattern; production needs per-user random sessions, HTTPS and a Secure cookie.

## References

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Top 10:2025 A01](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/) and [A05](https://top10.owasp.org/2025/A05_2025-Injection/)
