from flask import Flask, jsonify, send_file
import requests, re, json
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pathlib import Path

app = Flask(__name__)

SOURCE_URL = "https://dubaicityofgold.com/dubai-gold-rate-today/"
CACHE = Path("last_rates.json")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36"


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    out = {}

    for row in soup.find_all("tr"):
        cells = [" ".join(c.stripped_strings) for c in row.find_all(["th", "td"])]
        text = " ".join(cells)

        for k in ("24K", "22K", "21K", "18K"):
            if k in text and k not in out:
                nums = re.findall(
                    r"\d{2,4}(?:\.\d{1,2})?",
                    text.replace(",", "")
                )
                vals = [float(x) for x in nums if 100 <= float(x) <= 1000]

                if vals:
                    out[k] = vals[-1]

    if len(out) < 4:
        text = " ".join(soup.stripped_strings)

        for k in ("24K", "22K", "21K", "18K"):
            if k in out:
                continue

            m = re.search(
                rf"{k}.{{0,100}}?(\d{{3,4}}\.\d{{1,2}})",
                text,
                re.I
            )

            if m:
                out[k] = float(m.group(1))

    missing = [k for k in ("24K", "22K", "21K", "18K") if k not in out]

    if missing:
        raise RuntimeError(
            "Could not parse official page: " + ",".join(missing)
        )

    return out


def load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text())
        except:
            pass

    return {"rates": {}, "updated_at": None}


@app.get("/")
def screen():
    return send_file("screen.html")


@app.get("/<path:filename>")
def files(filename):
    return send_file(filename)


@app.get("/api/rates")
def rates():
    cached = load_cache()

    try:
        r = requests.get(
            SOURCE_URL,
            headers={
                "User-Agent": UA,
                "Accept-Language": "en-US,en;q=0.9"
            },
            timeout=20
        )

        r.raise_for_status()

        values = parse(r.text)

        payload = {
            "rates": values,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        CACHE.write_text(json.dumps(payload))

        return jsonify(payload)

    except Exception as e:
        if cached.get("rates"):
            cached["source_error"] = str(e)
            return jsonify(cached)

        return jsonify({
            "rates": {},
            "updated_at": None,
            "source_error": str(e)
        }), 503


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Cache-Control"] = "no-store"
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787)