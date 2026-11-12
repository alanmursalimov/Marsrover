"""Erzeugt docs/Marsrover_Anleitung.pdf (Kurzanleitung fuer rover.py).

Neu erzeugen (auf dem Laptop, braucht reportlab):
    pip install reportlab
    python3 docs/make_anleitung.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

OUT = Path(__file__).with_name("Marsrover_Anleitung.pdf")

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=13)
small = ParagraphStyle("small", parent=body, fontSize=9, leading=11.5)
title = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22, leading=26)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=16,
                    spaceBefore=10, spaceAfter=4)
code_style = ParagraphStyle("code", fontName="Courier", fontSize=9, leading=11.5)
cmd = ParagraphStyle("cmd", fontName="Courier-Bold", fontSize=9, leading=11.5)

GREY = colors.HexColor("#f2f2f2")
LINE = colors.HexColor("#bbbbbb")
HEAD = colors.HexColor("#333333")


def c(text):
    """Code im Fliesstext."""
    return f'<font name="Courier">{text}</font>'


def code(text):
    t = Table([[Preformatted(text.strip("\n"), code_style)]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def table(rows, left=70):
    data = [[Paragraph('<font color="white"><b>Befehl</b></font>', body),
             Paragraph('<font color="white"><b>Was passiert</b></font>', body)]]
    for a, b in rows:
        data.append([Paragraph(a, cmd), Paragraph(b, small)])
    t = Table(data, colWidths=[left * mm, (170 - left) * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GREY]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def section(heading, *flowables):
    return KeepTogether([Paragraph(heading, h2), *flowables])


story = [
    Paragraph("Marsrover – Befehle", title),
    Spacer(1, 2 * mm),
    Paragraph(f"Kurzanleitung für die Library {c('rover.py')} – Motoren, Sensoren und Servos", body),
    Spacer(1, 2 * mm),

    section("1. Start: immer oben in main.py", code("""
from rover import Rover
rover = Rover()
""")),

    section(
        "2. Fahren",
        Paragraph(f"Tempo immer <b>0 bis 100</b>. Mit {c('seconds=')} fährt der Rover so lange und "
                  f"stoppt dann selbst. Ohne {c('seconds')} fährt er weiter, bis ein neuer Befehl kommt "
                  f"oder main.py zu Ende ist.", body),
        Spacer(1, 2 * mm),
        table([
            ("rover.forward(50)", "vorwärts, fährt weiter"),
            ("rover.forward(50, seconds=2)", "2 Sekunden vorwärts, dann Stopp"),
            ("rover.backward(50)", "rückwärts"),
            ("rover.backward(50, seconds=2)", "2 Sekunden rückwärts, dann Stopp"),
            ("rover.turn_left(50)", "an Ort nach links drehen"),
            ("rover.turn_right(50)", "an Ort nach rechts drehen"),
            ("rover.turn_left(50, seconds=1)", "1 Sekunde links drehen, dann Stopp"),
            ("rover.drive(60, 30)", "links 60, rechts 30 -&gt; Kurve nach rechts"),
            ("rover.drive(-50, 50)", "negative Zahl = diese Seite rückwärts"),
            ("rover.drive(60, 30, seconds=2)", "Kurve 2 Sekunden lang, dann Stopp"),
            ("rover.stop()", "alle Motoren aus"),
            ("rover.wait(1.5)", "1.5 Sekunden warten – Motoren laufen weiter!"),
        ]),
        Spacer(1, 3 * mm),
        Paragraph("<b>Einzelne Motoren</b> – Treiber-Adresse und Klemme (J1 oder J5) selber wählen. "
                  "Die anderen Motoren bleiben, wie sie sind.", body),
        Spacer(1, 1 * mm),
        table([
            ('m = rover.motor(0x0F, "J1")', "Motor an Treiber 0x0F, Klemme J1"),
            ("m.speed(50)", "vorwärts, läuft weiter"),
            ("m.speed(-50, seconds=2)", "2 Sekunden rückwärts, dann Stopp"),
            ("m.stop()", "nur diesen Motor aus"),
            ('rover.motor(0x0E, "J5", invert=True)', "Motor, der falsch herum dreht"),
        ], left=78),
    ),

    section(
        "3. Mit der Tastatur steuern",
        table([
            ("rover.wasd()", "W / A / S / D fahren, Leertaste = Stopp, Q = beenden"),
            ("rover.wasd(speed=40)", "dasselbe, langsamer"),
        ]),
        Spacer(1, 2 * mm),
        Paragraph("Geht nur, wenn du main.py selbst im Terminal startest "
                  "(der Auto-Pull-Dienst hat keine Tastatur):", body),
        Spacer(1, 1 * mm),
        code("""
