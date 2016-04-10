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
from gui_form import Ui_SyncIt
class window :
	ui = Ui_SyncIt()
	def create(self):
		MainWindow = QtGui.QMainWindow()
		self.ui.setupUi(MainWindow)
		self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.sync_object = sync()
		QObject.connect(self.ui.pushButton,SIGNAL("clicked()"),self.sync_object.Login)
		QObject.connect(self.ui.pushButton_5,SIGNAL("clicked()"),self.makeTreeView)
		QObject.connect(self.ui.pushButton_2,SIGNAL("clicked()"),self.select_folder)
		# QObject.connect(self.ui.pushButton_2,SIGNAL("clicked()"),self.openFileDialog)
		self.treeMenu =  QtGui.QMenu()
		self.treeAction = QtGui.QAction('Download', self.treeMenu)
		self.treeAction.triggered.connect(self.download_folder)
		self.ui.treeWidget.addAction(self.treeAction)
		MainWindow.show()
		sys.exit(app.exec_())

	def select_folder(self):
		dir_name = QFileDialog.getExistingDirectory(self,'open dir','/home/arpit/',QFileDialog.ShowDirsOnly)
		print(dir_name)
		self.working_diretory = dir_name
	def makeTreeView(self):
		file_list = self.sync_object.ListFolder('root')
		print(file_list)
		self.root = QtGui.QTreeWidgetItem(self.ui.treeWidget, ["root"])
		# self.treeWidget.
		self.populateTreeWidget(file_list,self.root)
	def populateTreeWidget(self,file_list,parent):
		for element in file_list:
			if type(element) is dict:
				a = QtGui.QTreeWidgetItem(parent,[str(element["title"])])
				if len(element["list"]) > 0 :
					self.populateTreeWidget(element["list"],a)
			else :
				a = QtGui.QTreeWidgetItem(parent,[str(element)])

	def populateListView(self,parent='root'):
		print('hello')
		self.file_list = self.sync_object.ListFolder(parent)
		print(self.file_list)
		for element in self.file_list:
			if type(element) is dict:
				self.list_widget.addItem(element['title'])
				print(element['title'])
			else:
				print(element)
				self.list_widget.addItem(element)
	def download_folder(self):
		print(self.ui.treeWidget.currentItem().text(0))


class sync :
	#function for login
	def Login(self):
		gauth=GoogleAuth()
		gauth.LocalWebserverAuth()
		gauth.Authorize()
		self.drive=GoogleDrive(gauth)
		self.window_object = window()
		self.updateUI_on_Login()
	def LogOut(self):
		import webbrowser
		webbrowser.open('accounts.google.com/logout')
	def ListFolder(self,parent):
		filelist=[]
		self.filelist = []
		file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
		for f in file_list:
			if f['mimeType']=='application/vnd.google-apps.folder':	
				filelist.append({"id":f['id'],"title":f['title'],"list":self.ListFolder(f['id'])})
			else:
				filelist.append(f['title'])
		return filelist
	def get_username(self,drive):
		file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
		for file1 in file_list:
			emailId = list(file1["owners"])[0]["emailAddress"]
		return str(emailId)[:9]
	def updateUI_on_Login(self):
		self.window_object.ui.label_2.setText("Logged in as "+self.get_username(self.drive))
		self.window_object.ui.pushButton.setText("LogOut")
		QObject.disconnect(self.window_object.ui.pushButton,SIGNAL("clicked()"),self.Login)
		QObject.connect(self.window_object.ui.pushButton,SIGNAL("clicked()"),self.LogOut)
	def download(self,folder_id,destination_location):
		if not os.path.exists(destination_location):
			os.makedirs(destination_location)
		foldered_list=self.drive.ListFile({'q':  "'"+folder_id+"' in parents and trashed=false"}).GetList()
		for file2 in foldered_list:
			if file2['mimeType']=='application/vnd.google-apps.folder':
				download(file2['id'],destination_location+os.path.sep+file2['title'])
        		# print ('title: %s, id: %d' % (file2['title'], file2['size']))
			else:
				open(destination_location+os.path.sep+file2['title'],'w+')
				local_size=os.path.getsize(destination_location+os.path.sep+file2['title'])
				drive_size=file2['fileSize']
				if local_size!=drive_size:
					file=self.drive.CreateFile({'id': file2['id']})
					file.GetContentFile(destination_location+os.path.sep+file2['title'])
	def id_of_title(self,title,parent_directory_id):
		foldered_list=drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
		for file in foldered_list:
			if(file['title']==title):
				return file['id']
		return None
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	appcomp = window()
	appcomp.create()