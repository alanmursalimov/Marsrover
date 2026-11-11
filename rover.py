"""
===============================================================================
  rover.py  -  Library fuer den Marsrover (Grove I2C Motor Driver v1.3)
===============================================================================

USER GUIDE
----------

1. EINBINDEN (ganz oben in main.py)
-----------------------------------

    from rover import Rover

    rover = Rover()                 # ein Motortreiber auf Adresse 0x0F

    # Mit zwei Motortreibern (z.B. vorne 0x0F, hinten 0x0E):
    rover = Rover(addresses=[0x0F, 0x0E])


2. FAHREN
---------
Tempo immer von 0 bis 100.
100 = schnellstes ERLAUBTES Tempo (siehe max_speed), nicht volle Akku-Spannung.
seconds ist optional: mit seconds faehrt der Rover so lange und stoppt dann
selbst. Ohne seconds faehrt er weiter, bis ein neuer Befehl kommt ODER
main.py zu Ende ist (dann stoppen die Motoren sofort!). Darum am Schluss
immer seconds=... oder rover.wait(...) benutzen.

    rover.forward(50)               # vorwaerts mit Tempo 50, faehrt weiter
    rover.forward(50, seconds=2)    # 2 Sekunden vorwaerts, dann Stopp
    rover.backward(40)              # rueckwaerts
    rover.backward(40, seconds=1.5)
    rover.turn_left(50)             # an Ort nach links drehen (Panzerlenkung)
    rover.turn_right(50, seconds=1) # 1 Sekunde nach rechts drehen
    rover.stop()                    # alle Motoren aus

    rover.drive(60, 30)             # linke Seite 60, rechte Seite 30
                                    # -> faehrt eine Rechtskurve
    rover.drive(-50, 50)            # negative Zahl = diese Seite rueckwaerts
    rover.drive(60, 30, seconds=2)


2b. EINZELNE MOTOREN
--------------------
Du waehlst Treiber (Adresse) und Klemme ("J1" oder "J5") selber.
Die anderen Motoren bleiben dabei, wie sie sind.

    m = rover.motor(0x0F, "J1")     # Motor an Treiber 0x0F, Klemme J1
    m.speed(50)                     # vorwaerts mit Tempo 50, laeuft weiter
    m.speed(-50, seconds=2)         # 2 Sekunden rueckwaerts, dann Stopp
    m.stop()                        # nur diesen Motor aus

    hinten_rechts = rover.motor(0x0E, "J5", invert=True)  # dreht falsch herum

Der Treiber muss bei Rover(...) bekannt sein (addresses oder left/right).


3. WARTEN
---------

    rover.wait(1.5)                 # 1.5 Sekunden warten (Motoren laufen weiter!)


4. MIT DER TASTATUR STEUERN (WASD)
----------------------------------

    rover.wasd()                    # W/A/S/D fahren, Leertaste = Stopp,
                                    # Q = beenden
    rover.wasd(speed=40)            # langsamer

Funktioniert nur, wenn du main.py selbst im Terminal startest:
    sudo systemctl stop marsrover
    python3 ~/Marsrover/main.py
Der Auto-Pull-Dienst hat keine Tastatur, dort wird wasd() uebersprungen.


5. EINSTELLUNGEN BEIM ERSTELLEN
-------------------------------

    rover = Rover(
        addresses=[0x0F],     # I2C-Adressen der Motortreiber (DIP-Schalter)
        max_speed=60,         # Obergrenze in % der Akkuspannung.
                              # DG01D-Motoren sind fuer 4.5 V gebaut:
                              # bei 7.4-V-Akku nicht ueber ca. 60 gehen!
        invert_left=False,    # True, wenn die linke Seite falsch herum dreht
        invert_right=False,   # True, wenn die rechte Seite falsch herum dreht
        swap_sides=False,     # True = J1 ist RECHTS und J5 ist LINKS
        grovepi_address=0x04, # I2C-Adresse des GrovePi (Standard 0x04)
    )

    # Selber festlegen, welcher Motor zu welcher Seite gehoert
    # (Treiber-Adresse, Klemme). Dann braucht es addresses nicht:
    rover = Rover(
        left=[(0x0F, "J1"), (0x0E, "J1")],
        right=[(0x0F, "J5"), (0x0E, "J5")],
    )
    # Ohne left/right gilt die Konvention unten (J1 links, J5 rechts).

    # Nur Sensoren/Servos testen, ohne Motortreiber:
    rover = Rover(addresses=[])


6. VERKABELUNG (Konvention dieser Library)
------------------------------------------
Auf JEDEM Motortreiber:
    Klemme J1 (bei den LEDs IN1/IN2)  = Motor der LINKEN Seite
    Klemme J5 (bei den LEDs IN3/IN4)  = Motor der RECHTEN Seite
Faehrt bei forward() eine Seite rueckwaerts: entweder die zwei Kabel dieses
Motors an der Klemme tauschen oder invert_left / invert_right = True setzen.
Andersrum verkabelt (J1 rechts, J5 links)? -> swap_sides=True.


6b. SENSOREN UND AUSGAENGE AM GROVEPI (Port selber waehlen)
-----------------------------------------------------------
Du entscheidest, was wo eingesteckt ist. Den Port gibst du als Text an.
    Analoge Ports:  "A0", "A1", "A2"
    Digitale Ports: "D2" bis "D8"
Jeder Port darf nur einmal benutzt werden (sonst kommt eine Fehlermeldung).
Braucht die GrovePi-Library auf dem Pi (import grovepi).

    licht = rover.analog("A1")        # z.B. Lichtsensor an A1
    print(licht.read())               # Rohwert 0-1023

    abstand = rover.ultrasonic("D4")  # Ultraschall-Sensor an D4
    print(abstand.read())             # Abstand in cm

    taster = rover.digital_in("D3")   # z.B. Taster an D3
    print(taster.read())              # 0 oder 1

    led = rover.digital_out("D5")     # z.B. LED an D5
    led.on()
    led.off()


6c. SERVOS (Grove 16-Kanal PWM-Treiber, PCA9685)
------------------------------------------------
Adresse und Kanal (0-15) waehlst du selber. Die Adresse siehst du mit
i2cdetect -y 1 (Seeed-Standard laut Datenblatt: 0x7F - nachpruefen!).

    servo = rover.servo(channel=0, address=0x7F)
    servo.angle(90)                   # auf 90 Grad fahren (0-180)
    servo.off()                       # Servo stromlos (haelt nicht mehr)

Jeder Servo hat einen etwas anderen Pulsbereich. Standard ist vorsichtig
1000-2000 us (dann dreht er evtl. weniger als 180 Grad). Fuer mehr Weg
langsam erweitern, z.B.:
    servo = rover.servo(channel=1, address=0x7F, min_us=600, max_us=2400)
Brummt der Servo am Ende oder drueckt gegen den Anschlag -> Bereich
wieder kleiner machen!


7. BEISPIEL main.py
-------------------

    from rover import Rover

    rover = Rover()
    rover.forward(50, seconds=2)
    rover.turn_left(50, seconds=1)
    rover.backward(50, seconds=2)
    rover.stop()


8. SICHERHEIT
-------------
- Wenn main.py endet, abstuerzt, mit Ctrl+C abgebrochen oder vom
  Auto-Pull-Dienst neu gestartet wird, stoppen die Motoren automatisch.
- Beim Testen den Rover hochstellen (Raeder in der Luft)!


9. FEHLER
---------
Motoren drehen nicht (Treiber antwortet aber)
    -> motortest.py starten (testet den Treiber ohne diese Library):
           sudo systemctl stop marsrover
           python3 ~/Marsrover/motortest.py
       Akku an der Strom-Klemme des Treibers? Leuchten die LEDs IN1-IN4?
       Tempo 50 ist bei max_speed=60 nur 30 % der Akkuspannung - evtl.
       zu wenig zum Anlaufen.
"Motortreiber auf Adresse 0x0F antwortet nicht"
    -> Grove-Kabel pruefen, im Terminal  i2cdetect -y 1  ausfuehren und die
       angezeigte Adresse bei addresses=[...] eintragen.
Scan ist sehr langsam / zeigt gar nichts
    -> ein Treiber blockiert den Bus (wie Treiber Nr. 3). Abstecken.
"GrovePi-Library fehlt"
    -> die GrovePi-Software von Dexter Industries auf dem Pi installieren.
"Port ... ist schon belegt"
    -> du hast den gleichen Port zweimal benutzt.
===============================================================================
"""

