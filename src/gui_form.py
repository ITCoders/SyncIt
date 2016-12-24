# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_form.ui'
#
# Created: Fri Apr  8 17:08:42 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SyncIt(object):
    def setupUi(self, SyncIt):
        SyncIt.setObjectName(_fromUtf8("SyncIt"))
        SyncIt.resize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        SyncIt.setFont(font)
        self.centralwidget = QtGui.QWidget(SyncIt)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 70, 571, 301))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeWidget = QtGui.QTreeWidget(self.horizontalLayoutWidget)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.horizontalLayout.addWidget(self.treeWidget)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 40, 151, 17))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(620, 50, 161, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(647, 70, 121, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 130, 121, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(650, 200, 121, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(650, 280, 121, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(690, 540, 66, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(650, 340, 121, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        SyncIt.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SyncIt)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSyncIt = QtGui.QMenu(self.menubar)
        self.menuSyncIt.setObjectName(_fromUtf8("menuSyncIt"))
        SyncIt.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SyncIt)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SyncIt.setStatusBar(self.statusbar)
        self.menuSyncIt.addSeparator()
        self.menubar.addAction(self.menuSyncIt.menuAction())

        self.retranslateUi(SyncIt)
        QtCore.QMetaObject.connectSlotsByName(SyncIt)

    def retranslateUi(self, SyncIt):
        SyncIt.setWindowTitle(_translate("SyncIt", "MainWindow", None))
        self.label.setText(_translate("SyncIt", "Browse Drive", None))
        self.label_2.setText(_translate("SyncIt", "please Login", None))
        self.pushButton.setText(_translate("SyncIt", "Login", None))
        self.pushButton_2.setText(_translate("SyncIt", "ChooseDir", None))
        self.pushButton_3.setText(_translate("SyncIt", "New Folder", None))
        self.pushButton_4.setText(_translate("SyncIt", "Sync", None))
        self.label_3.setText(_translate("SyncIt", "Status", None))
        self.pushButton_5.setText(_translate("SyncIt", "Refresh", None))
        self.menuSyncIt.setTitle(_translate("SyncIt", "SyncIt", None))



