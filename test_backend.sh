#!/bin/bash
set -e

echo "=== 🧩 TEST BACKEND – La Favorita Bistro ==="

# 1️⃣ Health check
echo -n "1. Healthcheck... "
curl -sf http://localhost:8000/health >/dev/null && echo "✅ OK"

# 2️⃣ Login e token
echo -n "2. Login (admin/admin)... "
TOKEN=$(curl -s -X POST -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin" \
  http://localhost:8000/auth/login | jq -r '.access_token')
if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "❌ LOGIN FAILED"; exit 1
else
  echo "✅ OK"
fi

# 3️⃣ /me endpoint
echo -n "3. Current user... "
curl -sf -H "Authorization: Bearer $TOKEN" http://localhost:8000/me >/dev/null && echo "✅ OK"

# 4️⃣ /areas endpoint
echo -n "4. Areas list... "
curl -sf -H "Authorization: Bearer $TOKEN" http://localhost:8000/areas >/dev/null && echo "✅ OK"

# 5️⃣ /users endpoint
echo -n "5. Users list... "
curl -sf -H "Authorization: Bearer $TOKEN" http://localhost:8000/users >/dev/null && echo "✅ OK"

# 6️⃣ /tables endpoint
echo -n "6. Tables list... "
curl -sf -H "Authorization: Bearer $TOKEN" http://localhost:8000/tables >/dev/null && echo "✅ OK"

echo "🎯 Tutti i test base completati con successo!"
