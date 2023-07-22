import time
from programs import (
    about, clock, photos, quotes, settings, words
)

# Time Zone
UTC_OFFSET = -4 * 60 * 60

class Menu():
    def __init__(self, lcd, keys=None, info=None):
        self.lcd = lcd
        self.key_a = keys[0]
        self.key_b = keys[1]
        self.key_c = keys[2]
        self.key_u = keys[3]
        self.key_d = keys[4]
        self.key_l = keys[5]
        self.key_r = keys[6]
        self.info = info
        self.items = [
            "Clock",
            "Photos",
            "Words",
            "Quotes",
            "Files",
            "Settings",
            "About"
        ]
        self.cursor = 0
        self.time = None
        self._refresh_time()
        self.last_tick_time = time.ticks_ms()
    
    def _refresh_time(self):
        self.time = time.localtime(time.time() + UTC_OFFSET)
    
    def _draw_icon(self, icon, left):
        i, j = 0, 16
        for ir in icon:
            while ir > 0:
                if ir & 1:
                    self.lcd.pixel(left + j, i, self.lcd.white)
                j -= 1
                ir >>= 1
            i += 1
            j = 16
    
    
    def _refresh_topbar(self):
        line_height = 15
        self.lcd.fill_rect(0, 0, 240, line_height, self.lcd.gray)
        self.lcd.text('{:02d}:{:02d}:{:02d}'.format(self.time[3], self.time[4], self.time[5]), 88, 4, self.lcd.white)
        
        #ok_wifi_icon = [0, 0, 0x7f0, 0xff8, 0x180c, 0x3006, 0x23e2, 0x7f0, 0xc18, 0x808, 0x1c0, 0x1c0, 0x80]
        #no_wifi_icon = [0, 0, 0x7f0, 0xff8, 0x180c, 0x3006, 0x23e2, 0x7e8, 0xc08, 0x808, 0x1c8, 0x1c0, 0x88]
        ok_wifi_icon = [0, 0, 0xff0, 0x1ff8, 0x300c, 0x6006, 0x47e2, 0xff0, 0x1818, 0x1008, 0x3c0, 0x3c0, 0x180]
        no_wifi_icon = [0, 0, 0xff0, 0x1ff8, 0x300c, 0x6006, 0x47e2, 0xfe8, 0x1808, 0x1008, 0x3c8, 0x3c0, 0x188]
        wifi_icon = ok_wifi_icon if self.info['ip'] else no_wifi_icon
        self._draw_icon(wifi_icon, 0)
        
        battery_plug_icon = [0, 0, 0, 0x3ffe, 0x4001, 0x4781, 0xdfc1, 0xc7fd, 0xdfc1, 0x4781, 0x4001, 0x3ffe]
        battery_empty_icon = [0, 0, 0, 0x3ffe, 0x4001, 0x4001, 0xc001, 0xc001, 0xc001, 0x4001, 0x4001, 0x3ffe]
        
        plug_power = True
        battery_icon_left = 220
        if plug_power:
            self._draw_icon(battery_plug_icon, battery_icon_left)
        else:
            self._draw_icon(battery_empty_icon, battery_icon_left)
            battery_percent = 80
            battery_empty = int((100 - battery_percent) / 100 * 13)
            battery_width = 13 - battery_empty
            battery_color = self.lcd.green
            if battery_percent <= 20:
                battery_color = self.lcd.red
            elif battery_percent <= 40:
                battery_color = self.lcd.orange
            self.lcd.rect(battery_icon_left + 3 + battery_empty, 4, battery_width, 7, battery_color, True)
        self.lcd.show()

    
    def _refresh_menu(self):
        top_bar_height = 15
        line_height = 15
        
        # Background
        self.lcd.fill_rect(0, 15, 240, 135 - line_height, self.lcd.black)

        # Items
        for i, item in enumerate(self.items):
            text_color = self.lcd.white
            if i == self.cursor:
                self.lcd.fill_rect(0, top_bar_height + line_height * i, 240, line_height, self.lcd.white)
                text_color = self.lcd.black
            self.lcd.text(item, 4, top_bar_height + line_height * i + 4, text_color)
        self.lcd.show()
    
    def show(self):
        self.lcd.fill(self.lcd.black)
        self._refresh_topbar()
        self._refresh_menu()
        while True:
            if (self.key_u.value() == 0):
                if self.cursor > 0:
                    self.cursor -= 1
                    self._refresh_menu()
                time.sleep(0.2)
            if (self.key_d.value() == 0):
                if self.cursor < len(self.items) - 1:
                    self.cursor += 1
                    self._refresh_menu()
                time.sleep(0.2)
            
            if (self.key_b.value() == 0):
                if self.items[self.cursor] == "Clock":
                    clock.show_clock(self.lcd, self.key_a, self.key_b)
                if self.items[self.cursor] == "Photos":
                    photos.show_photo(self.lcd, self.key_a, self.key_b)
                elif self.items[self.cursor] == "Words":
                    words.show_words(self.lcd, self.key_a, self.key_b)
                elif self.items[self.cursor] == "Settings":
                    settings.show_settings(self.lcd, self.key_a, self.key_b)
                elif self.items[self.cursor] == "About":
                    about.show_about(self.lcd, self.key_a, self.info)
                elif self.items[self.cursor] == "Quotes":
                    quotes.show_quote(self.lcd, self.key_a, self.key_b)
                self._refresh_menu()
                        
            time.sleep(0.02)
            time_diff = (time.ticks_ms() - self.last_tick_time) // 1000
            if time_diff >= 1:
                self.last_tick_time = time.ticks_ms()
                self._refresh_time()
                self._refresh_topbar()
