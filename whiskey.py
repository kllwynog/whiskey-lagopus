import data as Data
import style as Style
import inventories as Inventories
from functools import partial
import sys, itertools, random
from PyQt5.QtWidgets import *#QApplication, QWidget, QDesktopWidget, QCheckBox, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QFrame, QGridLayout, QRadioButton, QLabel, QButtonGroup, QPushButton
from PyQt5.QtGui import *#QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import *#QSize, QRect

WIDTH = 1280
HEIGHT = 800

STYLESHEET = Style.STYLESHEET

POLARITY = [["−", "#ffd0d0", "m"],
            ["±", "#ffffff", "u"],
            ["+", "#d0d0ff", "p"]]

  
class NewInventory(QMainWindow):
  def __init__(self, whiskey):
    super().__init__()
    self.whiskey = whiskey
    self.setGeometry((screen.width() - WIDTH) / 3, (screen.height() - HEIGHT) / 3, WIDTH, HEIGHT)
    self.setWindowTitle("Whiskey: New segment inventory")
    self.container = QWidget(self)
    self.setCentralWidget(self.container)
    self.setStyleSheet(STYLESHEET)
    self.buttons = [[], []]

    self.consonantChart = QGridLayout()
    self.consonantChart.setSpacing(0)
    for consonant in Data.CONTOIDS2D:
      button = QPushButton(consonant[0], self)
      self.buttons[0].append(button)
      button.setProperty("class", "consonant newinv")
      button.clicked.connect(partial(self.addToInventory, button, "c"))
      self.consonantChart.addWidget(button, consonant[2], consonant[1])

    for i in range(10): # Consonant manners.
      for j in range(11 * 2): # Consonant places and voices.
        if self.consonantChart.itemAtPosition(i, j) == None:
          spacerButton = QPushButton("", self)
          spacerButton.setProperty("class", "spacer")
          self.consonantChart.addWidget(spacerButton, i, j)

    self.vowelChart = QGridLayout()
    self.vowelChart.setSpacing(0)
    for vowel in Data.VOCOIDS2D:
      button = QPushButton(vowel[0], self)
      self.buttons[1].append(button)
      button.setProperty("class", "vowel newinv")
      button.clicked.connect(partial(self.addToInventory, button, "v"))
      self.vowelChart.addWidget(button, vowel[1], vowel[2])

    for i in range(7): # Vowel heights.
      for j in range(5 * 2): # Vowel frontnesses and ringednesses.
        if self.vowelChart.itemAtPosition(i, j) == None:
          spacerButton = QPushButton("", self)
          spacerButton.setProperty("class", "spacer")
          self.vowelChart.addWidget(spacerButton, i, j)

    self.consonantChartHBox = QHBoxLayout()
    self.consonantChartHBox.addStretch(1)
    self.consonantChartHBox.addLayout(self.consonantChart)

    self.vowelChartHBox = QHBoxLayout()
    self.vowelChartHBox.addStretch(1)

    self.buttonGrid = QGridLayout()
    self.consonantChart.setSpacing(0)
    saveOnly = QPushButton("Save this inventory", self)
    saveLoad = QPushButton("Save and load this inventory", self)
    selectAll = QPushButton("Select all", self)
    rejectAll = QPushButton("Reject all", self)
    surprise = QPushButton("Surprise me!", self)
    saveOnly.setProperty("class", "newInventoryButton")
    saveLoad.setProperty("class", "newInventoryButton")
    selectAll.setProperty("class", "newInventoryButton")
    rejectAll.setProperty("class", "newInventoryButton")
    surprise.setProperty("class", "newInventoryButton")
    saveOnly.clicked.connect(self.saveOnly)
    saveLoad.clicked.connect(self.saveLoad)
    selectAll.clicked.connect(self.selectAll)
    rejectAll.clicked.connect(self.rejectAll)
    surprise.clicked.connect(self.surprise)
    self.buttonGrid.addWidget(saveOnly, 0, 0, 1, 2)
    self.buttonGrid.addWidget(saveLoad, 1, 0, 1, 2)
    self.buttonGrid.addWidget(selectAll, 2, 0)
    self.buttonGrid.addWidget(rejectAll, 2, 1)
    self.buttonGrid.addWidget(surprise, 3, 0, 1, 2)

    self.vowelChartHBox.addLayout(self.buttonGrid)
    self.vowelChartHBox.addStretch(1)
    self.vowelChartHBox.addLayout(self.vowelChart)

    self.chartBox = QVBoxLayout()
    self.chartBox.addStretch(1)
    self.chartBox.addLayout(self.consonantChartHBox)
    self.chartBox.addStretch(1)
    self.chartBox.addLayout(self.vowelChartHBox)
    self.chartBox.addStretch(1)

    self.container.setLayout(self.chartBox)

    self.buttonStates = [[0 for c in Data.CONTOIDS2D], [0 for v in Data.VOCOIDS2D]]

    self.inventory = [[], []]
  
  def prepare(self):
    for i in range(len(self.buttonStates)):
      for j in range(len(self.buttonStates[i])):
        state = self.buttonStates[i][j]
        if state == 0:
          self.buttons[i][j].setStyleSheet("background: #dcdad5; color: #b0b0b0;")
        elif state == 1:
          self.buttons[i][j].setStyleSheet("background: #f7f7f4; color: black;")
  
  def saveOnly(self):
    dialog = QFileDialog
    filename = dialog.getSaveFileName(self, "", "", "Whiskey files (*.wh);;")[0]
    if filename[-3:] != ".wh":
      filename += ".wh"

    Inventories.saveOnly(open(filename, "w"), self.buttons, self.buttonStates)

    return filename
  
  def saveLoad(self):
    self.whiskey.load(self.saveOnly())
    self.close()
  
  def rejectAll(self):
    self.buttonStates = [[1 for c in Data.CONTOIDS2D], [1 for v in Data.VOCOIDS2D]]
    for c in self.buttons[0]:
      self.addToInventory(c, "c")
    for v in self.buttons[1]:
      self.addToInventory(v, "v")
  
  def selectAll(self):
    self.buttonStates = [[0 for c in Data.CONTOIDS2D], [0 for v in Data.VOCOIDS2D]]
    for c in self.buttons[0]:
      self.addToInventory(c, "c")
    for v in self.buttons[1]:
      self.addToInventory(v, "v")
  
  def surprise(self):
    seed = random.randint(2, 10) / 12
    print(seed)
    self.buttonStates = [[(1 if random.random() < seed else 0) for c in Data.CONTOIDS2D], [(1 if random.random() < seed else 0) for v in Data.VOCOIDS2D]]
    for c in self.buttons[0]:
      self.addToInventory(c, "c")
    for v in self.buttons[1]:
      self.addToInventory(v, "v")

  def addToInventory(self, button, parity):
    segment = button.text()
    if parity == "c":
      state = self.buttonStates[0][self.buttons[0].index(button)]
      if state == 1:
        if segment in self.inventory[0]: self.inventory[0].remove(button.text())
        button.setStyleSheet("background: #dcdad5; color: #b0b0b0;")
        self.buttonStates[0][self.buttons[0].index(button)] = 0
      elif state == 0:
        if not segment in self.inventory[0]: self.inventory[0].append(button.text())
        button.setStyleSheet("background: #f7f7f4; color: black;")
        self.buttonStates[0][self.buttons[0].index(button)] = 1
    if parity == "v":
      state = self.buttonStates[1][self.buttons[1].index(button)]
      if state == 1:
        if segment in self.inventory[1]: self.inventory[1].remove(button.text())
        button.setStyleSheet("background: #dcdad5; color: #b0b0b0;")
        self.buttonStates[1][self.buttons[1].index(button)] = 0
      elif state == 0:
        if not segment in self.inventory[1]: self.inventory[1].append(button.text())
        button.setStyleSheet("background: #f7f7f4; color: black;")
        self.buttonStates[1][self.buttons[1].index(button)] = 1

    print(state, self.inventory)

