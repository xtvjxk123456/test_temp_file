# coding:utf-8

import PySide.QtGui as qg
# import PySide.QtCore as qc
import ui
import sys

buttons = {str(x) for x in range(10)}


class mywin(qg.QDialog, ui.Ui_Form):
    def __init__(self, parent=None):
        super(mywin, self).__init__(parent)
        self.setupUi(self)
        for x in buttons:
            self.buttonslayout.addWidget(qg.QPushButton(x))
        self.title.setText('there is 10 button')

app = qg.QApplication(sys.argv)
win = mywin()
win.show()
sys.exit(app.exec_())