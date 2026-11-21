import urllib.request
import json

url = "https://www.vpngate.net/api/iphone/"

try:
req = urllib.request.Request(
url,
headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as response:
    data = response.read()
    status = response.status

print("HTTP Status:", status)
print("Response Size:", len(data), "bytes")

text = data.decode("utf-8", errors="replace")

print("First 500 characters:")
print(text[:500])

if not text.strip():
    raise ValueError("Empty API response")

if "HostName" in text:
    print("CSV header detected")
else:
    print("CSV header NOT detected")

except Exception as e:
print("FETCH ERROR:", repr(e))
raise
