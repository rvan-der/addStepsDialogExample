import sys
from os import path as osp
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from addStepsDialogUi import Ui_addStepsDialog

CSTM_STEP_WIDGET_HEIGHT = 20
INDENTATION = 15

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
		layout.addSpacing(INDENTATION)
		layout.addWidget(button)
		self.setStyleSheet("QPushButton {background-color: rgb(90,90,90); color: rgb(150,220,255);}")

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
		self.addStepsTW.itemChanged.connect(self.changeItem)
		self.addStepsTW.expandAll()
		self.addStepsTW.setIndentation(INDENTATION)
		self.addStepsTW.setFocusPolicy(Qt.NoFocus)
		self.setWindowTitle("Manage steps")
		self.setStyleSheet("QTreeView::indicator {background-color: rgb(90,90,90); color: rgb(230,230,230); border: none;}\
							QTreeView::indicator:checked {image: url("+osp.join(osp.dirname(__file__), "check.png")+");}\
							QTreeView {background-color: rgb(100,100,100);}")
	
	def addPresets(self):
		for step in PRESETS:
			newTop = QTreeWidgetItem([step[0]])
			newTop.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
			newTop.setCheckState(0, Qt.Unchecked)
			newTop.setForeground(0, QBrush(QColor(220,220,220,255)))
			self.addStepsTW.addTopLevelItem(newTop)
			for i in range(1,len(step)):
				newChild = QTreeWidgetItem([step[i]])
				newChild.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
				newChild.setCheckState(0, Qt.Unchecked)
				newChild.setForeground(0, QBrush(QColor(220,220,220,255)))
				newTop.addChild(newChild)

	def addButtons(self):
		root = self.addStepsTW.invisibleRootItem()
		for i in range(root.childCount()):
			step = root.child(i)
			cstmSubItem = QTreeWidgetItem()
			cstmSubItem.setSizeHint(0, QSize(0, CSTM_STEP_WIDGET_HEIGHT))
			cstmSubItem.setFlags(Qt.ItemIsEnabled)
			cstmSubBtn = CustomStepWidget(self.addStepsTW, i)
			cstmSubBtn.click.connect(self.addCustomStep)
			step.addChild(cstmSubItem)
			self.addStepsTW.setItemWidget(cstmSubItem, 0, cstmSubBtn)
		cstmItem = QTreeWidgetItem()
		cstmItem.setSizeHint(0, QSize(0, CSTM_STEP_WIDGET_HEIGHT))
		cstmItem.setFlags(Qt.ItemIsEnabled)
		cstmBtn = CustomStepWidget(self.addStepsTW)
		cstmBtn.click.connect(self.addCustomStep)
		self.addStepsTW.addTopLevelItem(cstmItem)
		self.addStepsTW.setItemWidget(cstmItem, 0, cstmBtn)

	@Slot(int)
	def addCustomStep(self, parentIndex):
		if self.addStepsTW.state() == QAbstractItemView.EditingState:
			return
		step = QTreeWidgetItem()
		step.setCheckState(0, Qt.Checked)
		step.setForeground(0, QBrush(QColor(150,220,255,255)))
		step.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
		if parentIndex == -1:
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
			parentItem = self.addStepsTW.invisibleRootItem().child(parentIndex)
			parentItem.insertChild(parentItem.childCount() - 1, step)
		self.addStepsTW.editItem(step, 0)

	@Slot(QTreeWidgetItem, int)
	def changeItem(self, item, column):
		parent = item.parent()
		if item.checkState(0) == Qt.Unchecked:
			item.setForeground(0, QBrush(QColor(220,220,220,255)))
			if not parent:
				for i in range(item.childCount() - 1):
					item.child(i).setCheckState(0, Qt.Unchecked)
		else:
			if parent:
				parent.setCheckState(0, Qt.Checked)
			item.setForeground(0, QBrush(QColor(150,220,255,255)))

if __name__ == "__main__":
	app = QApplication(sys.argv)
	dialog = AddStepsDialog()
	dialog.exec_()
