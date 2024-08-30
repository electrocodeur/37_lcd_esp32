from machine import Pin
import time

class LCD:
    def __init__(self, rs, e, d4, d5, d6, d7):
        self.rs = Pin(rs, Pin.OUT)
        self.e = Pin(e, Pin.OUT)
        self.d4 = Pin(d4, Pin.OUT)
        self.d5 = Pin(d5, Pin.OUT)
        self.d6 = Pin(d6, Pin.OUT)
        self.d7 = Pin(d7, Pin.OUT)

        self.init_lcd()

    def init_lcd(self):
        time.sleep(0.05)  # wait for more than 40ms after VCC rises to 2.7V
        self.send_command(0x33)  # initialize
        self.send_command(0x32)  # initialize
        self.send_command(0x28)  # 4 bits mode, 2 line, 5x7 matrix
        self.send_command(0x0C)  # display on, cursor off
        self.send_command(0x06)  # increment cursor
        self.send_command(0x01)  # clear display
        time.sleep(0.002)  # command delay

    def send_command(self, command):
        self.rs.value(0)  # command mode
        self.send_byte(command)

    def send_byte(self, byte):
        self.d4.value((byte >> 4) & 0x01)
        self.d5.value((byte >> 5) & 0x01)
        self.d6.value((byte >> 6) & 0x01)
        self.d7.value((byte >> 7) & 0x01)

        self.e.value(1)
        time.sleep(0.001)
        self.e.value(0)

        self.d4.value(byte & 0x01)
        self.d5.value((byte >> 1) & 0x01)
        self.d6.value((byte >> 2) & 0x01)
        self.d7.value((byte >> 3) & 0x01)

        self.e.value(1)
        time.sleep(0.001)
        self.e.value(0)

    def display_string(self, string):
        self.rs.value(1)  # data mode
        for char in string:
            self.send_byte(ord(char))

    def clear(self):
        self.send_command(0x01)  # clear display
        time.sleep(0.002)  # command delay

# Configuration des broches
lcd = LCD(rs=12, e=14, d4=27, d5=26, d6=25, d7=33)

while True:
    # Utilisation
    lcd.display_string("Hello World!")
    time.sleep(2)
    lcd.clear()
    lcd.display_string("ESP32 LCD")
    time.sleep(2)
    lcd.clear()
    lcd.display_string("ElectroCodeur")
    time.sleep(2)
    lcd.clear()