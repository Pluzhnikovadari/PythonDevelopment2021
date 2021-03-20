import tkinter as tk
import tkinter.messagebox
import re


def parser(options):
    line = r"(\d+)\.*(\d*)\+*(\d*):(\d+)\.*(\d*)\+*(\d*)\/*([NEWS]*)"
    lst = list(re.compile(line).match(options).groups())
    lst[0] = int(lst[0])
    lst[3] = int(lst[3])
    lst[1] = int(lst[1]) if lst[1] else 1
    lst[4] = int(lst[4]) if lst[4] else 1
    lst[2] = int(lst[2]) + 1 if lst[2] else 1
    lst[5] = int(lst[5]) + 1 if lst[5] else 1
    lst[6] = lst[6] if lst[6] else "NEWS"
    return lst


class Application(tk.Frame):

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            for row in range(self.grid_size()[1]):
                self.columnconfigure(column, weight=1)
                self.rowconfigure(row, weight=1)

    def __getattr__(self, obj):
        if obj in dir(self):
            return self[obj]
        self.frame_name = obj
        return self.add_widget

    def add_widget(self, obj, options, **kwargs):

        class MyButton(obj):
            def __getattr__(self, obj):
                if obj in dir(self):
                    return self[obj]
                self.button_name = obj
                return self.add_widget

            def add_widget(self, obj, options, **kwargs):
                Button = obj(master=self, **kwargs)
                setattr(self, self.button_name, Button)
                params = parser(options)
                self.rowconfigure(params[0], weight=params[1])
                self.columnconfigure(params[3], weight=params[4])
                Button.grid(row=params[0],
                              column=params[3],
                              rowspan=params[2],
                              columnspan=params[5],
                              sticky=params[6])

        Frame = MyButton(master=self, **kwargs)
        setattr(self, self.frame_name, Frame)
        params = parser(options)
        self.rowconfigure(params[0], weight=params[1])
        self.columnconfigure(params[3], weight=params[4])
        Frame.grid(row=params[0],
                      column=params[3],
                      rowspan=params[2],
                      columnspan=params[5],
                      sticky=params[6])

    def create_widgets(self):
        '''Create all the widgets'''


class App(Application):
    def create_widgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event:
                        tkinter.messagebox.showinfo(self.message.split()[0],
                                                    self.message))


app = App(title="Sample application")
app.mainloop()
