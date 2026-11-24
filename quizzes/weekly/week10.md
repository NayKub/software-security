# Weekly Quiz — Week 10 (API Security)

**~5 min · in-class · 5 questions · low-stakes** (drop lowest). No devices / locked browser.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. **BOLA** (the #1 API risk) stands for:
   a) Broken Object Level Authorization  b) Basic OAuth Login Attack  c) Backend Object Load API  d) Broken Origin Logic Access
2. **Mass assignment** happens when:
   a) too many requests arrive  b) client input is bound to model fields it shouldn't set (e.g., `is_admin`)  c) the API is rate-limited  d) JSON is too large
3. Rate limiting primarily mitigates:
   a) XSS  b) brute force / resource exhaustion  c) SQLi  d) CSRF
4. In this week's lab, the `X-User-Id` header is only a teaching stand-in for identity because:
   a) it is too long to send  b) any client can type any value into it, so it proves nothing  c) the server encrypts it  d) APIs cannot read headers
5. Object-level authorization (the BOLA fix) must be checked:
   a) once, when the user logs in  b) on every request, for every object asked for  c) only for admin users  d) only in the browser
