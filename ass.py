import data as Data
import style as Style
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

class Whiskey(QMainWindow):

  def __init__(self):
    super().__init__()
    self.setGeometry((screen.width() - WIDTH) / 2, (screen.height() - HEIGHT) / 2, WIDTH, HEIGHT)
    self.statusBar().showMessage("%s is wonderful." % ["Everything", "Something", "Anything", "Nothing"][random.randint(0, 3)])
    self.setWindowTitle("Whiskey")
    self.setStyleSheet(STYLESHEET)

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

    self.vowelChart = QGridLayout()
    self.vowelChart.setSpacing(0)
    for vowel in Data.VOCOIDS2D:
      button = QPushButton(vowel[0], self.featuresFrame)
      vowel.append(button)
      button.setProperty("class", "vowel")
      button.clicked.connect(partial(self.setSegment, button))
      self.vowelChart.addWidget(button, vowel[1], vowel[2])

    for i in range(7): # Vowel heights.
      for j in range(10): # Vowel frontnesses and ringednesses.
        if self.vowelChart.itemAtPosition(i, j) == None:
          spacerButton = QPushButton("", self.featuresFrame)
          spacerButton.setProperty("class", "spacer")
          self.vowelChart.addWidget(spacerButton, i, j)

    self.vowelChartHBox = QHBoxLayout()
    self.vowelChartHBox.addStretch(1)
    self.vowelChartHBox.addLayout(self.vowelChart)
    self.vcChartVBox = QVBoxLayout()
    self.vcChartVBox.addStretch(1)
    self.vcChartVBox.addLayout(self.vowelChartHBox)
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
    self.newFeatureSetAction = self.fileMenu.addAction("New &Feature set")
    self.newFeatureSetAction = self.fileMenu.addAction("New &Segment inventory")

    self.editMenu = self.menu.addMenu("&Edit")

    self.viewMenu = self.menu.addMenu("&View")

    self.helpMenu = self.menu.addMenu("&Help")
    self.aboutAction = self.helpMenu.addAction("&About")
    self.aboutAction.triggered.connect(self.aboutWindow)
    self.languageAction = self.helpMenu.addAction("Change display &Language")

    #### The menu bar has now been created. ####
  
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

    for i in range(len(Data.VOCOIDS2D)):
      for j in range(len(Data.FEATURES)):
        vowel = Data.VOCOIDS2D[i]
        feature = Data.FEATURES[j]
        if feature[2] != 1 and feature[2] != vowel[j + 3]:
            self.darkenButton(vowel[-1])

  def setSegment(self, button):
    segment = []
    symbol = button.text()
    for w in Data.VOCOIDS:
      for v in w:
        if v[0] == symbol:
          segment = v
          break
    self.segmentSymbol.setText(symbol)
    self.segmentName.setText("I'm the " + Data.VOWELSTATS[0][segment[1]] + Data.VOWELSTATS[1][segment[2]] + Data.VOWELSTATS[2][segment[15]] + "vowel!")
    self.setFeaturesOfSegment(segment)
    for feature in Data.FEATURES:
      b = feature[4].button(feature[2])

    self.updateFeatures()
#   self.updateSegments() # Not necessary because updateFeatures() calls updateSegments().
  
  def darkenButton(self, button):
    button.setStyleSheet("background: #dcdad5; color: #a0a0a0;")

  def lightenButton(self, button):
    button.setStyleSheet("background: #f7f7f4; color: black;")

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
  
  def aboutWindow(self):
    about = QMessageBox(self)
    about.setWindowTitle("About Whiskey")
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

다겠않 지하름시 서해대 에움로괴 의몸
를기이리누 는없 가해 럼그
행서

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

  w = Whiskey()
  w.show()

  sys.exit(app.exec_())
