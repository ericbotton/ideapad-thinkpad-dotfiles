curl -X POST 'https://api.resend.com/emails' \
     -H 'Authorization: Bearer re_123456789' \ # <- API key from
     -H 'Content-Type: application/json' \     #    https://resend.com/docs/api-reference/introduction
     -d $'{
  "from": "me@example.com",
  "to": ["you@example.com"],
  "subject": "hello world",
  "text": "it works!"
}'
