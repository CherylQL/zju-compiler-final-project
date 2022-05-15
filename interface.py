# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 750)
        # self.right_widget = QtWidgets.QWidget()
        # self.right_widget.setGeometry(QtCore.QRect(20, 20, 31, 31))
        # self.right_widget.setStyleSheet("background-color: rgb(255,255,255);\n""border:none;\n")
        

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open = QtWidgets.QPushButton(self.centralwidget)
        self.open.setGeometry(QtCore.QRect(20, 20, 31, 31))
        self.open.setStyleSheet("QPushButton{border-image: url(:/pic/image/file.png)}"
            "QPushButton:hover{border-image: url(:/pic/image/file_h.png)}")
        self.open.setText("")
        self.open.setObjectName("open")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(20, 70, 31, 31))
        self.save.setStyleSheet("QPushButton{border-image: url(:/pic/image/save.png)}"
            "QPushButton:hover{border-image: url(:/pic/image/save_h.png)}")
        self.save.setText("")
        self.save.setObjectName("save")


        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(60, 5, 932, 740))
        self.tabWidget.setStyleSheet("background-color: rgb(255,255,255);\n""border:none;\n")
        self.tabWidget.setObjectName("tabWidget")
        self.sc = QtWidgets.QWidget()
        self.sc.setStyleSheet("    font-family:\"微软雅黑\";\n"
"    font-size:14px;")
        self.sc.setObjectName("sc")
        self.SourceCode = QtWidgets.QTextEdit(self.sc)
        self.SourceCode.setGeometry(QtCore.QRect(0, 20, 951, 751))
        self.SourceCode.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);\n"
"color: rgb(50, 50, 50);\n"
"font-size:16px;font-family:Consolas;\n"
"border : none;")
        self.SourceCode.setObjectName("SC")
        self.SC_P = QtWidgets.QLabel(self.sc)
        self.SC_P.setGeometry(QtCore.QRect(0, 0, 1011, 21))
        self.SC_P.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(129,129,129);\n"
"font-size:16px;font-family:Consolas;")
        self.SC_P.setIndent(12)
        self.SC_P.setObjectName("SC_P")
        self.sc_bg = QtWidgets.QLabel(self.sc)
        self.sc_bg.setGeometry(QtCore.QRect(-20, 0, 1051, 731))
        self.sc_bg.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.sc_bg.setText("")
        self.sc_bg.setObjectName("sc_bg")
        self.sc_bg.raise_()
        self.SourceCode.raise_()
        self.SC_P.raise_()
        self.tabWidget.addTab(self.sc, "")
        self.ir = QtWidgets.QWidget()
        self.ir.setObjectName("ir")
        self.IR = QtWidgets.QTextBrowser(self.ir)
        self.IR.setGeometry(QtCore.QRect(0, 20, 951, 751))
        self.IR.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(50, 50, 50);\n"
"font-size:16px;font-family:Consolas;\n"
"border : none;")
        self.IR.setObjectName("IR")
        self.label = QtWidgets.QLabel(self.ir)
        self.label.setGeometry(QtCore.QRect(-10, 0, 1031, 731))
        self.label.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.IR_P = QtWidgets.QLabel(self.ir)
        self.IR_P.setGeometry(QtCore.QRect(0, 0, 1021, 21))
        self.IR_P.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(129,129,129);\n"
"font-size:16px;font-family:Consolas;")
        self.IR_P.setIndent(12)
        self.IR_P.setObjectName("IR_P")
        self.label.raise_()
        self.IR.raise_()
        self.IR_P.raise_()
        self.tabWidget.addTab(self.ir, "")
        self.asm_2 = QtWidgets.QWidget()
        self.asm_2.setObjectName("asm_2")
        self.ASM = QtWidgets.QTextBrowser(self.asm_2)
        self.ASM.setGeometry(QtCore.QRect(0, 20, 951, 751))
        self.ASM.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(50, 50, 50);\n"
