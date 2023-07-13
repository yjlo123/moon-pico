import time
import random
import os
from fonts.roboto_mono_14x26 import draw_word as rm_draw_word
from fonts.ubuntu_mono_12x21 import draw_word as um_draw_word


def write_content_wrapped(lcd, content, line_top):
    line_height = 22
    chars_in_line = 20
    top = line_top
    while content:
        content = content.strip()
        if len(content) <= chars_in_line:
            # content longer than line
            #lcd.text(content, 0, top, lcd.white)
            um_draw_word(lcd, content, top, 0)
            break
        else:
            # content shorter than line
            if content[chars_in_line] == ' ':
                # line ends with a complete word
                #lcd.text(content[:30], 0, top, lcd.white)
                um_draw_word(lcd, content[:chars_in_line], top, 0)
                content = content[chars_in_line:]
            else:
                i = chars_in_line - 1
                while content[i] != ' ':
                    i -= 1
                    if i == 0:
                        break
                if i == 0:
                    # word longer than the line
                    #lcd.text(content[:30], 0, top, lcd.white)
                    um_draw_word(lcd, content[:chars_in_line], top, 0)
                    content = content[chars_in_line:]
                else:
                    #lcd.text(content[:i], 0, top, lcd.white)
                    um_draw_word(lcd, content[:i], top, 0)
                    content = content[i:]
            top += line_height



def load_random(lcd):
    file_path = "data"
    file_name = "gre1310.txt"
    files = os.ilistdir(file_path)
    entry = [x for x in files if x[0] == file_name]
    if not entry:
        return
    entry = entry[0]
    file_size = entry[3]
    line = None
    with open(file_path + "/" + file_name, 'rb') as f:
        while True:
            pos = random.randint(0, file_size)
            if not pos:
                line = f.readline()
                break
            f.seek(pos)
            f.readline() # skip this possibly incomplete line
            next_line = f.readline()
            if next_line:
                line = next_line
                break

    word, meaning = line.decode('utf-8').strip().split('\t')
    lcd.fill(lcd.black)
    #lcd.text(word, 0, 0, lcd.white)
    rm_draw_word(lcd, word, 0, 0)
    write_content_wrapped(lcd, meaning, 30)
    lcd.show()

def show_words(lcd, key_a, key_b):
    load_random(lcd)
    time.sleep(0.2)  # debounce
    while True:
        if (key_a.value() == 0):
            break
        if (key_b.value() == 0):
            load_random(lcd)
            time.sleep(0.2)
        time.sleep(0.01)

