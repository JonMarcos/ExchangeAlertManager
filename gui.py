from tkinter import *
import requests
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk

def update_label():
    response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR")
    name = response.json()["symbol"]
    value = response.json()['price']
    valor = name +' '+ value
    etiqueta.config(text=valor)
    master.after(1000, update_label)

# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   master.destroy()

master = Tk()
master.geometry("170x20")
master.overrideredirect(True)
master.attributes("-topmost", True)
master.resizable(width=False, height=False)
master.title("Exchange Alert Manager")

"""
image=Image.open("favicon.png")
menu=[item('Quit', quit_window)]
icon=pystray.Icon("name", image, "Exchange Alert Manager", menu)
icon.run()
"""


etiqueta = Label(master, text='')
etiqueta.pack()

update_label()

master.mainloop()
