import tkinter as tk
import ttkthemes
from tkinter import ttk

class VertNotebook(ttk.Frame):
    def __init__(self, *args, **kw):
        ttk.Frame.__init__(self, *args, **kw)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        # scrollable tabs
        self._listbox = tk.Listbox(self, width=1, background='lightgrey',
                                   highlightthickness=0, relief='raised')
        scroll = ttk.Scrollbar(self, orient='vertical', command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scroll.set)

        # list of widgets associated with the tabs
        self._tabs = []
        self._current_tab = None  # currently displayed tab

        scroll.grid(row=0, column=0, sticky='ns')
        self._listbox.grid(row=0, column=1, sticky='ns')
        # binding to display the selected tab
        self._listbox.bind('<<ListboxSelect>>', self.show_tab)

    def add(self, widget, label=''): # add tab
        self._listbox.insert('end', label)  # add label listbox
        # resize listbox to be large enough to show all tab labels
        self._listbox.configure(width=max(self._listbox.cget('width'), len(label)))
        if self._current_tab is not None:
            self._current_tab.grid_remove()
        self._tabs.append(widget)
        widget.grid(in_=self, column=2, row=0, sticky='ewns')
        self._current_tab = widget
        self._listbox.selection_clear(0, 'end')
        self._listbox.selection_set('end')
        self._listbox.see('end')

    def show_tab(self, event):
        print(event, self._listbox.curselection(), )
        try:
            widget = self._tabs[self._listbox.curselection()[0]]
            print(widget)
        except IndexError:
            return
        if self._current_tab is not None:
            self._current_tab.grid_remove()
        self._current_tab = widget
        widget.grid(in_=self, column=2, row=0, sticky='ewns')


