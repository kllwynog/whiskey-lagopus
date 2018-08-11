import tkinter as tk
from tkinter import ttk, Canvas
from tkinter.font import Font

WIDTH = 1366
HEIGHT = 768
GENTIUMSIZE = 28

polarity = ["+", "±", "−"]

features = [[ "cons",         "Consonantal", "0"],
            [ "syll",            "Syllabic", "0"],
            [  "son",            "Sonorant", "0"],
            [  "app",         "Approximant", "0"],
            ["voice",               "Voice", "0"],
            [   "sg",      "Spread Glottis", "0"],
            [   "cg", "Constricted Glottis", "0"],
            [ "cont",          "Continuant", "0"],
            [  "lat",             "Lateral", "0"],
            [  "del",     "Delayed Release", "0"],
            [  "nas",               "Nasal", "0"],
            [  "lab",              "Labial", "0"],
            [  "rnd",               "Round", "0"],
            [  "cor",             "Coronal", "0"],
            [  "ant",            "Anterior", "0"],
            [ "dist",         "Distributed", "0"],
            [  "str",            "Strident", "0"],
            [ "dors",              "Dorsal", "0"],
            [ "high",                "High", "0"],
            [  "low",                 "Low", "0"],
            ["front",               "Front", "0"],
            [ "back",                "Back", "0"],
            [  "atr",    "Adv. Tongue Root", "0"]];

def makeRadios(master, var):
  return [tk.Radiobutton(master, text = polarity[i], variable = v, value = i + 1, indicatoron = 0, background = "white", borderwidth = 0, cursor = "heart", height = 1, padx = 4, pady = 4, width = 2, font = "Arial 16", activeforeground = "black", fg = "grey") for i in range(3)]

root = tk.Tk()
root.geometry("%sx%s" % (WIDTH, HEIGHT))
root.title("yeah")

charis = Font(family = "media/CharisSIL-R.ttf", size = 64)
gentium = Font(family = "media/GentiumPlus-R.ttf", size = GENTIUMSIZE)

canvas = Canvas(root, bg = "#fbfbf4", width = WIDTH, height = HEIGHT)
vSunder = canvas.create_line(0, HEIGHT / 4, WIDTH / 3, HEIGHT / 4)
hSunder = canvas.create_line(WIDTH / 3, 0, WIDTH / 3, HEIGHT)
symbol = canvas.create_text((WIDTH / 6, HEIGHT / 8), text = "a", font = charis)

for i in range(12):
  canvas.create_text((48, HEIGHT / 3 + 0.75 * GENTIUMSIZE + 1.5 * GENTIUMSIZE * (i - 1)), text = "+", font = gentium)
  canvas.create_text((48 + 1.5 * GENTIUMSIZE, HEIGHT / 3 + 0.75 * GENTIUMSIZE + 1.5 * GENTIUMSIZE * (i - 1)), text = "±", font = gentium)
  canvas.create_text((48 + 3 * GENTIUMSIZE, HEIGHT / 3 + 0.75 * GENTIUMSIZE + 1.5 * GENTIUMSIZE * (i - 1)), text = "−", font = gentium)
  canvas.create_text((48 + 4.5 * GENTIUMSIZE, HEIGHT / 3 + 0.75 * GENTIUMSIZE + 1.5 * GENTIUMSIZE * (i - 1)), text = features[i][1], font = gentium)

#symbolCell = ttk.Frame(master, borderwidth = 1, relief = "sunken", width = WIDTH / 3, height = HEIGHT / 4)
#featureCell = ttk.Frame(master, borderwidth = 1, relief = "sunken", width = WIDTH / 3, height = HEIGHT * 3 / 4)
#chartCell = ttk.Frame(master, borderwidth = 1, relief = "sunken", width = WIDTH * 2 / 3, height = HEIGHT)

#feats = []
#for i in range(24):
#  feats.append(ttk.Frame(featureCell))#, width = WIDTH / 3, height = HEIGHT / 32))
#  feats[i].pack()
#  v = tk.IntVar()
#  radios = makeRadios(feats[i], v)
#  for r in radios:
#    r.grid(row = int(i / 2), column = radios.index(r) + 4 * int(i / 12))
#  tk.Label(feats[i], text = "Sonorant", font = "Arial 16").grid(row = 0, column = 3 + 4 * int(i / 12))

#master.grid(column = 0, row = 0, sticky = "nesw")
#symbolCell.grid(column = 0, row = 0, columnspan = 1, rowspan = 1)#, sticky = "nw")
canvas.pack()
#featureCell.grid(column = 0, row = 1, columnspan = 1, rowspan = 1)#, sticky = "nw")
#chartCell.grid(column = 1, row = 0, columnspan = 1, rowspan = 2)#, sticky = "ne")


root.mainloop()
