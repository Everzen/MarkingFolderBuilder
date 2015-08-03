##################################################################################################################################
##Developer: Richard Jones
##Contact:   3dframework@gmail.com
##
##Tool: Marking Folder Builder
##      - Tool to add folder structures that match up to students on a module
##      - Look to add XML data stripped straight from course sheets
##
##      -Widgets: For subclassing Pyside Widgets - TEST CODE - MORE TEST CODE
########################################################################################################################################


from PySide import QtGui, QtCore
# import maya.OpenMayaUI as apiUI

import moduleInfo


class StudentTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, student, headers, parent = None):
        self.student = student
        self.headers = headers
        self.itemInfo = []

        self.buildItem() #Collect the correct student information into the itemInfo
    	QtGui.QTreeWidgetItem.__init__(self,self.itemInfo)

    def buildItem(self):
        """A function that loops through all the header titles and matches them to the dictionary entries for the student data"""
        self.itemInfo = []
        for key in self.headers.keys():
            if self.headers[key]:
                self.itemInfo.append(self.student[key])

    def getStudent(self):
    	return self.student


class StudentTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(StudentTreeWidget, self).__init__(parent)
        moduleData = moduleInfo.moduleData("SFX5000_Report.xlsx")
        self.studentList = moduleData.getStudentList()
        
        self.studentInfoCategories = {"Bolton ID":True, "Surname": True, "Forename": True, "Network ID":False , "Disability": True, "Status Code": True,"Email":True, "Occurence":True, "Course Code":False, "Course Name":False, "Personal Tutor":False, "Personal Tutor Email":False}
        self.studentInfoHeaders = []

        self.buildHeaders()

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rCPopup)

        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.populateStudentList() #For intial testing populate the list, but this will be replaced by the drag and drop functionality


    def buildHeaders(self):
        self.studentInfoHeaders = []
        for key in self.studentInfoCategories.keys():
            if self.studentInfoCategories[key]:
                self.studentInfoHeaders.append(key)
        self.setHeaderLabels(self.studentInfoHeaders)


    def populateStudentList(self):
        """Function to populate the user treewidget with the names of students with the appropriate selection filters."""
        self.clear()

        for s in self.studentList:
            item = StudentTreeWidgetItem(s, self.studentInfoCategories)
            self.addTopLevelItem(item)   


    def rCPopup(self, pos):
        menu = QtGui.QMenu()
        rename = menu.addAction("Rename")
        delFolder = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(QtCore.QPoint(pos.x(),pos.y()+20)))
        if action == rename:
            print "RENAME"
            #self.renameFolderStructTwItem()
        elif action == delFolder:
            print "DELETE FOLDER"
            #self.delFolderTwItem()



class FolderStrucTW(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(FolderStrucTW, self).__init__(parent)

    def dragEnterEvent(self, event):
    	"""Function to overider dragEnterEvent to check that text is being used"""
    	if (event.mimeData().hasFormat('text/folderName')):
    		data = QtCore.QString(event.mimeData().data('text/folderName'))
    		event.accept()
    	else:
    		event.ignore()

    def dragMoveEvent(self, event):
    	"""Function to overider dragMoveEvent to check that text is being used"""
    	if event.mimeData().hasFormat("text/folderName"):
    		event.setDropAction(QtCore.Qt.CopyAction)
    		event.accept()
    	else:
    		event.ignore()

    def dropEvent(self, event): 
    	"""Function to overider dropEvent to check text has arrived and add it to the tree a is appropriate"""
        if (event.mimeData().hasFormat('text/folderName')):
            event.acceptProposedAction()
            #Create a new QTreeWidgetItem and transfer the text across so we have the correct name
            data = QtCore.QString(event.mimeData().data("text/folderName"))
            item = QtGui.QTreeWidgetItem()
            item.setText(0, data)
            mouseItem = self.itemAt(event.pos())
            if mouseItem != None:
            	#We have hit a treeWidgetItem to lets put our item underneath as a child of this item
            	mouseItem.addChild(item)
            else:
            	#If we have not hit a treeWidgetItem then we need to add a new top level Item
            	self.addTopLevelItem(item) 
            #Now expand out all branches of the tree 
            self.expandAll()
        else:
            event.ignore() 


class FolderNamesTabW(QtGui.QTableWidget):
	"""Class to subclass QTableWidget to give us control over how we handle the data on a startDrag"""
	def __init__(self, parent = None):
		super(FolderNamesTabW, self).__init__(parent)
        # self.setRowCount(4)
        # self.setColumnCount(3)
        # self.horizontalHeader().setVisible(False)
        # self.verticalHeader().setVisible(False)

	def startDrag(self, dropAction):
		mime = QtCore.QMimeData()
		cItem = self.currentItem()
		mime.setData("text/folderName", str(cItem.text()))
		drag = QtGui.QDrag(self)
		drag.setMimeData(mime) 
		drag.start(QtCore.Qt.CopyAction | QtCore.Qt.CopyAction)

