curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_shared_service_key" \
  -d '{
    "message": "Explain zero trust in one paragraph",
    "system_prompt": "You are a cybersecurity assistant."
  }'
