import time
import uos

def show_about(lcd, key_a, info):
    lcd.fill(lcd.black)
    lcd.text("Raspberry Pi Pico", 8, 10, lcd.red)
    lcd.text(str(info['ip']), 8, 20, lcd.green)
    lcd.text("Moon Pico", 8, 40, lcd.white)
    lcd.text("OS ver: 0.1", 8, 50, lcd.white)
    lcd.text("https://siwei.dev", 8, 60, lcd.white)
    
    stat = uos.statvfs('/')
    block_size_kb = stat[0] // 1024
    free_space = block_size_kb * stat[3]
    total_space = block_size_kb * stat[2]
    used_space = total_space - free_space
    avail_percent = str(round(free_space / total_space * 100, 2))
    lcd.text("Free space: {}KB ({}%)".format(free_space, avail_percent), 8, 80, lcd.white)
    lcd.text("Used space: {}KB".format(used_space), 8, 90, lcd.white)
    lcd.text("Total space: {}KB".format(total_space), 8, 100, lcd.white)
    
    lcd.rect(8, 110, 224, 10, lcd.white)
    bar_width = int(224 * used_space / total_space)
    lcd.rect(8, 110, 8 + bar_width, 10, lcd.white, True)
    
    lcd.show()
    while True:
        if (key_a.value() == 0):
            break
        time.sleep(0.01)
