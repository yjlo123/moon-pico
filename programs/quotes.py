import json
import time
import urequests

def get_quote():
    try:
        response = urequests.get("https://api.quotable.io/quotes/random")
        j = json.loads(response.text)[0]
    except Exception as e:
        print(e)
        return "", ""
    return j["content"], j["author"]

def write_quote(lcd, content, author):
    top = 10
    while content:
        lcd.text(content[:28], 8, top, lcd.white)
        content = content[28:]
        top += 15
    lcd.text('- ' + author, 15, top + 5, lcd.white)

def load_quote(lcd):
    lcd.fill(lcd.black)
    lcd.text("loading...", 0, 0, lcd.white)
    lcd.show()
    c, a = get_quote()
    lcd.fill(lcd.black)
    write_quote(lcd, c, a)
    lcd.show()

def show_quote(lcd, key_a, key_b):
    load_quote(lcd)
    time.sleep(0.2)  # debounce
    while True:
        if (key_a.value() == 0):
            break
        if (key_b.value() == 0):
            load_quote(lcd)
        time.sleep(0.01)
