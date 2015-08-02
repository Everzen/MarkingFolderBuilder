##################################################################################################################################
##Developer: Richard Jones
##Contact:   3dframework@gmail.com
##
##Tool: Marking Folder Builder
##		- Tool to add folder structures that match up to students on a module
##		- Look to add XML data stripped straight from course sheets - TEST CODE - MORE TEST CODE
########################################################################################################################################

import sys
from PySide import QtGui, QtCore
import copy

#############################################################################################################
import SVFX.system as SVFXS
import SVFX.fileControl as SVFXF


##Import Package Contents
import myWidgets



class MarkingFolderWindow(QtGui.QWidget):
    
	def __init__(self):
		super(MarkingFolderWindow, self).__init__()

		self.initUI()
	
	def initUI(self):

		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
		# fileSystemModel = QtGui.QFileSystemModel(self.folderStructTw) # Not sure that tehse next two lines are necessary - #Test
		# fileSystemModel.setReadOnly(False)

		introLabel = QtGui.QLabel("USER LIST - Please select the users that you wish to generate folders for, using the selection filters on the right")

		userTVFrame = QtGui.QFrame(self) # Create frame and Layout to hold all the User List View
		userTVFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		userTVLayout = QtGui.QVBoxLayout(userTVFrame)

		#################################################ADDING USER LIST - QTREEWIDGET#############################################
		self.userListTw =  QtGui.QTreeWidget() #This tree is to be replaced by the custom tree to handle student data and drag and drop
		self.userListTw.setHeaderLabels(["Surname","Forename","Login","Year","Course","Status"])
		self.userListTw.setMinimumWidth(620)


		################################################END OF USER LIST - QTREEWIDGET##############################################
		userTVLayout.addWidget(introLabel)
		userTVLayout.addWidget(self.userListTw)

		vOptionSplitter = QtGui.QSplitter(QtCore.Qt.Vertical) #Create splitter for the right hand side options

		filtersFrame = QtGui.QFrame(self) #Create a Frame for the top Listview Filters
		filtersFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		vboxFilterLayout = QtGui.QVBoxLayout(filtersFrame) # Create a Layout for the top User Filters buttons and labels

		filterLabel = QtGui.QLabel("Use Selection Filters") # Add top label to the filter layout
		vboxFilterLayout.addWidget(filterLabel)

		hboxUserChoices = QtGui.QHBoxLayout() #Create little layout for 3 User Filter ListView Widgets
		
		#################################################ADDING LV FILTERS#############################################
		self.courseLw = QtGui.QListWidget()
		self.courseLw.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.yearLw = QtGui.QListWidget()
		self.yearLw.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		self.statusLw = QtGui.QListWidget()
		self.statusLw.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

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
		# for index in xrange(self.courseLw.count()): self.courseLw.setItemSelected(self.courseLw.item(index),True)
		# for index in xrange(self.yearLw.count()): self.yearLw.setItemSelected(self.yearLw.item(index),True)
		# for index in xrange(self.statusLw.count()): self.statusLw.setItemSelected(self.statusLw.item(index),True)
		for index in xrange(self.courseLw.count()): self.courseLw.item(index).setSelected(True)
		for index in xrange(self.yearLw.count()): self.yearLw.item(index).setSelected(True)
		for index in xrange(self.statusLw.count()): self.statusLw.item(index).setSelected(True)
		################################################END OF LV FILTERS##############################################

		hboxUserChoices.addWidget(self.courseLw)
		hboxUserChoices.addWidget(self.yearLw)
		hboxUserChoices.addWidget(self.statusLw)

		vboxFilterLayout.addLayout(hboxUserChoices) 

		updateUserListBtn = QtGui.QPushButton("Update User List") #Create bottom push button to Update Filter List
		vboxFilterLayout.addWidget(updateUserListBtn)

		vOptionSplitter.addWidget(filtersFrame)  #Now the filters options are complete add them to the options vertical splitter - Top section of side splitter options

		lowerOptionsFrame = QtGui.QFrame(self) #Create a Frame for all the lower side options
		lowerOptionsFrame.setFrameShape(QtGui.QFrame.NoFrame)	
		lowerOptionsLayout = QtGui.QVBoxLayout(lowerOptionsFrame)

		foldersFrame = QtGui.QFrame(self) #Create a Frame for all folder options
		foldersFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		vBoxFolderLayout = QtGui.QVBoxLayout(foldersFrame) #Vertical layout to arrange all folder option


		folderLabel = QtGui.QLabel("SETUP MARKING FOLDER LOCATION AND STRUCTURE")
		vBoxFolderLayout.addWidget(folderLabel)
		
		hBoxFolders = QtGui.QHBoxLayout() # Create little horizontal layout for folder line edit and button
		folderLE = QtGui.QLineEdit()
		hBoxFolders.addWidget(folderLE)

		folderBtn = QtGui.QPushButton("Choose \n Directory")
		hBoxFolders.addWidget(folderBtn)

		vBoxFolderLayout.addLayout(hBoxFolders)
		
		lowerOptionsLayout.addWidget(foldersFrame)  #Add folder frame to our side lower options frame

		folderStructFrame = QtGui.QFrame(self) #Create a Frame for all folder structure options
		folderStructFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		vBoxFolderStructLayout = QtGui.QVBoxLayout(folderStructFrame) #Vertical layout to arrange all folder structure options

		sampleFolderLbl = QtGui.QLabel("SAMPLE FOLDERS") #Create and add label for Sample Folder Table Widget to drag and drop folder names
		vBoxFolderStructLayout.addWidget(sampleFolderLbl)

		#################################################ADDING Folder NAME - SUBCLASSED QTABLEWIDGET#############################################

		self.sampleFolderTabW = myWidgets.FolderNamesTabW() #Create and add Sample Folder subclassed (myWidgets) Table Widget to drag and drop folder names
		self.sampleFolderTabW.setRowCount(4)
		self.sampleFolderTabW.setColumnCount(3)
		self.sampleFolderTabW.horizontalHeader().setVisible(False)
		self.sampleFolderTabW.verticalHeader().setVisible(False)
		self.sampleFolderTabW.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.folderNamesList = ["Student_Name","Module_Name","Assignment_01", "Assignment_02", "Report", "Artefacts", "Animation", "Presentation", "Plan", "FinalImages", "Practical", "Assets"] # Data for Table Widget Folder Names
		self.populateSampleFolderNameTabW() #Populate this table for folder name dragging

		vBoxFolderStructLayout.addWidget(self.sampleFolderTabW)

		folderStructTW = QtGui.QTreeWidget() #Create and add Folder Tree Widget to drag and drop folder structure
		vBoxFolderStructLayout.addWidget(folderStructTW)

		clearFolderStructBtn = QtGui.QPushButton("Clear Folder Stucture")
		vBoxFolderStructLayout.addWidget(clearFolderStructBtn)

		lowerOptionsLayout.addWidget(folderStructFrame) #Add folder structure frame to our side lower options frame 


		folderCreateFrame = QtGui.QFrame(self) #Create a Frame for all final Folder Create
		folderCreateFrame.setFrameShape(QtGui.QFrame.Panel)
		folderCreateFrame.setLineWidth(3)
		folderCreateFrame.setFrameShadow(QtGui.QFrame.Raised)
		folderCreateLayout = QtGui.QVBoxLayout(folderCreateFrame)
		
		createFolderStructBtn = QtGui.QPushButton("CREATE MARKING FOLDERS")
		folderCreateLayout.addWidget(createFolderStructBtn)

		lowerOptionsLayout.addWidget(folderCreateFrame)  #Add folder create frame to our side lower options frame
		
		vOptionSplitter.addWidget(lowerOptionsFrame) #Now add this total side lower options frame to the main vertical side splitter


		topHSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal) #Create Top horizontal splitter to allow us to separate User List options from Side options
		topHSplitter.addWidget(userTVFrame)
		topHSplitter.addWidget(vOptionSplitter)

		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		
		topHbox = QtGui.QHBoxLayout() #Finish off with a top level Layout to hold the main splitter
		topHbox.addWidget(topHSplitter)

		self.setLayout(topHbox)   
		
		self.setGeometry(300, 300, 1100, 757)
		self.setWindowTitle('Marking Folder Builder')    
		self.show()

	def populateSampleFolderNameTabW(self):
		self.folderNameCounter = 0
		for i in range(0,4):
			for j in range(0,3):
				if self.folderNameCounter < len(self.folderNamesList):
					print "Item Created  " + self.folderNamesList[self.folderNameCounter]
					item = QtGui.QTableWidgetItem(self.folderNamesList[self.folderNameCounter])
					self.sampleFolderTabW.setItem(i,j,item)
					self.folderNameCounter += 1
					print str(i) + " " + str(j)




def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MarkingFolderWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()