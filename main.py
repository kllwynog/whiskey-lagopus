import tkinter as tk
from tkinter import ttk, Canvas

WIDTH = 1366
HEIGHT = 768

polarity = ["+", "0", "−"]

def makeRadios(master, var):
  return [tk.Radiobutton(master, text = polarity[i], variable = v, value = i + 1, indicatoron = 0, background = "white", borderwidth = 0, cursor = "heart", height = 1, padx = 4, pady = 4, width = 2, font = "Arial 16", activeforeground = "black", fg = "grey") for i in range(3)]

root = tk.Tk()
root.geometry("%sx%s" % (WIDTH, HEIGHT))
root.title("yeah")

master = ttk.Frame(root)#, padding = "16 16 16 16")
canvas = Canvas(root, bg = "blue", width = WIDTH / 4, height = HEIGHT / 4)
symbolCell = ttk.Frame(master, borderwidth = 1, relief = "sunken", width = WIDTH / 3, height = HEIGHT / 4)
featureCell = ttk.Frame(master, borderwidth = 1, relief = "sunken", width = WIDTH / 3, height = HEIGHT * 3 / 4)
chartCell = ttk.Frame(master, borderwidth = 1, relief = "sunken", width = WIDTH * 2 / 3, height = HEIGHT)

feats = []
for i in range(24):
  feats.append(ttk.Frame(featureCell))#, width = WIDTH / 3, height = HEIGHT / 32))
  feats[i].pack()
  v = tk.IntVar()
  radios = makeRadios(feats[i], v)
  for r in radios:
    r.grid(row = int(i / 2), column = radios.index(r) + 4 * int(i / 12))
  tk.Label(feats[i], text = "Sonorant", font = "Arial 16").grid(row = 0, column = 3 + 4 * int(i / 12))

master.grid(column = 0, row = 0, sticky = "nesw")
symbolCell.grid(column = 0, row = 0, columnspan = 1, rowspan = 1)#, sticky = "nw")
#canvas.grid(column = 0, row = 0, columnspan = 1, rowspan = 1)#, sticky = "nw")
featureCell.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)#, sticky = "nw")
chartCell.grid(column = 1, row = 0, columnspan = 1, rowspan = 2)#, sticky = "ne")


root.mainloop()
