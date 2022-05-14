import os

from parse import parser

class MainForm():
    def __init__(self):
        self.AbstractSyntsxTreeRoot = None
        self.IntermediateCode = None
        self.TargetCode = None
        self.SourceCode = None

    def getIntermediateCode(self):
        src_code = self.SourceCode.toPlainText()
        int_code = ""
        # if src_code == "":
        # # Some operation
        # else:
        self.AbstractSyntsxTreeRoot = parser.parse(src_code)
        return int_code

    def Compile(self):
        int_code = self.getIntermediateCode()

        #TODO: 生成目标代码

        #TODO: 写入二进制文件

    def Run(self):
        asm_code = self.Compile()

        #TODO: set program name according to asm file name
        program_name = ''

        #gcc compile
        ret = os.popen("gcc " + program_name + ".s" + " -o " + program_name)
        info = "gcc log:\n" + ret.read() + "\n"

        # run
        ret = os.popen(program_name)
        info += "program result:\n" + ret.read()

if __name__ == "__main__":
    print("main")