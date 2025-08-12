# sbas_teacher_auto.py
# Requires SikuliX API for Python: https://raiman.github.io/SikuliX1/downloads.html
# Run with:  sikulix -r sbas_teacher_auto.py

from sikuli import *

# -------------------------
# CONFIG - Replace with your image paths
# -------------------------
IMG_MAIN_RADIO1 = "C:/sbas_images/main_radio1.png"
IMG_MAIN_RADIO2 = "C:/sbas_images/main_radio2.png"
IMG_NEXT_BTN = "C:/sbas_images/next_button.png"

IMG_P1_RADIO1 = "C:/sbas_images/page1_radio1.png"
IMG_P1_RADIO2 = "C:/sbas_images/page1_radio2.png"

IMG_P2_SLIDER1 = "C:/sbas_images/page2_slider1.png"
IMG_P2_SLIDER2 = "C:/sbas_images/page2_slider2.png"
IMG_SCROLLBAR = "C:/sbas_images/page2_scrollbar.png"
IMG_SCROLLBAR_BOTTOM = "C:/sbas_images/page2_scrollbar_bottom.png"

# -------------------------
# FUNCTIONS
# -------------------------

def click_if_exists(img, timeout=3):
    """Click the image if found within timeout"""
    if exists(img, timeout):
        click(img)
        wait(0.5)

def drag_slider(img, offset_x):
    """Drag slider horizontally"""
    if exists(img, 3):
        m = find(img)
        dragDrop(m, Location(m.x + offset_x, m.y))

def scroll_section(scrollbar_img, scrollbar_end_img):
    """Scroll down small section by dragging scrollbar"""
    if exists(scrollbar_img, 3) and exists(scrollbar_end_img, 3):
        dragDrop(scrollbar_img, scrollbar_end_img)
        wait(1)

# -------------------------
# MAIN AUTOMATION
# -------------------------

def automate_sbas_teacher():
    # Make sure SBAS Teacher is on screen
    App.focus("SBAS Teacher")  # App name must match window title
    
    # ===== MAIN PAGE =====
    click_if_exists(IMG_MAIN_RADIO1)
    click_if_exists(IMG_MAIN_RADIO2)
    click_if_exists(IMG_NEXT_BTN)

    # ===== PAGE 1 =====
    click_if_exists(IMG_P1_RADIO1)
    click_if_exists(IMG_P1_RADIO2)
    click_if_exists(IMG_NEXT_BTN)

    # ===== PAGE 2 =====
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
