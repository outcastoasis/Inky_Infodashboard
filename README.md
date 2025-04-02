# Inky Infodashboard

Ein minimalistisches E-Ink-Dashboard für das **Inky Impression 7.3"**, simuliert am PC mit Pillow.

## Funktionen

- Anzeige von:
  - aktuellem Datum (mit deutschem Wochentag)
  - Wetter jetzt und in 6 Stunden (inkl. Symbolen)
  - aktuellen News aus dem 20min-RSS-Feed (Zentralschweiz)
  - QR-Code zum News-Artikel
- Vorschau lokal als PNG (`dashboard_simulation.png`)
- Darstellung vollständig mit Python (kein Browser nötig)

## Voraussetzungen

- Python 3.8+
- Bibliotheken:
  ```bash
  pip install pillow feedparser qrcode
  ```

## Struktur

```text
Inky_Infodashboard/
│
├── app.py                 # Hauptprogramm (generiert Dashboard)
├── weather.py             # Wetterdaten über OpenWeatherMap
├── config.py              # API-Schlüssel & Standort
├── icon_helper.py         # Pfade zu lokalen Wetter-Icons
├── icons_png/             # Lokale Wetter-Symbole (PNG)
├── static/fonts/          # Schriftarten (z. B. DejaVuSans)
├── .gitignore             # z. B. .env, __pycache__
└── dashboard_simulation.png
```

## Wetter-API

Du benötigst einen kostenlosen API-Key von [https://openweathermap.org](https://openweathermap.org)  
→ In `config.py` eintragen.

## RSS-Feed

Die News werden aus diesem RSS-Feed geladen:  
[20min Zentralschweiz](https://partner-feeds.beta.20min.ch/rss/20minuten/zentralschweiz)

## Vorschau

> Beispielbild folgt

---

Wenn du das Projekt später auf den Raspberry Pi bringst, kannst du die Ausgabe direkt auf dem E-Ink-Display anzeigen.