import atexit
import signal
import sys
import time

import smbus

# --- Register des Grove I2C Motor Driver v1.3 --------------------------------
_REG_SPEED = 0x82       # [Tempo Motor1, Tempo Motor2], je 0-255
_REG_DIRECTION = 0xAA   # [Richtungs-Bits, 0]
_DELAY = 0.02           # Pause nach jedem Befehl (der Chip ist langsam)

# Richtungs-Bits: Motor1 = Bits 0-1, Motor2 = Bits 2-3
_M1_FWD, _M1_BWD = 0b0010, 0b0001
_M2_FWD, _M2_BWD = 0b1000, 0b0100


class _Driver:
    """Ein einzelnes Motortreiber-Board (2 Motoren)."""

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.speeds = [0, 0]   # aktuelles Tempo J1, J5 (-255..255)
        try:
            self.bus.write_quick(address)
        except OSError:
            raise RuntimeError(
                f"Motortreiber auf Adresse {address:#04x} antwortet nicht. "
                "Kabel pruefen und 'i2cdetect -y 1' ausfuehren."
            ) from None

    def _write(self, register, data):
        for attempt in range(3):
            try:
                self.bus.write_i2c_block_data(self.address, register, data)
                time.sleep(_DELAY)
                return
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(0.05)

    def set(self, m1, m2):
        """m1, m2: -255..255 (negativ = rueckwaerts)."""
        self.speeds = [m1, m2]
        direction = (_M1_FWD if m1 >= 0 else _M1_BWD) | (_M2_FWD if m2 >= 0 else _M2_BWD)
        self._write(_REG_DIRECTION, [direction, 0])
        self._write(_REG_SPEED, [min(abs(int(m1)), 255), min(abs(int(m2)), 255)])

    def apply(self):
        """Gespeicherte Tempi (self.speeds) an das Board schicken."""
        self.set(*self.speeds)


