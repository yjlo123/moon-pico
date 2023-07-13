import ntptime
import time
from machine import Pin, PWM

from connect import do_connect
from lcd import LCD_1inch14
from menu import Menu

BL = 13
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(32768) #max 65535

LCD = LCD_1inch14()
key_a = Pin(15,Pin.IN,Pin.PULL_UP)
key_b = Pin(17,Pin.IN,Pin.PULL_UP)
key_u = Pin(2 ,Pin.IN,Pin.PULL_UP) # UP
key_c = Pin(3 ,Pin.IN,Pin.PULL_UP) # CENTRL
key_l = Pin(16 ,Pin.IN,Pin.PULL_UP) # LEFT
key_d = Pin(18 ,Pin.IN,Pin.PULL_UP) # DOWN
key_r = Pin(20 ,Pin.IN,Pin.PULL_UP) # RIGHT

class StartingLogger():
    def __init__(self, lcd):
        self.row = 0
        self.line_height = 10
        self.lcd = lcd
    
    def log(self, msg):
        self.lcd.text(msg, 4, self.line_height * self.row, self.lcd.white)
        self.row += 1
        self.lcd.show()

logger = StartingLogger(LCD)

logger.log("Connecting to WiFi")
ip = do_connect()
if not ip:
    logger.log("Failed to connect to WiFi")
else:
    logger.log("IP: " + ip)
    
    retry_sync_times = 3
    while retry_sync_times > 0:
        try:
            logger.log("Syncing time")
            ntptime.settime()
            break
        except Exception as e:
            print(e)
            logger.log("Failed to sync time, retrying")
            time.sleep(0.5)
            retry_sync_times -= 1

logger.log("Welcome")
time.sleep(0.5)

menu = Menu(LCD, (key_a, key_b, key_c, key_u, key_d, key_l, key_r), {
    'ip': ip
})
menu.show()

'''
logger.log("Loading initial content")
c, a = get_quote()
logger.log(a)

LCD.fill(LCD.black)
show_quote(c, a)
show_info()
LCD.show()

while(1):
    if(keyB.value() == 0):
        LCD.text("(loading...)", 140, 20, LCD.white)
        LCD.show()
        LCD.fill(LCD.black)
        show_info()
        c, a = get_quote()
        show_quote(c, a)
        LCD.show()
    time.sleep(0.01)
'''