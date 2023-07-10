import random
import tkinter as tk
from tkinter import ttk
import ttkthemes
from PIL import Image, ImageTk
import testclasses

class App(ttkthemes.ThemedTk):
    def __init__(self, title='App', gg=0, title2='eng to 87'):
        super().__init__()
        self.title(title)
        self.set_theme('black')
        self.geometry('1280x720')
        self.mainframe = ttk.LabelFrame(self, text='M')
        self.mainframe.pack(expand=True, fill='both')
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('topic2.TLabel', font='Arial 25')
        self.toolframe = ttk.LabelFrame(self.mainframe, text='T')
        self.toolframe.pack(fill='both', expand=True)
        self.title_l = ttk.Label(self.toolframe, text=title2, style='topic2.TLabel')
        self.title_l.pack()
        self.qaframe = ttk.LabelFrame(self.mainframe, text='QA')
        self.qaframe.pack(fill='both', expand=True)
        self.ts = testclasses.TNABaseUG(self.qaframe, equals=gg)
        self.ts.pack(fill='both', expand=True)
        self.ts.start()
        # self.questionframe = ttk.LabelFrame(self.qaframe, text='Q')
        # self.questionframe.pack(fill='both', expand=True, side='left')
        # self.answerframe = ttk.LabelFrame(self.qaframe, text='A')
        # self.answerframe.pack(fill='both', expand=True, side='left')





if __name__ == '__main__':

    with open('res01.txt', encoding='utf-8') as file:
        text1 = file.read()
    text1 = text1.replace('\n', '\t')
    text1 = text1.replace('\t\t', '\t')
    txt = text1.split('\t')
    random.shuffle(txt)
    inp = dict()
    for t in txt:
        print(t)
        try:
            a, b = t.split()
            inp[b] = a
        except:
            pass
    App(gg=inp).mainloop()
    print(txt)
    """
    with open('rec03.txt', encoding='utf-8') as file:
        text_en = file.read()
    with open('res03ru.txt', encoding='utf-8') as file:
        text_ru = file.read()

    en = text_en.split('\n')
    ru = text_ru.split('\n')
    inp1 = [[en[i], ru[i]] for i in range(len(en))]
    random.shuffle(inp1)
    inp = {b : a for a, b in inp1}
    App(gg=inp).mainloop()
    """
