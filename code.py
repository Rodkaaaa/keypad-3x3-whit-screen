import board
import busio
import rotaryio
import usb_hid
import time

from digitalio import DigitalInOut, Direction, Pull

import adafruit_ssd1306
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# =============================
# HID SETUP
# =============================

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
cc = ConsumerControl(usb_hid.devices)

MEDIA = 1
KEY = 2
WRITE = 3

MODE_NORMAL = 0
MODE_PAGE_SELECT = 1

current_mode = MODE_NORMAL

# =============================
# BUTTONS
# =============================

pins = [
    board.GP2, board.GP3, board.GP4,
    board.GP5, board.GP6, board.GP7,
    board.GP8, board.GP9, board.GP10,
]

buttons = []

for p in pins:
    btn = DigitalInOut(p)
    btn.direction = Direction.INPUT
    btn.pull = Pull.UP
    buttons.append(btn)

button_state = [False]*9

# =============================
# EC11 BUTTON
# =============================

enc_btn = DigitalInOut(board.GP11)
enc_btn.direction = Direction.INPUT
enc_btn.pull = Pull.UP

last_enc_btn = True

# =============================
# DISPLAY
# =============================

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

display = adafruit_ssd1306.SSD1306_I2C(
    128, 64, i2c, addr=0x3C
)

# =============================
# ENCODER
# =============================

encoder = rotaryio.IncrementalEncoder(board.GP18, board.GP19)
last_position = encoder.position

# =============================
# WRITE TEXT
# =============================

def write_text(text):
    layout.write(text)

# =============================
# STREAMDECK VISUALS
# =============================

def click_anim():
    for _ in range(2):
        display.invert(True)
        time.sleep(0.05)
        display.invert(False)
        time.sleep(0.05)

def show_action(label, action):

    display.fill(0)

    x = (128-(len(label)*8))//2
    display.text(label, x, 0, 2)

    if isinstance(action, str):
        cmd = action[:18]
        x = (128-(len(cmd)*6))//2
        display.text(cmd, x, 40, 1)

    display.show()

# =============================
# PAGES
# =============================

pages = [

# MULTIMEDIA
[
([ConsumerControlCode.MUTE],"MUTE",MEDIA),
([ConsumerControlCode.VOLUME_DECREMENT],"VOL-",MEDIA),
([ConsumerControlCode.VOLUME_INCREMENT],"VOL+",MEDIA),
([ConsumerControlCode.SCAN_PREVIOUS_TRACK],"PREV",MEDIA),
([ConsumerControlCode.PLAY_PAUSE],"PLAY",MEDIA),
([ConsumerControlCode.SCAN_NEXT_TRACK],"NEXT",MEDIA),
([Keycode.GUI,Keycode.UP_ARROW],"MAX",KEY),
([Keycode.GUI,Keycode.DOWN_ARROW],"MIN",KEY),
([Keycode.GUI,Keycode.L],"LOCK",KEY),
],
# MEDIA WEB 🌐 (YouTube / Spotify Web / Twitch)
[
([Keycode.K],"PLAY",KEY),                 # Play / Pause
([Keycode.SHIFT,Keycode.P],"PREV",KEY),   # Previous video
([Keycode.SHIFT,Keycode.N],"NEXT",KEY),   # Next video

([Keycode.J],"BACK10",KEY),               # -10 sec
([Keycode.L],"FWD10",KEY),                # +10 sec
([Keycode.M],"MUTE",KEY),                 # Mute video

([Keycode.F],"FULL",KEY),                 # Fullscreen
([Keycode.C],"CAPTION",KEY),              # Subtitles
([Keycode.T],"THEATER",KEY),              # Theater mode
],
# CODE
[
([Keycode.CONTROL,Keycode.S],"SAVE",KEY),
([Keycode.CONTROL,Keycode.Z],"UNDO",KEY),
([Keycode.CONTROL,Keycode.Y],"REDO",KEY),
([Keycode.CONTROL,Keycode.C],"COPY",KEY),
([Keycode.CONTROL,Keycode.V],"PASTE",KEY),
([Keycode.CONTROL,Keycode.X],"CUT",KEY),
([Keycode.CONTROL,Keycode.F],"FIND",KEY),
([Keycode.CONTROL,Keycode.SHIFT,Keycode.P],"CMD",KEY),
([Keycode.F5],"RUN",KEY),
],

# BROWSER
[
([Keycode.CONTROL,Keycode.T],"NEW",KEY),
([Keycode.CONTROL,Keycode.W],"CLOSE",KEY),
([Keycode.CONTROL,Keycode.TAB],"NEXT",KEY),
([Keycode.CONTROL,Keycode.SHIFT,Keycode.TAB],"PREV",KEY),
([Keycode.CONTROL,Keycode.L],"URL",KEY),
([Keycode.CONTROL,Keycode.R],"REFRESH",KEY),
([Keycode.CONTROL,Keycode.D],"FAV",KEY),
([Keycode.CONTROL,Keycode.SHIFT,Keycode.N],"PRIVATE",KEY),
([Keycode.F11],"FULL",KEY),
],

# WINDOWS
[
([Keycode.GUI,Keycode.D],"DESKTOP",KEY),
([Keycode.GUI,Keycode.TAB],"TASK",KEY),
([Keycode.ALT,Keycode.TAB],"ALT",KEY),
([Keycode.GUI,Keycode.E],"FILES",KEY),
([Keycode.GUI,Keycode.R],"RUN",KEY),
([Keycode.GUI,Keycode.I],"SET",KEY),
([Keycode.GUI,Keycode.P],"SCREEN",KEY),
([Keycode.GUI,Keycode.SHIFT,Keycode.S],"SNIP",KEY),
([Keycode.CONTROL,Keycode.SHIFT,Keycode.ESCAPE],"TASKMGR",KEY),
],

# STREAM
[
([Keycode.F13],"SC1",KEY),
([Keycode.F14],"SC2",KEY),
([Keycode.F15],"SC3",KEY),
([Keycode.F16],"START",KEY),
([Keycode.F17],"STOP",KEY),
([Keycode.F18],"MIC",KEY),
([Keycode.F19],"CAM",KEY),
([Keycode.F20],"CLIP",KEY),
([Keycode.F21],"MARK",KEY),
],

# GIT STREAMDECK 🔥
[
("git add .","ADD",WRITE),
("git commit -m \"\"","COMMIT",WRITE),
("git push","PUSH",WRITE),
("git pull","PULL",WRITE),
("code .","CODE",WRITE),
([Keycode.CONTROL,Keycode.GRAVE_ACCENT],"TERM",KEY),
("git status","STATUS",WRITE),
("clear","CLEAR",WRITE),
([Keycode.ESCAPE],"ESC",KEY),
],

# SQL SERVER 🔥
[
("EXEC ","EXEC",WRITE),
("SELECT TOP 100 * FROM ","SELECT",WRITE),
("INSERT INTO  VALUES ();","INSERT",WRITE),
("UPDATE  SET  WHERE ;","UPDATE",WRITE),
("DELETE FROM  WHERE ;","DELETE",WRITE),
("BEGIN TRANSACTION","BEGIN",WRITE),
("COMMIT","COMMIT",WRITE),
("ROLLBACK","ROLL",WRITE),
("SELECT GETDATE();","DATE",WRITE),
],

]

