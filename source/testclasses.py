import os
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import ttkthemes
from PIL import Image, ImageTk
import random
import pygame

pygame.init()


class TNABaseUG(ttk.Frame):
    def __init__(self, master=None, packm=None, root=None, close_handle=None):
        self.root = root
        if packm is None:
            packm = MatchTestPack()
        self.pack = packm
        self.eq = self.pack.equals
        self.pairs = []
        for key in self.eq:
            self.pairs.append((key, self.eq[key]))
        random.shuffle(self.pairs)
        self.keys = [pair[0] for pair in self.pairs]
        self.values = [pair[1] for pair in self.pairs]
        super().__init__(master)
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('secret.TLabel', font=self.pack.font_label)
        self.style.configure('all.TButton', font=self.pack.font_button)
        self.style.configure('std.all.TButton')
        self.style.configure('correct.all.TButton', background='green')
        self.style.configure('incorrect.all.TButton', background='red')
        self.style.configure('topic.TLabel', font='Arial 30')
        self.style.configure('title.TLabel', font='Arial 12 bold')
        self.style.configure('close.TButton', font='{Segoe UI} 13 italic')
        self.all_gb_labels = []
        self.all_cr_labels = []
        self.info_frame = ttk.Frame(self, height=80)
        self.info_frame.pack(fill='x')
        self.title_label = ttk.Label(self.info_frame, text=self.pack.title, style='title.TLabel')
        self.title_label.place(relx=0, rely=0, anchor='nw')
        self.text = ttk.Label(self.info_frame, text='&', style='topic.TLabel')
        self.text.place(relx=0, rely=1, anchor='sw')
        self.button_close = ttk.Button(self.info_frame, text='Закрыть тест X', style='close.TButton', command=self.close)
        self.button_close.place(relx=1, rely=0.5, relheight=1, anchor='e',  relwidth=0.5)
        self.answer_frame = ttk.Frame(self)
        self.answer_frame.pack(side='bottom', expand=True, fill='both')
        self.width = int(self.pack.size_grid)
        i = 0
        self.buttons = []
        for answer in self.values:
            self.buttons.append(ttk.Button(self.answer_frame, text=answer, style='std.all.TButton',
                                           command=lambda event=None, index=i: self.select(ind=index), **self.pack.size_button))
            self.buttons[-1].grid(column=i % self.width, row=i // self.width, **self.pack.grid_button)
            i += 1
        self.missed_els = [i for i in range(len(self.keys))]
        self.rightn = 0
        self.clicks = 0
        self.close_handle = close_handle

    def start(self):
        self.rightn = random.choice(self.missed_els)
        self.missed_els.remove(self.rightn)
        self.text.config(text=str(self.keys[self.rightn]))

    def close(self):
        self.destroy()
        self.close_handle()

    def select(self, event=None, a=None, ind=0):
        self.clicks += 1
        print(ind)
        if ind == self.rightn:
            self.buttons[ind].config(style='correct.all.TButton')
            for butt in self.buttons:
                if butt['style'] == 'incorrect.all.TButton':
                    butt.config(style='std.all.TButton')
            for x in self.all_gb_labels:
                x.destroy()
            try:
                self.rightn = random.choice(self.missed_els)
            except:
                self.text.config(text=f"{len(self.keys)}/{self.clicks}")
            self.missed_els.remove(self.rightn)
            self.text.config(text=str(self.keys[self.rightn]))
            self.all_cr_labels.append(ttk.Label(self.answer_frame, text=self.keys[ind], style='secret.TLabel', **self.pack.size_label))
            self.all_cr_labels[-1].grid(column=ind % self.width, row=ind // self.width, **self.pack.grid_label)
        else:
            if self.buttons[ind]['style'] != 'correct.all.TButton':
                self.buttons[ind].config(style='incorrect.all.TButton')
                self.all_gb_labels.append(ttk.Label(self.answer_frame, text=self.keys[ind], style='secret.TLabel', **self.pack.size_label))
                self.all_gb_labels[-1].grid(column=ind % self.width, row=ind // self.width, **self.pack.grid_label)


class MAPQuiZ(ttk.Frame):
    def __init__(self, master=None, packq=None, root=None, close_handle=None):

        super().__init__(master)
        self.packq = packq
        self.img_raw = packq.img()
        self.root = root
        self.labels = packq.labels
        self.keys = []
        self.values = []
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('TButton', font='Arial 8')
        self.style.configure('std.TButton', background='gray')
        self.style.configure('correct.TButton', background='green')
        self.style.configure('incorrect.TButton', background='red')
        self.style.configure('topic.TLabel', font='Arial 30')

        for pos in self.labels.keys():
            self.keys.append(self.labels[pos])
            self.values.append(pos)
        width, height = packq.size
        self.qframe = ttk.Frame(self, height=80)
        self.qframe.pack(fill='x')
        self.title_label = ttk.Label(self.qframe, text=self.packq.title)
        self.title_label.place(relx=0, rely=0, relwidth=0.5, relheight=0.2, anchor='nw')
        self.text = ttk.Label(self.qframe, text='Where is ?', style='topic.TLabel')
        self.text.place(relx=0, rely=0.2, anchor='nw', relwidth=0.5, relheight=0.8)
        self.butt_close = ttk.Button(self.qframe, text='Закрыть тест X', command=self.close)
        self.butt_close.place(relx=0.5, rely=0, relwidth=0.5, relheight=1, anchor='nw')
        self.mapframe = ttk.Frame(self, width=width + 60, height=height + 10)
        self.mapframe.pack()
        self.embed = tk.Frame(self.mapframe, width=width, height=height)  # creates embed frame for pygame window
        self.embed.place(x=0, y=0, width=width, height=height, anchor='nw')  # Adds grid
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
            self.buttons[-1].place(x=val[0], y=val[1])
            i += 1
        self.missed_els = [i for i in range(len(self.keys))]
        self.rightn = 0
        self.clicks = 0
        self.close_handle = close_handle

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
            #self.buttons[ind].config(text=self.keys[ind], width=len(self.keys[ind]) + 1)

        else:
            if self.buttons[ind]['style'] != 'correct.TButton':
                self.buttons[ind].config(style='incorrect.TButton')
                #self.buttons[ind].config(text=self.keys[ind], width=len(self.keys[ind]) + 1)
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

    def close(self, event=None):
        try:
            pygame.quit()
        except:
            pass
        self.destroy()
        self.close_handle()


class MatchTestPack:
    def __init__(self, title='', equals=None, thanks_text='', size_grid=0, size_button=None, size_label=None,
                 font_button='TkDefaultFont', font_label='TkDefaultFont', grid_label=None, grid_button=None, ):
        if equals is None:
            equals = dict()
        if size_button is None:
            size_button = {'width': 0}
        if size_label is None:
            size_label = {'width': 0}
        if grid_label is None:
            grid_label = {'padx':0,
                          'pady':0,
                          'ipadx':0,
                          'ipady':0,
                          'sticky': ''}
        if grid_button is None:
            grid_button = {'padx':0,
                          'pady':0,
                          'ipadx':0,
                          'ipady':0,
                          'sticky': ''}
        self.title = ''
        self.equals = equals
        self.thanks_text = thanks_text
        self.size_button = size_button
        self.grid_label = grid_label
        self.grid_button = grid_button
        self.font_label = font_label
        self.font_button = font_button
        self.size_label = size_label
        self.size_grid = size_grid