def _parse_address(a):
    """0x0F, 15 oder "0x0F" -> 15."""
    if isinstance(a, str):
        a = int(a, 0)
    return int(a)


def _parse_terminal(t):
    """"J1"/1 -> 0 (Motor 1),  "J5"/2 -> 1 (Motor 2)."""
    text = str(t).strip().upper()
    if text in ("J1", "1", "M1"):
        return 0
    if text in ("J5", "2", "M2"):
        return 1
    raise ValueError(f"Klemme {t!r} gibt es nicht. Erlaubt: \"J1\" oder \"J5\".")


class Motor:
    """Ein einzelner Motor (Treiber-Adresse + Klemme). Erstellen mit rover.motor(...)."""

    def __init__(self, rover, driver, channel, invert):
        self._rover = rover
        self._driver = driver
        self._channel = channel
        self.invert = invert
        self.address = driver.address
        self.terminal = ("J1", "J5")[channel]

    def speed(self, value, seconds=None):
        """Tempo -100..100 (negativ = rueckwaerts). Andere Motoren bleiben, wie sie sind."""
        self._driver.speeds[self._channel] = self._rover._scale(value, self.invert)
        self._driver.apply()
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        self._driver.speeds[self._channel] = 0
        self._driver.apply()

    def __repr__(self):
        return f"Motor({self.address:#04x}, {self.terminal})"


# --- PCA9685 (Grove 16-Kanal PWM-Treiber) fuer Servos ------------------------
class _PCA9685:
    def __init__(self, bus, address, freq=50):
        self.bus = bus
        self.address = address
        self.freq = freq
        try:
            bus.write_quick(address)
        except OSError:
            raise RuntimeError(
                f"PWM-Treiber auf Adresse {address:#04x} antwortet nicht. "
                "Kabel pruefen und 'i2cdetect -y 1' ausfuehren."
            ) from None
        prescale = round(25_000_000 / (4096 * freq)) - 1
        bus.write_byte_data(address, 0x00, 0x10)      # schlafen (noetig fuer Prescale)
        bus.write_byte_data(address, 0xFE, prescale)  # 50 Hz fuer Servos
        # aufwachen + Auto-Increment; ALLCALL aus, damit er nicht auch auf
        # 0x70 reagiert (dort sitzt standardmaessig der I2C-Hub TCA9548A)
        bus.write_byte_data(address, 0x00, 0x20)
        time.sleep(0.005)

    def pulse(self, channel, us):
        off = round(us * 4096 * self.freq / 1_000_000)
        self.bus.write_i2c_block_data(self.address, 0x06 + 4 * channel,
                                      [0, 0, off & 0xFF, off >> 8])

    def off(self, channel):
        # Bit "FULL OFF" setzen -> kein Signal mehr
        self.bus.write_i2c_block_data(self.address, 0x06 + 4 * channel, [0, 0, 0, 0x10])


