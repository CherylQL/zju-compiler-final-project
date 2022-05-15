import os
from os.path import exists, join
import shutil
from ctypes import CFUNCTYPE, c_double, c_int32
from ctypes import *
import llvmlite.binding as llvm
from Optimization import Optimization

class TargCodeGen:
    def __init__(self, ir_code=""):
        self.ir_code = ir_code

    def getIntCode(self, ir_code=""):
        self.ir_code = ir_code

    def gen_target_code(self):
        # llvm初始化
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.module = llvm.parse_assembly(self.ir_code)

        self.module.verify() # 验证

        self.opt = Optimization(self.module)
        self.opt.config()
        self.module = self.opt.opt_module()

        self.functions = [x for x in self.module.functions]

        path = "./cfgOpt/"
        if exists(path):
            shutil.rmtree(path)
        for func in self.functions:
            dot = llvm.view_dot_graph(llvm.get_function_cfg(func))
            dot.format = 'png'
            filePath = join(path, func.name)
            dot.render(filePath, view = False)

        tgt = llvm.Target.from_default_triple()
        tgt_machine = tgt.create_target_machine()
        asm_code = tgt_machine.emit_assembly(self.module)
        return asm_code

    def run_asm_code(self, args, func, ctype=c_int32):
        tgt = llvm.Target.from_default_triple()
        tgt_machine = tgt.create_target_machine()
        jitcomp = llvm.create_mcjit_compiler(llvm.parse_assembly(""), tgt_machine)
        jitcomp.add_module(self.module)
        jitcomp.finalize_object()
        jitcomp.run_static_constructors()

        ctype_int = [c_int32, c_int, c_int8, c_int16, c_int64]
        # ctype_uint = [c_uint32, c_uint, c_uint8, c_int16, c_uint64]
        ctype_long = [c_long, c_longlong]
        ctype_float = [c_float, c_double]

        if ctype in ctype_int or ctype in ctype_long:
            args = [int(item) for item in args]
        elif ctype in ctype_float:
            args = [float(item) for item in args]

        func_ptr = jitcomp.get_function_address(func)
        func_run = CFUNCTYPE(ctype)(func_ptr)
        return func_run(*args)