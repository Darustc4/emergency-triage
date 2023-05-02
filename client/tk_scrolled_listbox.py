# Credit to https://github.com/igeekdom/Custom-Tkinter-ScrolledListbox

import tkinter as tk
import customtkinter as ctk

class ScrolledListbox(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent)
        self.listbox = tk.Listbox(self, *args, **kwargs)
        self.listbox_scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind('<Enter>', self.enter)
        self.listbox.bind('<Leave>', self.leave)
        self.listvariable(kwargs.get('listvariable',None))


    def configure(self, **kwargs):
        self.listvariable(kwargs.get('listvariable',None))
        self.setbackground(kwargs.get('bg',None))
        self.setforeground(kwargs.get('fg',None))
        self.sethighlight(kwargs.get('highlightcolor',None))
        self.setselectbackground(kwargs.get('selectbackground',None))
        self.setexportselection(kwargs.get('exportselection',1))
        self.listbox.configure(**kwargs)


    def listvariable(self, item_list):
        if item_list != None:
            for item in item_list:
                self.listbox.insert(tk.END, item)

    def setexportselection(self, exportselection):
        self.listbox.configure(exportselection = exportselection)

    def setbackground(self, bg):
        if bg != None:
            self.listbox.configure(bg = bg)

    def setforeground(self, fg):
        if fg != None:
            self.listbox.configure(fg = fg)

    def sethighlight(self, highlightcolor):
        if highlightcolor != None:
            self.listbox.configure(highlightcolor = highlightcolor)

    def setselectbackground(self, selectbackground):
        if selectbackground != None:
            self.listbox.configure(selectbackground = selectbackground)

    def enter(self, event):
        self.listbox.config(cursor="hand2")

    def leave(self, event):
        self.listbox.config(cursor="")

    def insert(self, location, item):
        self.listbox.insert(location, item)

    def curselection(self):
        return self.listbox.curselection()

    def delete(self, first, last=None):
        self.listbox.delete(first, last)

    def delete_selected(self):
        selected_item = self.listbox.curselection()
        idx_count = 0
        for item in selected_item:
            self.listbox.delete(item - idx_count)
            idx_count += 1

    def delete_unselected(self):
        selected_item = self.listbox.curselection()
        idx_count = 0
        for i, listbox_entry in enumerate(self.listbox.get(0, tk.END)):
            if not listbox_entry in selected_item:
                self.listbox.delete(i - idx_count)
                idx_count += 1

    def clear_selected(self):
        selected_item = self.listbox.curselection()
        for index in selected_item:
            self.listbox.selection_clear(index)

    def disable_list(self):
        self.listbox.configure(state=tk.DISABLED)

    def activate_list(self):
        self.listbox.configure(state=tk.NORMAL)

    def set_selected(self, names):
        if names == None:
            return

        self.listbox.selection_clear(0, tk.END)
        for name in names:
            index = self.listbox.get(0, tk.END).index(name)
            self.listbox.selection_set(index)

    def get_selected(self):
        return [self.listbox.get(item) for item in self.listbox.curselection()]

if __name__ == '__main__':

    gui = tk.Tk()
    list_values = ['Test1','Test2','Test3','Test4','Test5','Test6','Test7',
                   'Test8','Test9','Test10','Test11','Test12','Test13','Test14']
    scrolled_listbox = ScrolledListbox(gui, selectmode=tk.MULTIPLE)
    scrolled_listbox.configure(listvariable=list_values)
    scrolled_listbox.configure(bg='yellow')
    scrolled_listbox.configure(selectbackground='red')
    scrolled_listbox.pack()


    gui.mainloop()