class Servo:
    """Ein Servo an einem Kanal des PWM-Treibers. Erstellen mit rover.servo(...)."""

    def __init__(self, board, channel, min_us, max_us, max_angle):
        self._board = board
        self.channel = channel
        self.min_us = min_us
        self.max_us = max_us
        self.max_angle = max_angle

    def angle(self, degrees):
        degrees = max(0, min(self.max_angle, degrees))
        us = self.min_us + (self.max_us - self.min_us) * degrees / self.max_angle
        self._board.pulse(self.channel, us)

    def off(self):
        self._board.off(self.channel)


# --- Sensoren / Ausgaenge am GrovePi -----------------------------------------
class _GrovePort:
    def __init__(self, gp, pin, name):
        self._gp = gp
        self.pin = pin
        self.port = name


class AnalogSensor(_GrovePort):
    def read(self):
        """Rohwert 0-1023."""
        return self._gp.analogRead(self.pin)


class DigitalIn(_GrovePort):
    def read(self):
        """0 oder 1."""
        return self._gp.digitalRead(self.pin)


class DigitalOut(_GrovePort):
    def set(self, value):
        self._gp.digitalWrite(self.pin, 1 if value else 0)

    def on(self):
        self.set(1)

    def off(self):
        self.set(0)


class Ultrasonic(_GrovePort):
    def read(self):
        """Abstand in cm."""
        return self._gp.ultrasonicRead(self.pin)


