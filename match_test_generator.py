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
import tkinterclasses


def treeview_sort_column(tv, col, reverse):
    l = [(int(tv.set(k, col)) if col == 3 else tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
        treeview_sort_column(tv, col, not reverse))


class SettingsPackMatchTG:
    def __init__(self, title='Foton Test System 2023 Pro', theme='black', tests_lib=None, recent_files=None):
        self.title = title
        self.theme = theme
        if tests_lib is None:
            tests_lib = set()
        self.tests_lib = tests_lib
        self.recent_files = recent_files
        if self.recent_files is None:
            self.recent_files = []

    def __str__(self):
        return f"""
        < SettingsPack object at 0x{id(self)}
        title={self.title}
        theme={self.theme}
        tests_lib={self.tests_lib} >
        """


class App(ttkthemes.ThemedTk):
    def __init__(self, title='FTS23 MatchT Generator', fsn='.fotontestsystem2023matchtestgeneratorsettingsfile1.sys',
                 theme='black'):
        super().__init__()
        self.title(title)
        self.set_theme(theme)
        self.init_settings(fsn)
        self.style = ttkthemes.ThemedStyle()
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack(fill='both', expand=1)
        self.notebook = ttk.Notebook(self.mainframe)
        self.notebook.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
        self.init_file_tab()
        self.init_test_tab()
        self.init_settings_tab()
        self.geometry('700x400+100+100')
        self.init_settings(fsn)
        self.commit_settings()
        self.style.configure('TNotebook.Tab', width=20, padding=[50, 15])
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self.style.configure('lefttab.TNotebook.Tab', width=20, padding=[50, 15])

    def init_settings(self, fsn):
        self.filename_settings = fsn
        try:
            with open(self.filename_settings, 'rb') as file:
                self.settings_pack = pickle.load(file)
        except:
            self.settings_pack = SettingsPackMatchTG()
        self.set_theme(self.settings_pack.theme)
        self.title(self.settings_pack.title)
        self.settings_pack.tests_lib = set(self.settings_pack.tests_lib)
    def init_test_tab(self):
        self.tab_test = ttk.Frame(self.notebook)
        self.tab_test.pack(fill='both', expand=1)
        self.notebook.add(self.tab_test, text='Редактор')
        self.tab_test_paned = ttk.PanedWindow(self.tab_test, orient=tk.HORIZONTAL)
        self.tab_test_paned.pack(fill='both', expand=1)
        self.tab_test_lf_pairs = ttk.LabelFrame(self.tab_test_paned, text='Редактор пар')
        self.tab_test_paned.add(self.tab_test_lf_pairs, weight=1)
        self.tab_test_tool_frame = ttk.Frame(self.tab_test_lf_pairs, height=50)
        self.tab_test_tool_frame.pack(fill='x')
        self.tab_test_butt_add = ttk.Button(self.tab_test_tool_frame, text='Добавить пару')
        self.tab_test_butt_add.place(relx=0, rely=0, anchor='nw', relwidth=0.4, relheight=1)
        self.tab_test_butt_del = ttk.Button(self.tab_test_tool_frame, text='Удалить пару')
        self.tab_test_butt_del.place(relx=0.4, rely=0, anchor='nw', relwidth=0.4, relheight=1)
        self.tab_test_butt_edit = ttk.Button(self.tab_test_tool_frame, text='Изменить\nпару')
        self.tab_test_butt_edit.place(relx=0.8, rely=0, anchor='nw', relwidth=0.2, relheight=1)
        self.test_tab_tv_frame = ttk.LabelFrame(self.tab_test_lf_pairs, text='Пары')
        self.test_tab_tv_frame.pack(fill='both', expand=1)
        columns = ("#1", "#2", "#3")
        self.test_tab_treeview_tests = ttk.Treeview(self.test_tab_tv_frame, show="headings", columns=columns)
        self.test_tab_treeview_tests.heading("#1", text="ID")
        self.test_tab_treeview_tests.heading("#2", text="Ключ")
        self.test_tab_treeview_tests.heading("#3", text="Значение")
        self.treetestysb = ttk.Scrollbar(self.test_tab_tv_frame, orient=tk.VERTICAL,
                                         command=self.test_tab_treeview_tests.yview)
        self.test_tab_treeview_tests.configure(yscroll=self.treetestysb.set)
        self.test_tab_treeview_tests.pack(side='left', fill='both', expand=True)
        self.treetestysb.pack(side='right', fill='y')
        treeview_sort_column(self.test_tab_treeview_tests, 0, False)
        treeview_sort_column(self.test_tab_treeview_tests, 1, False)
        treeview_sort_column(self.test_tab_treeview_tests, 2, False)
        self.tab_test_invert_frame = ttk.Frame(self.tab_test_lf_pairs, height=50)
        self.tab_test_invert_frame.pack(fill='x')
        self.tab_test_butt_i_pair = ttk.Button(self.tab_test_invert_frame, text='Инвертировать\nпару')
        self.tab_test_butt_i_pair.place(relx=0, rely=0, anchor='nw', relwidth=0.5, relheight=1)
        self.tab_test_butt_i_pairs = ttk.Button(self.tab_test_invert_frame, text='Инвертировать\nвсе пары')
        self.tab_test_butt_i_pairs.place(relx=0.5, rely=0, anchor='nw', relwidth=0.5, relheight=1)
        self.tab_test_lf_el = ttk.LabelFrame(self.tab_test_paned, text='Редактор элемента')
        self.tab_test_paned.add(self.tab_test_lf_el, weight=1)
        self.tab_test_el_example_butt_1 = ttk.Button(self.tab_test_lf_el, text='Пример', style='example.TButton')
        self.tab_test_el_example_butt_1.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20)
        self.tab_test_el_example_butt_2 = ttk.Button(self.tab_test_lf_el, text='Пример', style='example.TButton')
        self.tab_test_el_example_butt_2.grid(row=1, column=0, padx=20, pady=20, ipadx=20, ipady=20)
        self.tab_test_el_example_lab = ttk.Label(self.tab_test_lf_el, text='Пример', style='example.TLabel')
        self.tab_test_el_example_lab.grid(row=1, column=0, sticky='se')


    def commit_settings(self, event=None):
        with open(self.filename_settings, 'wb') as file:
            pickle.dump(self.settings_pack, file)
        print('settings have commited')
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self.style.configure('lefttab.TNotebook.Tab', width=20, padding=[80, 20])

    def init_file_tab(self):
        self.tab_file = ttk.Frame(self.notebook)
        self.tab_file.pack(fill='both', expand=1)
        self.notebook.add(self.tab_file, text='Файл')
        self.tab_file_vnotebook = ttk.Notebook(self.tab_file, style='lefttab.TNotebook')
        self.tab_file_vnotebook.pack(fill='both', expand=1)
        self.tab_file_tab_recent = ttk.Frame(self.tab_file_vnotebook)
        self.tab_file_tab_recent.pack(fill='both', expand=1)
        self.tab_file_vnotebook.add(self.tab_file_tab_recent, text=' Последнее ', padding=2,)
        self.id_recent=0
        self.update_recent_tab()
        self.tab_file_tab_lib = ttk.Frame(self.tab_file_vnotebook)
        self.tab_file_tab_lib.pack(fill='both', expand=1)
        self.tab_file_vnotebook.add(self.tab_file_tab_lib, text=' Библиотека', padding=2)
        self.init_tab_file_lib_tab()
        self.id_lib = 1
        self.tab_file_tab_save = ttk.Frame(self.tab_file_vnotebook)
        self.tab_file_tab_save.pack(fill='both', expand=1)
        self.tab_file_vnotebook.add(self.tab_file_tab_save, text=' Сохранить ', padding=2)
        self.init_tab_file_save_tab()
        self.tab_file_tab_create = ttk.Frame(self.tab_file_vnotebook)
        self.tab_file_tab_create.pack(fill='both', expand=1)
        self.tab_file_vnotebook.add(self.tab_file_tab_create, text='  Создать  ', padding=2)
        self.init_tab_file_create_tab()
        self.tab_file_tab_open = ttk.Frame(self.tab_file_vnotebook)
        self.tab_file_tab_open.pack(fill='both', expand=1)
        self.tab_file_vnotebook.add(self.tab_file_tab_open, text='  Открыть  ', padding=2)
        self.init_tab_file_open_tab()
    def init_tab_file_open_tab(self):
        self.tab_file_tab_open_butt_open = ttk.Button(self.tab_file_tab_open, text='Открыть файл в проводнике Windows ...')
        self.tab_file_tab_open_butt_open.grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10, sticky='nsew')
        self.tab_file_tab_open_butt_lib = ttk.Button(self.tab_file_tab_open,
                                                      text='Открыть в библиотеке тестов ...', command=lambda e=None: self.tab_file_vnotebook.select(self.id_lib))
        self.tab_file_tab_open_butt_lib.grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10, sticky='nsew')
        self.tab_file_tab_open_butt_rec = ttk.Button(self.tab_file_tab_open,
                                                      text='Последние файлы ...', command=lambda e=None: (self.tab_file_vnotebook.select(self.id_recent), print(self.id_recent)))
        self.tab_file_tab_open_butt_rec.grid(row=2, column=0, ipadx=10, ipady=15, padx=10, pady=10, sticky='nsew')
    def init_tab_file_create_tab(self):
        self.tab_file_tab_create_butt_create = ttk.Button(self.tab_file_tab_create, text='Создать новый пустой тест на соответствие элементов', command=self.fontchoose)
        self.tab_file_tab_create_butt_create.grid(row=0, column=0, ipadx=10, ipady=15,
                                                padx=10, pady=10)
    def init_tab_file_save_tab(self):
        self.tab_file_tab_save_entry = ttk.Entry(self.tab_file_tab_save, width=100)
        self.tab_file_tab_save_entry.grid(row=0, column=0, sticky='e', padx=[10, 0], pady=10, ipadx=10, ipady=15)
        self.tab_file_tab_save_butt_se = ttk.Button(self.tab_file_tab_save, text='Сохранить')
        self.tab_file_tab_save_butt_se.grid(row=0, column=1, sticky='w', padx=[0, 10], pady=10, ipadx=10, ipady=15)
        self.tab_file_tab_save_butt_saveas = ttk.Button(self.tab_file_tab_save,
                                                        text='Сохранить как ... в проводнике Windows')
        self.tab_file_tab_save_butt_saveas.grid(row=1, column=0, columnspan=2, sticky='nsew', ipadx=10, ipady=15, padx=10, pady=10)

    def init_tab_file_lib_tab(self):
        self.tab_file_tab_lib_tool_frame = ttk.Frame(self.tab_file_tab_lib, height=50)
        self.tab_file_tab_lib_tool_frame.pack(fill='x')
        self.tab_file_tab_lib_butt_delete = ttk.Button(self.tab_file_tab_lib_tool_frame,
                                                       text='Удалить тест из библиотеки')
        self.tab_file_tab_lib_butt_delete.place(relx=0.5, rely=0, relheight=1, relwidth=0.5, anchor='nw')
        self.tab_file_tab_lib_butt_open = ttk.Button(self.tab_file_tab_lib_tool_frame, text='Открыть тест')
        self.tab_file_tab_lib_butt_open.place(relx=0, rely=0, relheight=1, relwidth=0.5, anchor='nw')
        self.tab_file_tab_lib_tv_frame = ttk.Frame(self.tab_file_tab_lib)
        self.tab_file_tab_lib_tv_frame.pack(fill='both', expand=1)
        columns = ("#1", "#2", "#3")
        self.tab_file_tab_lib_treeview_tests = ttk.Treeview(self.tab_file_tab_lib_tv_frame, show="headings",
                                                            columns=columns)
        self.tab_file_tab_lib_treeview_tests.heading("#1", text="ID")
        self.tab_file_tab_lib_treeview_tests.heading("#2", text="Название")
        self.tab_file_tab_lib_treeview_tests.heading("#3", text="Файл")
        self.tab_file_tab_lib_treeysb = ttk.Scrollbar(self.tab_file_tab_lib_tv_frame, orient=tk.VERTICAL,
                                                      command=self.tab_file_tab_lib_treeview_tests.yview)
        self.tab_file_tab_lib_treeview_tests.configure(yscroll=self.tab_file_tab_lib_treeysb.set)
        self.tab_file_tab_lib_treeview_tests.pack(side='left', fill='both', expand=True)
        self.tab_file_tab_lib_treeysb.pack(side='right', fill='y')
        treeview_sort_column(self.tab_file_tab_lib_treeview_tests, 0, False)
        treeview_sort_column(self.tab_file_tab_lib_treeview_tests, 1, False)
        treeview_sort_column(self.tab_file_tab_lib_treeview_tests, 2, False)

    def update_recent_tab(self, event=None):
        try:
            print(self.tab_file_tab_recent_list_of_labels)
        except:
            self.tab_file_tab_recent_list_of_labels = []
        if self.settings_pack.recent_file is None:
            self.settings_pack.recent_file = []
        while len(self.settings_pack.recent_file) > 10:
            self.settings_pack.recent_file.pop(0)
        self.commit_settings()
        for l in self.tab_file_tab_recent_list_of_labels:
            l.destroy()
        self.tab_file_tab_recent_list_of_labels = []
        for file in self.settings_pack.recent_file:
            try:
                with open(file, 'rb') as f:
                    t = pickle.load(f)
                title = t.title
                self.tab_file_tab_recent_list_of_labels.append(ttk.LabelFrame(self.tab_file_tab_recent))
                self.tab_file_tab_recent_list_of_labels[-1].pack(fill='x', ipadx=100, ipady=20, padx=10, pady=10)
                self.tab_file_tab_recent_list_of_labels.append(
                    ttk.Label(self.tab_file_tab_recent_list_of_labels[-1], text=title, style='large.TLabel'))
                self.tab_file_tab_recent_list_of_labels[-1].place(relx=0, rely=0, anchor='nw')
                self.tab_file_tab_recent_list_of_labels.append(
                    ttk.Label(self.tab_file_tab_recent_list_of_labels[-2], text=file))
                self.tab_file_tab_recent_list_of_labels[-1].place(relx=1, rely=1, anchor='se')
                self.tab_file_tab_recent_list_of_labels.append(ttk.Button(self.tab_file_tab_recent_list_of_labels[-3], text='Добавить в библиотеку'))
                self.tab_file_tab_recent_list_of_labels[-1].place(relx=1, rely=0.5, anchor='e')
            except:
                pass
        if len(self.tab_file_tab_recent_list_of_labels) == 0:
            self.tab_file_tab_recent_list_of_labels.append(
                ttk.Label(self.tab_file_tab_recent, text='Последних файлов нет...', style='large.TLabel'))
            self.tab_file_tab_recent_list_of_labels[-1].pack(fill='both', expand=1)

    def init_settings_tab(self):
        self.settings_tab = ttk.Frame(self.notebook)
        self.settings_tab.pack(fill='both', expand=1)
        self.notebook.add(self.settings_tab, text='Настройки')
        ttk.Label(self.settings_tab, text='Тема:').grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10)
        self.settings_tab_combo_theme = ttk.Combobox(self.settings_tab, values=self.style.get_themes())
        self.settings_tab_combo_theme.grid(row=0, column=1, columnspan=2, ipadx=10, ipady=15, padx=10, pady=10, sticky='we')
        self.settings_tab_combo_theme.bind("<<ComboboxSelected>>", self.select_theme)
        ttk.Label(self.settings_tab, text='Название:').grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10)
        self.settings_tab_entry_title = ttk.Entry(self.settings_tab, width=len(self.settings_pack.title) + 5)
        self.settings_tab_entry_title.grid(row=1, column=1, ipadx=10, ipady=15, padx=10, pady=10)
        self.settings_tab_entry_title.insert('end', self.settings_pack.title)
        self.settings_tab_butt_title = ttk.Button(self.settings_tab, text='Сменить название', command=self.change_title)
        self.settings_tab_butt_title.grid(row=1, column=2, ipadx=10, ipady=15, padx=10, pady=10)

    def change_title(self, event=None):
        self.settings_pack.title = self.settings_tab_entry_title.get()
        self.settings_tab_entry_title.config(width=len(self.settings_pack.title) + 5)
        self.title(self.settings_pack.title)
        self.commit_settings()

    def select_theme(self, event=None):
        self.settings_pack.theme = self.settings_tab_combo_theme.get()
        self.set_theme(self.settings_pack.theme)

        self.commit_settings()

    def fontchoose(self, event=None, default_font=None):
        if type(default_font) == type(list()):
            default_font = ' '.join(list(map(str, default_font)))
        if default_font is None:
            default_font = 'TkDefaultFont'
        self.__font_from_font_chooser = 'TkDefaultFont'
        def font_changed(font):
            self.__font_from_font_chooser = font

        self.tk.call('tk', 'fontchooser', 'configure','-font', default_font, '-command', self.register(font_changed))
        self.tk.call('tk', 'fontchooser', 'show')
        print('choosed',self.__font_from_font_chooser)
        return self.__font_from_font_chooser


if __name__ == '__main__':
    App().mainloop()
