import tkinter as tk
from tkinter import ttk
import ttkthemes
from PIL import Image, ImageTk


class TNABaseQ(ttk.Frame):
    def __init__(self, master=None, answers=None, qtext='', rightn=3):

        if answers == 0:
            self.answers = ['', '', '', '']
        else:
            self.answers = answers
        self.q_text=qtext
        self.rightn=rightn
        super().__init__(master)
        self.style = ttkthemes.ThemedStyle()
        self.style.configure('TButton', font='Arial 50')
        self.style.configure('std.TButton', background='gray')
        self.style.configure('correct.TButton', background='green')
        self.style.configure('incorrect.TButton', background='red')
        self.style.configure('topic.TLabel', font='Arial 30')
        self.text = ttk.Label(self, text=self.q_text, style='topic.TLabel')
        self.text.pack(side='top')
        #self.text.insert(tk.END, self.q_text)
        self.answer_frame = ttk.Frame(self)
        self.answer_frame.pack(side='bottom', expand=True, fill='both')
        self.a_label = ttk.Label(self.answer_frame, text='?')
        self.a_label.grid(columnspan=2, row=0, column=0)
        whn = int(len(self.answers)**0.5+0.999999)
        i = 0
        self.buttons = []
        for answer in self.answers:
            self.buttons.append(ttk.Button(self.answer_frame, text=answer, style='std.TButton', command=lambda event=None, index=i, ans=answer: self.select(a=ans, ind=index), width=len(answer)+1))
            self.buttons[-1].grid(row= (i // whn)+ 1 , column=i % whn, ipadx=5, ipady=5, pady=5, padx=5, sticky='nsew')
            i+= 1



    def select(self, event=None, a=None, ind=0):
        print(ind)
        if ind ==self.rightn-1:
            self.buttons[ind].config(style='correct.TButton')
        else:
            self.buttons[ind].config(style='incorrect.TButton')