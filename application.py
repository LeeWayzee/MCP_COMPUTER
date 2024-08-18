from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import machine, sys, os
from images import *
from settings import *

# 基础矩形类
class RectBase:
    def __init__(self, rec_x, rec_y, rec_width, rec_height, line_width):
        self.rec_x = rec_x
        self.rec_y = rec_y
        self.rec_width = rec_width
        self.rec_height = rec_height
        self.line_width = line_width
        
    def draw_rect(self, root, thickness=None):
        if thickness is None:
            thickness = self.line_width
        for i in range(thickness):
            root.rect(self.rec_x + i, self.rec_y + i, self.rec_width - 2 * i, self.rec_height - 2 * i, 1)

# 应用矩形类
class AppRect(RectBase):
    def __init__(self, rec_x, rec_y, rec_width, rec_height, line_width, symbol):
        super().__init__(rec_x, rec_y, rec_width, rec_height, line_width)
        self.symbol = symbol
        self.inverted = False
    
    def draw(self, root, inverted=False):
        if inverted:
            root.fill_rect(self.rec_x, self.rec_y, self.rec_width, self.rec_height, 1)  # 填充白色
            root.text(self.symbol, self.rec_x + 5, self.rec_y + 10, 0)  # 黑色文字
            root.rect(self.rec_x, self.rec_y, self.rec_width, self.rec_height, 0)  # 黑色边框
        else:
            root.fill_rect(self.rec_x, self.rec_y, self.rec_width, self.rec_height, 0)  # 填充黑色
            root.text(self.symbol, self.rec_x + 5, self.rec_y + 10, 1)  # 白色文字
            root.rect(self.rec_x, self.rec_y, self.rec_width, self.rec_height, 1)  # 白色边框
        
# 矩形组类
class RectGroup:
    def __init__(self, rects):
        self.rects = rects
        self.selected_index = 0
    
    def draw(self, root):
        for i, rect in enumerate(self.rects):
            rect.draw(root, inverted=(i == self.selected_index))
    
    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.rects)
        
# 文本文件选择器类
class TextFileSelector:
    def __init__(self, file_list):
        self.file_list = file_list
        self.selected_index = 0

    def draw(self, root):
        root.fill(0)
        for i, filename in enumerate(self.file_list):
            inverted = (i == self.selected_index)
            y = 15 + i * 10
            if inverted:
                root.fill_rect(0, y, 128, 10, 1)  # 反色背景
                root.text(filename, 2, y, 0)  # 黑色文字
            else:
                root.text(filename, 2, y, 1)  # 白色文字
        root.show()

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.file_list)

    def select_previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.file_list)

    def get_selected_file(self):
        return self.file_list[self.selected_index]

# 在 TextFileSelector 类基础上，我们可以创建一个 ImageSelector 类
class ImageSelector:
    def __init__(self, image_names):
        self.image_names = image_names
        self.selected_index = 0

    def draw(self, root):
        root.fill(0)
        for i, image_name in enumerate(self.image_names):
            inverted = (i == self.selected_index)
            y = 15 + i * 10
            if inverted:
                root.fill_rect(0, y, 128, 10, 1)  # 反色背景
                root.text(image_name, 2, y, 0)  # 黑色文字
            else:
                root.text(image_name, 2, y, 1)  # 白色文字
        root.show()

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.image_names)

    def select_previous(self):
        self.selected_index = (self.selected_index - 1) % len(self.image_names)

    def get_selected_image_index(self):
        return self.selected_index

class ImageViewer:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.images = self.load_images()
        self.selected_index = 0
    
    def load_images(self):
        
        return [aixin,hundred,together,mcplogo]

    def draw(self):
        self.screen.fill(0)
        if self.images:
            image = self.images[self.selected_index]
            for y in range(len(image)):
                for x in range(len(image[y])):
                    self.screen.pixel(x, y, image[y][x])  # 根据图像数据绘制像素
        self.screen.show()

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.images)
        self.draw()

# 文本查看器类
class TextViewer:
    def __init__(self, text_lines):
        self.text_lines = text_lines
        self.current_line = 0

    def draw(self, root):
        root.fill(0)
        visible_lines = self.text_lines[self.current_line:self.current_line + 5]
        for i, line in enumerate(visible_lines):
            root.text(line.strip(), 0, i * 10)
        root.show()

    def scroll_up(self):
        if self.current_line > 0:
            self.current_line -= 1

    def scroll_down(self):
        if self.current_line < len(self.text_lines) - 5:
            self.current_line += 1

# 关于查看器类
class AboutViewer:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_lines = []
        self.current_line = 0
        self.load_about_text()
    
    def load_about_text(self):
        with open('about.txt', 'r') as file:
            self.text_lines = file.readlines()
    
    def draw(self):
        self.screen.fill(0)
        start_line = self.current_line
        for i in range(5):
            if start_line + i < len(self.text_lines):
                self.screen.text(self.text_lines[start_line + i].strip(), 0, i * 12)
        self.screen.show()
    
    def scroll(self):
        if self.current_line + 5 < len(self.text_lines):
            self.current_line += 1
        else:
            self.current_line = 0

