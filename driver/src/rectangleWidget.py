# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\rectangleWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(295, 319)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.propertiesForm = QtWidgets.QFormLayout()
        self.propertiesForm.setObjectName("propertiesForm")
        self.widthLabel_4 = QtWidgets.QLabel(Form)
        self.widthLabel_4.setObjectName("widthLabel_4")
        self.propertiesForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.widthLabel_4)
        self.widthLineEdit_4 = QtWidgets.QLineEdit(Form)
        self.widthLineEdit_4.setObjectName("widthLineEdit_4")
        self.propertiesForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.widthLineEdit_4)
        self.heightLabel_4 = QtWidgets.QLabel(Form)
        self.heightLabel_4.setObjectName("heightLabel_4")
        self.propertiesForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.heightLabel_4)
        self.heightLineEdit_4 = QtWidgets.QLineEdit(Form)
        self.heightLineEdit_4.setObjectName("heightLineEdit_4")
        self.propertiesForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.heightLineEdit_4)
        self.redLabel_4 = QtWidgets.QLabel(Form)
        self.redLabel_4.setObjectName("redLabel_4")
        self.propertiesForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.redLabel_4)
        self.redLineEdit_4 = QtWidgets.QLineEdit(Form)
        self.redLineEdit_4.setObjectName("redLineEdit_4")
        self.propertiesForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.redLineEdit_4)
        self.greenLabel_4 = QtWidgets.QLabel(Form)
        self.greenLabel_4.setObjectName("greenLabel_4")
        self.propertiesForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.greenLabel_4)
        self.greenLineEdit_4 = QtWidgets.QLineEdit(Form)
        self.greenLineEdit_4.setObjectName("greenLineEdit_4")
        self.propertiesForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.greenLineEdit_4)
        self.blueLabel_4 = QtWidgets.QLabel(Form)
        self.blueLabel_4.setObjectName("blueLabel_4")
        self.propertiesForm.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.blueLabel_4)
        self.blueLineEdit_4 = QtWidgets.QLineEdit(Form)
        self.blueLineEdit_4.setObjectName("blueLineEdit_4")
        self.propertiesForm.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.blueLineEdit_4)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.propertiesForm.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.verticalLayout.addLayout(self.propertiesForm)
        self.positionForm = QtWidgets.QFormLayout()
        self.positionForm.setObjectName("positionForm")
        self.horizontalCornerLineEdit_3 = QtWidgets.QLineEdit(Form)
        self.horizontalCornerLineEdit_3.setObjectName("horizontalCornerLineEdit_3")
        self.positionForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.horizontalCornerLineEdit_3)
        self.verticalCornerLabel_3 = QtWidgets.QLabel(Form)
        self.verticalCornerLabel_3.setObjectName("verticalCornerLabel_3")
        self.positionForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.verticalCornerLabel_3)
        self.verticalCornerLineEdit_3 = QtWidgets.QLineEdit(Form)
        self.verticalCornerLineEdit_3.setObjectName("verticalCornerLineEdit_3")
        self.positionForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.verticalCornerLineEdit_3)
        self.horizontalCornerLabel_3 = QtWidgets.QLabel(Form)
        self.horizontalCornerLabel_3.setObjectName("horizontalCornerLabel_3")
        self.positionForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.horizontalCornerLabel_3)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.positionForm.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_2)
        self.verticalLayout.addLayout(self.positionForm)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.widthLabel_4.setText(_translate("Form", "Width"))
        self.heightLabel_4.setText(_translate("Form", "Height"))
        self.redLabel_4.setText(_translate("Form", "Red"))
        self.greenLabel_4.setText(_translate("Form", "Green"))
        self.blueLabel_4.setText(_translate("Form", "Blue"))
        self.label.setText(_translate("Form", "Properties"))
        self.verticalCornerLabel_3.setText(_translate("Form", "Vertical Corner"))
        self.horizontalCornerLabel_3.setText(_translate("Form", "Horizontal Corner"))
        self.label_2.setText(_translate("Form", "Initial Position"))
        self.pushButton.setText(_translate("Form", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
