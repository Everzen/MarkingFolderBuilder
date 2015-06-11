
##TDFRAMEWORK IMPORTS######################
import TDFramework.system as TDFS
import TDFramework.fileControl as TDFF

#Source code for some common Maya/PyQt functions we will be using
#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)
from PySide import QtGui, QtCore
import maya.OpenMayaUI as apiUI
import copy

#############################################################################################################
##Import Package Contents
import myWidgets

#############################################################################################################
#Start Engine and Grab User Info
engineInfo = TDFS.EngineInfo()
userList = engineInfo.getUserInfo()

#############################################################################################################

def getMayaWindow():
	"""
	Get the main Maya window as a QtGui.QMainWindow instance
	@return: QtGui.QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return sip.wrapinstance(long(ptr), QtCore.QObject)

def toQtObject(mayaName):
	"""
	Convert a Maya ui path to a Qt object
	@param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
	@return: PyQt representation of that object
	"""
	ptr = apiUI.MQtUtil.findControl(mayaName)
	if ptr is None:
		ptr = apiUI.MQtUtil.findLayout(mayaName)
	if ptr is None:
		ptr = apiUI.MQtUtil.findMenuItem(mayaName)
	if ptr is not None:
		return sip.wrapinstance(long(ptr), QtCore.QObject)



##MAIN FUNCTIONALITY######################################################
from PyQt4 import uic
#If you put the .ui file for this example elsewhere, just change this path.
listExample_form, listExample_base = uic.loadUiType('N:/TDF_Ops/Resources/Experiments/PyQtUis/UserFolderBoy.ui')
class ListExample(listExample_form, listExample_base):
	def __init__(self, parent=getMayaWindow()):
		super(ListExample, self).__init__(parent)
		self.setupUi(self)
		fileSystemModel = QtGui.QFileSystemModel(self.folderStructTw)
		fileSystemModel.setReadOnly(False)

		#Data
		self.userListLwElements = list(userList)
		self.folderNamesList = ["Student_Name","Module_Name","Assignment_01", "Assignment_02", "Report", "Artefacts", "Animation", "Presentation", "Plan", "FinalImages", "Practical", "Assets"]
		self.rootDir = None

		#Setup UserList Header Labels
		self.userListTw.setHeaderLabels(["Surname","Forename","Login","Year","Course","Status"])
		
		QtGui.QListWidgetItem("SFX", self.courseLw)
		QtGui.QListWidgetItem("VFX", self.courseLw)
		QtGui.QListWidgetItem("GAR", self.courseLw)
		QtGui.QListWidgetItem("FPI", self.courseLw)


		QtGui.QListWidgetItem("Year 1", self.yearLw)
		QtGui.QListWidgetItem("Year 2", self.yearLw)
		QtGui.QListWidgetItem("Year 3", self.yearLw)
		QtGui.QListWidgetItem("Year 4", self.yearLw)

		QtGui.QListWidgetItem("Student", self.statusLw)
		QtGui.QListWidgetItem("Lecturer", self.statusLw)

		#Select all options in Filters
		for index in xrange(self.courseLw.count()): self.courseLw.setItemSelected(self.courseLw.item(index),True)
		for index in xrange(self.yearLw.count()): self.yearLw.setItemSelected(self.yearLw.item(index),True)
		for index in xrange(self.statusLw.count()): self.statusLw.setItemSelected(self.statusLw.item(index),True)

		#Populate Folder Names
		self.populateFolderNameTabW()

		#Populate Folder Structure Tree Widget
		#folderStructModuleName = QtGui.QTreeWidgetItem(["Module_Name"])
		#folderStructModuleName.setFlags(folderStructModuleName.flags() | QtCore.Qt.ItemIsEditable)
		#self.folderStructTw.addTopLevelItem(folderStructModuleName)
		#self.folderStructTw.setEditTriggers(self.folderStructTw.DoubleClicked)

		#Populate User List
		self.populateUserListTw()

		#Connect UI Elements
		self.updateUserListBtn.clicked.connect(self.updateUserListBtnPress)
		self.clearFolderStrucBtn.clicked.connect(self.clearFolderStructPress)
		self.directoryBtn.clicked.connect(self.directoryBtnPress)
		self.genFolderBtn.clicked.connect(self.generateMarkingFolders)

		
		#self.folderStructTw.itemDoubleClicked.connect(self.editTreeWidget)


		#Add contect sensitive menus to User List Tree Widget
		self.userListTw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.userListTw.customContextMenuRequested.connect(self.userListPopup)

		#Add contect sensitive menus to Folder Structure Tree Widget
		self.folderStructTw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.folderStructTw.customContextMenuRequested.connect(self.folderStructVPopup)
		

		# item=QtGui.QTreeWidgetItem(["Jones","Richard","rpj1","VFX","NA","Lecture"])
		# self.userListTw.addTopLevelItem(item)
		# #Setup Contect Sensitive Menus
		# self.dragFromLw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# self.dragFromLw.customContextMenuRequested.connect(self.tVPopup)

		# engineInfo = TDFS.EngineInfo()
		# userList = engineInfo.getUserInfo()
		# print str(userList)	
		# print ("userList[0] =" + str(help(userList[0]))) 	
		
		# self.dragFromLw.itemPressed.connect(self.findItem)
		# for u in userList:
		#     SuperListWidgetItem(self.dragFromLw, u)
		# #lWItem = QtGui.QListWidgetItem("Hazel", self.dragFromLw)

	def getCourseFilter(self):
		"""A function to return an array for the course Filter Listwidget"""
		filterList = []
		for index in xrange(self.courseLw.count()): 
			if self.courseLw.item(index).isSelected():
				filterList.append(str(self.courseLw.item(index).text()))
		return filterList

	def getYearFilter(self):
		"""A function to return an array for the Year Filter Listwidget"""
		filterList = []
		for index in xrange(self.yearLw.count()): 
			if self.yearLw.item(index).isSelected():
				filterList.append(index + 1)
		return filterList

	def getStatusFilter(self):
		"""A function to return an array for the Status Filter Listwidget"""
		filterList = []
		for index in xrange(self.statusLw.count()): 
			if self.statusLw.item(index).isSelected():
				filterList.append(str(self.statusLw.item(index).text()))
		return filterList

	def filterUser(self):
		"""Function to establish User List after selection Filters"""
		filteredUserList = []
		tempList = []

		for u in userList:
			for statusFilter in self.getStatusFilter():
				if u.getStatus() == statusFilter:
					tempList.append(u)
		
		filteredUserList = list(tempList)
		tempList = []
		for u in filteredUserList:
			for yearFilter in self.getYearFilter():
				if str(u.getYear()) == str(yearFilter) or u.getYear() == "NA":
					if u not in tempList: tempList.append(u)

		filteredUserList = list(tempList)
		tempList = []
		for u in filteredUserList:
			for courseFilter in self.getCourseFilter():
				if u.getCourse() == courseFilter:
					tempList.append(u)

		self.userListLwElements = tempList
		return self.userListLwElements

	def populateUserListTw(self):
		"""Function to populate the user treewidget with the names of students with the appropriate selection filters."""
		self.userListTw.clear()
		for u in self.userListLwElements:
			item = myWidgets.UserTreeWidgetItem(u)
			self.userListTw.addTopLevelItem(item)				

	def updateUserListBtnPress(self):
		self.filterUser()
		self.populateUserListTw()

	def directoryBtnPress(self):
		folderDir = QtGui.QFileDialog.getExistingDirectory()
		self.rootDir = folderDir
		self.directoryLe.setText(folderDir)
		
	def clearFolderStructPress(self):
		"""Function to clear the contents of the folder structure tree view"""
		self.folderStructTw.clear()

	def populateFolderNameTabW(self):
		self.folderNameCounter = 0
		for i in range(0,4):
			for j in range(0,3):
				if self.folderNameCounter < len(self.folderNamesList):
					item = QtGui.QTableWidgetItem(self.folderNamesList[self.folderNameCounter])
					self.folderNameTabW.setItem(i,j,item)
					self.folderNameCounter += 1

	def folderStructVPopup(self, pos):
		menu = QtGui.QMenu()
		rename = menu.addAction("Rename")
		delFolder = menu.addAction("Delete")
		action = menu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x()+630,pos.y()+410)))
		if action == rename:
				self.renameFolderStructTwItem()
		elif action == delFolder:
				self.delFolderTwItem()

	def renameFolderStructTwItem(self):
		cItem = self.folderStructTw.currentItem()
		cItem.setFlags(cItem.flags() | QtCore.Qt.ItemIsEditable)
		self.folderStructTw.editItem(cItem)

	def delFolderTwItem(self):
		cItem = self.folderStructTw.currentItem()
		cItem.setFlags(cItem.flags() | QtCore.Qt.NoItemFlags)
		self.folderStructTw.removeItemWidget(cItem,0)

	def userListPopup(self, pos):
		menu = QtGui.QMenu()
		hideUsers = menu.addAction("Hide")
		showUsers = menu.addAction("Show Only")
		action = menu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x(),pos.y()+70)))
		if action == hideUsers:
				self.hideUsersTwItem()
		elif action == showUsers:
				self.showUsersTwItem()

	def showUsersTwItem(self):
		"""Function that redraws the tree with only the selected users. It does this by copying the user object and recreating the treeWidgetItems for the redraw"""
		newUserList = []
		for i in xrange(self.userListTw.topLevelItemCount()):
			if self.userListTw.topLevelItem(i).isSelected():
					newUser = copy.copy(self.userListTw.topLevelItem(i).getUser())
					newUserList.append(newUser)
		#Clear the tree
		self.userListTw.clear()
		for u in newUserList:
			item = myWidgets.UserTreeWidgetItem(u)
			self.userListTw.addTopLevelItem(item)	

	def hideUsersTwItem(self):
		"""Function that redraws the tree removing the selected users. It does this by copying the user object and recreating the treeWidgetItems for the redraw"""
		newUserList = []
		for i in xrange(self.userListTw.topLevelItemCount()):
			if not self.userListTw.topLevelItem(i).isSelected():
					newUser = copy.copy(self.userListTw.topLevelItem(i).getUser())
					newUserList.append(newUser)
		#Clear the tree
		self.userListTw.clear()
		for u in newUserList:
			item = myWidgets.UserTreeWidgetItem(u)
			self.userListTw.addTopLevelItem(item)
	
	def getSelectedUsers(self):
		#First of all grab the selected users
		userFolderList = []
		for i in xrange(self.userListTw.topLevelItemCount()):
				if self.userListTw.topLevelItem(i).isSelected():
					userName = self.userListTw.topLevelItem(i).getUser().getSurname() + "_" + self.userListTw.topLevelItem(i).getUser().getForename()
					userFolderList.append(userName)
		return userFolderList


	def createMarkingFolder(self, folderStrucItem, path):
		"""Function to iteratively loop through the tree and build the folder structure"""
		folderName = str(folderStrucItem.text(0))
		if folderName == "Student_Name":
			#We have hit a student folder where all the names need to now be fed in
			userFolderList = self.getSelectedUsers()
			for u in userFolderList:
				folderFullPath = TDFF.FileMan((path + "/" + u))
				folderFullPath.createDir()
				for i in xrange(folderStrucItem.childCount()):
					self.createMarkingFolder(folderStrucItem.child(i), folderFullPath.getFile())
		else:
			folderFullPath = TDFF.FileMan((path + "/" + folderName))
			folderFullPath.createDir()
			for i in xrange(folderStrucItem.childCount()):
				self.createMarkingFolder(folderStrucItem.child(i), folderFullPath.getFile())

	def generateMarkingFolders(self):
		"""Function to execute the iterative loop and creation of folder structure"""
		if self.rootDir != None and self.userListTw.topLevelItemCount() != 0 and self.folderStructTw.topLevelItemCount() != 0:
			for i in xrange(self.folderStructTw.topLevelItemCount()):
				#now iterative create the folder structures
				self.createMarkingFolder(self.folderStructTw.topLevelItem(i), self.rootDir)
		else:
			print "There has been an error. No root has been declared, no users selected, or no folder structure specified"







fred = ListExample()
fred.show()