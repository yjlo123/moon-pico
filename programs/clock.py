import time
from fonts.roboto_mono_14x26 import draw_word as rm_draw_word

# Time Zone
UTC_OFFSET = -4 * 60 * 60

def _get_new_time():
    return time.localtime(time.time() + UTC_OFFSET)

def _refresh(lcd, current_time):
    lcd.fill(lcd.black)
    
    time_str = '{:02d}:{:02d}:{:02d}'.format(current_time[3], current_time[4], current_time[5])
    rm_draw_word(lcd, time_str, 0, 0)
    
    lcd.rect(8, 110, 224, 10, lcd.white, True)
    lcd.show()

def show_clock(lcd, key_a, key_b):
    current_time = _get_new_time()
    last_tick_time = time.ticks_ms()
    _refresh(lcd, current_time)

    while True:
        if (key_a.value() == 0):
            break
        time.sleep(0.02)
        time_diff = (time.ticks_ms() - last_tick_time) // 1000
        if time_diff >= 1:
            last_tick_time = time.ticks_ms()
            current_time = _get_new_time()
            _refresh(lcd, current_time)
