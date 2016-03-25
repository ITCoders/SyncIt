import os
import webbrowser
#from subprocess import call
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
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
		self.login_object = sync()
		QObject.connect(self.ui.pushButton_2,SIGNAL("clicked()"),self.login_object.Login)
		QObject.connect(self.ui.pushButton_3,SIGNAL("clicked()"),self.populateListView)
		Dialog.show()
		self.list_widget = self.ui.listWidget
		self.list_widget.itemClicked.connect(self.list_widget.Clicked)
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
		self.ROOT_FOLDER_PATH = dir_name		
		self.ROOT_FOLDER_PATH,self.ROOT_FOLDER_NAME = os.path.split(self.ROOT_FOLDER_PATH)
		print(self.ROOT_FOLDER_NAME)
	def populateListView(self,parent='root'):
		print('hello')
		self.file_list = self.login_object.ListFolder(parent)
		print(self.file_list)
		for element in self.file_list:
			if type(element) is dict:
				self.list_widget.addItem(element['title'])
				print(element['title'])
			else:
				print(element)
				self.list_widget.addItem(element)

class sync :
	#function for login
	def Login(self):
		gauth=GoogleAuth()
		gauth.LocalWebserverAuth()
		gauth.Authorize()
		self.drive=GoogleDrive(gauth)
		return self.drive
	def ListFolder(self,parent):
		filelist=[]
		file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
		for f in file_list:
			if f['mimeType']=='application/vnd.google-apps.folder':	
				filelist.append({"id":f['id'],"title":f['title'],"list":self.ListFolder(f['id'])})
			else:
				filelist.append(f['title'])
		return filelist
	# def populateList(self,parent='root'):
	# 	print('hello')
	# 	self.file_list = self.ListFolder(parent)
	# 	print(self.file_list)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	appcomp = window()
	appcomp.creater()