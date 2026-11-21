import urllib.request
import csv
import json
import io

url = "http://www.vpngate.net/api/"

servers = []

try:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response = urllib.request.urlopen(
        req,
        timeout=30
    )

    data = response.read().decode(
        "utf-8",
        errors="ignore"
    )

    lines = data.splitlines()

    # Skip API comment and CSV header
    csv_data = "\n".join(lines[2:])

    reader = csv.reader(io.StringIO(csv_data))

    for cols in reader:

        if len(cols) < 15:
            continue

        try:
            # Skip API footer
            if cols[0].startswith("*"):
                continue

            speed = int(cols[4])
            config = cols[14]

            # Filter servers
            if speed > 5000000 and len(config) > 100:

                servers.append({
                    "country": cols[5],
                    "country_code": cols[6],
                    "speed_mbps": round(speed / 1000000, 2),
                    "ping": cols[3],
                    "ip": cols[1],
                    "hostname": cols[0],
                    "ovpn_base64": config
                })

        except (ValueError, IndexError):
            continue

    # Sort fastest servers first
    servers.sort(
        key=lambda x: x["speed_mbps"],
        reverse=True
    )

    # Save top 30
    top_servers = servers[:30]

    with open(
        "servers.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            top_servers,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Total servers found:", len(servers))
    print("Total saved:", len(top_servers))
    print("File saved: servers.json")

except Exception as e:
    print("Error:", str(e))
