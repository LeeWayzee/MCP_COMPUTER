import time,os,machine
from machine import Pin,I2C
from application import *
from images import *


# 获取 content 文件夹中的所有文本文件
content_folder = "content"
text_files = [f for f in os.listdir(content_folder) if f.endswith(".txt")]
images_list = [aixin,hundred,together,mcplogo]

#use 16 and 17 as sda and scl
i2c = I2C(0,sda=Pin(16),scl=Pin(17))

# Debounce times
debounce_time_ms = 500
last_select_time = 0
last_confirm_time = 0

# Current mode: 0 = selection, 1 = clock
current_mode = 0

# Button Pins
btn_select = Pin(19, Pin.IN, Pin.PULL_DOWN)
btn_confirm = Pin(20, Pin.IN, Pin.PULL_DOWN)
high_signal_pin = Pin(18, Pin.IN, Pin.PULL_UP)
btn_scroll = Pin(21, Pin.IN, Pin.PULL_DOWN)

# Global state
screen_width = 128
screen_height = 64
i2c = I2C(0, sda=Pin(16), scl=Pin(17))

rect_rows = 1
rect_cols = 4
rect_width=25
rect_height=30
line_width=1

# (settings.py)

# 定义每个矩形框对应的功能名称
function_names = ["Clock", "Texts", "Image", "About"]

# 定义表示每个矩形框的符号或文本
rect_symbols = ["@", "$", "[]", "?"]  # 可以根据需要替换为适当的符号

# 更新 create_centered_rect_group 函数以包含符号
def create_centered_rect_group(screen_width, screen_height, rows, cols, rect_width, rect_height, line_width):
    h_spacing = (screen_width - cols * rect_width) // (cols + 1)
    v_spacing = (screen_height - rows * rect_height) // (rows + 1)
    
    rects = []
    
    for row in range(rows):
        for col in range(cols):
            x = h_spacing + col * (rect_width + h_spacing)
            y = v_spacing + row * (rect_height + v_spacing)
            symbol = rect_symbols[row * cols + col]
            rects.append(AppRect(x, y, rect_width, rect_height, line_width, symbol))
            
    return RectGroup(rects)

# Example: 4x4 grid of rectangles
#rect_group = create_centered_rect_group(screen_width, screen_height,rows=3, cols=3, rect_width=15, rect_height=15, line_width=1)






