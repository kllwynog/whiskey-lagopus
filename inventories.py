import csv
import data as Data

TIPA_IPA = {"a": "a",
            "b": "b",
            "c": "c",
            "d": "d",
            "e": "e",
            "f": "f",
            "g": "ɡ",
            "h": "h",
            "i": "i",
            "j": "j",
            "k": "k",
            "l": "l",
            "m": "m",
            "n": "n",
            "o": "o",
            "p": "p",
            "q": "q",
            "r": "r",
            "s": "s",
            "t": "t",
            "u": "u",
            "v": "v",
            "w": "w",
            "x": "x",
            "y": "y",
            "z": "z",
            "A": "ɑ",
            "B": "β",
            "C": "ç",
            "D": "ð",
            "E": "ɛ",
            "F": "ɸ",
            "G": "ɣ",
            "H": "ɦ",
            "I": "ɪ",
            "J": "ʝ",
            "K": "ʁ",
            "L": "ʎ",
            "M": "ɱ",
            "N": "ŋ",
            "O": "ɔ",
            "P": "ʔ",
            "Q": "ʕ",
            "R": "ɾ",
            "S": "ʃ",
            "T": "θ",
            "U": "ʊ",
            "V": "ʋ",
            "W": "ɯ",
            "X": "χ",
            "Y": "ʏ",
            "Z": "ʒ",
            "ʙ": "ʙ",
            "ɢ": "ɢ",
            "ʜ": "ʜ",
            "ʟ": "ʟ",
            "ʀ": "ʀ",
           "pf": "p͡f",
           "ts": "t͡s",
           "dz": "d͡z",
           "tS": "t͡ʃ",
           "dZ": "d͡ʒ",
            "0": "ʉ",
            "1": "ɨ",
            "2": "ʌ",
            "3": "ɜ",
            "4": "ɥ",
            "5": "ɐ",
            "6": "ɒ",
            "7": "ɤ",
            "8": "ɵ",
            "9": "ɘ",
            "%": "ø",
            "@": "ə",
            "=": "ɶ",
            "#": "æ",
            ")": "ɟ",
            "(": "ɳ",
            "^": "ɲ",
            "&": "œ",
            "+": "ɬ",
            "[": "ʈ",
            "]": "ɖ",
            "{": "ʂ",
            "}": "ʐ",
            "/": "ɹ",
           }

COMMON_TIPA = ["p", "b", "t", "d", "[", "]", "c", ")", "k", "g", "q", "ɢ", "P", "pf", "ts", "dz", "tS", "dZ",
               "m", "M", "n", "(", "^", "N",
               "F", "B", "f", "v", "T", "D", "s", "z", "S", "Z", "{", "}", "C", "J", "x", "G", "X", "K", "h", "H",
               "l", "+", "L", "ʟ", "r", "/", "ʀ",
               "V", "R", "j", "l", "L", "4", "w",
               "i", "y", "1", "0", "W", "u", "I", "Y", "U", "e", "%", "9", "8", "7", "o", "@", "E", "&", "3", "2", "O", "5", "#", "a", "=", "A", "6"
              ]

ENGLISH = ["p", "b", "t", "d", "k", "g", "t͡ʃ", "d͡ʒ"
           "m", "n", "ŋ",
           "f", "v", "θ", "ð", "s", "z", "ʃ", "ʒ", "h",
           "ɹ", "j", "l", "w",
           "i", "u", "ɪ", "ʊ", "ə", "ɛ", "ɜ", "ʌ", "ɔ", "æ", "ɑ"
          ]

ENG_TIPA = ["p", "b", "t", "d", "k", "g", "tS", "dZ"
            "m", "n", "N",
            "f", "v", "T", "D", "s", "z", "S", "Z", "h",
            "R", "j", "l", "w",
            "i", "u", "I", "U", "@", "E", "3", "O", "#", "A"
           ]

TUR_TIPA = ["p", "b", "t", "d", "k", "g", "tS", "dZ",
            "m", "n",
            "s", "z",
            "j", "l",
            "i", "y", "W", "u", "e", "%", "o", "a"
           ]

def convert(inventory):
  for i in range(len(inventory)):
    segment = inventory[i]
    if segment in TIPA_IPA:
      inventory[i] = TIPA_IPA.get(segment)
  return inventory

# turns the ugly list of coordinates into a beautiful list
def beautify(file):
  reader = csv.reader(file)
  inventory = []
  for row in reader:
    if len(row) == 0 or row[0] == "": continue
    if row[0] == "c":
      for c in Data.CONTOIDS2D:
        if row[1] == c[0]:
          inventory.append(c[0])
        continue
    elif row[0] == "v":
      for v in Data.VOCOIDS2D:
        if row[1] == v[0]:
          inventory.append(v[0])
          continue
 
  return convert(inventory)

def uglify(file):
  writer = csv.writer(file, delimiter = ",")

  for c in Data.CONTOIDS2D:
    if c[-1].isEnabled():
      #writer.writerow(["c", c[1], c[2]])
      writer.writerow(["c", c[0]])
  for v in Data.VOCOIDS2D:
    if v[-1].isEnabled():
      #writer.writerow(["v", v[1], v[2]])
      writer.writerow(["v", v[0]])

  file.close()

def toList(contoids, vocoids):
  listified = "["
  for c in contoids:
    if c[-1].isEnabled():
      print(c)
      listified += "\"%s\", " % c[0]
  
  listified += "]"
  return listified

def saveOnly(file, buttons, buttonStates):
  writer = csv.writer(file, delimiter = ",")

  for i in range(len(buttonStates[0])):
    c = buttonStates[0][i]
    if c == 1: writer.writerow(["c", buttons[0][i].text()])

  for i in range(len(buttonStates[1])):
    v = buttonStates[1][i]
    if v == 1: writer.writerow(["v", buttons[1][i].text()])

  file.close()
