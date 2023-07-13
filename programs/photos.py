import time
import bmp_file_reader as bmpr

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)

def show_photo(lcd, key_a, key_b):
    lcd.fill(lcd.black)
    lcd.text("loading...", 0, 0, lcd.white)
    lcd.show()
    pics = ["xp.bmp", "win11.bmp"]
    idx = 0
    exit_photos = False
    while not exit_photos:
        with open('img/' + pics[idx], "rb") as file_handle:
            reader = bmpr.BMPFileReader(file_handle)
            img_height = reader.get_height()
            chunk_size = img_height // 5
            for i in range(0, img_height):
                row = reader.get_row(i)
                for j, color in enumerate(row):
                    r, g, b = color.red, color.green, color.blue
                    lcd.pixel(j, i, colour(r, g, b))
                if i > 0 and i % chunk_size == 0:
                    lcd.show()
#                     for x in range(5):
#                         for y in range(5):
#                             lcd.pixel(5*j+x, 5*i+y, colour(r, g, b))
        lcd.show()
        while True:
            if (key_a.value() == 0):
                exit_photos = True
                break
            if (key_b.value() == 0):
                idx = (idx + 1) % len(pics)
                time.sleep(0.2)
                break
            time.sleep(0.01)
