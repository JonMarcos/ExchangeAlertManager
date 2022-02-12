import tkinter as tk
import requests
import pystray
from PIL import Image
from time import sleep
import constants as c
import threading

class Win(tk.Tk):

    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.geometry("170x20+900+1019")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(width=False, height=False)
        self.title("Exchange Alert Manager")
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

    def configure_window(self):
        slave1 = Slave(self)
        slave1.mainloop()

class Slave(tk.Toplevel):

    def __init__(self,master):
        tk.Toplevel.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y

class Label(tk.Label):

    def __init__(self, master=None, text=''):
        tk.Label.__init__(self, master, text=text)
        self.pack()

    def update_label(self, master):
        try:
            response = requests.get(c.BINANCE_API_URL + c.BTCEUR)
            name = response.json()["symbol"]
            value = response.json()['price']
            if(float(value)>c.HIGH_PRICE):
                self.config(bg=c.RED)
                master.config(bg=c.RED)
            if(float(value)<c.LOW_PRICE):
                self.config(bg=c.GREEN)
                master.config(bg=c.GREEN)
            else:
                self.config(bg=c.BLUE)
                master.config(bg=c.BLUE)
        except requests.exceptions.ConnectionError:
            name = "Connection"
            value = "Error"
        valor = name +' '+ value
        self.config(text=valor)
        master.after(1000, self.update_label,master)


# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   master.destroy()

def show_window(icon, item):
    icon.stop()
    master.state("normal")


def minimize_window():
    master.state("withdrawn")
    image=Image.open("C:/Users/Jon/github/ExchangeAlertManager/favicon.png")
    icon_menu=pystray.Menu(pystray.MenuItem('Quit', quit_window),pystray.MenuItem('Show',show_window))
    icon=pystray.Icon("name", image, "Exchange Alert Manager", icon_menu)
    icon.run()

def my_popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)

master_win = Win()

my_menu = tk.Menu(master_win, tearoff=False)
my_menu.add_command(label="Configure", command=master_win.configure_window)
my_menu.add_separator()
my_menu.add_command(label="Minimize", command=minimize_window)
my_menu.add_command(label="Close", command=master_win.destroy)

master_win.bind("<Button-3>", my_popup)

etiqueta = Label(master_win, text='')

etiqueta.update_label(master_win)

master_win.mainloop()
