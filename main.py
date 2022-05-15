import os

from parse import parser
from intermediateRepresentationGenerator import IntRepGen
import sys
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox
from PyQt5.QtCore import Qt

from interface import Ui_MainWindow
from GenTargCode import TargCodeGen
from visualize import Viz

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)
        self.SC_P.setText(str(sys.path[0]))
        self.ASM_P.setText(str(sys.path[0]))
        self.IR_P.setText(str(sys.path[0]))

        # self.SourceCode = None
        # self.SourceCode.setText("")
        self.AbstractSyntsxTreeRoot = None
        self.IntermediateRepresentation = IntRepGen()
        self.TargetCode = TargCodeGen()

        self.ASMCode = None

        self.astroot = None

    def getIntermediateRepresentation(self):
        src_code = self.SourceCode
        int_code = ""
        if src_code == "":
            self.Open()
            src_code = self.SourceCode.toPlainText()
        else:
            self.AbstractSyntsxTreeRoot = parser.parse(src_code)
            self.IntermediateRepresentation.initial(self.AbstractSyntsxTreeRoot)
            int_code = self.IntermediateRepresentation.Generation()
            self.IR.setText(int_code)
        return int_code


    def Gen_Tree(self):
        source_code = self.SourceCode.toPlainText()
        if source_code == '':
            source_code = self.Open()
        if self.IR.toPlainText() == '':
            self.astroot = parser.parse(source_code)
        Viz(self.astroot).png()
        filepath = sys.path[0] + '\\ParsingTree.png'
        self.AST_P.setText(filepath)

        img = QImage()
        img.load(filepath)
        img.scaled(self.AST.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.AST.setScaledContents(True)
        self.AST.setPixmap(QPixmap.fromImage(img))

    def Compile(self):
        int_code = self.getIntermediateRepresentation()
        print(int_code)
        #TODO: 生成目标代码
        func_name = []
        for func in self.IntermediateRepresentation.FuncList:
            func_name.append(func.name)

        self.TargetCode.getIntCode(int_code)
        asm_code = self.TargetCode.gen_target_code()

        #TODO: 写入二进制文件
        self.ASMCode = asm_code
        self.ASM.setText(asm_code)

        filepath = self.SC_P.text().split('.')[0]
        filepath = filepath + '.s'
        print(filepath)
        self.ASM_P.setText(filepath)

        # with open(filepath, 'w') as fout:
        #     fout.write(asm_code)
        return asm_code

    def Run(self):
        self.SC_P.setText(self.SC_P.text() + '\Test\TestCase3.pas')
        print(self.SC_P.text())
        asm_code = self.Compile()

        #TODO: set program name according to asm file name
        program_name = self.SC_P.text().split('.')[0]

        #gcc compile
        ret = os.popen("gcc " + program_name + ".s" + " -o " + program_name)
        info = "gcc log:\n" + ret.read() + "\n"

        # run
        ret = os.popen(program_name)
        info += "program result:\n" + ret.read()

        # show result?
        QMessageBox.information(self, 'run result', info, buttons=QMessageBox.Ok)

    def Open(self):
        content = ""
        sc_name, filetype = QFileDialog.getOpenFileName(caption="选取文件", directory=os.getcwd(),
                                                        filter="All Files (*);;Pascal Code(.pas);;Pascal Code(.spl)")
        if sc_name.split(".")[-1] != 'pas' and sc_name.split(".")[-1] != 'spl':
            QMessageBox.critical(self, 'File Type Not Right', 'The type of file selected is not supported!',
                                 buttons=QMessageBox.Cancel)
        else:
            with open(sc_name, 'r') as fin:
                content = fin.read()
            self.SourceCode.setText(content)
            self.SC_P.setText(sc_name)
            self.IR_P.setText(sc_name)
            self.AST_P.setText(sc_name)
        return content

    def Save(self):
        path = self.SC_P.text()
        content = self.SourceCode.toPlainText()
        with open(path, 'w') as fin:
            fin.write(content)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainForm = MainForm()

    f = open('./Test/TestCase3.pas', 'r', encoding='utf-8')
    mainForm.SourceCode = f.read()
    f.close()
    mainForm.Run()

    # mainForm.show()
    # sys.exit(app.exec_())