sudo systemctl stop marsrover
python3 ~/Marsrover/main.py
"""),
    ),

    section(
        "4. Sensoren und Ausgänge am GrovePi – Port selber wählen",
        Paragraph("Du entscheidest, was wo eingesteckt ist. Analoge Ports: <b>A0, A1, A2</b>. "
                  "Digitale Ports: <b>D2 bis D8</b>. Jeder Port darf nur einmal benutzt werden.", body),
        Spacer(1, 2 * mm),
        table([
            ('licht = rover.analog("A1")', "analoger Sensor (z.B. Licht) an A1"),
            ("licht.read()", "Rohwert 0 bis 1023"),
            ('abstand = rover.ultrasonic("D4")', "Ultraschall-Sensor an D4"),
            ("abstand.read()", "Abstand in cm"),
            ('taster = rover.digital_in("D3")', "digitaler Eingang (z.B. Taster) an D3"),
            ("taster.read()", "0 oder 1"),
            ('led = rover.digital_out("D5")', "digitaler Ausgang (z.B. LED) an D5"),
            ("led.on() / led.off()", "einschalten / ausschalten"),
        ], left=78),
        Spacer(1, 1 * mm),
        Paragraph(f"Braucht die GrovePi-Library (Dexter Industries) auf dem Pi. "
                  f"Fahren geht auch ohne sie.", small),
    ),

    section(
        "5. Servos (Grove 16-Kanal PWM-Treiber)",
        Paragraph(f"Kanal <b>0 bis 15</b> und I2C-Adresse wählst du selber. "
                  f"Adresse mit {c('i2cdetect -y -a 1')} prüfen (Seeed-Standard: 0x7F). "
                  f"Hängt der Treiber am I2C-Hub, sucht {c('rover.servo()')} den Hub-Port selber.", body),
        Spacer(1, 2 * mm),
        table([
            ("servo = rover.servo(channel=0, address=0x7F)", "Servo an Kanal 0"),
            ("servo.angle(90)", "auf 90 Grad fahren (0 bis 180)"),
            ("servo.off()", "Servo stromlos – hält nicht mehr"),
            ("rover.servo(channel=1, address=0x7F, min_us=600, max_us=2400)",
             "grösserer Pulsbereich = mehr Weg"),
            ("rover.servo(channel=0, address=0x7F, hub_port=3)", "Hub-Port fest einstellen (None = ohne Hub)"),
        ], left=95),
        Spacer(1, 1 * mm),
        Paragraph("Standard ist vorsichtig 1000–2000 µs (dreht evtl. weniger als 180 Grad). "
                  "Bereich langsam erweitern. Brummt der Servo am Ende oder drückt gegen den "
                  "Anschlag -&gt; Bereich wieder kleiner machen!", small),
    ),

    section(
        "6. Einstellungen",
        table([
            ("Rover(addresses=[0x0F, 0x0E])", f"zwei Motortreiber (Adressen mit {c('i2cdetect -y 1')} prüfen)"),
            ("Rover(addresses=[])", "ohne Motortreiber – nur Sensoren/Servos testen"),
            ("Rover(max_speed=60)", "Höchsttempo in % der Akkuspannung. DG01D sind "
                                    "4.5-V-Motoren: bei 7.4 V nicht über ca. 60"),
            ("Rover(invert_right=True)", "rechte Seite dreht falsch herum "
                                         "(Rover dreht bei forward() an Ort)"),
            ("Rover(invert_left=True)", "linke Seite dreht falsch herum"),
            ("Rover(swap_sides=True)", "Motoren andersrum eingesteckt: J1 = rechts, J5 = links"),
            ("Rover(grovepi_address=0x04)", "I2C-Adresse des GrovePi (Standard 0x04)"),
            ('Rover(left=[(0x0F, "J1"), (0x0E, "J1")],<br/>right=[(0x0F, "J5"), (0x0E, "J5")])',
             "selber festlegen, welche Motoren links und rechts sind (Adresse, Klemme). "
             "Ersetzt addresses und swap_sides"),
        ]),
        Spacer(1, 1 * mm),
        Paragraph("Mehrere Einstellungen gehen zusammen, z.B. "
                  + c("Rover(addresses=[0x0F], max_speed=50, swap_sides=True)"), small),
    ),

    section("7. Beispiel main.py", code("""
