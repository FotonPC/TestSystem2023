import os
import pygame
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog

root = tk.Tk()
fn = filedialog.askopenfilename()
img = Image.open(fn)
width, height = img.width, img.height
max_wh = max(width, height)
new_width = int(width / max_wh * 1000)
new_height = int(height / max_wh * 1000)
img2 = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
img2.save('img.png')
embed = tk.Frame(root, width = new_width, height = new_height) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((new_width,new_height))
screen.fill(pygame.Color(255,255,255))

pygame.display.update()
mode = img2.mode
size = img2.size
data = img2.tobytes()
print(mode, size)
print(type(mode))
print(type(size))
print(type(data))

py_image = pygame.image.fromstring(data, size, mode)
screen.blit(py_image, (250, 250))

pygame.display.update()
root.update()
def on_exit(event=0):
    global running
    running = False
root.protocol('WM_DELETE_WINDOW', on_exit)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    screen.blit(py_image, (0, 0))
    pygame.display.update()
    root.update()
pygame.quit()