class Rover:
    """Panzer-gelenkter Rover. Siehe User Guide oben in dieser Datei."""

    def __init__(self, addresses=None, max_speed=80,
                 invert_left=False, invert_right=False,
                 swap_sides=False, grovepi_address=0x04,
                 left=None, right=None):
        # left/right: welche Motoren zu welcher Seite gehoeren,
        # z.B. left=[(0x0F, "J1"), (0x0E, "J1")]
        left = [(_parse_address(a), _parse_terminal(t)) for a, t in (left or [])]
        right = [(_parse_address(a), _parse_terminal(t)) for a, t in (right or [])]
        if addresses is None:
            addresses = sorted({a for a, _ in left + right}) or [0x0F]
        if isinstance(addresses, (int, str)):
            addresses = [addresses]
        addresses = [_parse_address(a) for a in addresses]
        for a, _ in left + right:
            if a not in addresses:
                addresses.append(a)
        self.max_speed = max(0, min(100, max_speed))
        self.invert_left = invert_left
        self.invert_right = invert_right
        self.swap_sides = swap_sides
        self.grovepi_address = grovepi_address
        self._grovepi = None
        self._pwm_boards = {}
        self._used = {}            # belegte Ports -> wofuer
        self._bus = smbus.SMBus(1)
        self._drivers = [_Driver(self._bus, a) for a in addresses]
        by_addr = {d.address: d for d in self._drivers}
        if left or right:
            self._left = [(by_addr[a], ch) for a, ch in left]
            self._right = [(by_addr[a], ch) for a, ch in right]
        else:
            # Standard: auf jedem Treiber J1 = links, J5 = rechts
            l_ch, r_ch = (1, 0) if swap_sides else (0, 1)
            self._left = [(d, l_ch) for d in self._drivers]
            self._right = [(d, r_ch) for d in self._drivers]

        atexit.register(self._safe_stop)
        # Auto-Pull-Dienst beendet Programme mit SIGTERM -> trotzdem stoppen
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

        self.stop()

    # --- Grundbefehl ---------------------------------------------------------
    def drive(self, left, right, seconds=None):
        """Linke und rechte Seite einzeln, je -100..100."""
        left = self._scale(left, self.invert_left)
        right = self._scale(right, self.invert_right)
        for d, ch in self._left:
            d.speeds[ch] = left
        for d, ch in self._right:
            d.speeds[ch] = right
        for d in self._drivers:
            d.apply()
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    # --- Bequeme Befehle -----------------------------------------------------
    def forward(self, speed=50, seconds=None):
        self.drive(speed, speed, seconds)

    def backward(self, speed=50, seconds=None):
        self.drive(-speed, -speed, seconds)

    def turn_left(self, speed=50, seconds=None):
        self.drive(-speed, speed, seconds)

    def turn_right(self, speed=50, seconds=None):
        self.drive(speed, -speed, seconds)

    def stop(self):
        for d in self._drivers:
            d.set(0, 0)

    def wait(self, seconds):
        time.sleep(seconds)

    # --- Tastatursteuerung ---------------------------------------------------
    def wasd(self, speed=50):
        """W/A/S/D fahren, Leertaste = Stopp, Q = beenden."""
        if not sys.stdin.isatty():
            print("wasd(): keine Tastatur (laeuft im Dienst?) -> uebersprungen")
            return
        import termios
        import tty

        keys = {
            "w": lambda: self.forward(speed),
            "s": lambda: self.backward(speed),
            "a": lambda: self.turn_left(speed),
            "d": lambda: self.turn_right(speed),
            " ": self.stop,
        }
        print("W/A/S/D = fahren, Leertaste = Stopp, Q = beenden")
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                key = sys.stdin.read(1).lower()
                if key == "q":
                    break
                if key in keys:
                    keys[key]()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            self.stop()

    # --- Einzelne Motoren ----------------------------------------------------
    def motor(self, address=0x0F, terminal="J1", invert=False):
        """Ein einzelner Motor, z.B. rover.motor(0x0F, "J5").speed(50, seconds=2)."""
        address = _parse_address(address)
        for d in self._drivers:
            if d.address == address:
                return Motor(self, d, _parse_terminal(terminal), invert)
        raise ValueError(
            f"Kein Motortreiber auf {address:#04x}. Bekannt: "
            + ", ".join(f"{d.address:#04x}" for d in self._drivers)
            + " -> Adresse bei Rover(addresses=[...]) eintragen."
        )

    # --- Sensoren, Ausgaenge, Servos (Port selber waehlen) --------------------
    def analog(self, port):
        """Analoger Sensor an A0-A2, z.B. rover.analog("A1")."""
        return AnalogSensor(*self._grove_port(port, "A", "analog"))

    def digital_in(self, port):
        """Digitaler Eingang an D2-D8, z.B. rover.digital_in("D3")."""
        gp, pin, name = self._grove_port(port, "D", "digital_in")
        gp.pinMode(pin, "INPUT")
        return DigitalIn(gp, pin, name)

    def digital_out(self, port):
        """Digitaler Ausgang an D2-D8, z.B. rover.digital_out("D5")."""
        gp, pin, name = self._grove_port(port, "D", "digital_out")
        gp.pinMode(pin, "OUTPUT")
        return DigitalOut(gp, pin, name)

    def ultrasonic(self, port):
        """Grove Ultraschall-Sensor an D2-D8, z.B. rover.ultrasonic("D4")."""
        return Ultrasonic(*self._grove_port(port, "D", "ultrasonic"))

    def servo(self, channel, address=0x7F, min_us=1000, max_us=2000, max_angle=180):
        """Servo an Kanal 0-15 des PWM-Treibers mit I2C-Adresse address."""
        if not 0 <= channel <= 15:
            raise ValueError(f"Servo-Kanal {channel} gibt es nicht. Erlaubt: 0-15.")
        self._claim(f"PWM {address:#04x} Kanal {channel}", "servo")
        if address not in self._pwm_boards:
            self._pwm_boards[address] = _PCA9685(self._bus, address)
        return Servo(self._pwm_boards[address], channel, min_us, max_us, max_angle)

    # --- intern --------------------------------------------------------------
    def _claim(self, name, what):
        if name in self._used:
            raise ValueError(f"Port {name} ist schon belegt ({self._used[name]}).")
        self._used[name] = what

    def _grove_port(self, port, kind, what):
        allowed = {"A": range(0, 3), "D": range(2, 9)}[kind]
        text = str(port).strip().upper()
        if text.isdigit():
            text = kind + text
        if text[:1] != kind or not text[1:].isdigit() or int(text[1:]) not in allowed:
            raise ValueError(
                f"Port {port!r} passt nicht fuer {what}. Erlaubt: "
                + ", ".join(f"{kind}{n}" for n in allowed)
            )
        self._claim(text, what)
        if self._grovepi is None:
            try:
                import grovepi
            except ImportError:
                raise RuntimeError(
                    "GrovePi-Library fehlt (import grovepi). "
                    "GrovePi-Software von Dexter Industries auf dem Pi installieren."
                ) from None
            grovepi.address = self.grovepi_address
            self._grovepi = grovepi
        return self._grovepi, int(text[1:]), text

    def _scale(self, value, invert):
        value = max(-100, min(100, value))
        if invert:
            value = -value
        return value * self.max_speed / 100 * 255 / 100

    def _safe_stop(self):
        try:
            self.stop()
        except Exception:
            pass
