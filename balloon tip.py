# coding:utf-8

import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import shiboken
import maya.OpenMayaUI as apiUI


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)


class popupMessage(QtGui.QLabel):
    def __init__(self, parent, message="", timeout=2000):
        super(popupMessage, self).__init__(parent)
        self.message = message
        self.setMargin(10)
        self.timer = QtCore.QTimer()
        self.timer.start(timeout)
        self.timer.timeout.connect(self.times_up)  # connect it to your update function

        effect = QtGui.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(2, 2)
        self.setGraphicsEffect(effect)

        self.showMessage(self.message)

        self.setStyleSheet('''
            QLabel {
                background-color: rgba(80,150,250,200);
                border: 2px solid rgba(60,130,250,250);
                border-radius: 4px;
            }
        ''')

    def times_up(self):
        self.close()
        self.parentWidget().adjustSize()
        self.parentWidget().update()

    def showMessage(self, message=None):
        self.setText(message)
        self.adjustSize()
        self.update()
        self.show()

        # center = self.parentWidget().size()
        # self.move(center.width() * .5 - self.width() * .5, 10);


class messageArea(QtGui.QDialog):
    def __init__(self, parent):
        super(messageArea, self).__init__(parent)

        self.deleteTimer = QtCore.QTimer()
        self.deleteTimer.timeout.connect(self.clean)

        self.setFixedWidth(200)
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(2)
        self.setLayout(self.mainlayout)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.popMessages = {}
        for x in range(5):
            mes = popupMessage(self, 'this is meassage({})'.format(x), 2000 + 1000 * x)
            self.mainlayout.addWidget(mes)
            self.popMessages.update({mes: 2000 + 1000 * x})

        center = self.parentWidget().size()
        self.move(center.width() * .5 - self.width() * .5, center.height() * .5)

        self.deleteTimer.start(max(self.popMessages.values()) + 2000)

    def showUI(self):
        self.update()
        self.adjustSize()
        self.show()

    def clean(self):
        self.close()
        self.deleteLater()


m = messageArea(getMayaWindow())
m.showUI()
