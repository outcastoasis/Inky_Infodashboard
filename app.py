from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from weather import fetch_weather, fetch_weather_later
from icon_helper import get_icon_path
import locale
import feedparser
import qrcode

def draw_wrapped_text(draw, text, font, max_width, position, line_spacing=5, fill="black"):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        test_width = draw.textbbox((0, 0), test_line, font=font)[2]
        if test_width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)  # letzte Zeile

    x, y = position
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        line_height = bbox[3] - bbox[1]
        y += line_height + line_spacing

# Sprache für Datum setzen (für Windows)
locale.setlocale(locale.LC_TIME, "deu_deu")  # oder "German_Germany"

# Farben
BLACK = "black"
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

# Display-Größe
resolution = (800, 480)
img = Image.new("RGB", resolution, color="white")
draw = ImageDraw.Draw(img)

# Mittellinie zeichnen
middle_x = resolution[0] // 2
draw.line([(middle_x, 0), (middle_x, resolution[1])], fill="black", width=2)

# Schriftarten
font_big = ImageFont.truetype("static/fonts/DejaVuSans-Bold.ttf", 42)
font_day = ImageFont.truetype("static/fonts/DejaVuSans.ttf", 20)
font_label = ImageFont.truetype("static/fonts/DejaVuSans-Bold.ttf", 26)
font_value = ImageFont.truetype("static/fonts/DejaVuSans.ttf", 22)

# Datum oben links
today = datetime.now()
weekday = today.strftime("%A")  # z. B. "Mittwoch"
day = today.strftime("%d")
month = today.strftime("%B")    # z. B. "Apr"

# Wochentag zeichnen
draw.text((10, 10), weekday, font=font_big, fill=BLACK)

# Breite des Textes exakt berechnen
bbox = draw.textbbox((10, 10), weekday, font=font_big)
text_width = bbox[2] - bbox[0]
x_date = 10 + text_width + 10  # Abstand von 10px

# Tag und Monat übereinander zeichnen
draw.text((x_date, 10), day, font=font_day, fill=BLACK)       # oben
draw.text((x_date, 35), month, font=font_day, fill=BLACK)     # unten

# Wetterdaten laden
weather_now = fetch_weather()
weather_later = fetch_weather_later()

# Funktion: PNG-Icon einfügen
def paste_png(draw_img, png_path, position, size=(80, 80)):
    try:
        icon = Image.open(png_path).convert("RGBA").resize(size)
        draw_img.paste(icon, position, icon)
    except Exception as e:
        print(f"Fehler beim Laden des Icons: {e}")

# Abschnitt: Wetter jetzt
draw.text((10, 120), "Wetter Jetzt", font=font_label, fill=BLACK)
paste_png(img, get_icon_path(weather_now['icon']), (10, 160))
draw.text((110, 160), weather_now["description"], font=font_value, fill=BLACK)
draw.text((110, 190), f"{weather_now['temperature']}°", font=font_value, fill=ORANGE)
draw.text((110, 220), f"{weather_now['wind']} Wind", font=font_value, fill=BLUE)

# Abschnitt: Wetter in 6 Stunden
draw.text((10, 280), "Wetter in 6 Stunden", font=font_label, fill=BLACK)
paste_png(img, get_icon_path(weather_later['icon']), (10, 320))
draw.text((110, 320), weather_later["description"], font=font_value, fill=BLACK)
draw.text((110, 350), f"{weather_later['temperature']}°", font=font_value, fill=ORANGE)
draw.text((110, 380), f"{weather_later['wind']} Wind", font=font_value, fill=BLUE)

# RSS-Feed-URL
rss_url = "https://partner-feeds.beta.20min.ch/rss/20minuten/zentralschweiz"

# Feed parsen
feed = feedparser.parse(rss_url)

# Ersten Artikel extrahieren
first_entry = feed.entries[0]
news_title = first_entry.title

# Schriftarten
font_news_title = ImageFont.truetype("static/fonts/DejaVuSans-Bold.ttf", 26)
font_news_content = ImageFont.truetype("static/fonts/DejaVuSans.ttf", 20)

# Positionen
news_x = middle_x + 20
news_y = 10

draw.text((news_x, news_y), "News", font=font_news_title, fill="black")

# QR-Code aus dem Artikel-Link generieren
qr = qrcode.QRCode(box_size=2, border=1)  # kompakter QR
qr.add_data(first_entry.link)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qr_img = qr_img.resize((70, 70))  # optional skalieren

# QR-Code auf dem Dashboard einfügen
qr_position = (news_x, news_y + 40)
img.paste(qr_img, qr_position)

# Text daneben setzen
text_offset_x = qr_position[0] + 70  # 60 + 10 Abstand
text_offset_y = qr_position[1]
draw_wrapped_text(draw, news_title, font_news_content, max_width=300, position=(text_offset_x, text_offset_y))


# Bild anzeigen/speichern
img.save("dashboard_simulation.png")
img.show()
