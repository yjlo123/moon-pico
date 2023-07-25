import time
from fonts.roboto_mono_14x26 import draw_word as rm_draw_word
from fonts.cn_date_16x16 import draw_word as cn_draw_word

# Time Zone
UTC_OFFSET = -4 * 60 * 60
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

CHINESE_NUM = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
CHINESE_WEEK = ['一', '二', '三', '四', '五', '六', '日']
CHINESE_TIME_PERIODS = ['半夜', '凌晨', '黎明', '清晨', '早上', '上午', '中午', '午后', '下午', '傍晚', '晚上', '深夜']

def _num_to_chinese(num, zero_fill=False):
    if num <= 10:
        if zero_fill and 0 < num < 10:
           return CHINESE_NUM[0] + CHINESE_NUM[num]
        return CHINESE_NUM[num]
    res = CHINESE_NUM[10] + ('' if num % 10 == 0 else CHINESE_NUM[num % 10])
    if num // 20 > 0:
        res = CHINESE_NUM[num // 10] + res
    return res

def _get_new_time():
    return time.localtime(time.time() + UTC_OFFSET)

def _refresh(lcd, current_time):
    lcd.fill(lcd.black)
    
    year, month, mday, hour, minute, second, weekday, yearday = current_time
    
    # time_str = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
    is_am = True
    hour_12 = hour
    if hour >= 12:
        is_am = False
        if hour > 12:
            hour_12 -= 12
    time_str = '{:02d}:{:02d} {}'.format(hour_12, minute, 'AM' if is_am else 'PM')
    rm_draw_word(lcd, time_str, 0, 8, scale=2)
    
    date_str = '{}, {} {}'.format(WEEKDAYS[weekday], mday, MONTHS[month-1])
    left = (240 - 14 * len(date_str)) // 2
    rm_draw_word(lcd, date_str, 50, left)
    
    year_chinese = ''
    for d in str(year):
        year_chinese += CHINESE_NUM[int(d)]
    
    date_chinese = '{}月{}日 星期{}'.format(_num_to_chinese(month), _num_to_chinese(mday), CHINESE_WEEK[weekday])
    left = (240 - 16 * len(date_chinese)) // 2
    cn_draw_word(lcd, date_chinese, 90, left)

    period_chinese = CHINESE_TIME_PERIODS[(hour + 1) % 24 // 2]
    if minute == 0:
        time_chinese = '{}{}点整'.format(period_chinese, _num_to_chinese(hour_12))
    else:
        time_chinese = '{}{}点{}分'.format(period_chinese, _num_to_chinese(hour_12), _num_to_chinese(minute, zero_fill=True))
    left = (240 - 16 * len(time_chinese)) // 2
    cn_draw_word(lcd, time_chinese, 110, left)

    #lcd.rect(8, 110, 224, 10, lcd.white, True)
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
