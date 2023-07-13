import time
#from fonts.roboto_mono_14x26 import draw_word
from fonts.ubuntu_mono_12x21 import draw_word

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)

def show_settings(lcd, key_a, key_b):
    lcd.fill(lcd.black)
#     draw_word(lcd, 'ABCDEFGHIJKLMNOPQ', 0, 0)
#     draw_word(lcd, 'RSTUVWXYZ!"#$%&()', 27, 0)
#     draw_word(lcd, 'abcdefghijklmnopq', 54, 0)
#     draw_word(lcd, 'rstuvwxyz\'*+,-./?', 81, 0)
#     draw_word(lcd, '0123456789:;<=>@~', 108, 0)
    draw_word(lcd, 'abcdefghijklmnopq', 0, 0, spacing=2)
    draw_word(lcd, 'rstuvwxyz!"#$\'()*', 22, 0, spacing=2)
    draw_word(lcd, 'ABCDEFGHIJKLMNOPQ', 44, 0, spacing=2)
    draw_word(lcd, 'RSTUVWXYZ%&+,-.:;', 66, 0, spacing=2)
    draw_word(lcd, '0123456789/<=>?@[', 88, 0, spacing=2)
    draw_word(lcd, '\\]^_`{|}~', 110, 0, spacing=2)
    
    lcd.show()
    time.sleep(0.2)  # debounce
    while True:
        if (key_a.value() == 0):
            break
        time.sleep(0.01)

