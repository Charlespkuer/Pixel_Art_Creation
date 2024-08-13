import pygame
import sys
from tkinter import Tk, simpledialog, filedialog
import json
import os

import color_standard as color

# 初始化 Pygame
pygame.init()

# 设置像素大小和绘制区域
pixel_size = 20
grid_width = 25
grid_height = 25

# 设置屏幕尺寸
screen_width = grid_width * pixel_size + 150
screen_height = grid_height * pixel_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Art Creation")

# 定义颜色
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHTGRAY = (180, 180, 180)
DARK = (30, 30, 30)

color16 = color.colors16
color64 = color.colors64
selected_color = BLACK

# 初始化网格，交替设置GRAY和LIGHTGRAY颜色
grid = [[LIGHTGRAY if (x + y) % 2 == 0 else GRAY for x in range(grid_width)] for y in range(grid_height)]

# 初始化字体
font = pygame.font.SysFont(None, 24)

packs = 4
color_mode = 16

# 绘制颜色选择器
def draw_color_selector():
    colors = color16 if color_mode == 16 else color64
    for i, color in enumerate(colors):
        x = grid_width * pixel_size + 30 + (i // packs) * (pixel_size + 2)
        y = (i % packs) * (pixel_size + 2)
        pygame.draw.rect(screen, color, (x, y, pixel_size, pixel_size))
        if color == selected_color:
            pygame.draw.rect(screen, (235,235,235), (x-1, y-1, pixel_size+2, pixel_size+2), 3)

# 通用绘制按钮函数
def draw_button(button_x, button_y, button_width, botton_height, text_content):
    pygame.draw.rect(screen, color.white, (button_x, button_y, button_width, botton_height))
    text = font.render(text_content, True, BLACK)
    text_x = button_x + (button_width - text.get_width()) // 2
    text_y = button_y + (botton_height - text.get_height()) // 2
    screen.blit(text, (text_x, text_y))

# 清除绘制痕迹
def clear_drawing():
    for y in range(grid_height):
        for x in range(grid_width):
            grid[y][x] = LIGHTGRAY if (x + y) % 2 == 0 else GRAY

# 绘制网格线
def draw_grid():
    for x in range(0, grid_width * pixel_size, pixel_size):
        if x // pixel_size % 5 == 0:
            pygame.draw.line(screen, DARK, (x, 0), (x, grid_height * pixel_size))
    for y in range(0, grid_height * pixel_size, pixel_size):
        if y // pixel_size % 5 == 0:
            pygame.draw.line(screen, DARK, (0, y), (grid_width * pixel_size, y))

# 初始化 Tkinter
root = Tk()
root.withdraw()  # 隐藏主窗口

# 保存像素画为透明背景的 PNG 文件
def save_pixel_art():
    pixel_art = pygame.Surface((grid_width * pixel_size, grid_height * pixel_size), pygame.SRCALPHA)
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] != (LIGHTGRAY if (x + y) % 2 == 0 else GRAY):
                pygame.draw.rect(pixel_art, grid[y][x], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    file_name = simpledialog.askstring("Save Pixel Art", "Enter file name:")
    if file_name and file_name.strip():
        save_path = os.path.join("Saved Model", f"{file_name}.png")
        os.makedirs("Saved Model", exist_ok=True)
        pygame.image.save(pixel_art, save_path)
        save_grid_to_file(file_name)

# 保存网格数据到文件
def save_grid_to_file(file_name):
    save_path = os.path.join("Saved Model", f"{file_name}.json")
    os.makedirs("Saved Model", exist_ok=True)
    with open(save_path, "w") as file:
        json.dump(grid, file)

# 从文件加载网格数据
def load_grid_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            loaded_grid = json.load(file)
            for y in range(grid_height):
                for x in range(grid_width):
                    grid[y][x] = tuple(loaded_grid[y][x])

def handle_events():
    global running, drawing, erasing, selected_color, color_mode, packs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < grid_width * pixel_size and y < grid_height * pixel_size:
                grid_x = x // pixel_size
                grid_y = y // pixel_size
                if event.button == 1:  # 左键填色
                    grid[grid_y][grid_x] = selected_color
                    drawing = True
                elif event.button == 3:  # 右键清除填色
                    grid[grid_y][grid_x] = LIGHTGRAY if (grid_x + grid_y) % 2 == 0 else GRAY
                    erasing = True
            else:
                for i, color in enumerate(color16 if color_mode == 16 else color64):
                    cx = grid_width * pixel_size + 30 + (i // packs) * (pixel_size + 2)
                    cy = (i % packs) * (pixel_size + 2)
                    if cx <= x <= cx + pixel_size and cy <= y <= cy + pixel_size:
                        selected_color = color
                        break
                if screen_width - 90 < x < screen_width - 10 and screen_height - 40 < y < screen_height - 10:
                    save_pixel_art()
                elif screen_width - 90 < x < screen_width - 10 and screen_height - 80 < y < screen_height - 50:
                    clear_drawing()
                elif screen_width - 90 < x < screen_width - 10 and screen_height - 120 < y < screen_height - 90:
                    load_grid_from_file()
                elif screen_width - 135 < x < screen_width - 105 and screen_height - 40 < y < screen_height - 10:
                    color_mode = 16
                    packs = 4
                elif screen_width - 135 < x < screen_width - 105 and screen_height - 80 < y < screen_height - 50:
                    color_mode = 64
                    packs = 16
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键释放
                drawing = False
            elif event.button == 3:  # 右键释放
                erasing = False
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if x < grid_width * pixel_size and y < grid_height * pixel_size:
                grid_x = x // pixel_size
                grid_y = y // pixel_size
                if drawing:
                    grid[grid_y][grid_x] = selected_color
                elif erasing:
                    grid[grid_y][grid_x] = LIGHTGRAY if (grid_x + grid_y) % 2 == 0 else GRAY

def main():
    global running, drawing, erasing
    running = True
    drawing = False
    erasing = False
    while running:
        handle_events()

        for y in range(grid_height):
            for x in range(grid_width):
                pygame.draw.rect(screen, grid[y][x], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
        
        screen.fill(DARK, (grid_width * pixel_size, 0, 150, screen_height))
        draw_grid()
        draw_color_selector()
        draw_button(screen_width - 90, screen_height - 40, 80, 30, "Save")
        draw_button(screen_width - 90, screen_height - 80, 80, 30, "Clear")
        draw_button(screen_width - 90, screen_height - 120, 80, 30, "Load")
        draw_button(screen_width - 135, screen_height - 40, 30, 30, "16")
        draw_button(screen_width - 135, screen_height - 80, 30, 30, "64")

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()