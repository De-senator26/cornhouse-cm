import http.client, json

conn = http.client.HTTPConnection('127.0.0.1', 8000)
payload = json.dumps({'message': 'How do I plant maize?'})
headers = {'Content-Type': 'application/json'}
conn.request('POST', '/chat/api/', payload, headers)
res = conn.getresponse()
print(res.status, res.reason)
print(res.read().decode())
