from settings import *
from application import *

# 初始化
screen = SSD1306_I2C(screen_width, screen_height, i2c)
rect_group = create_centered_rect_group(screen_width, screen_height + 15,
                                        rows=rect_rows, cols=rect_cols, rect_width=rect_width,
                                        rect_height=rect_height, line_width=line_width)

text_viewer = TextViewer([])
about_viewer = AboutViewer(screen, screen_width, screen_height)
text_selector = TextFileSelector(text_files)
image_viewer = ImageViewer(screen, screen_width, screen_height)  # 初始化 ImageViewer
image_selector = ImageSelector(["Love","100days","Together","MicroPython"])

def draw_selection_screen():
    screen.fill(0)
    screen.hline(0, 15, screen_width, 1)
    current_function = function_names[rect_group.selected_index]
    screen.text(current_function, 45, 5)
    rect_group.draw(screen)
    screen.show()
    
def draw_clock_screen():
    screen.fill(0)
    current_time = time.localtime()
    time_str = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])
    date_str = "{:02}-{:02}-{:02}".format(current_time[0], current_time[1], current_time[2])
    
    screen.text('Clock', 45, 5)
    screen.hline(0, 15, screen_width, 1)
    screen.text(time_str, 30, 30)
    screen.text(date_str, 20, 45)
    screen.show()

def draw_text_selection_screen():
    text_selector.draw(screen)

def draw_text_viewer_screen():
    text_viewer.draw(screen)

def draw_about_screen():
    about_viewer.draw()

def draw_image_screen():
    image_viewer.draw()  # 显示图像

def on_select(pin):
    global current_mode, last_select_time
    current_time = time.ticks_ms()
    
    if time.ticks_diff(current_time, last_select_time) > debounce_time_ms:
        if current_mode == 0:  # 主界面
            rect_group.select_next()
            draw_selection_screen()
        elif current_mode == 1:  # 时钟界面
            current_mode = 0
            draw_selection_screen()
        elif current_mode == 2:  # 文本选择界面
            current_mode = 0  # 返回主界面
            draw_selection_screen()
        elif current_mode == 3:  # 文本查看界面
            current_mode = 2  # 返回文本选择界面
            draw_text_selection_screen()
        elif current_mode == 4:  # 关于界面
            current_mode = 0
            draw_selection_screen()
        elif current_mode == 5:  # 图像选择界面
            current_mode = 0
            draw_selection_screen()
        
        last_select_time = current_time


def on_confirm(pin):
    global current_mode, last_confirm_time, image_viewer
    current_time = time.ticks_ms()
    
    if time.ticks_diff(current_time, last_confirm_time) > debounce_time_ms:
        if current_mode == 0:  # 主界面
            if rect_group.selected_index == 0:  # 时钟
                current_mode = 1
                draw_clock_screen()
            elif rect_group.selected_index == 1:  # 文本选择
                current_mode = 2
                draw_text_selection_screen()
            elif rect_group.selected_index == 2:  # 图像选择
                current_mode = 5
                image_selector.draw(screen)
            elif rect_group.selected_index == 3:  # 关于
                current_mode = 4
                draw_about_screen()
        elif current_mode == 2:  # 文本选择界面
            text_selector.select_next()
            draw_text_selection_screen()
        elif current_mode == 3:  # 文本查看界面
            text_viewer.scroll_up()  # 向上滚动一行
            draw_text_viewer_screen()
        elif current_mode == 5:  # 图像选择界面
            selected_image_index = image_selector.get_selected_image_index()
            image_viewer.selected_index = selected_image_index  # 设置选中的图像索引
            image_viewer.draw()
        
        last_confirm_time = current_time

def on_scroll(pin):
    global current_mode, last_select_time, text_viewer, image_selector
    current_time = time.ticks_ms()
    
    if time.ticks_diff(current_time, last_select_time) > debounce_time_ms:
        if current_mode == 2:  # 文本选择界面
            selected_file = text_selector.get_selected_file()
            with open(f'{content_folder}/{selected_file}', 'r') as file:
                text_lines = file.readlines()
            text_viewer = TextViewer(text_lines)
            current_mode = 3
            draw_text_viewer_screen()
        elif current_mode == 3:  # 文本查看界面
            text_viewer.scroll_down()  # 向下滚动一行
            draw_text_viewer_screen()
        elif current_mode == 5:  # 图像选择界面
            image_selector.select_next()
            image_selector.draw(screen)
        
        last_select_time = current_time

# 设置按钮的中断处理
btn_select.irq(trigger=Pin.IRQ_FALLING, handler=on_select)
btn_confirm.irq(trigger=Pin.IRQ_FALLING, handler=on_confirm)
btn_scroll.irq(trigger=Pin.IRQ_FALLING, handler=on_scroll)

# 初始绘制主界面
draw_selection_screen()

if __name__ == "__main__":
    last_select_time = 0  # 初始化 last_select_time
    while True:
        try:
            if current_mode == 1:  # 时钟界面
                draw_clock_screen()
            elif current_mode == 4:  # 关于界面
                about_viewer.draw()
            time.sleep(1)
        except KeyboardInterrupt:
            screen.init_display()
            sys.exit()
#main.py