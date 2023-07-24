import os
import pygame
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog, simpledialog
import pickle
import pack_mapqf

root = tk.Tk()
fn = filedialog.askopenfilename()
img = Image.open(fn)
width, height = img.width, img.height
max_wh = max(width, height)
new_width = int(width / max_wh * 1000)
new_height = int(height / max_wh * 1000)
img2 = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
img2.save('img.png')
embed = tk.Frame(root, width=new_width, height=new_height)  # creates embed frame for pygame window
embed.grid(columnspan=(600), rowspan=500)  # Adds grid
embed.pack(side=LEFT)  # packs window to the left
buttonwin = tk.Frame(root, width=75, height=500)
buttonwin.pack(side=LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((new_width, new_height))
screen.fill(pygame.Color(255, 255, 255))

pygame.display.update()
mode = img2.mode
size = img2.size
data = img2.tobytes()


py_image = pygame.image.fromstring(data, size, mode)
screen.blit(py_image, (250, 250))

pygame.display.update()
root.update()


def on_exit(event=0):
    global running
    running = False


root.protocol('WM_DELETE_WINDOW', on_exit)
running = True
labels = dict()
my_font = pygame.font.SysFont('Comic Sans MS', 10)
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if not event.pos in labels.keys():
                n = simpledialog.askstring('Введите объект', 'введите объект')
                if not n in labels.values():
                    labels[event.pos] = n
    screen.blit(py_image, (0, 0))
    for pos in labels.keys():
        txt = my_font.render(labels[pos], True, (255, 0, 0))
        screen.blit(txt, pos)
    pygame.display.update()
    root.update()
pygame.quit()
fn = filedialog.asksaveasfilename()
packq = pack_mapqf.MapQuizPackFile(mode, size, data, labels)
with open(fn, 'wb') as f:
    pickle.dump(packq, f, protocol=5)
