LEGEND JEWELRY — LIVE GOLD RATE SCREEN

Files:
- screen.html                 Full-screen gold-rate display.
- legend_clean_background.png Legend Jewelry background artwork with blank rate areas.
- server.py                   Flask server that fetches the public Dubai gold-rate page and exposes /api/rates.
- requirements.txt            Python dependencies.
- last_rates.json             Last cached successful rates.
- render.yaml                 Render web-service configuration.

DESIGN:
- Uses the new Legend Jewelry marble artwork.
- Live rate numbers are black.
- 24K / 22K / 21K / 18K rates are updated from /api/rates.
- The screen refreshes rates every 60 seconds.

LOCAL RUN:
1) Install Python 3.
2) pip install -r requirements.txt
3) python server.py
4) Open http://localhost:8787/ in Chrome.
5) Press F11 for full screen.

RENDER:
1) Upload these files to the GitHub repository connected to Render.
2) In Render, create a Web Service from the repository, or use render.yaml.
3) Build Command: pip install -r requirements.txt
4) Start Command: python server.py
5) Render supplies PORT automatically; server.py uses it.

The server keeps the last successful rate in last_rates.json if the source page is
temporarily unavailable. The source page is public and is parsed server-side; it is
not an official API. If the source website changes its HTML, the parser may need an update.
