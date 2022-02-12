from tkinter import *
import requests
from pystray import MenuItem as item, Menu as menu
import pystray
from PIL import Image, ImageTk
from time import sleep

def update_label():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR")
        name = response.json()["symbol"]
        value = response.json()['price']
        if(float(value)>39000):
            etiqueta.config(bg="#FF758A")
            master.config(bg="#FF758A")
        if(float(value)<37000):
            etiqueta.config(bg="#85FF7A")
            master.config(bg="#85FF7A")
        else:
            etiqueta.config(bg="#4FC4EB")
            master.config(bg="#4FC4EB")
    except requests.exceptions.ConnectionError:
        name = "Connection"
        value = "Error"
    valor = name +' '+ value
    etiqueta.config(text=valor)
    master.after(1000, update_label)

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
    icon_menu=menu(item('Quit', quit_window),item('Show',show_window))
    icon=pystray.Icon("name", image, "Exchange Alert Manager", icon_menu)
    icon.run()

def my_popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)

master = Tk()
master.geometry("170x20+900+1019")
master.overrideredirect(True)
master.attributes("-topmost", True)
master.resizable(width=False, height=False)
master.title("Exchange Alert Manager")

my_menu = Menu(master, tearoff=False)
my_menu.add_command(label="Minimize", command=minimize_window)
my_menu.add_command(label="Close", command=master.destroy)

master.bind("<Button-3>", my_popup)

etiqueta = Label(master, text='')
etiqueta.pack()

update_label()

master.mainloop()
