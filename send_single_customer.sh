response=$(curl -sS -f \
  -w '\nHTTP status: %{http_code}\n' \
  -X POST 'https://jsonplaceholder.typicode.com/posts' \
  -H 'Content-Type: application/json' \
  -d '{"title":"Test post","body":"Testing my page","userId":1}')
curl_exit=$?

printf '%s\n' "$response"
printf 'curl exit code: %s\n' "$curl_exit"
