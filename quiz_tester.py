import os
import pygame
import random
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog, simpledialog
import pickle
import pack_mapqf
import ttkthemes
from tkinter import messagebox as msgbox
import tkinter.messagebox

import testclasses


def treeview_sort_column(tv, col, reverse):
    l = [(int(tv.set(k, col)) if col == 3 else tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
        treeview_sort_column(tv, col, not reverse))

class SettingsPack:
    def __init__(self, title='Foton Test System 2023 Pro', theme='black', tests=None):
        self.title = title
        self.theme = theme
        if tests is None:
            tests=set()
        self.tests = tests

    def __str__(self):
        return f"""
        < SettingsPack object at 0x{id(self)}
        title={self.title}
        theme={self.theme}
        tests={self.tests} >
        """


class App(ttkthemes.ThemedTk):
    def __init__(self, title='Foton Test System 2023 Pro', fsn='.fotontestsystem2023mainapptestersettingsfile1.sys',  theme='black'):
        super().__init__()
        self.title(title)
        self.set_theme(theme)
        self.init_settings(fsn)
        self.style = ttkthemes.ThemedStyle()
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill='both', expand=1)
        self.notebook = ttk.Notebook(self.mainframe)
        self.notebook.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
        self.init_test_tab()
        self.init_settings_tab()
        self.update_tv_tests()
        self.geometry('700x400+100+100')
        self.test = None


    def init_settings(self,fsn):
        self.filename_settings = fsn
        try:
            with open(self.filename_settings, 'rb') as file:
                self.settings_pack = pickle.load(file)
        except:
            self.settings_pack = SettingsPack()
        self.set_theme(self.settings_pack.theme)
        self.title(self.settings_pack.title)
        if type(self.settings_pack.tests) == type(list()):
            self.settings_pack.tests = set(self.settings_pack.tests)

    def init_test_tab(self):
        self.test_tab = ttk.Frame(self.notebook)
        self.test_tab.pack(fill='both', expand=1)
        self.notebook.add(self.test_tab, text='Тесты')
        self.test_tab_labelframe_operate_tests = ttk.LabelFrame(self.test_tab, height=60)
        self.test_tab_labelframe_operate_tests.pack(fill='x')
        self.test_tab_butt_add_test = ttk.Button(self.test_tab_labelframe_operate_tests, text='Добавить тест +', command=self.add_test)
        self.test_tab_butt_add_test.place(relx=0, rely=0, anchor='nw', relwidth=0.33, relheight=1)
        self.test_tab_butt_launch_test = ttk.Button(self.test_tab_labelframe_operate_tests, text='Запустить тест', command=self.launch_test)
        self.test_tab_butt_launch_test.place(relx=0.33, rely=0, relheight=1, relwidth=0.34, anchor='nw')
        self.test_tab_butt_del_test = ttk.Button(self.test_tab_labelframe_operate_tests, text='Удалить тест -', command=self.delete_test)
        self.test_tab_butt_del_test.place(relx=0.67, rely=0, relheight=1, relwidth=0.33, anchor='nw')
        self.test_tab_tv_frame = ttk.LabelFrame(self.test_tab)
        self.test_tab_tv_frame.pack(fill='both', expand=1)
        columns = ("#1", "#2", "#3")
        self.test_tab_treeview_tests = ttk.Treeview(self.test_tab_tv_frame, show="headings", columns=columns)
        self.test_tab_treeview_tests.heading("#1", text="ID")
        self.test_tab_treeview_tests.heading("#2", text="Название")
        self.test_tab_treeview_tests.heading("#3", text="Файл")
        self.treetestysb = ttk.Scrollbar(self.test_tab_tv_frame, orient=tk.VERTICAL, command=self.test_tab_treeview_tests.yview)
        self.test_tab_treeview_tests.configure(yscroll=self.treetestysb.set)
        self.test_tab_treeview_tests.pack(side='left', fill='both', expand=True)
        self.treetestysb.pack(side='right', fill='y')
        treeview_sort_column(self.test_tab_treeview_tests, 0, False)
        treeview_sort_column(self.test_tab_treeview_tests, 1, False)
        treeview_sort_column(self.test_tab_treeview_tests, 2, False)



    def delete_test(self, event=None):
        cur = self.test_tab_treeview_tests.focus()
        it = self.test_tab_treeview_tests.item(cur)
        filename = it['values'][2]
        self.settings_pack.tests.remove(filename)
        self.update_tv_tests()


    def launch_test(self,ent=None):
        cur = self.test_tab_treeview_tests.focus()
        it = self.test_tab_treeview_tests.item(cur)
        filename = it['values'][2]
        try:
            with open(filename, 'rb') as file:
                pack = pickle.load(file)
        except:
            msgbox.showerror('Ошибка', 'Ошибка при считывании файла, либо открытия, либо загрузки файла')

        if filename.endswith('.fts23v2'):
            try:
                self.test = testclasses.MAPQuiZ(self.mainframe, packq=pack, root=self, close_handle=self.on_close_test)
                self.test.place(relx=0, rely=0, anchor='nw', relheight=1, relwidth=1)
                self.test.start()
            except:
                msgbox.showerror('Ошибка', 'Ошибка при создании теста, видимо данные упакованы не в том формате')
        elif filename.endswith('.fts23m'):
            try:
                self.test = testclasses.TNABaseUG(self.mainframe, packq=pack, root=self, close_handle=self.on_close_test)
                self.test.place(relx=0, rely=0, anchor='nw', relheight=1, relwidth=1)
                self.test.start()
            except:
                msgbox.showerror('Ошибка', 'Ошибка при создании теста, видимо данные упакованы не в том формате')

    def commit_settings(self, event=None):
        with open(self.filename_settings, 'wb') as file:
            pickle.dump(self.settings_pack, file)
    def add_test(self, event=None):
        filename = filedialog.askopenfilename(filetypes=(('FTS23 Карта-Тест V2 .fts23v2', '*.fts23v2'), ('FTS23 ТестСоответвие',  '*.fts23m')))
        self.settings_pack.tests.add(filename)
        self.update_tv_tests()


    def update_tv_tests(self, event=None):
        self.commit_settings()
        self.test_tab_treeview_tests.delete(*self.test_tab_treeview_tests.get_children())
        for test in self.settings_pack.tests:
            try:
                with open(test, 'rb') as file:
                    packq = pickle.load(file)
                t = packq.title
                self.test_tab_treeview_tests.insert('', 'end', values=(str(id(packq)), t, test))
            except:
                self.test_tab_treeview_tests.insert('', 'end', values=('ошибка', 'ошибка - удали этот тест', test))

    def init_settings_tab(self):
        self.settings_tab = ttk.Frame(self.notebook)
        self.settings_tab.pack(fill='both', expand=1)
        self.notebook.add(self.settings_tab, text='Настройки')
        ttk.Label(self.settings_tab, text='Тема:').grid(row=0, column=0, pady=5, padx=5, ipadx=2, ipady=2)
        self.settings_tab_combo_theme = ttk.Combobox(self.settings_tab, values=self.style.get_themes())
        self.settings_tab_combo_theme.grid(row=0, column=1, columnspan=2, padx=5, pady=5, ipadx=2, ipady=2, sticky='we')
        self.settings_tab_combo_theme.bind("<<ComboboxSelected>>", self.select_theme)
        ttk.Label(self.settings_tab, text='Название:').grid(row=1, column=0, ipadx=2, ipady=2, padx=5, pady=5)
        self.settings_tab_entry_title = ttk.Entry(self.settings_tab, width=len(self.settings_pack.title)+5)
        self.settings_tab_entry_title.grid(row=1, column=1, padx=5, pady=5, ipadx=2, ipady=2)
        self.settings_tab_entry_title.insert('end', self.settings_pack.title)
        self.settings_tab_butt_title = ttk.Button(self.settings_tab, text='Сменить название', command=self.change_title)
        self.settings_tab_butt_title.grid(row=1, column=2, padx=5, pady=5, ipadx=2, ipady=2)

    def change_title(self, event=None):
        self.settings_pack.title = self.settings_tab_entry_title.get()
        self.settings_tab_entry_title.config(width=len(self.settings_pack.title)+5)
        self.title(self.settings_pack.title)
        self.commit_settings()
    def select_theme(self, event=None):
        self.set_theme(self.settings_tab_combo_theme.get())
        self.settings_pack.theme = self.settings_tab_combo_theme.get()
        self.commit_settings()
    def on_close_test(self, event=None):
        self.test = None


if __name__ == '__main__':
    App().mainloop()