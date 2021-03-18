import tkinter as tk


class InputLabel(tk.Label):
    def __init__(self, master=None, bg="white", fg="black"):
        self.S = tk.StringVar()
        super().__init__(master, cursor="xterm", relief="raised",
                         font=("Cousine", 16), takefocus=True,
                         textvariable=self.S, anchor=tk.NW, bg=bg,
                         fg=fg)
        self.F = tk.Frame(self, bg="white", height=32, width=1)
        self.strip_coords = [0, 0]
        self.F.place(x=self.strip_coords[0], y=self.strip_coords[1])
        self.strip_flag = False

        self.change_strip()
        self.bind('<Key>', self.key_control)
        self.bind('<Button-1>', self.mouse_control)
        self.bind('<Return>', self.ignore)

    def change_strip_coords(self, position):
        if position > len(self.S.get()):
            return
        self.strip_coords[0] = position
        self.F.place(x=self.strip_coords[0] * 19 + 1, y=1)

    def ignore(self, event):
        pass

    def change_strip(self):
        if self.strip_flag:
            self.F.configure(bg=self.master['bg'])
            self.strip_flag = False
        else:
            self.F.configure(bg="black")
            self.strip_flag = True
        self.master.after(200, self.change_strip)

    def key_control(self, event):
        if event.keysym == "Right":
            self.change_strip_coords(self.strip_coords[0] + 1)
        elif event.keysym == "Left":
            self.change_strip_coords(self.strip_coords[0] - 1)
        elif event.keysym == 'BackSpace':
            if self.strip_coords[0] > 0:
                self.S.set(self.S.get()[:self.strip_coords[0] - 1]
                           + self.S.get()[self.strip_coords[0]:])
                self.change_strip_coords(self.strip_coords[0] - 1)
        elif event.keysym == 'Delete':
                if self.strip_coords[0] < len(self.S.get()):
                    self.S.set(self.S.get()[:self.strip_coords[0]]
                               + self.S.get()[self.strip_coords[0] + 1:])
        elif event.keysym == 'Tab':
            self.ignore(event)
        elif event.keysym == "Home":
            self.change_strip_coords(0)
        elif event.keysym == "End":
            self.change_strip_coords(len(self.S.get()))
        elif event.char:
            self.S.set(self.S.get()[:self.strip_coords[0]]
                       + event.char + self.S.get()[self.strip_coords[0]:])
            self.change_strip_coords(self.strip_coords[0] + 1)

    def mouse_control(self, event):
        self.focus_set()
        self.change_strip_coords(event.x // 19 + 1)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky='NEWS')
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.labelText = InputLabel(self)
        self.labelText.grid(sticky="EW")
        self.buttonQuit = tk.Button(self, text="Quit",
                                    command=self.master.quit)
        self.buttonQuit.grid()

        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1, uniform='col')
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1, uniform='row')


app = Application()
app.master.title('Text Editor')
app.mainloop()
