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

import testclasses
import tkinterclasses


def treeview_sort_column(tv, col, reverse):
    """
    Функция включает сортировку в Treeview по нажатию на заголовок колонки, по содержимому этой колонки
    Enable sort in ttk.Treeview by click on heading of column, sorting by values of column
    :param tv: tkinter.ttk.Treeview
    :param col: number of column
    :param reverse: boolean
    :return: Nothing
    """
    l = [(int(tv.set(k, col)) if col == 3 else tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
        treeview_sort_column(tv, col, not reverse))


class SettingsPackMatchTG:
    """
    Пак для настроек для MatchGenerator
    """

    def __init__(self, title='Foton Test System 2023 Pro', theme='black', tests_lib=None, recent_files=None):
        """
        Пак для настроек для FTS23 MatchGenerator
        :param title: название
        :param theme: тема
        :param tests_lib: библиотека тестов - список файлов
        :param recent_files: последние файлы - список до 10 файлов
        """
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

        self.init_settings_tab()
        self.init_test_tab()
        self.geometry('700x400+100+100')
        self.init_settings(fsn)
        self.commit_settings()
        self.update_library()
        self.style.configure('TNotebook.Tab', width=20, padding=[50, 15])
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self.style.configure('lefttab.TNotebook.Tab', width=20, padding=[50, 15])
        self.style.configure('large.TLabel', font='{Segoe UI} 15')
        self.notebook.hide(2)
        self.filename = ''

    def init_settings(self, fsn):
        """
        Docs:
        Initializes settings file and loads settings from it to the app
        Инициализирует файл с настройками и загружает сохраненные настройки в программу
        :param fsn: settings filename
        :return: nothing
        """
        self.filename_settings = fsn
        if os.path.isfile(self.filename_settings):
            try:
                # try to open the settings file
                with open(self.filename_settings,
                          'rb') as file:  # open file with 'rb' mode, because pickle saves it in binary format
                    self.settings_pack = pickle.load(file)  # load pickled settings
            except:
                # creating a new settings package for app
                self.settings_pack = SettingsPackMatchTG()
        else:
            # handle if settings file is directory and app can not save settings
            msgbox.showerror(title='Ошибка', message='Файл настроек не существует')
            msgbox.showerror(title='Critical error',
                             message='Application can not load settings file and settings and can not save settings')
            msgbox.showerror(title='Critical error',
                             message=f'Delete file {os.getcwd()}\\{fsn} and restart application')
            msgbox.showerror(title='Critical error',
                             message=f'Delete directory {os.getcwd()}\\{fsn} and restart application')
        self.set_theme(self.settings_pack.theme)  # set the theme from settings
        self.title(self.settings_pack.title)  # set the title from settings
        self.settings_pack.tests_lib = list(set(self.settings_pack.tests_lib))

    def init_settings_tab(self):
        """
        Method to initialize the settings tab with the given settings
        :return: nothing
        """
        self.settings_tab = ttk.Frame(self.notebook)  # create the tab frame
        self.settings_tab.pack(fill='both', expand=1)  # pack the tab
        self.notebook.add(self.settings_tab, text='Настройки')  # add the tab to the notebook
        ttk.Label(self.settings_tab, text='Тема:').grid(row=0, column=0, ipadx=10, ipady=15, padx=10,
                                                        pady=10)  # create and grid label with 'theme' label to the tab
        self.settings_tab_combo_theme = ttk.Combobox(self.settings_tab,
                                                     values=self.style.get_themes())  # add the combobox to the tab to choose the theme
        self.settings_tab_combo_theme.grid(row=0, column=1, columnspan=2, ipadx=10, ipady=15, padx=10, pady=10,
                                           sticky='we')  # grid combobox
        self.settings_tab_combo_theme.bind("<<ComboboxSelected>>",
                                           self.select_theme)  # bind the combobox for selection events to select the theme
        ttk.Label(self.settings_tab, text='Название:').grid(row=1, column=0, ipadx=10, ipady=15, padx=10,
                                                            pady=10)  # add label with 'title' label to the tab and grid it
        self.settings_tab_entry_title = ttk.Entry(self.settings_tab, width=len(
            self.settings_pack.title) + 5)  # add entry title to the tab and grid it
        self.settings_tab_entry_title.grid(row=1, column=1, ipadx=10, ipady=15, padx=10, pady=10)
        self.settings_tab_entry_title.insert('end',
                                             self.settings_pack.title)  # insert title from the settings file to the entry
        self.settings_tab_butt_title = ttk.Button(self.settings_tab, text='Сменить название',
                                                  command=self.change_title)  # add button to changing title
        self.settings_tab_butt_title.grid(row=1, column=2, ipadx=10, ipady=15, padx=10, pady=10)  # grid this button

    def init_test_tab(self):
        """
        Создает вкладку с редактором теста
        :return: nothing / None
        """
        # Главный фрейм вкладки
        self.tab_test = ttk.Frame(self.notebook)
        self.tab_test.pack(fill='both', expand=1)
        self.notebook.add(self.tab_test, text='Редактор')  # Добавляем вкладку к Notebook
        ### tool frame=============================
        if 'tool frame':
            # Фрейм для мета-информации теста
            self.test_tab_tool = ttk.Frame(self.tab_test)
            self.test_tab_tool.pack(fill='x')  # горизонтально растягиваем
            # Надпись про название
            self.test_tab_label_title = ttk.Label(self.test_tab_tool, text='Название')
            self.test_tab_label_title.grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10, rowspan=2)
            # Поле ввода для названия
            self.test_tab_entry_title = ttk.Entry(self.test_tab_tool, width=69)
            self.test_tab_entry_title.grid(row=0, column=1, ipadx=10, ipady=15, padx=10, pady=10, rowspan=2)
            # Надпись про благодарность
            self.test_tab_label_title = ttk.Label(self.test_tab_tool, text='Благодарность\nза прохождение')
            self.test_tab_label_title.grid(row=0, column=2, ipadx=10, ipady=15, padx=10, pady=10, rowspan=2)
            # Текст для благодарности
            self.test_tab_tnx_text = tk.Text(self.test_tab_tool, width=33, height=3, bg='white',
                                             relief=tk.FLAT)  # Делаем плоский рельеф для более нормального стиля
            self.test_tab_tnx_text.grid(row=0, column=3, padx=[10, 0], pady=2,
                                        sticky='ns',
                                        )  # Делаем padx (10, 0) для того чтобы текст примыкал к скроллу
            # Скролл для текста
            self.test_tab_tnx_ysb = ttk.Scrollbar(self.test_tab_tool, orient=tk.VERTICAL,  # Вертикальный
                                                  command=self.test_tab_tnx_text.yview)
            self.test_tab_tnx_ysb.grid(row=0, column=4, padx=[0, 10], pady=2,
                                       sticky='ns')  # padx=(0,10) чтобы примыкал к тексту + прилипание север-юг чтобы растянуть сверху вниз
            # Прикрепляем к тексту комманду изменения скролла
            self.test_tab_tnx_text.config(yscrollcommand=self.test_tab_tnx_ysb.set)
            self.test_tab_label_width = ttk.Label(self.test_tab_tool, text='Ширина в кнопках')
            self.test_tab_label_width.grid(row=0, column=5, ipady=15, padx=5)
            self.test_tab_spinbox_width = ttk.Spinbox(self.test_tab_tool, from_=0, to=30)
            self.test_tab_spinbox_width.grid(row=0, column=6, padx=5)
            self.test_tab_spinbox_width.set(0)
            # make new button to display size configuration
            self.test_tab_button_size = ttk.Button(self.test_tab_tool, text='Показать сетку кнопок',
                                                   command=self.show_table_of_buttons)
            self.test_tab_button_size.grid(row=0, column=7, ipady=15, padx=5)
            self.test_tab_button_add_to_library = ttk.Button(self.test_tab_tool, text='Добавить в библиотеку',
                                                             command=self.add_test_to_library)
            self.test_tab_button_add_to_library.grid(row=0, column=8, ipady=15, padx=5)
            self.test_tab_button_add_to_library.config(state='disabled')

        # делаем panedwindow горизонтальный
        self.tab_test_paned = ttk.PanedWindow(self.tab_test, orient=tk.HORIZONTAL)
        self.tab_test_paned.pack(fill='both', expand=1)  # Растягиваем во все стороны
        # Фрейм с подписью для редактора пар
        self.tab_test_lf_pairs = ttk.LabelFrame(self.tab_test_paned, text='Редактор пар')
        self.tab_test_paned.add(self.tab_test_lf_pairs, weight=1)  # Добавляем фрейм к panedwindow
        ################################ кнопки сверху =================================================================
        if 'кнопки сверху фрейм':
            # Фрейм для кнопок сверху
            self.tab_test_tool_frame = ttk.Frame(self.tab_test_lf_pairs, height=50)
            self.tab_test_tool_frame.pack(fill='x')  # Растягиваем горизонтально
            # Кнопка для добавления пары
            self.tab_test_butt_add = ttk.Button(self.tab_test_tool_frame, text='Добавить пару',
                                                command=self.add_test_pair)
            self.tab_test_butt_add.place(relx=0, rely=0, anchor='nw', relwidth=0.4, relheight=1)  # прикрепляем для 4/10
            # Кнопка для удаления пары
            self.tab_test_butt_del = ttk.Button(self.tab_test_tool_frame, text='Удалить пару',
                                                command=self.del_test_pair)
            self.tab_test_butt_del.place(relx=0.4, rely=0, anchor='nw', relwidth=0.4,
                                         relheight=1)  # Прикрепляем для еще 4/10
            # Кнопка для изменения пары
            self.tab_test_butt_edit = ttk.Button(self.tab_test_tool_frame, text='Изменить\nпару',
                                                 command=self.edit_test_pair)
            self.tab_test_butt_edit.place(relx=0.8, rely=0, anchor='nw', relwidth=0.2,
                                          relheight=1)  # Прикрепляем для последних 2/10
        # Фрейм с надписью Пары для таблицы со скроллом
        if 'фрейм с надписью пары для таблиц':
            self.test_tab_tv_frame = ttk.LabelFrame(self.tab_test_lf_pairs, text='Пары')
            self.test_tab_tv_frame.pack(fill='both', expand=1)  # Растягиваем его во все стороны
            columns = ("#1", "#2", "#3")  # начальные номера для разметки заголовков
            self.test_tab_treeview_tests = ttk.Treeview(self.test_tab_tv_frame, show="headings", columns=columns)
            self.test_tab_treeview_tests.heading("#1", text="ID")  # Первый заголовок
            self.test_tab_treeview_tests.heading("#2", text="Ключ")  # Второй заголовок
            self.test_tab_treeview_tests.heading("#3", text="Значение")  # Третий заголовок
            # Ставим вертикальный скролл для таблицы
            self.treetestysb = ttk.Scrollbar(self.test_tab_tv_frame, orient=tk.VERTICAL,
                                             command=self.test_tab_treeview_tests.yview)
            self.test_tab_treeview_tests.configure(yscroll=self.treetestysb.set)  # Привязываем команду скролла
            self.test_tab_treeview_tests.pack(side='left', fill='both',
                                              expand=True)  # Пакуем влево с растяжкой во все стороны
            self.treetestysb.pack(side='right', fill='y')  # Пакуем справо с вертикальной растяжкой
            treeview_sort_column(self.test_tab_treeview_tests, 0, False)  # Включаем сортировку для первого столбца
            treeview_sort_column(self.test_tab_treeview_tests, 1, False)  # Включаем сортировку для второго столбца
            treeview_sort_column(self.test_tab_treeview_tests, 2, False)  # Включаем сортировку для третьего столбца
            self.test_tab_treeview_tests.bind('<<TreeviewSelect>>', self.show_selected_el)
        # Фрейм для кнопок инвертирования снизу
        if 'фрейм для кнопок инвертирования снизу':
            self.tab_test_invert_frame = ttk.Frame(self.tab_test_lf_pairs, height=50)  # Высотой 50 пикселей
            self.tab_test_invert_frame.pack(fill='x')  # Растягиваем горизонтально
            # Кнопка инвертирования пары
            self.tab_test_butt_i_pair = ttk.Button(self.tab_test_invert_frame, text='Инвертировать\nпару',
                                                   command=self.invert_test_pair)
            self.tab_test_butt_i_pair.place(relx=0, rely=0, anchor='nw', relwidth=0.5, relheight=1)
            self.tab_test_butt_i_pairs = ttk.Button(self.tab_test_invert_frame, text='Инвертировать\nвсе пары',
                                                    command=self.invert_test_pairs_all)
            self.tab_test_butt_i_pairs.place(relx=0.5, rely=0, anchor='nw', relwidth=0.5, relheight=1)
        # редактор элемента --------------------
        if 'редактор элемента':
            self.tab_test_lf_el = ttk.LabelFrame(self.tab_test_paned, text='Редактор элемента')
            self.tab_test_paned.add(self.tab_test_lf_el, weight=1)
            self.tab_test_el_paned = ttk.PanedWindow(self.tab_test_lf_el, orient=tk.VERTICAL)
            self.tab_test_el_paned.pack(fill='both', expand=1)
            self.tab_test_lf_examples = ttk.LabelFrame(self.tab_test_lf_el, text='Примеры')
            self.tab_test_el_paned.add(self.tab_test_lf_examples, weight=1)

            self.tab_test_el_example_butt_1 = ttk.Button(self.tab_test_lf_examples, text='ExampleПример',
                                                         style='example.TButton')
            self.tab_test_el_example_butt_1.grid(row=0, column=0)
            self.tab_test_el_example_butt_2 = ttk.Button(self.tab_test_lf_examples, text='ExampleПример',
                                                         style='example.TButton')
            self.tab_test_el_example_butt_2.grid(row=0, column=1)
            self.tab_test_el_example_lab = ttk.Label(self.tab_test_lf_examples, text='ExampleПример',
                                                     style='example.TLabel')
            self.tab_test_el_example_lab.grid(row=0, column=1, sticky='se')

            self.tab_test_paned_el = ttk.PanedWindow(self.tab_test_lf_el, orient=tk.HORIZONTAL)
            self.tab_test_el_paned.add(self.tab_test_paned_el, weight=1)
            self.tab_test_el_lf_button = ttk.LabelFrame(self.tab_test_paned_el, text='Редактор кнопки')
            self.tab_test_paned_el.add(self.tab_test_el_lf_button, weight=1)
            ################ init button lf el ####################
            """
            # ============= Label + Spinbox pair ============== #
            self.tab_test_el_lf_button_label = ttk.Label(self.tab_test_el_lf_button, text='param:')
            self.tab_test_el_lf_button_label.grid(row=0, column=0)
            self.tab_test_el_lf_button_spinbox = ttk.Spinbox(self.tab_test_el_lf_button, from_=0, to=100)
            self.tab_test_el_lf_button_spinbox.grid(row=0, column=1)
            """
            # ============= Entry + Button ============== # -- FONT
            self.tab_test_el_lf_button_button_font = ttk.Button(self.tab_test_el_lf_button, text='Выбрать шрифт',
                                                                command=self.choose_font_button)
            self.tab_test_el_lf_button_button_font.grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_entry_font = ttk.Entry(self.tab_test_el_lf_button)
            self.tab_test_el_lf_button_entry_font.grid(row=0, column=1, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_entry_font.insert('end', 'TkDefaultFont')
            # ============= Label + Spinbox pair ============== # --- WIDTH
            self.tab_test_el_lf_button_label_width = ttk.Label(self.tab_test_el_lf_button, text='width=')
            self.tab_test_el_lf_button_label_width.grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_spinbox_width = ttk.Spinbox(self.tab_test_el_lf_button, from_=0, to=100,
                                                                   command=self.set_spinboxes_button)
            self.tab_test_el_lf_button_spinbox_width.set(0)
            self.tab_test_el_lf_button_spinbox_width.grid(row=1, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- IPADX
            self.tab_test_el_lf_button_label_ipadx = ttk.Label(self.tab_test_el_lf_button, text='ipadx=')
            self.tab_test_el_lf_button_label_ipadx.grid(row=3, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_spinbox_ipadx = ttk.Spinbox(self.tab_test_el_lf_button, from_=0, to=100,
                                                                   command=self.set_spinboxes_button)
            self.tab_test_el_lf_button_spinbox_ipadx.set(0)
            self.tab_test_el_lf_button_spinbox_ipadx.grid(row=3, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- IPADY
            self.tab_test_el_lf_button_label_ipady = ttk.Label(self.tab_test_el_lf_button, text='ipady=')
            self.tab_test_el_lf_button_label_ipady.grid(row=4, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_spinbox_ipady = ttk.Spinbox(self.tab_test_el_lf_button, from_=0, to=100,
                                                                   command=self.set_spinboxes_button)
            self.tab_test_el_lf_button_spinbox_ipady.set(0)
            self.tab_test_el_lf_button_spinbox_ipady.grid(row=4, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- PADX
            self.tab_test_el_lf_button_label_padx = ttk.Label(self.tab_test_el_lf_button, text='padx=')
            self.tab_test_el_lf_button_label_padx.grid(row=5, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_spinbox_padx = ttk.Spinbox(self.tab_test_el_lf_button, from_=0, to=100,
                                                                  command=self.set_spinboxes_button)
            self.tab_test_el_lf_button_spinbox_padx.set(0)
            self.tab_test_el_lf_button_spinbox_padx.grid(row=5, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- PADY
            self.tab_test_el_lf_button_label_pady = ttk.Label(self.tab_test_el_lf_button, text='pady=')
            self.tab_test_el_lf_button_label_pady.grid(row=6, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_spinbox_pady = ttk.Spinbox(self.tab_test_el_lf_button, from_=0, to=100,
                                                                  command=self.set_spinboxes_button)
            self.tab_test_el_lf_button_spinbox_pady.set(0)
            self.tab_test_el_lf_button_spinbox_pady.grid(row=6, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- STICKY
            self.tab_test_el_lf_button_label_sticky = ttk.Label(self.tab_test_el_lf_button, text='sticky=')
            self.tab_test_el_lf_button_label_sticky.grid(row=7, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_button_spinbox_sticky = ttk.Spinbox(self.tab_test_el_lf_button,
                                                                    command=self.set_spinboxes_button,
                                                                    values=['', 'n', 's', 'e', 'w', 'nw', 'ne', 'sw',
                                                                            'se',
                                                                            'ns', 'we', 'nse', 'nws', 'wes', 'wen',
                                                                            'nsew'])
            self.tab_test_el_lf_button_spinbox_sticky.set('')
            self.tab_test_el_lf_button_spinbox_sticky.grid(row=7, column=1, ipadx=10, padx=10, pady=10)
            self.tab_test_el_lf_label = ttk.LabelFrame(self.tab_test_paned_el, text='Редактор подписи')
            self.tab_test_paned_el.add(self.tab_test_el_lf_label, weight=1)
            ###################### init label edit #################
            # ============= Entry + Button ============== # -- FONT
            self.tab_test_el_lf_label_button_font = ttk.Button(self.tab_test_el_lf_label, text='Выбрать шрифт',
                                                               command=self.choose_font_label)
            self.tab_test_el_lf_label_button_font.grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_entry_font = ttk.Entry(self.tab_test_el_lf_label)
            self.tab_test_el_lf_label_entry_font.grid(row=0, column=1, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_entry_font.insert('end', 'TkDefaultFont')
            # ============= Label + Spinbox pair ============== # --- WIDTH
            self.tab_test_el_lf_label_label_width = ttk.Label(self.tab_test_el_lf_label, text='width=')
            self.tab_test_el_lf_label_label_width.grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_spinbox_width = ttk.Spinbox(self.tab_test_el_lf_label, from_=0, to=100,
                                                                  command=self.set_spinboxes_label)
            self.tab_test_el_lf_label_spinbox_width.set(0)
            self.tab_test_el_lf_label_spinbox_width.grid(row=1, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- IPADX
            self.tab_test_el_lf_label_label_ipadx = ttk.Label(self.tab_test_el_lf_label, text='ipadx=')
            self.tab_test_el_lf_label_label_ipadx.grid(row=3, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_spinbox_ipadx = ttk.Spinbox(self.tab_test_el_lf_label, from_=0, to=100,
                                                                  command=self.set_spinboxes_label)
            self.tab_test_el_lf_label_spinbox_ipadx.set(0)
            self.tab_test_el_lf_label_spinbox_ipadx.grid(row=3, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- IPADY
            self.tab_test_el_lf_label_label_ipady = ttk.Label(self.tab_test_el_lf_label, text='ipady=')
            self.tab_test_el_lf_label_label_ipady.grid(row=4, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_spinbox_ipady = ttk.Spinbox(self.tab_test_el_lf_label, from_=0, to=100,
                                                                  command=self.set_spinboxes_label)
            self.tab_test_el_lf_label_spinbox_ipady.set(0)
            self.tab_test_el_lf_label_spinbox_ipady.grid(row=4, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- PADX
            self.tab_test_el_lf_label_label_padx = ttk.Label(self.tab_test_el_lf_label, text='padx=')
            self.tab_test_el_lf_label_label_padx.grid(row=5, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_spinbox_padx = ttk.Spinbox(self.tab_test_el_lf_label, from_=0, to=100,
                                                                 command=self.set_spinboxes_label)
            self.tab_test_el_lf_label_spinbox_padx.set(0)
            self.tab_test_el_lf_label_spinbox_padx.grid(row=5, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- PADY
            self.tab_test_el_lf_label_label_pady = ttk.Label(self.tab_test_el_lf_label, text='pady=')
            self.tab_test_el_lf_label_label_pady.grid(row=6, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_spinbox_pady = ttk.Spinbox(self.tab_test_el_lf_label, from_=0, to=100,
                                                                 command=self.set_spinboxes_label)
            self.tab_test_el_lf_label_spinbox_pady.set(0)
            self.tab_test_el_lf_label_spinbox_pady.grid(row=6, column=1, ipadx=10, padx=10, pady=10)
            # ============= Label + Spinbox pair ============== # --- STICKY
            self.tab_test_el_lf_label_label_sticky = ttk.Label(self.tab_test_el_lf_label, text='sticky=')
            self.tab_test_el_lf_label_label_sticky.grid(row=7, column=0, ipadx=10, ipady=15, padx=10, pady=10)
            self.tab_test_el_lf_label_spinbox_sticky = ttk.Spinbox(self.tab_test_el_lf_label,
                                                                   command=self.set_spinboxes_label,
                                                                   values=['', 'n', 's', 'e', 'w', 'nw', 'ne', 'sw',
                                                                           'se',
                                                                           'ns', 'we', 'nse', 'nws', 'wes', 'wen',
                                                                           'nsew'])
            self.tab_test_el_lf_label_spinbox_sticky.set('se')
            self.tab_test_el_lf_label_spinbox_sticky.grid(row=7, column=1, ipadx=10, padx=10, pady=10)

    def init_file_tab(self):
        """
        Initialize the file tab with sub tabs
        :return: nothing
        """
        self.tab_file = ttk.Frame(self.notebook)  # create the file tab frame
        self.tab_file.pack(fill='both', expand=1)  # pack the file tab
        self.notebook.add(self.tab_file, text='Файл')  # add the tab to the notebook
        self.tab_file_vnotebook = ttk.Notebook(self.tab_file,
                                               style='lefttab.TNotebook')  # make vertical notebook in the file tab
        self.tab_file_vnotebook.pack(fill='both', expand=1)  # pack the vertical notebook
        self.tab_file_tab_recent = ttk.Frame(self.tab_file_vnotebook)  # create the recent files tab frame
        self.tab_file_tab_recent.pack(fill='both', expand=1)  # pack it
        self.tab_file_vnotebook.add(self.tab_file_tab_recent, text=' Последнее ',
                                    padding=2, )  # add the recent files tab frame to the vertical notebook
        self.id_recent = 0  # set id to the recent files tab
        self.update_recent_tab()  # update the recent files tab and initializing the recent files tab
        self.tab_file_tab_lib = ttk.Frame(self.tab_file_vnotebook)  # create the library files tab frame
        self.tab_file_tab_lib.pack(fill='both', expand=1)  # pack the library files
        self.tab_file_vnotebook.add(self.tab_file_tab_lib, text=' Библиотека',
                                    padding=2)  # add the library tab frame to the vertical notebook
        self.init_tab_file_lib_tab()  # initialize the library files tab
        self.id_lib = 1  # set id to the library files tab
        self.tab_file_tab_save = ttk.Frame(self.tab_file_vnotebook)  # create the save tab frame
        self.tab_file_tab_save.pack(fill='both', expand=1)  # pack it
        self.tab_file_vnotebook.add(self.tab_file_tab_save, text=' Сохранить ',
                                    padding=2)  # add the save tab frame to the vertical notebook
        self.init_tab_file_save_tab()  # initialize the save tab
        self.tab_file_tab_create = ttk.Frame(self.tab_file_vnotebook)  # create the create tab frame
        self.tab_file_tab_create.pack(fill='both', expand=1)  # pack it
        self.tab_file_vnotebook.add(self.tab_file_tab_create, text='  Создать  ',
                                    padding=2)  # add the create tab frame to the vertical notebook
        self.init_tab_file_create_tab()  #
        self.tab_file_tab_open = ttk.Frame(self.tab_file_vnotebook)
        self.tab_file_tab_open.pack(fill='both', expand=1)
        self.tab_file_vnotebook.add(self.tab_file_tab_open, text='  Открыть  ', padding=2)
        self.init_tab_file_open_tab()

    def init_tab_file_save_tab(self):
        """
        initialize the tab save
        :return: nothing
        """
        self.tab_file_tab_save_entry = ttk.Entry(self.tab_file_tab_save, width=100)  # create a new entry with file name
        self.tab_file_tab_save_entry.grid(row=0, column=0, sticky='e', padx=[10, 0], pady=10, ipadx=10,
                                          ipady=15)  # grid the entry
        self.tab_file_tab_save_butt_se = ttk.Button(self.tab_file_tab_save, text='Сохранить',
                                                    command=self.save)  # create a new save-button
        self.tab_file_tab_save_butt_se.grid(row=0, column=1, sticky='w', padx=[0, 10], pady=10, ipadx=10,
                                            ipady=15)  # grid the button
        self.tab_file_tab_save_butt_saveas = ttk.Button(self.tab_file_tab_save,
                                                        text='Сохранить как ... в проводнике Windows',
                                                        command=self.save_as_win)  # create the button to save the file using the Windows File System
        self.tab_file_tab_save_butt_saveas.grid(row=1, column=0, columnspan=2, sticky='nsew', ipadx=10, ipady=15,
                                                padx=10, pady=10)  # grid button

    def init_tab_file_lib_tab(self):
        """
        Initialize the tab file library
        :return: nothing
        """
        self.tab_file_tab_lib_tool_frame = ttk.Frame(self.tab_file_tab_lib,
                                                     height=50)  # create the toolbar frame for the tab file library
        self.tab_file_tab_lib_tool_frame.pack(fill='x')  # pack the toolbar frame horizontally
        self.tab_file_tab_lib_butt_delete = ttk.Button(self.tab_file_tab_lib_tool_frame,
                                                       text='Удалить тест из библиотеки',
                                                       command=self.del_test_from_library)  # create a button that deletes the file from the library
        self.tab_file_tab_lib_butt_delete.place(relx=0.5, rely=0, relheight=1, relwidth=0.5,
                                                anchor='nw')  # place button
        self.tab_file_tab_lib_butt_open = ttk.Button(self.tab_file_tab_lib_tool_frame,
                                                     text='Открыть тест',
                                                     command=self.launch_test_from_library)  # create a button that opens test from the library
        self.tab_file_tab_lib_butt_open.place(relx=0, rely=0, relheight=1, relwidth=0.5, anchor='nw')  # place button
        self.tab_file_tab_lib_tv_frame = ttk.Frame(
            self.tab_file_tab_lib)  # create a frame for pack treeview with scrollbar
        self.tab_file_tab_lib_tv_frame.pack(fill='both', expand=1)  # pack frame
        columns = ("#1", "#2", "#3")  # define columns
        self.tab_file_tab_lib_treeview_tests = ttk.Treeview(self.tab_file_tab_lib_tv_frame, show="headings",
                                                            columns=columns)  # create table for tests for library
        self.tab_file_tab_lib_treeview_tests.heading("#1", text="ID")  # define heading ID
        self.tab_file_tab_lib_treeview_tests.heading("#2", text="Название")  # define heading name
        self.tab_file_tab_lib_treeview_tests.heading("#3", text="Файл")  # define heading filename
        self.tab_file_tab_lib_treeysb = ttk.Scrollbar(self.tab_file_tab_lib_tv_frame, orient=tk.VERTICAL,
                                                      command=self.tab_file_tab_lib_treeview_tests.yview)
        self.tab_file_tab_lib_treeview_tests.configure(yscroll=self.tab_file_tab_lib_treeysb.set)
        self.tab_file_tab_lib_treeview_tests.pack(side='left', fill='both', expand=True)
        self.tab_file_tab_lib_treeysb.pack(side='right', fill='y')
        treeview_sort_column(self.tab_file_tab_lib_treeview_tests, 0, False)
        treeview_sort_column(self.tab_file_tab_lib_treeview_tests, 1, False)
        treeview_sort_column(self.tab_file_tab_lib_treeview_tests, 2, False)

    #
    def init_tab_file_open_tab(self):
        self.tab_file_tab_open_butt_open = ttk.Button(self.tab_file_tab_open,
                                                      text='Открыть файл в проводнике Windows ...',
                                                      command=self.open_win)
        self.tab_file_tab_open_butt_open.grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10, sticky='nsew')
        self.tab_file_tab_open_butt_lib = ttk.Button(self.tab_file_tab_open,
                                                     text='Открыть в библиотеке тестов ...',
                                                     command=lambda e=None: self.tab_file_vnotebook.select(self.id_lib))
        self.tab_file_tab_open_butt_lib.grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10, sticky='nsew')
        self.tab_file_tab_open_butt_rec = ttk.Button(self.tab_file_tab_open,
                                                     text='Последние файлы ...', command=lambda e=None: (
                self.tab_file_vnotebook.select(self.id_recent), print(self.id_recent)))
        self.tab_file_tab_open_butt_rec.grid(row=2, column=0, ipadx=10, ipady=15, padx=10, pady=10, sticky='nsew')

    def init_tab_file_create_tab(self):
        self.tab_file_tab_create_butt_create = ttk.Button(self.tab_file_tab_create,
                                                          text='Создать новый пустой тест на соответствие элементов',
                                                          command=self.create_test)
        self.tab_file_tab_create_butt_create.grid(row=0, column=0, ipadx=10, ipady=15,
                                                  padx=10, pady=10)

    # Функция для показа сетки кнопок в таблицу с заданной шириной
    def show_table_of_buttons(self, event=None):
        # Нужно расположить все кнопки в таблицу с заданной шириной
        top = tk.Toplevel(self)
        frame = ttk.Frame(top)
        frame.pack(fill='both', expand=1)
        width = int(self.test_tab_spinbox_width.get())
        i = 0
        for clild in self.test_tab_treeview_tests.get_children():
            selected, key, value = self.test_tab_treeview_tests.item(clild)['values']
            ttk.Button(frame, text=value, width=self.tab_test_el_lf_button_spinbox_width.get(),
                       style='example.TButton').grid(column=i % width, row=i // width,
                                                     padx=self.tab_test_el_lf_button_spinbox_padx.get(),
                                                     pady=self.tab_test_el_lf_button_spinbox_pady.get(),
                                                     ipadx=self.tab_test_el_lf_button_spinbox_ipadx.get(),
                                                     ipady=self.tab_test_el_lf_button_spinbox_ipady.get(),
                                                     sticky=self.tab_test_el_lf_button_spinbox_sticky.get())
            # make a label with simular parameters
            ttk.Label(frame, text=key, width=self.tab_test_el_lf_label_spinbox_width.get(),
                      style='example.TLabel').grid(column=i % width, row=i // width,
                                                   padx=self.tab_test_el_lf_label_spinbox_padx.get(),
                                                   pady=self.tab_test_el_lf_label_spinbox_pady.get(),
                                                   ipadx=self.tab_test_el_lf_label_spinbox_ipadx.get(),
                                                   ipady=self.tab_test_el_lf_label_spinbox_ipady.get(),
                                                   sticky=self.tab_test_el_lf_label_spinbox_sticky.get())

            i += 1

        def dismiss():
            top.grab_release()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", dismiss)  # intercept close button
        top.transient(self)  # dialog window is related to main
        top.wait_visibility()  # can't grab until window appears, so we wait
        top.grab_set()  # ensure all input goes to our window
        top.resizable(False, False)
        top.wait_window()

    # Функция для добавления файлов в библиотеку тестов
    def add_test_to_library(self, event = None, filename=None):
        if not filename is None:
            self.settings_pack.tests_lib.append(
                filename) if not filename in self.settings_pack.tests_lib else 0
            if filename in self.settings_pack.recent_file:
                self.settings_pack.recent_file.remove(filename)
                self.settings_pack.recent_file.append(filename)
            self.update_recent_tab()
            self.update_library()
            return
        # Добавляет файл с именем из self.filename в библиотеку тестов
        self.settings_pack.tests_lib.append(self.filename) if not self.filename in self.settings_pack.tests_lib else 0
        if self.filename in self.settings_pack.recent_file:
            self.settings_pack.recent_file.remove(self.filename)
            self.settings_pack.recent_file.append(self.filename)
        self.update_recent_tab()
        self.update_library()

    def del_test_from_library(self, event=None, filename=None):
        # Удаляет файл из библиотеки тестов
        if filename is None:
            selected = self.tab_file_tab_lib_treeview_tests.focus()
            _, title, filename = self.tab_file_tab_lib_treeview_tests.item(selected)['values']
        self.settings_pack.tests_lib.remove(filename)
        self.update_library()  # обновляет список файлов в библиотеке тестов

    def launch_test_from_library(self, event=None, filename=None):
        if filename is None:
            selected = self.tab_file_tab_lib_treeview_tests.focus()
            _, title, filename = self.tab_file_tab_lib_treeview_tests.item(selected)['values']
        self._open_test(filename)

    def show_selected_el(self, event=None):
        selected = self.test_tab_treeview_tests.focus()
        selected, key, value = self.test_tab_treeview_tests.item(selected)['values']
        self.tab_test_el_example_butt_1.config(text=value)
        self.tab_test_el_example_butt_2.config(text=value)
        self.tab_test_el_example_lab.config(text=key)

    def add_test_pair(self, event=None):
        def dismiss():
            dlg.grab_release()
            dlg.destroy()

        def add_pair():
            if not e1.get() in self.test.equals.keys():
                self.test.equals[e1.get()] = e2.get()
                ID = str(id(dlg))
                self.test_tab_treeview_tests.insert('', 'end', values=(ID, e1.get(), e2.get()), iid=ID)
                self.test_tab_treeview_tests.see(ID)
                self.test_tab_treeview_tests.focus(ID)
                self.test_tab_treeview_tests.selection_set(ID)
            dismiss()

        dlg = Toplevel(self)
        frame = ttk.Frame(dlg)
        frame.pack(fill='both', expand=1)
        ttk.Label(frame, text='Элемент 1').grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10)
        ttk.Label(frame, text='Элемент 2').grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10)
        e1 = ttk.Entry(frame)
        e1.grid(row=0, column=1, columnspan=2, ipadx=10, ipady=15, padx=10, pady=10)
        e2 = ttk.Entry(frame)
        e2.grid(row=1, column=1, columnspan=2, ipadx=10, ipady=15, padx=10, pady=10)
        ttk.Button(frame, text='Добавить', command=add_pair).grid(row=2, column=0, columnspan=2, sticky='we', ipadx=10,
                                                                  ipady=15, padx=10, pady=10)
        ttk.Button(frame, text='Отмена', command=dismiss).grid(row=2, column=2, ipadx=10, ipady=15, padx=10, pady=10)
        dlg.protocol("WM_DELETE_WINDOW", dismiss)  # intercept close button
        dlg.transient(self)  # dialog window is related to main
        dlg.wait_visibility()  # can't grab until window appears, so we wait
        dlg.grab_set()  # ensure all input goes to our window
        dlg.resizable(0, 0)
        dlg.wait_window()  # block until window is destroyed

    def del_test_pair(self, event=None):
        selected = self.test_tab_treeview_tests.focus()
        selected, key, value = self.test_tab_treeview_tests.item(selected)['values']
        del self.test.equals[key]
        self.test_tab_treeview_tests.delete(selected)

    def edit_test_pair(self, event=None):
        selected = self.test_tab_treeview_tests.focus()
        selected, key, value = self.test_tab_treeview_tests.item(selected)['values']

        def dismiss():
            dlg.grab_release()
            dlg.destroy()

        def add_pair():
            if 1:
                del self.test.equals[key]
                self.test.equals[e1.get()] = e2.get()
                ID = selected
                self.test_tab_treeview_tests.delete(selected)
                self.test_tab_treeview_tests.insert('', 'end', values=(ID, e1.get(), e2.get()), iid=ID)
                self.test_tab_treeview_tests.see(ID)
                self.test_tab_treeview_tests.focus(ID)
                self.test_tab_treeview_tests.selection_set(ID)
            dismiss()

        dlg = Toplevel(self)
        frame = ttk.Frame(dlg)
        frame.pack(fill='both', expand=1)
        ttk.Label(frame, text='Элемент 1').grid(row=0, column=0, ipadx=10, ipady=15, padx=10, pady=10)
        ttk.Label(frame, text='Элемент 2').grid(row=1, column=0, ipadx=10, ipady=15, padx=10, pady=10)
        e1 = ttk.Entry(frame)
        e1.grid(row=0, column=1, columnspan=2, ipadx=10, ipady=15, padx=10, pady=10)
        e1.insert('end', key)
        e1.config(state='readonly')
        e2 = ttk.Entry(frame)
        e2.grid(row=1, column=1, columnspan=2, ipadx=10, ipady=15, padx=10, pady=10)
        e2.insert('end', value)
        ttk.Button(frame, text='Изменить', command=add_pair).grid(row=2, column=0, columnspan=2, sticky='we', ipadx=10,
                                                                  ipady=15, padx=10, pady=10)
        ttk.Button(frame, text='Отмена', command=dismiss).grid(row=2, column=2, ipadx=10, ipady=15, padx=10, pady=10)
        dlg.protocol("WM_DELETE_WINDOW", dismiss)  # intercept close button
        dlg.transient(self)  # dialog window is related to main
        dlg.wait_visibility()  # can't grab until window appears, so we wait
        dlg.grab_set()  # ensure all input goes to our window
        dlg.resizable(0, 0)
        dlg.wait_window()  # block until window is destroyed

    def invert_test_pair(self, event=None):
        selected = self.test_tab_treeview_tests.focus()
        selected, key, value = self.test_tab_treeview_tests.item(selected)['values']
        del self.test.equals[key]
        self.test.equals[value] = key
        self.test_tab_treeview_tests.delete(selected)
        self.test_tab_treeview_tests.insert('', 'end', values=(selected, value, key), iid=selected)
        self.test_tab_treeview_tests.see(selected)
        self.test_tab_treeview_tests.focus(selected)
        self.test_tab_treeview_tests.selection_set(selected)

    def invert_test_pairs_all(self, event=None):
        # invert all pairs in the treeview
        for i in self.test_tab_treeview_tests.get_children():
            selected, key, value = self.test_tab_treeview_tests.item(i)['values']
            del self.test.equals[key]
            self.test.equals[value] = key
            self.test_tab_treeview_tests.delete(i)
            self.test_tab_treeview_tests.insert('', 'end', values=(i, value, key), iid=i)
            self.test_tab_treeview_tests.see(i)
            self.test_tab_treeview_tests.focus(i)
            self.test_tab_treeview_tests.selection_set(i)

    def choose_font_button(self, event=None):
        font = self.fontchoose(default_font=self.tab_test_el_lf_button_entry_font.get())
        self.style.configure('example.TButton', font=font)
        self.tab_test_el_lf_button_entry_font.delete(0, 'end')
        self.tab_test_el_lf_button_entry_font.insert('end', font)

    def choose_font_label(self, event=None):
        font = self.fontchoose(default_font=self.tab_test_el_lf_label_entry_font.get())
        self.style.configure('example.TLabel', font=font)
        self.tab_test_el_lf_label_entry_font.delete(0, 'end')
        self.tab_test_el_lf_label_entry_font.insert('end', font)

    def set_spinboxes_label(self, event=None):
        self.tab_test_el_example_lab.grid(column=1, row=0,
                                          ipadx=self.tab_test_el_lf_label_spinbox_ipadx.get(),
                                          ipady=self.tab_test_el_lf_label_spinbox_ipady.get(),
                                          padx=self.tab_test_el_lf_label_spinbox_padx.get(),
                                          pady=self.tab_test_el_lf_label_spinbox_pady.get(),
                                          sticky=self.tab_test_el_lf_label_spinbox_sticky.get(),
                                          )
        self.tab_test_el_example_lab.config(width=self.tab_test_el_lf_label_spinbox_width.get())

    def set_spinboxes_button(self, event=None):
        self.tab_test_el_example_butt_1.grid(column=0, row=0,
                                             ipadx=self.tab_test_el_lf_button_spinbox_ipadx.get(),
                                             ipady=self.tab_test_el_lf_button_spinbox_ipady.get(),
                                             padx=self.tab_test_el_lf_button_spinbox_padx.get(),
                                             pady=self.tab_test_el_lf_button_spinbox_pady.get(),
                                             sticky=self.tab_test_el_lf_button_spinbox_sticky.get(),
                                             )
        self.tab_test_el_example_butt_1.config(width=self.tab_test_el_lf_button_spinbox_width.get())
        self.tab_test_el_example_butt_2.grid(column=1, row=0,
                                             ipadx=self.tab_test_el_lf_button_spinbox_ipadx.get(),
                                             ipady=self.tab_test_el_lf_button_spinbox_ipady.get(),
                                             padx=self.tab_test_el_lf_button_spinbox_padx.get(),
                                             pady=self.tab_test_el_lf_button_spinbox_pady.get(),
                                             sticky=self.tab_test_el_lf_button_spinbox_sticky.get(),
                                             )
        self.tab_test_el_example_butt_2.config(width=self.tab_test_el_lf_button_spinbox_width.get())

    def commit_settings(self, event=None):
        with open(self.filename_settings, 'wb') as file:
            pickle.dump(self.settings_pack, file)
        print('settings have commited')
        self.style.configure('TNotebook.Tab', width=20, padding=[50, 15])
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        self.style.configure('lefttab.TNotebook.Tab', width=20, padding=[50, 15])
        self.style.configure('large.TLabel', font='{Segoe UI} 15')
        try:
            self.set_spinboxes_button()
            self.set_spinboxes_label()
        except:
            print('test tab wasnt initialized')

    def _save_test_as(self, filename=''):
        self.test.title = self.test_tab_entry_title.get()
        self.test.thanks_text = self.test_tab_tnx_text.get(1.0, 'end')
        self.test.size_grid = self.test_tab_spinbox_width.get()
        self.test.font_label = self.tab_test_el_lf_label_entry_font.get()
        self.test.font_button = self.tab_test_el_lf_button_entry_font.get()
        self.test.grid_button = {'ipadx': self.tab_test_el_lf_button_spinbox_ipadx.get(),
                                 'ipady': self.tab_test_el_lf_button_spinbox_ipady.get(),
                                 'padx': self.tab_test_el_lf_button_spinbox_padx.get(),
                                 'pady': self.tab_test_el_lf_button_spinbox_pady.get(),
                                 'sticky': self.tab_test_el_lf_button_spinbox_sticky.get()}
        self.test.grid_label = {'ipadx': self.tab_test_el_lf_label_spinbox_ipadx.get(),
                                'ipady': self.tab_test_el_lf_label_spinbox_ipady.get(),
                                'padx': self.tab_test_el_lf_label_spinbox_padx.get(),
                                'pady': self.tab_test_el_lf_label_spinbox_pady.get(),
                                'sticky': self.tab_test_el_lf_label_spinbox_sticky.get()}
        self.test.size_button = {'width': self.tab_test_el_lf_button_spinbox_width.get()}
        self.test.size_label = {'width': self.tab_test_el_lf_label_spinbox_width.get()}
        if filename == '':
            raise ValueError('filename is empty')
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.test, file)
        except:
            msgbox.showerror(title='Ошибка', message='Не удалось сохранить тест')
            return
        msgbox.showinfo(title='Успешно', message='Тест сохранен')
        self.test_tab_button_add_to_library.config(state='normal')
        self.filename = filename
        self.tab_file_tab_save_entry.delete(0, 'end')
        self.tab_file_tab_save_entry.insert('end', filename)
        # добавляем тест в последние файлы
        self.settings_pack.recent_file.append(self.filename)
        self.update_recent_tab()
        self.commit_settings()

    def create_test(self, event=None):
        self.notebook.select(2)
        self.tab_test.destroy()
        self.init_test_tab()
        self.notebook.select(2)
        self.test = testclasses.MatchTestPack()

    def _open_test(self, filename=''):
        # check if filename is empty
        if filename == '':
            raise ValueError('filename is empty')
        try:
            with open(filename, 'rb') as file:
                self.test = pickle.load(file)
        except:
            msgbox.showerror(title='Ошибка', message='Не удалось открыть тест')
            return

        self.test_tab_button_add_to_library.config(state='normal')
        self.filename = filename
        self.tab_file_tab_save_entry.delete(0, 'end')
        self.tab_file_tab_save_entry.insert('end', filename)
        # set parameters in test tab from test
        self.test_tab_entry_title.delete(0, 'end')
        self.test_tab_entry_title.insert('end', self.test.title)
        self.test_tab_spinbox_width.set(self.test.size_grid)
        self.test_tab_tnx_text.delete(1.0, 'end')
        self.test_tab_tnx_text.insert('end', self.test.thanks_text)
        self.tab_test_el_lf_button_spinbox_width.set(self.test.size_button['width'])
        self.tab_test_el_lf_button_spinbox_ipadx.set(self.test.grid_button['ipadx'])
        # set ipady
        self.tab_test_el_lf_button_spinbox_ipady.set(self.test.grid_button['ipady'])
        self.tab_test_el_lf_button_spinbox_padx.set(self.test.grid_button['padx'])
        self.tab_test_el_lf_button_spinbox_pady.set(self.test.grid_button['pady'])
        # set sticky
        self.tab_test_el_lf_button_spinbox_sticky.set(self.test.grid_button['sticky'])
        # set label
        # set width
        self.tab_test_el_lf_label_spinbox_width.set(self.test.size_label['width'])
        self.tab_test_el_lf_label_spinbox_ipadx.set(self.test.grid_label['ipadx'])
        self.tab_test_el_lf_label_spinbox_sticky.set(self.test.grid_label['sticky'])
        self.tab_test_el_lf_label_spinbox_ipady.set(self.test.grid_label['ipady'])
        self.tab_test_el_lf_label_spinbox_padx.set(self.test.grid_label['padx'])
        self.tab_test_el_lf_label_spinbox_pady.set(self.test.grid_label['pady'])
        self.tab_test_el_lf_label_entry_font.delete(0, 'end')
        self.tab_test_el_lf_label_entry_font.insert('end', self.test.font_label)
        self.tab_test_el_lf_button_entry_font.delete(0, 'end')
        self.tab_test_el_lf_button_entry_font.insert('end', self.test.font_button)
        # clear treeview
        for child in self.test_tab_treeview_tests.get_children():
            self.test_tab_treeview_tests.delete(child)
        for key in self.test.equals.keys():
            value = self.test.equals[key]
            selected = str(id(self.test.equals[key]))
            self.test_tab_treeview_tests.insert('', 'end', iid=selected, values=(selected, key, value))
        self.notebook.select(2)
        self.settings_pack.recent_file.append(self.filename)
        self.update_recent_tab()

    def save_as_win(self, event=None):
        # save as using windows dialog window filedialog
        filename = filedialog.asksaveasfilename(filetypes=(('FTS23 MatchTest', '*.fts23m'),),
                                                defaultextension='.fts23m',
                                                **({'initialfile': self.filename} if self.filename != '' else dict()))
        if filename:
            self._save_test_as(filename)

    def open_win(self, event=None):
        filename = filedialog.askopenfilename(filetypes=(('FTS23 MatchTest', '*.fts23m'),))
        if filename:
            self._open_test(filename)

    def save(self, event=None):
        self._save_test_as(self.tab_file_tab_save_entry.get())

    def update_library(self, event=None):
        # этот метод обновляет таблицу библиотеки
        for i in self.tab_file_tab_lib_treeview_tests.get_children():
            self.tab_file_tab_lib_treeview_tests.delete(i)
        for filename in self.settings_pack.tests_lib:
            # load test from pickle file
            try:
                with open(filename, 'rb') as file:
                    test = pickle.load(file)
            except:
                continue
            # insert test to treeview
            ID = str(id(test))
            self.tab_file_tab_lib_treeview_tests.insert('', 'end', iid=ID, values=(ID, test.title, filename))

    def update_recent_tab(self, event=None):
        try:
            print(self.tab_file_tab_recent_list_of_labels)
        except:
            self.tab_file_tab_recent_list_of_labels = []
        while len(self.settings_pack.recent_file) > 10:
            self.settings_pack.recent_file.pop(0)

        self.settings_pack.recent_file = list(set(self.settings_pack.recent_file))

        self.commit_settings()
        for l in self.tab_file_tab_recent_list_of_labels:
            l.destroy()
        self.tab_file_tab_recent_list_of_labels = []
        for file in reversed(self.settings_pack.recent_file):
            try:
                with open(file, 'rb') as f:
                    t = pickle.load(f)
                title = t.title
                self.tab_file_tab_recent_list_of_labels.append(
                    ttk.LabelFrame(self.tab_file_tab_recent, text=title, height=60))
                self.tab_file_tab_recent_list_of_labels[-1].pack(fill='x', pady=5, padx=10)
                self.tab_file_tab_recent_list_of_labels[-1].bind('<Double-Button-1>',
                                                                 lambda event=None, fn=file: self._open_test(fn))
                self.tab_file_tab_recent_list_of_labels.append(
                    ttk.Label(self.tab_file_tab_recent_list_of_labels[-1], text=title, style='large.TLabel'))
                self.tab_file_tab_recent_list_of_labels[-1].place(relx=0, rely=0, anchor='nw')
                self.tab_file_tab_recent_list_of_labels[-1].bind('<Double-Button-1>',
                                                                 lambda event=None, fn=file: self._open_test(fn))
                self.tab_file_tab_recent_list_of_labels.append(
                    ttk.Label(self.tab_file_tab_recent_list_of_labels[-2], text=file))
                self.tab_file_tab_recent_list_of_labels[-1].place(relx=1, rely=1, anchor='se')
                self.tab_file_tab_recent_list_of_labels[-1].bind('<Double-Button-1>',
                                                                 lambda event=None, fn=file: self._open_test(fn))
                self.tab_file_tab_recent_list_of_labels.append(
                    ttk.Button(self.tab_file_tab_recent_list_of_labels[-3], text='Добавить в библиотеку',
                               command=lambda event=None, fn=file: self.add_test_to_library(filename=fn)))
                self.tab_file_tab_recent_list_of_labels[-1].place(relx=1, rely=0, anchor='ne', width=200)
            except:
                pass
        if len(self.tab_file_tab_recent_list_of_labels) == 0:
            self.tab_file_tab_recent_list_of_labels.append(
                ttk.Label(self.tab_file_tab_recent, text='Последних файлов нет...', style='large.TLabel'))
            self.tab_file_tab_recent_list_of_labels[-1].pack(fill='both', expand=1)
        self.commit_settings()

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

        self.tk.call('tk', 'fontchooser', 'configure', '-font', default_font, '-command', self.register(font_changed))
        self.tk.call('tk', 'fontchooser', 'show')
        print('choosed', self.__font_from_font_chooser)
        return self.__font_from_font_chooser


if __name__ == '__main__':
    App().mainloop()