class Whiskey(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setGeometry((screen.width() - WIDTH) / 2, (screen.height() - HEIGHT) / 2, WIDTH, HEIGHT)
    self.statusBar().showMessage("I am Whiskey Lagopus, but you can call me %s." % ["Whiskers", "W-dawg", "Mr. Bun-buns", "the Destructor"][random.randint(0, 3)])
    self.setWindowTitle("Whiskey Lagopus")
    self.setStyleSheet(STYLESHEET)

    self.activeLanguage = Inventories.convert(Inventories.COMMON_TIPA)
    self.isShowingActiveLanguage = True

    # I am the large container; I contain multitudes.
    self.container = QWidget(self)
    self.setCentralWidget(self.container)

    # We are the hollow men.
    self.segmentFrame = QFrame(self)
    self.featuresFrame = QFrame(self)
    self.chartFrame = QFrame(self)
    self.segmentFrame.setProperty("class", "segmentFrame")
    self.featuresFrame.setProperty("class", "featuresFrame")
    self.chartFrame.setProperty("class", "chartFrame")

    #### The segment frame will now be created. ####

#   self.segmentSymbolHBox = QHBoxLayout()

    # The segment symbol.
    self.segmentSymbol = QLabel("", self.segmentFrame)
    self.segmentSymbol.setProperty("class", "segmentSymbol")
    self.segmentSymbol.setTextInteractionFlags(Qt.TextSelectableByMouse)
#   self.segmentSymbolHBox.addStretch(1)
#   self.segmentSymbolHBox.addWidget(self.segmentSymbol)
#   self.segmentSymbolHBox.addStretch(1)

#   self.segmentNameVBox = QVBoxLayout()

    # The segment name.
    self.segmentName = QLabel("", self.segmentFrame)
    self.segmentName.setProperty("class", "segmentName")
    self.segmentName.setTextInteractionFlags(Qt.TextSelectableByMouse)
#   self.segmentNameVBox.addLayout(self.segmentSymbolHBox)
#   self.segmentNameVBox.addWidget(self.segmentName)

    # The reset all features button and its wrapper.
#   self.resetButtonHBox = QHBoxLayout()
#   self.resetButtonHBox.addStretch(1)
    self.resetButton = QPushButton("Reset All", self.segmentFrame)
    self.resetButton.setProperty("class", "resetButton")
    self.resetButton.clicked.connect(self.resetAll)

    # Add segment symbol, segment name, and reset button to grid, and create appropriate padding.
    self.segmentFrameGrid = QGridLayout()
    self.segmentFrameGrid.setColumnStretch(0, 1)
    self.segmentFrameGrid.setColumnStretch(1, 1)
    self.segmentFrameGrid.setColumnStretch(3, 1)
    self.segmentFrameGrid.setColumnStretch(4, 1)
    self.segmentFrameGrid.addWidget(self.segmentSymbol, 0, 2)
    self.segmentFrameGrid.addWidget(self.segmentName, 1, 1, 1, 3)
    self.segmentFrameGrid.addWidget(self.resetButton, 2, 0, 1, 5)

    # Add symbol grid to symbol frame.
    self.segmentFrame.setLayout(self.segmentFrameGrid)

    #### The segment frame has been created. ####

    #### The features frame will now be created. ####

    self.featureFrameColumns = QHBoxLayout()
    self.featureFrameLeftColumn = QVBoxLayout()
    self.featureFrameRightColumn = QVBoxLayout()
    self.featureFrameColumns.addLayout(self.featureFrameLeftColumn)
    self.featureFrameColumns.addLayout(self.featureFrameRightColumn)
    self.featureFrameLeftColumn.addStretch(1)
    self.featureFrameRightColumn.addStretch(1)

#   self.featurePumButtonGroups = []

    for feature in Data.FEATURES:
      hbox = QHBoxLayout()
      hbox.setSpacing(0)
      group = QButtonGroup(self.featuresFrame) # Create a button group.
      feature.append(group)
#     self.featurePumButtonGroups.append(group) # Add the current button group to the button group matrix.
      name = QLabel(feature[1], self.featuresFrame) # Create a feature name label.
      name.setProperty("class", "featureName ") # Stylise the feature name label.
      for i in range(3): # Iterate over polarities.
        button = QPushButton(POLARITY[i][0], self.featuresFrame) # Create a button for each feature polarity.
        group.addButton(button, i) # Add the button to the button group.
        button.setProperty("class", "featval ") # Stylise the button.
        if i == 0:
          button.setProperty("class", "featval featvalm ")
        elif i == 1:
          button.setStyleSheet("color: black;")
        elif i == 2:
          button.setProperty("class", "featval featvalp ")
#       button.clicked.connect(partial(self.recolour, button)) # Attach an event handler to the button.
        button.clicked.connect(partial(self.updateSegments, button)) # Attach an event handler to the button.
        hbox.addWidget(button) # Add the button to the feature wrapper.
      hbox.addWidget(name) # Add the label to the feature wrapper.
      hbox.addStretch(1)
      if self.featureFrameLeftColumn.count() < 15: # Determine if the feature family should be placed in the left or in the right column.
        self.featureFrameLeftColumn.addLayout(hbox)
        if feature[3] == 1:
          self.featureFrameLeftColumn.addStretch(1)
      else:
        self.featureFrameRightColumn.addLayout(hbox)
        if feature[3] == 1:
          self.featureFrameRightColumn.addStretch(1)

    self.featureFrameLeftColumn.addStretch(1)
    self.featureFrameRightColumn.addStretch(1)
    self.featuresFrame.setLayout(self.featureFrameColumns)

    #### The features frame has been created. ####

    #### The IPA chart frame will now be created. ####

    self.buttonStates = [[1 for c in Data.CONTOIDS2D], [1 for v in Data.VOCOIDS2D]]

    self.consonantChart = QGridLayout()
    self.consonantChart.setSpacing(0)
    for consonant in Data.CONTOIDS2D:
      button = QPushButton(consonant[0], self.featuresFrame)
      consonant.append(button)
      button.setProperty("class", "consonant")
      button.clicked.connect(partial(self.setSegment, button))
      self.consonantChart.addWidget(button, consonant[2], consonant[1])

    for i in range(10): # Consonant manners.
      for j in range(11 * 2): # Consonant places and voices.
        if self.consonantChart.itemAtPosition(i, j) == None:
          spacerButton = QPushButton("", self.featuresFrame)
          spacerButton.setProperty("class", "spacer")
          self.consonantChart.addWidget(spacerButton, i, j)

    self.vowelChart = QGridLayout()
    self.vowelChart.setSpacing(0)
    for vowel in Data.VOCOIDS2D:
      button = QPushButton(vowel[0], self.featuresFrame)
      vowel.append(button)
      button.setProperty("class", "vowel")
      button.clicked.connect(partial(self.setSegment, button))
      self.vowelChart.addWidget(button, vowel[1], vowel[2])

    for i in range(7): # Vowel heights.
      for j in range(5 * 2): # Vowel frontnesses and ringednesses.
        if self.vowelChart.itemAtPosition(i, j) == None:
          spacerButton = QPushButton("", self.featuresFrame)
          spacerButton.setProperty("class", "spacer")
          self.vowelChart.addWidget(spacerButton, i, j)

    self.consonantChartHBox = QHBoxLayout()
    self.consonantChartHBox.addStretch(1)
    self.consonantChartHBox.addLayout(self.consonantChart)

    self.vowelChartHBox = QHBoxLayout()
    self.vowelChartHBox.addStretch(1)
    self.vowelChartHBox.addLayout(self.vowelChart)

    self.vcChartVBox = QVBoxLayout()
    self.vcChartVBox.addStretch(1)
    self.vcChartVBox.addLayout(self.consonantChartHBox)
    self.vcChartVBox.addStretch(1)
    self.vcChartVBox.addLayout(self.vowelChartHBox)
    self.vcChartVBox.addStretch(1)
    self.chartFrame.setLayout(self.vcChartVBox)

    self.chartFrameGrid = QGridLayout()
    self.chartFrameGrid.addWidget(self.segmentFrame, 0, 0, 1, 2)
    self.chartFrameGrid.addWidget(self.featuresFrame, 1, 0, 3, 2)
    self.chartFrameGrid.addWidget(self.chartFrame, 0, 2, 4, 5)
    self.container.setLayout(self.chartFrameGrid)

    #### The features frame has been created. ####

    #### The menu bar will now be created. ####

    self.menu = self.menuBar()
    self.fileMenu = self.menu.addMenu("&File")
    self.newFeatureSetAction = self.fileMenu.addAction("New feature set")
    self.newInventoryAction = self.fileMenu.addAction("New segment inventory")
    self.newInventoryAction.triggered.connect(self.newInventory)
    self.newInventoryAction.setShortcut("Ctrl+N")
    self.newInventoryWindow = NewInventory(self)

    self.fileMenu.addSeparator()
    self.openFeatureSetAction = self.fileMenu.addAction("Open feature set")
    self.openInventoryAction = self.fileMenu.addAction("Open segment inventory")
    self.openInventoryAction.triggered.connect(self.openInventory)
    self.openInventoryAction.setShortcut("Ctrl+O")
    self.fileMenu.addSeparator()
    self.saveFeatureSetAction = self.fileMenu.addAction("Save current feature set")
    self.saveInventoryAction = self.fileMenu.addAction("Save current segment inventory")
    self.saveInventoryAction.triggered.connect(self.saveInventory)
    self.saveInventoryAction.setShortcut("Ctrl+S")
    self.fileMenu.addSeparator()
    self.saveAsFeatureSetAction = self.fileMenu.addAction("Save current feature set as")
    self.saveAsInventoryAction = self.fileMenu.addAction("Save current segment inventory as")
    self.fileMenu.addSeparator()
    self.quitAction = self.fileMenu.addAction("Quit")
    self.quitAction.triggered.connect(self.quit)
    self.dontQuitAction = self.fileMenu.addAction("Don't quit")
    self.dontQuitAction.triggered.connect(self.dontQuit)

    self.editMenu = self.menu.addMenu("&Edit")
    self.addFeatureAction = self.editMenu.addAction("Add a feature")
    self.addSegmentAction = self.editMenu.addAction("Add a segment")
    self.editMenu.addSeparator()
    self.editFeatureSetAction = self.editMenu.addAction("Edit a feature")
    self.editFeatureSetAction = self.editMenu.addAction("Edit a segment")
    self.editMenu.addSeparator()
    self.editFeatureSetAction = self.editMenu.addAction("Edit current feature set")
    self.editInventoryAction = self.editMenu.addAction("Edit current segment inventory")

    self.viewMenu = self.menu.addMenu("&View")
    self.showLanguageAction = self.viewMenu.addAction("Only show active language")
    self.showLanguageAction.setCheckable(True)
    self.showLanguageAction.setChecked(True)
    self.showLanguageAction.triggered.connect(self.toggleShowActiveLanguage)
    self.showPulmonicAction = self.viewMenu.addAction("Show all pulmonic sounds")
    self.showAllAction = self.viewMenu.addAction("Show all sounds")
    self.viewMenu.addSeparator()
    self.themeAction = self.viewMenu.addAction("Change theme")
    self.changeLanguageAction = self.viewMenu.addAction("Change display language")

    self.helpMenu = self.menu.addMenu("&Help")
    self.aboutAction = self.helpMenu.addAction("&About")
    self.aboutAction.triggered.connect(self.aboutWindow)
    self.aboutAction.setShortcut("F12")

    #### The menu bar has now been created. ####

    self.updateFeatures() #this makes it not look horrible when you startup, also fix the fonts lmao
    # that means when you add custom features it'll probably need a self.updateFeatures() here too
  
  def updateFeatures(self):
    for feature in Data.FEATURES:
      id = feature[2]
      bg = feature[4]
      if not bg.button(id).isChecked():
        self.recolour(bg.button(id))

    self.updateSegments()

  def findFeature(self, button):
    for feature in Data.FEATURES:
      if button in feature[4].buttons():
        return feature

    return None
 
  def updateSegments(self, button = None):
    if button != None:
      self.setFeaturesOfFeatures(button)
      self.recolour(button)

    for vowel in Data.VOCOIDS2D:
      self.lightenButton(vowel[-1])

    for consonant in Data.CONTOIDS2D:
      self.lightenButton(consonant[-1])

    for i in range(len(Data.VOCOIDS2D)):
      vowel = Data.VOCOIDS2D[i]
      if self.isShowingActiveLanguage and vowel[0] not in self.activeLanguage:
        self.hideButton(vowel[-1])
      else:
        for j in range(len(Data.FEATURES)):
          feature = Data.FEATURES[j]
          if feature[2] != 1:
            if feature[2] == 0 and vowel[j + 3] == 1:
              self.greyenButton(vowel[-1])
            if feature[2] != vowel[j + 3]:
              self.darkenButton(vowel[-1])

    for i in range(len(Data.CONTOIDS2D)):
      consonant = Data.CONTOIDS2D[i]
      if self.isShowingActiveLanguage and consonant[0] not in self.activeLanguage:
        self.hideButton(consonant[-1])
      else:
        for j in range(len(Data.FEATURES)):
          feature = Data.FEATURES[j]
          if feature[2] != 1:
            if feature[2] == 0 and consonant[j + 3] == 1:
              self.greyenButton(consonant[-1])
            if feature[2] != consonant[j + 3]:
              self.darkenButton(consonant[-1])

  def setSegment(self, button):
    segment = []
    symbol = button.text()
    for s in Data.CONTOIDS2D + Data.VOCOIDS2D:
      if s[0] == symbol:
        segment = s
        break
    self.segmentSymbol.setText(symbol)
    if s in Data.CONTOIDS2D:
      self.segmentName.setText("I'm the " + Data.CONSONANTSTATS[0][segment[7]] + Data.CONSONANTSTATS[1][int(segment[1] / 2)] + Data.CONSONANTSTATS[2][segment[2]] + "!")
    else:
      self.segmentName.setText("I'm the " + Data.VOWELSTATS[0][segment[1]] + Data.VOWELSTATS[1][segment[2]] + Data.VOWELSTATS[2][segment[15]] + "vowel!")
    self.setFeaturesOfSegment(segment)
    for feature in Data.FEATURES:
      b = feature[4].button(feature[2])

    self.updateFeatures()
  
  def darkenButton(self, button):
    button.setStyleSheet("background: #dcdad5; color: #b0b0b0;")
    self.setButtonState(button, 0)

  def greyenButton(self, button):
    button.setStyleSheet("color: #b0b0b0;")
    self.setButtonState(button, 2)

  def lightenButton(self, button):
    button.setStyleSheet("background: #f7f7f4; color: black;")
    self.setButtonState(button, 1)
    button.setEnabled(True)
  
  def setButtonState(self, button, value):
    return

    segment = button.text()
    for i in range(len(Data.CONTOIDS2D)):
      c = Data.CONTOIDS2D[i]
      print(i, Data.CONTOIDS2D[i], c)
      if c[0] == segment:
        self.buttonStates[0][i] == value
        print(segment, self.buttonStates)
        break
    for i in range(len(Data.VOCOIDS2D)):
      v = Data.VOCOIDS2D[i]
      if v[0] == segment:
        self.buttonStates[1][i] == value
        print(segment, self.buttonStates)
        break

  def hideButton(self, button):
    button.setStyleSheet("background: #dcdad5; color: #dcdad5;")
    button.setEnabled(False)

  def setFeaturesOfSegment(self, segment):
    for i in range(len(Data.FEATURES)):
      Data.FEATURES[i][2] = segment[i + 3]

# Because you're inevitably going to be confused by this function, what it does is update the feature values in the big ol' matrix to match with the checked buttons.
  def setFeaturesOfFeatures(self, button):
    feature = self.findFeature(button)
    feature[2] = feature[4].id(button)
#   id = feature[4].checkedId()
#   print(str(feature) + " " + str(id))
#   if id == -1:
#     print("yeah yeah")
#     feature[2] = 1
#   else:
#     feature[2] = id

#   for feature in Data.FEATURES:
#     id = feature[4].checkedId()
#     print(feature[4].buttons()[2].isChecked())
#     if id == -1:
#       print(str(feature) + " " + str(id))
#       feature[2] = 1
#     else:
#       feature[2] = id
 
  def recolour(self, button):
    group = button.group()
    id = group.id(button)
    styles = ["", "", ""]
    styles[id] = "color: black; "
    for i in range(len(group.buttons())):
      styles[i] += "background: " + POLARITY[id][1] + ";"
      group.buttons()[i].setStyleSheet(styles[i])
  
  def resetAll(self):
    for feature in Data.FEATURES:
      feature[2] = 1

    self.segmentName.setText("")
    self.segmentSymbol.setText("")

    self.updateFeatures()
    self.updateSegments()

  def addClass(self, widget, value):
    widget.setProperty("class", widget.property("class") + value + " ")
    widget.setProperty("class", widget.property("class").replace("  ", " "))
    return widget
  
  def quit(self):
    quit = QDialog(self)
    quit.resize(320, 160)
    quit.setWindowTitle("Whiskey: Quit")

    quitLabel = QLabel("Are you sure?", quit)
    quitLabelBox = QHBoxLayout()
    quitLabelBox.addStretch(1)
    quitLabelBox.addWidget(quitLabel)
    quitLabelBox.addStretch(1)

    quitYes = QPushButton(quit)
    quitYes.setText("Yes")
    quitYes.clicked.connect(partial(self.quitForReal, quit))

    quitNo = QPushButton(quit)
    quitNo.setText("No")
    quitNo.clicked.connect(partial(self.quitForFake, quit))

    quitHBox = QHBoxLayout()
    quitHBox.addStretch(1)
    quitHBox.addWidget(quitYes)
    quitHBox.addWidget(quitNo)
    quitHBox.addStretch(1)

    quitVBox = QVBoxLayout()
    quitVBox.addStretch(1)
    quitVBox.addLayout(quitLabelBox)
    quitVBox.addStretch(1)
    quitVBox.addLayout(quitHBox)
    quitVBox.addStretch(1)
    quit.setLayout(quitVBox)
    quit.exec_()
  
  def quitForReal(self, window):
    window.close()
    self.close()
  
  def quitForFake(self, window):
    window.close()
  
  def dontQuit(self):
    dontQuit = QMessageBox(self)
    dontQuit.resize(320, 160)
    dontQuit.setWindowTitle("Whiskey: Don't quit")
    dontQuit.setText("Okay, I won't quit.")
    dontQuit.exec_()
  
  def newInventory(self):
    for i in range(len(Data.CONTOIDS2D)):
      c = Data.CONTOIDS2D[i]
      print(c[-1], c[-1].isEnabled())
      if c[-1].isEnabled():
        self.newInventoryWindow.buttonStates[0][i] = 1
    for i in range(len(Data.VOCOIDS2D)):
      v = Data.VOCOIDS2D[i]
      if v[-1].isEnabled():
        self.newInventoryWindow.buttonStates[1][i] = 1
    self.newInventoryWindow.prepare()
    self.newInventoryWindow.show()
  
  def toggleShowActiveLanguage(self):
    self.isShowingActiveLanguage = not self.isShowingActiveLanguage
    self.updateSegments()

  def openInventory(self):
    filename = QFileDialog.getOpenFileName(self, "", "", "Whiskey files (*.wh);; Text files (*.txt);; Other files (*)")[0]
    self.load(filename)

  def load(self, filename):
    self.activeLanguage = Inventories.beautify(open(filename))
    self.showLanguageAction.setChecked(True)
    self.isShowingActiveLanguage = True
    self.resetAll()
    self.updateFeatures()
    self.statusBar().showMessage("New segment inventory \"%s\" loaded." % filename)
  
  def saveInventory(self):
    dialog = QFileDialog
    filename = dialog.getSaveFileName(self, "", "", "Whiskey files (*.wh);;")[0]
    if filename[-3:] != ".wh":
      print(".wh" == filename[-3:])
      filename += ".wh"

    Inventories.uglify(open(filename, "w"))
  
  def aboutWindow(self):
    about = QMessageBox(self)
    about.setWindowTitle("Whiskey: About")
    about.setText("""
© 2018 Klaus Llwynog.

This file is part of Whiskey Lagopus.

Whiskey is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Whiskey is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Whiskey.  If not, see <http://www.gnu.org/licenses/>.

Contact me with bugs, errors, questions, or comments at kllwynog@gmail.com.
    """)
    about.exec_()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  screen = QDesktopWidget().screenGeometry()

  gentiumID = QFontDatabase.addApplicationFont("media/GentiumPlus-R.ttf")
  gentium = QFontDatabase.applicationFontFamilies(gentiumID)

  charisID = QFontDatabase.addApplicationFont("media/CharisSIL-R.ttf")
  charis = QFontDatabase.applicationFontFamilies(charisID)

  doulosID = QFontDatabase.addApplicationFont("media/DoulosSIL-R.ttf")
  doulos = QFontDatabase.applicationFontFamilies(doulosID)

  w = Whiskey()
  w.show()

  sys.exit(app.exec_())

#다겠않 지하름시 서해대 에움로괴 의몸
#를기이리누 는없 가해 럼그
#행서
