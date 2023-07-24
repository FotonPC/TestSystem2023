import pickle
import random
import tkinter as tk
from tkinter import ttk
import ttkthemes
from PIL import Image, ImageTk
import testclasses
import pack_mapqf
from tkinter import filedialog

class App(ttkthemes.ThemedTk):
    def __init__(self, title='App', gg=0):
        super().__init__()
        self.title(title)
        self.set_theme('black')
        self.geometry('1280x720')
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(expand=True, fill='both')
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('topic2.TLabel', font='Arial 10')
        self.toolframe = ttk.Frame(self.mainframe)
        self.toolframe.pack(fill='x')
        self.title_l = ttk.Label(self.toolframe, text=gg.title, style='topic2.TLabel')
        self.title_l.pack()
        self.qaframe = ttk.Frame(self.mainframe)
        self.qaframe.pack(fill='both', expand=1)
        self.ts = testclasses.MAPQuiZ(self.qaframe, gg, root=self)
        self.ts.pack(fill='both', expand=True)
        self.ts.start()
        # self.questionframe = ttk.LabelFrame(self.qaframe, text='Q')
        # self.questionframe.pack(fill='both', expand=True, side='left')
        # self.answerframe = ttk.LabelFrame(self.qaframe, text='A')
        # self.answerframe.pack(fill='both', expand=True, side='left')





if __name__ == '__main__':

    with open(filedialog.askopenfilename(filetypes=(('FotonTestSystem2023 QuizMap v2', '*.fts23v2'),)), 'rb') as file:
        pack = pickle.load(file)
    print(pack)
    App(gg=pack).mainloop()

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
