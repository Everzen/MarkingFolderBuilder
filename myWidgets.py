##################################################################################################################################
##Developer: Richard Jones
##Contact:   3dframework@gmail.com
##
##Tool: Marking Folder Builder
##      - Tool to add folder structures that match up to students on a module
##      - Look to add XML data stripped straight from course sheets
##
##      -Widgets: For subclassing Pyside Widgets
########################################################################################################################################


from PySide import QtGui, QtCore
# import maya.OpenMayaUI as apiUI


class UserTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, lWUser, parent = None):
        self.user = lWUser
    	QtGui.QTreeWidgetItem.__init__(self,[lWUser.getSurname(),lWUser.getForename(),lWUser.getID(),lWUser.getYear(),lWUser.getCourse(), lWUser.getStatus()])

    def getUser(self):
    	return self.user


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

	def startDrag(self, dropAction):
		mime = QtCore.QMimeData()
		cItem = self.currentItem()
		mime.setData("text/folderName", str(cItem.text()))
		drag = QtGui.QDrag(self)
		drag.setMimeData(mime) 
		drag.start(QtCore.Qt.CopyAction | QtCore.Qt.CopyAction)

