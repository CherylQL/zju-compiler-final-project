import os

from parse import parser
from intermediateCodeGenerator import IntCodeGen

class MainForm():
    def __init__(self):
        self.AbstractSyntsxTreeRoot = None
        self.IntermediateCode = IntCodeGen()
        self.TargetCode = None
        self.SourceCode = None

    def getIntermediateCode(self):
        src_code = self.SourceCode
        int_code = ""
        # if src_code == "":
        # # Some operation
        # else:
        self.AbstractSyntsxTreeRoot = parser.parse(src_code)
        self.IntermediateCode.initial(self.AbstractSyntsxTreeRoot)
        int_code = self.IntermediateCode.Generation()
        return int_code

    def Compile(self):
        int_code = self.getIntermediateCode()
        print(int_code)
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
    mainForm = MainForm()
    f = open('./Test/TestCase3.pas', 'r', encoding='utf-8')
    mainForm.SourceCode = f.read()
    f.close()
    mainForm.Compile()