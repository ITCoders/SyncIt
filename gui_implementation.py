import sys
import os
from PyQt4 import QtGui,QtDesigner,QtCore
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
import subprocess
from gui import Ui_Dialog
class window(QtGui.QFileDialog):
	"""docstring for window"""
	ui = Ui_Dialog()
	def creater(self):
		Dialog = QtGui.QDialog()
		self.ui.setupUi(Dialog)
		QObject.connect(self.ui.pushButton,SIGNAL("clicked()"),self.onclick_pushbutton)
		Dialog.show()
		list_widget = self.ui.listWidget
		list_widget.addItem("item1")
		list_widget.addItem("item2")
		list_widget.addItem("item3")
		list_widget.itemClicked.connect(list_widget.Clicked)
		sys.exit(app.exec_())
	def onclick_pushbutton(self):
		# subprocess.call(["nautilus"])
		# self.select_files()
		self.select_folders()
	def select_files(self):
		filename = QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getenv("HOME"))
		print(filename)
	def select_folders(self):
		dir_name = QFileDialog.getExistingDirectory(self,'open dir','/home/arpit/',QFileDialog.ShowDirsOnly)
		print(dir_name)
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	appcomp = window()
	appcomp.creater()