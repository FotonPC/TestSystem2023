import os
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import ttkthemes
from PIL import Image, ImageTk
import testquestions
import random
import pygame
pygame.init()

class TNABaseUG(ttk.LabelFrame):
    def __init__(self, master=None, equals=None):

        if equals == None:
            self.equals = {"WTF":"WTF"}
        else:
            self.equals = equals
        self.keys = list(self.equals.keys())
        self.values = list(self.equals.values())
        super().__init__(master, text='quiz')
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('secret.TLabel', font='Arial 15')
        self.style.configure('TButton', font='Arial 25')
        self.style.configure('std.TButton', background='gray')
        self.style.configure('correct.TButton', background='green')
        self.style.configure('incorrect.TButton', background='red')
        self.style.configure('topic.TLabel', font='Arial 30')
        self.all_gb_labels = []
        self.all_cr_labels = []
        self.text = ttk.Label(self, text='&', style='topic.TLabel')
        self.text.pack()
        self.answer_frame = ttk.Frame(self)
        self.answer_frame.pack(side='bottom', expand=True, fill='both')
        self.a_label = ttk.Label(self.answer_frame, text='?')
        self.a_label.grid(columnspan=2, row=0, column=0)
        self.whn = int(len(list(self.equals.keys()))**0.5+0.999999)
        i = 0
        self.buttons = []
        for answer in self.values:
            self.buttons.append(ttk.Button(self.answer_frame, text=answer, style='std.TButton', command=lambda event=None, index=i: self.select(ind=index), width=len(answer)+1))
            self.buttons[-1].grid(row= (i // self.whn)+ 1 , column=i % self.whn, ipadx=5, ipady=5, pady=5, padx=5, sticky='nsew')
            i+= 1
        self.missed_els = [i for i in range(len(self.keys))]
        self.rightn=0
        self.clicks = 0

    def start(self):
        self.rightn=random.choice(self.missed_els)
        self.missed_els.remove(self.rightn)
        self.text.config(text=str(self.keys[self.rightn]))
    def select(self, event=None, a=None, ind=0):
        self.clicks += 1
        print(ind)
        if ind ==self.rightn:
            self.buttons[ind].config(style='correct.TButton')
            for butt in self.buttons:
                if butt['style'] == 'incorrect.TButton':
                     butt.config(style='std.TButton')
            for x in self.all_gb_labels:
                x.destroy()
            try:
                self.rightn = random.choice(self.missed_els)
            except:
                self.text.config(text=f"{len(self.keys)}/{self.clicks}")
            self.missed_els.remove(self.rightn)
            self.text.config(text=str(self.keys[self.rightn]))
            self.all_cr_labels.append(ttk.Label(self.answer_frame, text=self.keys[ind], style='secret.TLabel'))
            self.all_cr_labels[-1].grid(row=(ind // self.whn) + 1, column=ind % self.whn, sticky='se')
        else:
            if self.buttons[ind]['style'] != 'correct.TButton':
                self.buttons[ind].config(style='incorrect.TButton')
                self.all_gb_labels.append(ttk.Label(self.answer_frame, text=self.keys[ind], style='secret.TLabel'))
                self.all_gb_labels[-1].grid(row= (ind // self.whn)+ 1 , column=ind % self.whn, sticky='se')


class MAPQuiZ(ttk.Frame):
    def __init__(self, master=None,  packq=None, root=None):

        super().__init__(master)
        self.packq =packq
        self.img_raw = packq.img()
        self.root=root
        self.labels = packq.labels
        self.keys=[]
        self.values = []
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('secret.TLabel', font='Arial 15')
        self.style.configure('TButton', font='Arial 8')
        self.style.configure('std.TButton', background='gray')
        self.style.configure('correct.TButton', background='green')
        self.style.configure('incorrect.TButton', background='red')
        self.style.configure('topic.TLabel', font='Arial 30')

        for pos in self.labels.keys():
            self.keys.append(self.labels[pos])
            self.values.append(pos)
        width, height = packq.size
        self.qframe = ttk.Frame(self)
        self.qframe.pack(fill='x', expand=1)
        self.text = ttk.Label(self.qframe, text='Where is ?', style='topic.TLabel')
        self.text.pack(expand=1)
        self.mapframe = ttk.Frame(self, width=width+60, height=height+60)
        self.mapframe.pack()
        self.embed = tk.Frame(self.mapframe, width=width, height=height)  # creates embed frame for pygame window
        self.embed.place(x=30, y=30, width=width, height=height, anchor='nw')  # Adds grid
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(pygame.Color(255, 0, 255))
        pygame.display.update()
        self.prepare_img()
        self.screen.blit(self.img, (0, 0))
        pygame.display.update()
        self.clicked = []
        print(self.img_raw)
        self.after(100, self.loop)
        self.root.bind("<Configure>", self.handle_config)
        i = 0
        self.all_gb_labels = []
        self.all_cr_labels = []
        self.buttons = []
        for val in self.values:
            self.buttons.append(ttk.Button(self.mapframe, text='', style='std.TButton',
                                           command=lambda event=None, index=i: self.select(ind=index), width=1))
            self.buttons[-1].place(x=val[0]+30, y=val[1]+30)
            i += 1
        self.missed_els = [i for i in range(len(self.keys))]
        self.rightn = 0
        self.clicks = 0

    def start(self):
        self.rightn = random.choice(self.missed_els)
        self.missed_els.remove(self.rightn)
        self.text.config(text=str(self.keys[self.rightn]))

    def select(self, event=None, a=None, ind=0):
        self.clicks += 1
        print(ind)
        if ind == self.rightn:
            self.buttons[ind].config(style='correct.TButton')
            for butt in self.buttons:
                if butt['style'] == 'incorrect.TButton':
                    butt.config(style='std.TButton')
                    butt.config(text='', width=1)
            for x in self.all_gb_labels:
                x.destroy()
            try:
                self.rightn = random.choice(self.missed_els)
            except:
                tkinter.messagebox.showinfo('Done!', self.packq.thanks_text)
                self.text.config(text=f"{len(self.keys)}/{self.clicks}")
            self.missed_els.remove(self.rightn)
            self.text.config(text=str(self.keys[self.rightn]))
            self.buttons[ind].config(text=self.keys[ind], width=len(self.keys[ind])+1)

        else:
            if self.buttons[ind]['style'] != 'correct.TButton':
                self.buttons[ind].config(style='incorrect.TButton')
                self.buttons[ind].config(text=self.keys[ind], width=len(self.keys[ind])+1)
        self.handle_config()


    def prepare_img(self):
        self.img = pygame.image.fromstring(*self.img_raw)

    def call_lk(self, param=None):
        if param in self.clicked:
            return
    def loop(self):
        self.handle_config()
        self.after(1000, self.loop)
    def handle_config(self, event=None):
        self.screen.blit(self.img, (0, 0))
        self.draw_markers()
        pygame.display.update()

    def draw_markers(self):
        for val in self.values:
            pygame.draw.circle(self.screen, (255, 0, 0), val, 4, 2)