"border: none;\n"
"font-size:16px;font-family:Consolas;")
        self.ASM.setObjectName("ASM")
        self.asm_bg = QtWidgets.QLabel(self.asm_2)
        self.asm_bg.setGeometry(QtCore.QRect(0, 0, 1011, 711))
        self.asm_bg.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.asm_bg.setText("")
        self.asm_bg.setObjectName("asm_bg")
        self.ASM_P = QtWidgets.QLabel(self.asm_2)
        self.ASM_P.setGeometry(QtCore.QRect(0, 0, 1011, 21))
        self.ASM_P.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(129,129,129);\n"
"font-size:16px;font-family:Consolas;")
        self.ASM_P.setIndent(12)
        self.ASM_P.setObjectName("ASM_P")
        self.asm_bg.raise_()
        self.ASM.raise_()
        self.ASM_P.raise_()
        self.tabWidget.addTab(self.asm_2, "")
        self.ast = QtWidgets.QWidget()
        self.ast.setObjectName("ast")
        self.AST_P = QtWidgets.QLabel(self.ast)
        self.AST_P.setGeometry(QtCore.QRect(0, 0, 1011, 21))
        self.AST_P.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"color: rgb(129,129,129);\n"
"font-size:16px;font-family:Consolas;")
        self.AST_P.setIndent(12)
        self.AST_P.setObjectName("AST_P")
        self.AST = QtWidgets.QLabel(self.ast)
        self.AST.setGeometry(QtCore.QRect(0, 20, 951, 721))
        self.AST.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(50, 50, 50);\n"
"font-size:32px;font-weight:bold;font-family:Consolas;")
        self.AST.setTextFormat(QtCore.Qt.PlainText)
        self.AST.setAlignment(QtCore.Qt.AlignCenter)
        self.AST.setObjectName("AST")
        self.tabWidget.addTab(self.ast, "")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(-10, 0, 1011, 751))
        self.bg.setStyleSheet("background-color: rgb(36, 36, 36);")
        self.bg.setText("")
        self.bg.setObjectName("bg")
        self.compile = QtWidgets.QPushButton(self.centralwidget)
        self.compile.setGeometry(QtCore.QRect(20, 120, 30, 30))
        self.compile.setStyleSheet("QPushButton{border-image: url(:/pic/image/compile.png)}"
            "QPushButton:hover{border-image: url(:/pic/image/compile_h.png)}")
        self.compile.setText("")
        self.compile.setObjectName("compile")
        self.tree = QtWidgets.QPushButton(self.centralwidget)
        self.tree.setGeometry(QtCore.QRect(20, 170, 30, 30))
        self.tree.setStyleSheet("QPushButton{border-image: url(:/pic/image/tree.png)}"
            "QPushButton:hover{border-image: url(:/pic/image/tree_h.png)}")
        self.tree.setText("")
        self.tree.setObjectName("tree")
        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(20, 220, 30, 30))
        self.run.setStyleSheet("QPushButton{border-image: url(:/pic/image/run.png)}"
            "QPushButton:hover{border-image: url(:/pic/image/run_h.png)}")
        self.run.setText("")
        self.run.setObjectName("run")
        self.bg.raise_()
        self.open.raise_()
        self.save.raise_()
        self.tabWidget.raise_()
        self.compile.raise_()
        self.tree.raise_()
        self.run.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.open.clicked.connect(MainWindow.Open)
        self.save.clicked.connect(MainWindow.Save)
        self.compile.clicked.connect(MainWindow.Compile)
        self.tree.clicked.connect(MainWindow.Gen_Tree)
        self.run.clicked.connect(MainWindow.Run)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        '''背景透明度'''
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SC_P.setText(_translate("MainWindow", "filepath"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sc), _translate("MainWindow", "Source Code"))
        self.IR_P.setText(_translate("MainWindow", "filepath"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ir), _translate("MainWindow", "Intermediate Code"))
        self.ASM_P.setText(_translate("MainWindow", "filepath"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.asm_2), _translate("MainWindow", "Assembly Code"))
        self.AST_P.setText(_translate("MainWindow", "filepath"))
        self.AST.setText(_translate("MainWindow", "Please Generate AST"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ast), _translate("MainWindow", "AST"))


import source_rc
