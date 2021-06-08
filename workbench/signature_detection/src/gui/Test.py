# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(974, 621)
        self.ButtonClickMe = QtWidgets.QPushButton(Dialog)
        self.ButtonClickMe.setGeometry(QtCore.QRect(170, 560, 95, 30))
        self.ButtonClickMe.setCheckable(True)
        self.ButtonClickMe.setChecked(True)
        self.ButtonClickMe.setAutoDefault(False)
        self.ButtonClickMe.setObjectName("ButtonClickMe")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(170, 480, 347, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Image_True = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.Image_True.setObjectName("Image_True")
        self.horizontalLayout.addWidget(self.Image_True)
        self.Image_Falsche = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.Image_Falsche.setObjectName("Image_Falsche")
        self.horizontalLayout.addWidget(self.Image_Falsche)
        self.Image_Noise = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.Image_Noise.setObjectName("Image_Noise")
        self.horizontalLayout.addWidget(self.Image_Noise)
        self.choosenFile = QtWidgets.QLabel(Dialog)
        self.choosenFile.setGeometry(QtCore.QRect(520, 70, 401, 20))
        self.choosenFile.setObjectName("choosenFile")
        self.Image_Label = QtWidgets.QLabel(Dialog)
        self.Image_Label.setGeometry(QtCore.QRect(200, 150, 66, 20))
        self.Image_Label.setObjectName("Image_Label")
        self.Label_Vorhersage = QtWidgets.QLabel(Dialog)
        self.Label_Vorhersage.setGeometry(QtCore.QRect(180, 70, 211, 20))
        self.Label_Vorhersage.setObjectName("Label_Vorhersage")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ButtonClickMe.setText(_translate("Dialog", "Check"))
        self.Image_True.setText(_translate("Dialog", "Richtig"))
        self.Image_Falsche.setText(_translate("Dialog", "Falsch"))
        self.Image_Noise.setText(_translate("Dialog", "Rauschen"))
        self.choosenFile.setText(_translate("Dialog", "Ausgewählte Datei"))
        self.Image_Label.setText(_translate("Dialog", "TextLabel"))
        self.Label_Vorhersage.setText(_translate("Dialog", "TextLabel"))

