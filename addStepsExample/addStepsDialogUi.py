# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addStepsDialogUi.ui'
#
# Created: Fri Jun 15 15:36:08 2018
#      by: pyside2-uic  running on PySide2 5.11.0a1.dev1525357569
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_addStepsDialog(object):
    def setupUi(self, addStepsD):
        addStepsD.setObjectName("addStepsD")
        addStepsD.resize(200, 300)
        addStepsD.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(addStepsD)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setObjectName("gridLayout")
        self.stepsCancelPB = QtWidgets.QPushButton(addStepsD)
        self.stepsCancelPB.setObjectName("stepsCancelPB")
        self.gridLayout.addWidget(self.stepsCancelPB, 1, 0, 1, 1)
        self.stepsOkPB = QtWidgets.QPushButton(addStepsD)
        self.stepsOkPB.setObjectName("stepsOkPB")
        self.gridLayout.addWidget(self.stepsOkPB, 1, 1, 1, 1)
        self.addStepsTW = QtWidgets.QTreeWidget(addStepsD)
        self.addStepsTW.setStyleSheet("QTreeView::branch {  border-image: url(none.png); }")
        self.addStepsTW.setLineWidth(0)
        self.addStepsTW.setAutoScroll(True)
        self.addStepsTW.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.addStepsTW.setAutoExpandDelay(0)
        self.addStepsTW.setRootIsDecorated(False)
        self.addStepsTW.setUniformRowHeights(False)
        self.addStepsTW.setItemsExpandable(False)
        self.addStepsTW.setExpandsOnDoubleClick(False)
        self.addStepsTW.setColumnCount(1)
        self.addStepsTW.setObjectName("addStepsTW")
        self.addStepsTW.header().setVisible(False)
        self.addStepsTW.header().setMinimumSectionSize(15)
        self.gridLayout.addWidget(self.addStepsTW, 0, 0, 1, 2)

        self.retranslateUi(addStepsD)
        QtCore.QMetaObject.connectSlotsByName(addStepsD)

    def retranslateUi(self, addStepsD):
        addStepsD.setWindowTitle(QtWidgets.QApplication.translate("addStepsD", "Dialog", None, -1))
        self.stepsCancelPB.setText(QtWidgets.QApplication.translate("addStepsD", "Cancel", None, -1))
        self.stepsOkPB.setText(QtWidgets.QApplication.translate("addStepsD", "Ok", None, -1))
        self.addStepsTW.headerItem().setText(0, QtWidgets.QApplication.translate("addStepsD", "1", None, -1))

