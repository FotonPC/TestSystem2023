import os
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog, simpledialog
import pickle
import pack_mapqf
import ttkthemes
from tkinter import messagebox as msgbox

class App(ttkthemes.ThemedTk):
    def __init__(self, title='MapQuizGenerator', version=1.0, theme='black', filename_settings=''):
        super().__init__()
        self.geometry('1000x300+100+100')
        self.fsn = filename_settings
        self.title(title + ' v' + str(version))
        self.set_theme(theme, 1, 1)
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill='both', expand=True)
        self.notebook = ttk.Notebook(self.mainframe)
        self.notebook.place(relheight=1, relwidth=1, relx=0, rely=0, anchor='nw')
        self.main_tab = ttk.Frame(self.notebook)
        self.main_tab.pack(fill='both', expand=1)
        self.notebook.add(self.main_tab, text='  Quiz  ')
        self.toolframe = ttk.LabelFrame(self.main_tab, text='Tools')
        self.toolframe.pack(fill='x')
        self.butt_create = ttk.Button(self.toolframe, text='Create new quiz', command=self.create_new_quiz)
        self.butt_create.grid(row=0, column=0, padx=10, pady=10, ipadx=4, ipady=4)
        self.butt_open_and_modify = ttk.Button(self.toolframe, text='Open quiz and edit', command=self.open_and_modify_quiz)
        self.butt_open_and_modify.grid(row=0, column=1, padx=10, pady=10, ipadx=4, ipady=4)
        self.butt_get_img= ttk.Button(self.toolframe, text='Save image from quiz as ..', command=self.get_img_from_quiz)
        self.butt_get_img.grid(row=0, column=2, padx=10, pady=10, ipadx=4, ipady=4)
        self.butt_saveas = ttk.Button(self.toolframe, text='Save quiz as ...', command=self.saveas_quiz)
        self.butt_saveas.grid(row=0, column=3, padx=10, pady=10, ipadx=4, ipady=4)
        self.butt_save = ttk.Button(self.toolframe, text='Save quiz', command=self.save_handle)
        self.butt_save.grid(row=0, column=4, padx=10, pady=10, ipadx=4, ipady=4)
        self.quizframe = ttk.LabelFrame(self.main_tab, text='Quiz')
        self.quizframe.pack(fill='both')
        self.quizframe.pack_forget()
        self.imgframe = ttk.Frame(self.quizframe)
        self.imgframe.pack(side='left')
        self.toolquiz_frame = ttk.LabelFrame(self.quizframe, text='Quiz Content')
        self.toolquiz_frame.pack(side='right', fill='y')
        self.edit_labels_frame = ttk.LabelFrame(self.toolquiz_frame, text='LabelEdit')
        self.edit_labels_frame.pack(fill='y')
        self.listbox_labels = tk.Listbox(self.edit_labels_frame, relief='flat', height=10, width=30, selectmode='single')
        self.listbox_labels.pack(fill='x', ipadx=4, ipady=4, padx=10, pady=10)
        self.butt_del_label = ttk.Button(self.edit_labels_frame, text='Delete label', command=self.del_label_quiz)
        self.butt_del_label.pack( ipadx=4, ipady=4, padx=10, pady=10)
        self.title_label = ttk.Label(self.toolquiz_frame, text='Quiz Title')
        self.title_label.pack()
        self.entry_title = ttk.Entry(self.toolquiz_frame, width=0)
        self.entry_title.pack(fill='x')
        self.tnxtxt_label = ttk.Label(self.toolquiz_frame, text='Thanks for passed quiz')
        self.tnxtxt_label.pack()
        self.tnxtxt_text = tk.Text(self.toolquiz_frame)
        self.tnxtxt_text.pack(fill='both', expand=True)
        self.sett_tab = ttk.Frame(self.notebook)
        self.sett_tab.pack(fill='both', expand=1)
        self.notebook.add(self.sett_tab, text='  Settings  ')
        self.style=ttkthemes.ThemedStyle()
        self.combo_theme = ttk.Combobox(self.sett_tab, values=self.style.get_themes())
        self.combo_theme.grid(row=0, column=0)
        self.combo_theme.bind("<<ComboboxSelected>>", self.select_theme)
        os.environ['SDL_WINDOWID'] = str(self.imgframe.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.init()
        pygame.display.init()
        self.screen = None
        self.size = (0, 0)
        self.filename = ''


    def select_theme(self, event=None):
        self.set_theme(self.combo_theme.get())
        with open(self.fsn, 'w+') as file:
            file.write(self.combo_theme.get())



    def create_new_quiz(self, event=None):
        self.filename = ''
        filename = filedialog.askopenfilename(filetypes=(('Images', '*.png *.jpg *.jpeg *.jpeg_large *.jpg_large *.bmp *.gif'),
                                                         ('All', '*')))
        if not filename:
            return 'dick'
        try:
            img = Image.open(filename)
            width, height = img.width, img.height
            max_wh = max(width, height)
            new_width = int(width / max_wh * 1000)
            new_height = int(height / max_wh * 1000)
            img2 = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        except:
            msgbox.showerror('Error', 'Image cannot opens')
        self.imgframe.config(width=new_width, height=new_height)
        screen = pygame.display.set_mode((new_width, new_height))
        screen.fill(pygame.Color(255, 255, 255))

        pygame.display.update()
        mode = img2.mode
        size = img2.size
        data = img2.tobytes()
        self.packq = pack_mapqf.MapQuizPackFile(mode=mode, size=size, data=data)

        py_image = pygame.image.fromstring(data, size, mode)
        screen.blit(py_image, (250, 250))

        pygame.display.update()
        self.update()
        self.quizframe.pack(fill='both', expand=True)
        def on_exit(event=0):
            global running
            running = False
            pygame.quit()

        self.protocol('WM_DELETE_WINDOW', on_exit)
        running = True
        self.labels = dict()
        self.labels_val = []
        self.update_listbox_labels()
        self.entry_title.delete(0, 'end')
        self.tnxtxt_text.delete(1.0, 'end')
        my_font = pygame.font.SysFont('Arial', 10)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not event.pos in self.labels.keys():
                        n = simpledialog.askstring('Entry obj', "entry obj's name pls")
                        if not n in self.labels.values():
                            self.labels[event.pos] = n
                        self.labels_val = list(self.labels.values())
                        self.update_listbox_labels()
            screen.blit(py_image, (0, 0))
            for pos in self.labels.keys():
                txt = my_font.render(self.labels[pos], True, (255, 0, 0))
                screen.blit(txt, pos)
            pygame.display.update()
            self.update()

    def update_listbox_labels(self):
        self.listbox_labels.delete(0, 'end')
        for val in self.labels_val:
            self.listbox_labels.insert('end', val)

    def del_label_quiz(self):
        selind = self.listbox_labels.curselection()[0]
        val = self.listbox_labels.get(selind, selind)[0]
        new_dict = dict()
        for k in self.labels:
            if not self.labels[k] == val:
                new_dict[k] = self.labels[k]
        self.labels = new_dict
        self.labels_val = list(self.labels.values())
        self.update_listbox_labels()
    def open_and_modify_quiz(self, event=None):
        fn = filedialog.askopenfilename(filetypes=(('FotonTestSystem23 Quiz v2', '*.fts23v2'),))
        if not fn:
            return
        try:
            with open(fn, 'rb') as file:
                self.packq = pickle.load(file)
        except:
            msgbox.showerror('Error', 'file not supported')
            return
        self.filename = fn
        new_width = width = self.packq.size[0]
        new_height = height = self.packq.size[1]
        self.imgframe.config(width=new_width, height=new_height)
        screen = pygame.display.set_mode((new_width, new_height))
        screen.fill(pygame.Color(255, 255, 255))

        pygame.display.update()
        mode, size, data = self.packq.mode, self.packq.size, self.packq.data

        py_image = pygame.image.fromstring(data, size, mode)
        screen.blit(py_image, (250, 250))

        pygame.display.update()
        self.update()
        self.quizframe.pack(fill='both', expand=True)

        def on_exit(event=0):
            self.running = False
            pygame.quit()
            self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_exit)
        self.running = True
        self.labels = self.packq.labels
        self.labels_val = self.packq.labels.values()
        self.entry_title.delete(0, 'end')
        self.entry_title.insert('end', self.packq.title)
        self.tnxtxt_text.delete(1.0, 'end')
        self.tnxtxt_text.insert('end', self.packq.thanks_text)
        self.update_listbox_labels()
        my_font = pygame.font.SysFont('Arial', 10)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not event.pos in self.labels.keys():
                        n = simpledialog.askstring('Entry obj', "entry obj's name pls")
                        if not n in self.labels.values():
                            self.labels[event.pos] = n
                        self.labels_val = list(self.labels.values())
                        self.update_listbox_labels()
            screen.blit(py_image, (0, 0))
            for pos in self.labels.keys():
                txt = my_font.render(self.labels[pos], True, (255, 0, 0))
                screen.blit(txt, pos)
            pygame.display.update()
            self.update()

    def get_img_from_quiz(self, event=None):
        pygame.image.save(pygame.image.fromstring(*self.packq.img()), filedialog.asksaveasfilename(filetypes=(('PNG Image', '*.png'),), defaultextension='.png'))

    def saveas_quiz(self, event=None):
        fn = filedialog.asksaveasfilename(filetypes=(('FotonTestSystem23 Quiz v2', '*.fts23v2'),), defaultextension='.fts23v2')
        if not fn:
            return
        self.filename = fn
        self.packq.title = self.entry_title.get()
        self.packq.thanks_text = self.tnxtxt_text.get(1.0, 'end')
        self.packq.labels = self.labels
        with open(self.filename, 'wb') as f:
            pickle.dump(self.packq, f, protocol=5)
        msgbox.showinfo('Done!', f'Quiz has saved to: {self.filename}')
        

    def save_handle(self, event=None):
        if self.filename == '':
            self.saveas_quiz()
        else:
            self.save_quiz()

    def save_quiz(self, event=None):
        self.packq.title = self.entry_title.get()
        self.packq.thanks_text = self.tnxtxt_text.get(1.0, 'end')
        self.packq.labels = self.labels
        with open(self.filename, 'wb') as f:
            pickle.dump(self.packq, f, protocol=5)
        msgbox.showinfo('Done!', f'Quiz has saved to: {self.filename}')


if __name__ == '__main__':
    fsn = '.fotontestsystem2023mapquizgeneratorsettingsv2.0.sys'
    theme = 'black'
    try:
        with open(fsn) as file:
            theme = file.read()
    except:
        with open(fsn, 'w+') as file:
            file.write(theme)
    App(version=2.0, theme=theme, filename_settings = fsn).mainloop()