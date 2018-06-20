import sys
from os import path as osp
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from addStepsDialogUi import Ui_addStepsDialog

CSTM_STEP_WIDGET_HEIGHT = 20

PRESETS = [["step1", "step1.1"], ["step2", "step2.1", "step2.2"], ["step3"], ["step4", "step4.1", "step4.2"]]


class CustomStepWidget(QWidget):

	click = Signal(int)

	def __init__(self, owner, parentIndex=-1):
		super(CustomStepWidget, self).__init__(owner)
		self.parentIndex = parentIndex
		self.setContentsMargins(0,0,0,0)
		layout = QHBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.setSpacing(0)
		layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		self.setLayout(layout)
		button = QPushButton("add custom")
		button.setFixedHeight(CSTM_STEP_WIDGET_HEIGHT - 2)
		button.setMaximumWidth(90)
		button.clicked.connect(self.emitClick)
		layout.addWidget(button)

	def emitClick(self):
		self.click.emit(self.parentIndex)


class AddStepsDialog(QDialog, Ui_addStepsDialog):

	def __init__(self):
		super(AddStepsDialog, self).__init__()
		self.setupUi(self)
		self.addPresets()
		self.addButtons()
		self.postSetup()

	def postSetup(self):
		self.addStepsTW.expandAll()
		self.setWindowTitle("Manage steps")
	
	def addPresets(self):
		for step in PRESETS:
			newTop = QTreeWidgetItem([step[0]])
			newTop.setFlags(Qt.ItemIsEnabled)
			self.addStepsTW.addTopLevelItem(newTop)
			for i in range(1,len(step)):
				newChild = QTreeWidgetItem([step[i]])
				newChild.setFlags(Qt.ItemIsEnabled)
				newTop.addChild(newChild)

	def addButtons(self):
		root = self.addStepsTW.invisibleRootItem()
		for i in range(root.childCount()):
			step = root.child(i)
			cstmSubItem = QTreeWidgetItem()
			cstmSubItem.setSizeHint(0, QSize(0, CSTM_STEP_WIDGET_HEIGHT))
			cstmSubItem.setFlags(Qt.ItemIsEnabled)
			cstmSubWidget = CustomStepWidget(self.addStepsTW, i)
			cstmSubWidget.click.connect(self.addCustomStep)
			step.addChild(cstmSubItem)
			self.addStepsTW.setItemWidget(cstmSubItem, 0, cstmSubWidget)
		cstmItem = QTreeWidgetItem()
		cstmItem.setSizeHint(0, QSize(0, CSTM_STEP_WIDGET_HEIGHT))
		cstmItem.setFlags(Qt.ItemIsEnabled)
		cstmWidget = CustomStepWidget(self.addStepsTW)
		cstmWidget.click.connect(self.addCustomStep)
		self.addStepsTW.addTopLevelItem(cstmItem)
		self.addStepsTW.setItemWidget(cstmItem, 0, cstmWidget)

	@Slot(int)
	def addCustomStep(self, parentIndex):
		if self.addStepsTW.state() == QAbstractItemView.EditingState:
			return
		step = QTreeWidgetItem()
		step.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
		if parentIndex == -1:
			# no parent --> add top level item and add a child button to it
			index = self.addStepsTW.invisibleRootItem().childCount() - 1
			self.addStepsTW.insertTopLevelItem(index, step)
			child = QTreeWidgetItem()
			child.setSizeHint(0, QSize(0, CSTM_STEP_WIDGET_HEIGHT))
			child.setFlags(Qt.ItemIsEnabled)
			cstmWidget = CustomStepWidget(self.addStepsTW, index)
			cstmWidget.click.connect(self.addCustomStep)
			step.addChild(child) #<-- ISN'T THIS SUPPOSED TO WORK??
			self.addStepsTW.setItemWidget(child, 0, cstmWidget)
		else:
			# parent exists --> add child step to it
			parentItem = self.addStepsTW.invisibleRootItem().child(parentIndex)
			parentItem.insertChild(parentItem.childCount() - 1, step)
		self.addStepsTW.editItem(step, 0)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	dialog = AddStepsDialog()
	dialog.exec_()
