# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.getpathButton = QtWidgets.QPushButton(self.centralwidget)
        self.getpathButton.setGeometry(QtCore.QRect(50, 40, 93, 28))
        self.getpathButton.setObjectName("getpathButton")
        self.output_img = QtWidgets.QLabel(self.centralwidget)
        self.output_img.setGeometry(QtCore.QRect(240, 120, 1211, 791))
        self.output_img.setPixmap(QtGui.QPixmap("C:/Users/win 10/Pictures/Screenshots/Screenshot (1).png"))
        self.output_img.setScaledContents(True)
        self.output_img.setObjectName("output_img")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(690, 40, 93, 28))
        self.runButton.setObjectName("runButton")
        self.End_line = QtWidgets.QLabel(self.centralwidget)
        self.End_line.setGeometry(QtCore.QRect(480, 20, 55, 16))
        self.End_line.setObjectName("End_line")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(250, 50, 160, 20))
        self.horizontalSlider.setMaximum(500)
        self.horizontalSlider.setSingleStep(5)
        self.horizontalSlider.setPageStep(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSlider.setTickInterval(0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(480, 50, 160, 20))
        self.horizontalSlider_2.setMaximum(500)
        self.horizontalSlider_2.setSingleStep(5)
        self.horizontalSlider_2.setPageStep(50)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(370, 20, 55, 16))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(540, 20, 55, 16))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.start_line = QtWidgets.QLabel(self.centralwidget)
        self.start_line.setGeometry(QtCore.QRect(250, 20, 55, 16))
        self.start_line.setObjectName("start_line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getpathButton.setText(_translate("MainWindow", "Get Video"))
        self.output_img.setText(_translate("MainWindow", "output"))
        self.runButton.setText(_translate("MainWindow", "Run"))
        self.End_line.setText(_translate("MainWindow", "End Line"))
        self.start_line.setText(_translate("MainWindow", "Start Line"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

