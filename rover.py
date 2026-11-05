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
selbst. Ohne seconds faehrt er weiter, bis du einen neuen Befehl gibst.

    rover.forward(50)               # vorwaerts mit Tempo 50, faehrt weiter
    rover.forward(50, seconds=2)    # 2 Sekunden vorwaerts, dann Stopp
    rover.backward(40)              # rueckwaerts
    rover.backward(40, seconds=1.5)
    rover.turn_left(50)             # an Ort nach links drehen (Panzerlenkung)
    rover.turn_right(50, seconds=1) # 1 Sekunde nach rechts drehen
    rover.stop()                    # alle Motoren aus

    rover.drive(60, 30)             # linke Seite 60, rechte Seite 30
                                    # -> faehrt eine Linkskurve
    rover.drive(-50, 50)            # negative Zahl = diese Seite rueckwaerts
    rover.drive(60, 30, seconds=2)


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
    )


6. VERKABELUNG (Konvention dieser Library)
------------------------------------------
Auf JEDEM Motortreiber:
    Klemme J1 (bei den LEDs IN1/IN2)  = Motor der LINKEN Seite
    Klemme J5 (bei den LEDs IN3/IN4)  = Motor der RECHTEN Seite
Faehrt bei forward() eine Seite rueckwaerts: entweder die zwei Kabel dieses
Motors an der Klemme tauschen oder invert_left / invert_right = True setzen.


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
"Motortreiber auf Adresse 0x0F antwortet nicht"
    -> Grove-Kabel pruefen, im Terminal  i2cdetect -y 1  ausfuehren und die
       angezeigte Adresse bei addresses=[...] eintragen.
Scan ist sehr langsam / zeigt gar nichts
    -> ein Treiber blockiert den Bus (wie Treiber Nr. 3). Abstecken.
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
        direction = (_M1_FWD if m1 >= 0 else _M1_BWD) | (_M2_FWD if m2 >= 0 else _M2_BWD)
        self._write(_REG_DIRECTION, [direction, 0])
        self._write(_REG_SPEED, [min(abs(int(m1)), 255), min(abs(int(m2)), 255)])


class Rover:
    """Panzer-gelenkter Rover. Siehe User Guide oben in dieser Datei."""

    def __init__(self, addresses=(0x0F,), max_speed=60,
                 invert_left=False, invert_right=False):
        if isinstance(addresses, int):
            addresses = [addresses]
        self.max_speed = max(0, min(100, max_speed))
        self.invert_left = invert_left
        self.invert_right = invert_right
        self._bus = smbus.SMBus(1)
        self._drivers = [_Driver(self._bus, a) for a in addresses]

        atexit.register(self._safe_stop)
        # Auto-Pull-Dienst beendet Programme mit SIGTERM -> trotzdem stoppen
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

        self.stop()

    # --- Grundbefehl ---------------------------------------------------------
    def drive(self, left, right, seconds=None):
        """Linke und rechte Seite einzeln, je -100..100."""
        left = self._scale(left, self.invert_left)
        right = self._scale(right, self.invert_right)
        for d in self._drivers:
            d.set(left, right)
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

    # --- intern --------------------------------------------------------------
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
