#!/bin/sh

curl -X POST 'https://api.resend.com/emails' \
     -H 'Authorization: Bearer re_123456789' \
     -H 'Content-Type: application/json' \
     -d $'{
  "from": "edb619@hotmail.com",
  "to": ["ericbotton@gmail.com"],
  "subject": "hello world",
  "text": "it works!"
}'
