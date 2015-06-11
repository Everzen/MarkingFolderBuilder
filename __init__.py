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

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

		introLabel = QtGui.QLabel("USER LIST - Please select the users that you wish to generate folders for, using the selection filters on the right")
		# introLabel.move(5,10)

		# topLeftSplitter = QtGui.QFrame()
		# topLeftSplitter.setFrameShape(QtGui.QFrame.StyledPanel)

		# topRightSplitter = QtGui.QFrame()
		# topRightSplitter.setFrameShape(QtGui.QFrame.StyledPanel)
 

		userLV = QtGui.QListWidget()
		userLV.resize(900, 681)
		# userLV.move(5,30)

		userlVFrame = QtGui.QFrame(self) # Create frame and Layout to hold all the User List View
		userlVFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		userlVLayout = QtGui.QVBoxLayout(userlVFrame)

		userlVLayout.addWidget(introLabel)
		userlVLayout.addWidget(userLV)

		vOptionSplitter = QtGui.QSplitter(QtCore.Qt.Vertical) #Create splitter for the right hand side options

		filtersFrame = QtGui.QFrame(self) #Create a Frame for the top Listview Filters
		filtersFrame.setFrameShape(QtGui.QFrame.StyledPanel)
		vboxFilterLayout = QtGui.QVBoxLayout(filtersFrame) # Create a Layout for the top User Filters buttons and labels

		filterLabel = QtGui.QLabel("Use Selection Filters") # Add top label to the filter layout
		vboxFilterLayout.addWidget(filterLabel)

		hboxUserChoices = QtGui.QHBoxLayout() #Create little layout for 3 User Filter ListView Widgets
		courseLV = QtGui.QListWidget()
		yearLV = QtGui.QListWidget()
		statusLV = QtGui.QListWidget()

		hboxUserChoices.addWidget(courseLV)
		hboxUserChoices.addWidget(yearLV)
		hboxUserChoices.addWidget(statusLV)

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

		sampleFolderTabW = QtGui.QTableWidget() #Create and add Sample Folder Table Widget to drag and drop folder names
		vBoxFolderStructLayout.addWidget(sampleFolderTabW)

		folderStructTW = QtGui.QTreeWidget() #Create and add Folder Tree Widget to drag and drop folder structure
		vBoxFolderStructLayout.addWidget(folderStructTW)

		clearFolderStructBtn = QtGui.QPushButton("Clear Folder Stucture")
		vBoxFolderStructLayout.addWidget(clearFolderStructBtn)

		lowerOptionsLayout.addWidget(folderStructFrame) #Add folder structure frame to our side lower options frame 


		folderCreateFrame = QtGui.QFrame(self) #Create a Frame for all final Folder Create
		folderCreateFrame.setFrameShape(QtGui.QFrame.Panel)
		folderCreateFrame.setLineWidth(3)
		folderCreateFrame.setFrameShadow(QtGui.QFrame.Raised)
		# folderCreateFrame.setFrameShape(QtGui.QFrame.NoFrame)
		folderCreateLayout = QtGui.QVBoxLayout(folderCreateFrame)
		
		createFolderStructBtn = QtGui.QPushButton("CREATE MARKING FOLDERS")
		folderCreateLayout.addWidget(createFolderStructBtn)

		lowerOptionsLayout.addWidget(folderCreateFrame)  #Add folder create frame to our side lower options frame
		
		vOptionSplitter.addWidget(lowerOptionsFrame) #Now add this total side lower options frame to the main vertical side splitter


		topHSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal) #Create Top horizontal splitter to allow us to separate User List options from Side options
		topHSplitter.addWidget(userlVFrame)
		topHSplitter.addWidget(vOptionSplitter)

		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
		
		topHbox = QtGui.QHBoxLayout() #Finish off with a top level Layout to hold the main splitter
		topHbox.addWidget(topHSplitter)

		self.setLayout(topHbox)   
		
		self.setGeometry(300, 300, 987, 757)
		self.setWindowTitle('Tooltips')    
		self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()