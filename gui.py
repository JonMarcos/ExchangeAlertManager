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
        self.title(c.TITLE)
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)
        my_menu = MyMenu(self, False)
        self.bind('<Button-3>',my_menu.popup)
        etiqueta = Label(self, text='', api_url=c.BINANCE_API_URL, coin=c.BTCEUR)

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

    def minimize_window(self):
        self.state("withdrawn")
        image=Image.open(c.FAVICON)
        icon_menu=pystray.Menu(pystray.MenuItem('Quit', self.quit_window),pystray.MenuItem('Show', self.show_window))
        icon=pystray.Icon("name", image, c.TITLE, icon_menu)
        icon.run()

    # Define a function for quit the window
    def quit_window(self, icon):
       icon.stop()
       self.destroy()

    def show_window(self, icon):
        icon.stop()
        self.state("normal")


class Slave(tk.Toplevel):
    """
    Fix only possible to open one configuration window
    """
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

    def __init__(self, master=None, text='', api_url='', coin=''):
        tk.Label.__init__(self, master, text=text)
        self.pack()
        self.price = ''
        self.symbol = ''
        self.update_label(master, api_url + coin)

    def get_request(self, api_url):
        try:
            received = requests.get(api_url)
            self.symbol = received.json()["symbol"]
            self.price = received.json()['price']
        except requests.exceptions.ConnectionError:
            self.price = "Error"
            self.symbol = "Connection"

    def update_label(self, master, api_url):
        """
        Look up if this method needs his own class
        """
        t = threading.Thread(target=self.get_request, args=(api_url,))
        t.start()
        try:
            if(float(self.price)>c.HIGH_PRICE):
                self.config(bg=c.RED)
                master.config(bg=c.RED)
            if(float(self.price)<c.LOW_PRICE):
                self.config(bg=c.GREEN)
                master.config(bg=c.GREEN)
            else:
                self.config(bg=c.BLUE)
                master.config(bg=c.BLUE)
        except ValueError:
            self.config(bg=c.YELLOW)
            master.config(bg=c.YELLOW)
            if self.symbol != "Connection":
                self.symbol = "Connecting..."

        valor = self.symbol +' '+ self.price
        self.config(text=valor)
        master.after(1000, self.update_label, master, api_url)


class MyMenu(tk.Menu):

    def __init__(self, master=None, tearoff=False):
        tk.Menu.__init__(self, master, tearoff=tearoff)
        self.add_command(label="Configure", command=master.configure_window)
        self.add_separator()
        self.add_command(label="Minimize", command=master.minimize_window)
        self.add_command(label="Close", command=master.destroy)

    def popup(self, e):
        self.tk_popup(e.x_root, e.y_root)


if __name__ == '__main__':
    master_win = Win()
    master_win.mainloop()
