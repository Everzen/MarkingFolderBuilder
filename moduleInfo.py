import xlrd #For reading Excel Files
import xlsxwriter #For Writing Excel Files
from operator import itemgetter #Used to automatically sort a dictionary by a key value!

import SVFX.system as SVFXS 


class moduleData():
	"""A class to strip all of the data out of an excel document containing module student groups"""
	def __init__(self, xlsxFile):
		"""function to initialise class with correct file data"""
		self.xlsxFile = xlsxFile
		self.workbook = xlrd.open_workbook(self.xlsxFile) #Pick out the Xlsx file and the first worksheet
		self.worksheet = self.workbook.sheet_by_index(0)

		self.moduleCode = None
		self.moduleName = None
		self.moduleTutor = None
		self.academicYear = None
		self.semester = None

		self.studentInfoHeaders = []
		self.studentList = [] #The user list should be a list of dictionaries all containing the relevant details that we want to work with

		self.titleInfoRow = 0
		self.studentStartRow = 0
		self.studentEndRow = 0
		self.studentStartColumn = 1
		self.studentEndColumn = 16 #This value is hardcoded for this sheet, since the sheet.ncols seems to return extra columns!		

		print "MY Sheet cell is" + str(self.worksheet.cell_value(5,1)) #This hardcode link picks out the module information. Breakdown into separate titles
		print "Doc Rows " + str(self.worksheet.nrows)

		self.getModuleTitleInfo()
		self.getStudentInfo()

	def getModuleTitleInfo(self):
		"""Function to strip the main module data out of the module xlsx file"""
		pass

	def getStudentInfo(self):
		"""Function that searches out the student block of data in the xlsx file and populates some student info"""
		self.studentList = [] #Clear teh student list
		#First of all scane for the Start row and the title Row for the student data
		for r in xrange(0,self.worksheet.nrows):
			cellVal = str(self.worksheet.cell_value(r,1)) #Data in the Sugden report is filled out to start down column B (column 1)
			print "Checked cell value is " + cellVal
			if cellVal == "Bolton ID":
				self.titleInfoRow = r 
				self.studentStartRow = r + 1

		#Now scen for the last row of student data by looking for the next empty line
		r = self.studentStartRow
		while not self.studentEndRow:
			cellVal = str(self.worksheet.cell_value(r,1)) #Data in the Sugden report is filled out to start down column B (column 1)
			if not cellVal:
				self.studentEndRow = r
			r += 1

		#Now find the major categories that define a user from the central 
		self.studentInfoHeaders = []
		for c in range(1, self.studentEndColumn): #Data in the Sugden report is filled out to start down column B (column 1)
			cellVal = self.worksheet.cell_value(self.titleInfoRow,c)
			if cellVal: self.studentInfoHeaders.append(cellVal)

		print "self.studentInfoHeaders : " + str(self.studentInfoHeaders)

		#Now populate the student data into these headings!
		for r in xrange(self.studentStartRow,self.studentEndRow):
			student = {} #Create an empty dictionary student
			for c in xrange(1, self.studentEndColumn): #Data in the Sugden report is filled out to start down column B (column 1)
				cat = self.worksheet.cell_value(self.titleInfoRow,c) #USe titleRow to create the category name
				student[cat] = self.worksheet.cell_value(r,c)
			self.studentList.append(student)

		self.studentList = sorted(self.studentList, key=itemgetter('Surname')) #Sort the users into surname alphabetical order

		print "User List is: " + str(self.studentList)


	def getStudentList(self):
		return self.studentList

	def getStudentInfoHeaders(self):
		return self.studentInfoHeaders






##PRACTICE EXECUTION
#module = moduleData("SFX5000_Report.xlsx")
