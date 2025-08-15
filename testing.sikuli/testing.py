# sbas_teacher_auto.py
# Requires SikuliX API for Python: https://raiman.github.io/SikuliX1/downloads.html
# Run with:  sikulix -r sbas_teacher_auto.py

import sys
from sikuli import *

# -------------------------
# CONFIG - Replace with your image paths
# -------------------------

# ENCODE
encode = "/sbas-ss/encode.jpg"

# Message Type Buttons
MT_1 = "/sbas-ss/message_types/1.png"
MT_2 = "/sbas-ss/message_types/2.png"
MT_3 = "/sbas-ss/message_types/3.png"
MT_4 = "/sbas-ss/message_types/4.png"
MT_5 = "/sbas-ss/message_types/5.png"
MT_6 = "/sbas-ss/message_types/6.png"
MT_7 = "/sbas-ss/message_types/7.png"
MT_9 = "/sbas-ss/message_types/9.png"
MT_10 = "/sbas-ss/message_types/10.png"
MT_12 = "/sbas-ss/message_types/12.png"
MT_17 = "/sbas-ss/message_types/17.png"
MT_18 = "/sbas-ss/message_types/18.png"
MT_24 = "/sbas-ss/message_types/24.png"
MT_25 = "/sbas-ss/message_types/25.png"
MT_26 = "/sbas-ss/message_types/26.png"
MT_27 = "/sbas-ss/message_types/27.png"
MT_28 = "/sbas-ss/message_types/28.png"

# Preambles
PREAMBLE_53 = "/sbas-ss/preambles/53.png"
PREAMBLE_9A = "/sbas-ss/preambles/9A.png"
PREAMBLE_C6 = "/sbas-ss/preambles/C6.png"

# IODP
IODP = "/sbas-ss/iodps/iodp.png"


#MT-1
sample = "/sbas-ss/mt-1/21.jpg"


# write the same till 210


IMG_P2_SLIDER1 = "C:/sbas_images/page2_slider1.png"
IMG_P2_SLIDER2 = "C:/sbas_images/page2_slider2.png"
IMG_SCROLLBAR = "C:/sbas_images/page2_scrollbar.png"
IMG_SCROLLBAR_BOTTOM = "C:/sbas_images/page2_scrollbar_bottom.png"

# -------------------------
# FUNCTIONS
# -------------------------

def click_IODP(num):
    iodp_region = find(IODP)   # Locate the box
    x = iodp_region.x
    y = iodp_region.y

    # Define locations relative to top-left corner of the found image
    IODP_0 = Location(x + 25, y + 40)
    IODP_1 = Location(x + 70, y + 40)
    IODP_2 = Location(x + 115, y + 40)
    IODP_3 = Location(x + 160, y + 40)

    if(num == 0):
        click(IODP_0)   
    elif(num == 1):
        click(IODP_1)
    elif(num == 2): 
        click(IODP_2)
    elif(num == 3):
        click(IODP_3)

def click_if_exists(img, timeout=0):
    """Click the image if found within timeout"""
    if exists(Pattern(img).similar(0.7), timeout):
        click(img)
    else:
        print("Could not find:", img)

def drag_slider(img, offset_x):
    """Drag slider horizontally"""
    if exists(img, 3):
        m = find(img)
        dragDrop(m, Location(m.x + offset_x, m.y))

def scroll_section(scrollbar_img, scrollbar_end_img):
    """Scroll down small section by dragging scrollbar"""
    if exists(scrollbar_img, 3) and exists(scrollbar_end_img, 3):
        dragDrop(scrollbar_img, scrollbar_end_img)

# -------------------------
# MAIN AUTOMATION
# -------------------------

def automate_sbas_teacher():
    # Make sure SBAS Teacher is on screen
    App.focus("SBAS Teacher")  # App name must match window title

    # ===== MAIN PAGE =====
    click_if_exists(MT_1)

    # ===== PAGE 1 =====
    if sys.argv[1] == u'1':
        if sys.argv[2] == u'53':
            click_if_exists(PREAMBLE_53)
            print("Clicked Preamble 53")
        elif sys.argv[2] == "9A":
            click_if_exists(PREAMBLE_9A)    
        elif sys.argv[2] == "C6":
            click_if_exists(PREAMBLE_C6)

    if sys.argv[3] == u'0':
        click_IODP(0)  # Click IODP 0
    elif sys.argv[3] == u'1':
        click_IODP(1)
    elif sys.argv[3] == u'2':
        click_IODP(2)
    elif sys.argv[3] == u'3':
        click_IODP(3)
    

    click_if_exists(sample)

    click_if_exists(encode)


    # ===== PAGE 2 =====
    if sys.argv[2] == "2":
        drag_slider(IMG_P2_SLIDER1, 50)   # move 50px right
        drag_slider(IMG_P2_SLIDER2, -30)  # move 30px left
        scroll_section(IMG_SCROLLBAR, IMG_SCROLLBAR_BOTTOM)
        # You can add more slider drags here after scroll
        click_if_exists(IMG_NEXT_BTN)

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    automate_sbas_teacher()
