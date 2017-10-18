# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created: Tue Jun 06 10:18:09 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(311, 150)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(Form)
        self.title.setText("")
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonslayout = QtGui.QHBoxLayout()
        self.buttonslayout.setObjectName("buttonslayout")
        self.verticalLayout.addLayout(self.buttonslayout)
        self.hh = QtGui.QTextEdit(Form)
        self.hh.setObjectName("hh")
        self.verticalLayout.addWidget(self.hh)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