page_names=[
"MULTIMEDIA",
"MEDIA WEB",
"CODE",
"BROWSER",
"WINDOWS",
"STREAM",
"GIT",
"SQL",
]

current_page=0
page_selector_index=0

# =============================
# DRAW MENU
# =============================

def draw():

    display.fill(0)

    if current_mode==MODE_NORMAL:

        title=page_names[current_page]
        x=(128-(len(title)*8))//2
        display.text(title,x,0,2)

        y=28
        x=0

        for i,key in enumerate(pages[current_page]):
            display.text(key[1],x,y,1)
            x+=42
            if (i+1)%3==0:
                x=0
                y+=12

    else:

        center_y=28

        for offset in range(-1,2):

            index=page_selector_index+offset
            if index<0 or index>=len(page_names):
                continue

            name=page_names[index]

            if offset==0:
                x=(128-(len(name)*8))//2
                display.text(name,x,center_y,2)
            else:
                y=center_y+(offset*16)
                x=(128-(len(name)*6))//2
                display.text(name,x,y,1)

    display.show()

draw()

# =============================
# MAIN LOOP
# =============================

while True:

    # EC11 CLICK
    if not enc_btn.value and last_enc_btn:

        if current_mode==MODE_NORMAL:
            current_mode=MODE_PAGE_SELECT
            page_selector_index=current_page
        else:
            current_page=page_selector_index
            current_mode=MODE_NORMAL

        draw()
        time.sleep(0.25)

    last_enc_btn=enc_btn.value

    # ENCODER
    position=encoder.position

    if position!=last_position:

        diff=position-last_position

        if current_mode==MODE_NORMAL:
            cc.send(
                ConsumerControlCode.VOLUME_INCREMENT
                if diff>0 else
                ConsumerControlCode.VOLUME_DECREMENT
            )
        else:
            page_selector_index+=diff
            page_selector_index=max(0,min(page_selector_index,len(pages)-1))
            draw()

        last_position=position

    # BUTTONS
    if current_mode==MODE_NORMAL:

        for i,btn in enumerate(buttons):

            pressed=not btn.value

            if pressed and not button_state[i]:

                action,label,mode=pages[current_page][i]

                show_action(label,action)
                click_anim()

                try:
                    if mode==KEY:
                        kbd.send(*action)
                    elif mode==MEDIA:
                        cc.send(action[0])
                    elif mode==WRITE:
                        write_text(action)
                except:
                    pass

                time.sleep(0.35)
                draw()

                button_state[i]=True

            if not pressed and button_state[i]:

                action,_,mode=pages[current_page][i]

                try:
                    if mode==KEY:
                        kbd.release(*action)
                except:
                    pass

                button_state[i]=False