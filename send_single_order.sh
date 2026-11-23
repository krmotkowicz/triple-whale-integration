response=$(curl -sS \
  -w '\nHTTP status: %{http_code}\n' \
  -X POST 'https://api.triplewhale.com/api/v2/data-in/orders' \
  -H 'Content-Type: application/json' \
  -H "x-api-key: $TRIPLE_WHALE_API_KEY" \
  -d '{
    "shop": "example123.com",
    "order_id": "111",
    "created_at": "2026-11-22T00:00:00Z",  
    "currency": "AUD",
    "customer": {
      "id": "111",
      "email": "cust111@example.com"
    },
    "order_revenue": 500
  }')

curl_exit=$?

printf '%s\n' "$response"
printf 'curl exit code: %s\n' "$curl_exit"
