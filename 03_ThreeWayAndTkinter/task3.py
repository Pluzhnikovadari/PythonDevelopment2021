import tkinter as tk
import tkinter.messagebox
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky='NEWS')
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        for i in range(4):
            self.columnconfigure(i, weight=1, uniform='col')
        for i in range(1, 5):
            self.rowconfigure(i, weight=1, uniform='row')

        self.newButton = tk.Button(self, text='New', command=self.update)
        self.newButton.grid(row=0, column=0, columnspan=2)
        self.quitButton = tk.Button(self, text='Exit', command=self.quit)
        self.quitButton.grid(row=0, column=2, columnspan=2)

        self.buttons = []
        for i in range(15):
            button = tk.Button(self, text=str(i + 1))
            button['command'] = lambda button=button, i=i: self.move(button, i)
            self.buttons.append(button)
        self.update()

    def update(self):
        self.coords = list(range(16))
        random.shuffle(self.coords)
        for position, button in zip(self.coords, self.buttons):
            button.grid(row=position//4+1, column=position % 4, sticky='NEWS')
        self.isallowable()

    def move(self, button, i):
        row, column = self.coords[i] // 4, self.coords[i] % 4
        delta_row, delta_column = self.coords[-1] // 4, self.coords[-1] % 4
        if abs(row - delta_row) + abs(column - delta_column) == 1:
            self.coords[-1], self.coords[i] = self.coords[i], self.coords[-1]
            button.grid(row=delta_row + 1, column=delta_column, sticky='NEWS')
            self.checkwin()

    def checkwin(self):
        if self.coords == list(range(16)):
            tk.messagebox.showinfo(message='You win!')
            self.new_field()

    def isallowable(self):
        temp = []
        summary = 0
        for position in self.coords:
            delta = position
            for elem in temp:
                if elem < position:
                    delta -= 1
            summary += delta
            temp.append(position)
        if summary % 2 == 0:
            self.update()


app = Application()
app.master.title('The Game')
app.mainloop()
