import urllib.request
import json

url = "http://vpngate.net"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', errors='ignore')

servers = []
lines = response.splitlines()

for line in lines[2:]:
    parts = line.split(',')
    if len(parts) >= 15:
        try:
            speed = int(parts[4])  # Speed in bps
            ping = parts[3]
            country = parts[5]
            country_code = parts[6]
            ovpn_base64 = parts[14]

            # Sirf 10 Mbps se tez aur valid config wale servers lein
            if speed > 10000000 and len(ovpn_base64) > 100:
                servers.append({
                    "country": country,
                    "country_code": country_code,
                    "speed_mbps": round(speed / 1000000, 1),
                    "ping": ping,
                    "ovpn_base64": ovpn_base64
                })
        except Exception:
            continue

# Speed ke hisab se sort karein (sab se tez upar)
servers.sort(key=lambda x: x["speed_mbps"], reverse=True)

# Top 30 fast servers save karein
with open("servers.json", "w", encoding="utf-8") as f:
    json.dump(servers[:30], f, indent=2)

print(f"Saved {len(servers[:30])} servers successfully.")
