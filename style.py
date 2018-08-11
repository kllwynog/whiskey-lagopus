STYLESHEET = """
.segmentFrame, .featuresFrame, .chartFrame {
  border: 1px solid black;
}

QFrame.segmentFrame {
  background: #fbfbf4;
}

QLabel.segmentSymbol {
  font-family: CharisSIL;
  font-size: 64pt;
}

QLabel.segmentName {
  padding-bottom: 48px;
  font-size: 16pt;
}

QPushButton.resetButton {
  font-size: 20pt;
  height: 48px;
  width: 64px;
  outline: 0;
  border: 2px solid #808080;
}

QPushButton.resetButton:hover {
  background: #ffff80;
}

QLabel.featureName {
  font-family: sans-serif;
  font-size: 14pt;
  border: none;
  padding-left: 8px;
}

QPushButton.featval {
  color: #909090;
  outline: 0;
  background: white;
  width: 32px;
  height: 28px;
  font-size: 16pt;
  border: none;
  border-top: 2.5px solid black;
  border-bottom: 2.5px solid black;
}

QPushButton.featval:hover {
  color: black;
}

QPushButton.featvalm {
  border-left: 2.5px solid black; border-top-left-radius: 16px; border-bottom-left-radius: 16px;
}

QPushButton.featvalp {
  border-right: 2.5px solid black; border-top-right-radius: 16px; border-bottom-right-radius: 16px;
}

QPushButton.selectedm {
  background: #ffd0d0;
}

QPushButton.selectedu {
  background: #ffffff;
}

QPushButton.selectedp {
  background: #d0d0ff;
}

QPushButton.vowel, QPushButton.spacer {
  background: #f7f7f4;
  font-family: CharisSIL;
  font-size: 24pt;
  height: 48px;
  width: 64px;
  outline: 0;
  border: 1px solid #808080;
  vertical-align: middle;
  text-align: center;
}

/*
QPushButton.vowel:hover, QPushButton.darkened:hover {
  background: white;
  color: #29a329;
}
*/

.darkened {
  color: red;
}

.fuckballs {
  color: red;
}

QPushButton.spacer {
  background: #dcdad5;
}
"""