from rover import Rover

rover = Rover()
abstand = rover.ultrasonic("D4")
arm = rover.servo(channel=0, address=0x7F)

arm.angle(90)
rover.forward(40)                  # losfahren
while abstand.read() > 20:         # bis ein Hindernis naeher als 20 cm ist
    rover.wait(0.1)
rover.stop()
rover.turn_left(50, seconds=1)
""")),

    section(
        "8. Terminal-Befehle auf dem Pi",
        table([
            ("python3 ~/Marsrover/main.py", "Code von Hand starten (Ctrl+C = abbrechen)"),
            ("sudo systemctl stop marsrover", "Auto-Pull + Auto-Start pausieren"),
            ("sudo systemctl start marsrover", "Auto-Pull wieder einschalten"),
            ("journalctl -u marsrover -f", "Ausgabe vom laufenden Code ansehen"),
            ("i2cdetect -y -a 1", "zeigt alle I2C-Geräte (Motortreiber = 0f, GrovePi = 04). "
                                  "Ohne -a fehlen 0x00–0x07 und 0x78–0x7F"),
            ("python3 ~/Marsrover/motortest.py", "Motortreiber ohne rover.py testen "
                                                 "(z.B. motortest.py 0x0F J5 70)"),
        ]),
    ),

    section(
        "9. Gut zu wissen",
        *[Paragraph("• " + t, body) for t in [
            f"Verkabelung: Klemme <b>J1</b> (bei IN1/IN2) = linker Motor, "
            f"Klemme <b>J5</b> (bei IN3/IN4) = rechter Motor (oder {c('swap_sides=True')}).",
            "Motoren stoppen automatisch, wenn main.py endet, abstürzt oder abgebrochen wird. "
            "Servos und LEDs bleiben, wie sie sind.",
            "Nie Code direkt auf dem Pi ändern – der nächste Push überschreibt ihn.",
            "Beim Testen Rover hochstellen (Räder in der Luft)!",
            f"Fehler „antwortet nicht“ -&gt; Kabel prüfen, {c('i2cdetect -y 1')}. Treiber Nr. 3 ist defekt.",
            "Motoren drehen nicht, Treiber antwortet -&gt; Akku an der Strom-Klemme des Treibers? "
            "LEDs IN1–IN4 an? motortest.py probieren. Tempo 50 bei max_speed=60 ist nur 30 % "
            "der Akkuspannung.",
            "Fehler „Port ... ist schon belegt“ -&gt; gleichen Port zweimal benutzt.",
            "Fehler „GrovePi-Library fehlt“ -&gt; GrovePi-Software auf dem Pi installieren.",
        ]],
    ),
]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                        topMargin=16 * mm, bottomMargin=16 * mm,
                        title="Marsrover – Befehle", author="Marsrover-Team")
doc.build(story)
print("geschrieben:", OUT)
