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
    closed = QtCore.Signal()

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
        self.timer.stop()
        self.close()
        self.closed.emit()
        self.parentWidget().adjustSize()
        self.parentWidget().update()

    def showMessage(self, message=None):
        self.setText(message)
        self.adjustSize()
        self.update()
        self.show()

        # center = self.parentWidget().size()
        # self.move(center.width() * .5 - self.width() * .5, 10);


class messageArea(QtGui.QWidget):
    def __init__(self, parent, lifespan=3000):
        super(messageArea, self).__init__(parent)

        self.setFixedWidth(200)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.lifespan = lifespan
        self.deleteTimer = QtCore.QTimer(self)
        self.deleteTimer.timeout.connect(self.clean)
        self._isDeleted = False

        self.mainlayout = QtGui.QVBoxLayout(self)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setSpacing(10)
        self.setLayout(self.mainlayout)

        self.popMessages = {}

        center = self.parentWidget().size()
        self.move(center.width() * .5 - self.width() * .5, center.height() * .5)

        self.deleteTimer.start(self.lifespan)

    def showUI(self):
        self.update()
        self.adjustSize()
        self.show()

    def clean(self):
        # 在没有message的情况下lifespan =lifespan
        self.deleteTimer.stop()
        self.close()
        self.deleteLater()
        self._isDeleted = True

    def isDeleted(self):
        return self._isDeleted

    def addMessage(self, message, timeout=3000):
        mes = popupMessage(self, message, timeout)
        self.mainlayout.addWidget(mes)
        mes.closed.connect(self.updateTime)
        self.popMessages.update({mes: timeout})
        self.resetDeleteTimer()

    def resetDeleteTimer(self):
        if not self.popMessages.values():
            maxTime = self.lifespan
        else:
            maxTime = max(self.popMessages.values())
        self.deleteTimer.stop()
        # 在有message的情况下lifespan+1000
        self.deleteTimer.start(maxTime + 1000)

    def updateTime(self, ):
        mes = self.sender()

        self.popMessages.pop(mes)
        self.resetDeleteTimer()


m = messageArea(getMayaWindow())
m.showUI()
