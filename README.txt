LEGEND JEWELRY — LIVE GOLD RATE SCREEN

Files:
- screen.html              The full-screen kiosk display.
- legend_clean_background.png  Your Legend-branded artwork, cleaned for live values.
- server.py                Fetches the Dubai City of Gold page and exposes /api/rates.
- requirements.txt         Python packages.

RUN:
1) Install Python 3 on the computer/mini-PC that will drive the kiosk.
2) Open Terminal/CMD in this folder.
3) pip install -r requirements.txt
4) python server.py
5) Open screen.html in Chrome.
6) Press F11 for full screen.

The screen checks the server every 60 seconds.
The server stores the last successful official rate, so a temporary connection error
does not replace the displayed price with a made-up number.

IMPORTANT:
Dubai City of Gold states that its suggested retail jewellery rate is updated three
times daily (9 AM, 3 PM and 8 PM UAE time). This package reads the public page rather
than claiming an official public API. If the website changes its HTML or blocks the
server, the parser may need adjustment.

For a permanent kiosk, the next step is hosting server.py on a small always-on cloud
server and changing API_URL in screen.html from localhost to that HTTPS address.
