import os
import shutil
from random import randint

import llvmlite.binding as llvm
from llvmlite import ir

from parse import parser
from CompilerError import *
from TypeDict import TYPE as type_t
from TypeDict import IRTYPE as ir_type_t
from symbolTable import SymbolTable

class IntRepGen:

    def __init__(self, astRoot = ""):
        self.AstRoot = astRoot
        self.CaseList = list()
        self.FuncList = list()
        self.SymbolTable = SymbolTable()

        self.default = None

    def initial(self, astRoot):
        self.AstRoot = astRoot
        self.CaseList = list()
        self.FuncList = list()
        self.SymbolTable = SymbolTable()

        self.default = None

    def Generation(self):
        if (self.AstRoot == None):
            raise TreeContentException(["Abstract syntax tree content is invalid: %s" % (self.AstRoot)])
        self.module = ir.Module(self.AstRoot.children[0].children[1].name)
        self.triggerFuncByName(self.AstRoot)
        ret = self.module.__repr__()
        print(ret)
        self.cfgGraphGenerator()
        return ret

    def triggerFuncByName(self, n):
        func = n.type
        return getattr(self, func)(n)

    def cfgGraphGenerator(self, flush=True, show=False, root_p="./cfgPic/"):
        if os.path.exists(root_p) and flush:
            shutil.rmtree(root_p)
        for func in self.FuncList:
            dot = llvm.get_function_cfg(func)
            dot = llvm.view_dot_graph(dot)
            dot.format = 'png'
            filepath = os.path.join(root_p, func.name)
            dot.render(filepath, view=show)

    def irshow(self):
        self.triggerFuncByName(self.AstRoot)
        return self.module

    def program(self, node):
        self.SymbolTable.initial()
        self.main_type = ir.FunctionType(ir.VoidType(), ())

        self.main_func = ir.Function(self.module, self.main_type, 'main')

        self.block = self.main_func.append_basic_block('main')
        self.FuncList.append(self.main_func)

        self.builder = ir.IRBuilder(self.block)
        self.triggerFuncByName(node.children[1])
        self.builder.ret_void()

    def info(self, node):
        print(f"Debug Info: Node [ type: {node.type}, name: {node.name}, children: {node.children} ]")

    def label_part(self, n):
        pass

    def const_part(self, node):
        if len(node.children) >= 2:
            self.triggerFuncByName(node.children[1])
        else:
            return

    def const_expr_list(self, node):
        arg_array = node.children[-4:]
        st_name = arg_array[0].name
        con_value = self.triggerFuncByName(arg_array[2])
        if len(self.SymbolTable.SymTables) <= 1:
            addr = ir.GlobalVariable(self.module, con_value.type, st_name)
            try:
                if con_value.type.intrinsic_name == 'i32':
                    addr.initializer = ir.Constant(ir.IntType(32), int(con_value.constant))
                elif con_value.type.intrinsic_name == 'i8':
                    addr.initializer = ir.Constant(ir.IntType(8), int(con_value.constant))
                elif con_value.type.intrinsic_name == 'f64':
                    addr.initializer = ir.Constant(ir.DoubleType(), float(con_value.constant))
            except AttributeError:
                addr.initializer = con_value
            addr.global_constant = True
        else:
            addr = self.builder.alloca(con_value.type)
            self.builder.store(con_value, addr)
        self.SymbolTable.insert([st_name, addr])
        if len(node.children) != 5:
            pass
        else:
            self.triggerFuncByName(node.children[0])

    def const_value(self, node):
        n_type = node.children[0].type
        value = node.children[0].name
        if n_type in type_t.keys():
            ir_type = type_t[n_type]
            if ir_type.intrinsic_name == 'i8':
                value = ord(value[1])
            ret = ir.Constant(ir_type, value)
            return ret
        else:
            value = bytes(value.strip('"'), encoding='utf-8').decode('unicode-escape')
            value = value + '\0'
            ret = ir.Constant(ir.ArrayType(ir.IntType(8), len(value)), bytearray(value.encode("utf8")))
            return ret

    def routine(self, n):
        for i in range(len(n.children)):
            self.triggerFuncByName(n.children[i])

    def routine_part(self, n):
        for i in range(len(n.children)):
            self.triggerFuncByName(n.children[i])

    def routine_head(self, n):
        for i in range(len(n.children)):
            self.triggerFuncByName(n.children[i])

    def subroutine(self, n):
        for i in range(len(n.children)):
            self.triggerFuncByName(n.children[i])

    def type_part(self, n):
        l = len(n.children)
        self.triggerFuncByName(n.children[l - 1])

    def type_decl(self, node):
        tp = node.children[0].type
        if tp == "simple_type_decl":
            return self.simple_type_decl(node.children[0])
        elif tp == "record_type_decl":
            return self.record_type_decl(node.children[0])
        elif tp == "array_type_decl":
            return self.array_type_decl(node.children[0])

    def simple_type_decl(self, node):
        tp = node.children[0].type
        if tp == "SYS_TYPE":
            spl_type = node.children[0].name.upper()
            ret = type_t[spl_type]
            return ret

    def array_type_decl(self, node):
        tp = node.children[2].type
        if tp == "simple_type_decl" :
            nm = node.children[2].children[0].children[0].name
            if nm != "1":
                raise InTypeException(["Cannot create array"])
            else:
                spl_type = node.children[5].children[0].children[0].name.upper()
                ret = type_t[spl_type]
                return ["array", ret, node.children[2].children[2].children[0].name]
        elif tp == "array_type_decl_part":
            nm1 = node.children[2].children[0].children[0].children[0].name
            nm2 = node.children[2].children[2].children[0].children[0].name
            if nm1 != "1" or nm2 != "1":
                raise InTypeException(["Cannot create array"])
            else:
                spl_type = node.children[5].children[0].children[0].name.upper()
                ret = type_t[spl_type]
                return ["array-array", ret, node.children[2].children[0].children[2].children[0].name,
                        node.children[2].children[2].children[2].children[0].name]
            return
    def arr_type_part(self, node):
        return

    def type_decl_list(self, n):
        for i in range(len(n.children)):
            self.triggerFuncByName(n.children[i])

    def type_def(self, node):
        n = node.children[0].name
        tp = node.children[2].children[0].type
        if tp == "record_type_decl":
            ty_array = self.type_decl(node.children[2])
            tp_bd = [ir.IntType(32)]
            ct = 1
            for tp in ty_array[1]:
                tp_bd += [tp[1]]
                index = ir.Constant(ir.IntType(32), ct)
                self.SymbolTable.insert([n + "." + tp[0], index])
                ct += 1
            strarr = ir.LiteralStructType(tp_bd)
            addr = self.builder.alloca(strarr)
            self.SymbolTable.insert([n, addr])
        elif tp == "array_type_decl":
            array_list = self.type_decl(node.children[2])
            array_type = ir.ArrayType(array_list[1], int(array_list[2]) + 1)
            addr = self.builder.alloca(array_type)
            self.SymbolTable.insert([n, addr])

    def var_part(self, n):
        l = len(n.children)
        self.triggerFuncByName(n.children[l - 1])

    def var_decl_list(self, n):
        for i in range(len(n.children)):
            self.triggerFuncByName(n.children[i])

    def var_decl(self, node):
        node_array = self.name_list(node.children[0])

        if node.children[2].children[0].type == "simple_type_decl":
            ir_type = self.type_decl(node.children[2])
            for n in node_array:
                if len(self.SymbolTable.SymTables) <= 1:
                    addr = ir.GlobalVariable(self.module, ir_type, n)
                    if ir_type.intrinsic_name == 'i32':
                        addr.initializer = ir.Constant(ir.IntType(32), 0)
                    elif ir_type.intrinsic_name == 'i8':
                        addr.initializer = ir.Constant(ir.IntType(8), 0)
                    elif ir_type.intrinsic_name == 'f64':
                        addr.initializer = ir.Constant(ir.DoubleType(), 0)

                else:
                    addr = self.builder.alloca(ir_type)

                self.SymbolTable.insert([n, addr])

        elif node.children[2].children[0].type == "record_type_decl":
            tp_array = self.type_decl(node.children[2])
            for n in node_array:
                tp_con = [ir.IntType(32)]
                ct = 1
                for tp in tp_array[1]:
                    tp_con += [tp[1]]
                    index = ir.Constant(ir.IntType(32), ct)
                    try:
                        ist = [n + "." + tp[0], index]
                        self.SymbolTable.insert(ist, 0)
                    except MulDefException:
                        pass
                    ct += 1
                strarr = ir.LiteralStructType(tp_con)
                addr = self.builder.alloca(strarr)
                self.SymbolTable.insert([n, addr])

        elif node.children[2].children[0].type == "array_type_decl":
            array_list = self.type_decl(node.children[2])
            if array_list[0] == "array":
                array_type = ir.ArrayType(array_list[1], int(array_list[2]) + 1)
                for n in node_array:
                    if len(self.SymbolTable.SymTables) <= 1:
                        addr = ir.GlobalVariable(self.module, array_type, n)
                        addr.initializer = ir.Constant(array_type, [0 for v in range(int(array_list[2]) + 1)])
                        # addr.initializer = ir.Constant(array_type, [0 for v in range(int(array_list[2]) + 1)])
                    else :
                        addr = self.builder.alloca(array_type)
                    self.SymbolTable.insert([n, addr])
            elif array_list[0] == "array-array":
                array_col_type = ir.ArrayType(array_list[1], int(array_list[3]) + 1)
                array_col_value = int(array_list[3])
                array_type = ir.ArrayType(array_col_type, int(array_list[2]) + 1)
                for n in node_array:
                    if len(self.SymbolTable.SymTables) <= 1:
                        addr = ir.GlobalVariable(self.module, array_type, n)
                        addr.initializer = ir.Constant(array_type, [[0 for v in range(int(array_list[3]) + 1)] for x in range(int(array_list[2]) + 1)])
                    else :
                        addr = self.builder.alloca(array_type)
                    # TODO: new insert function
                    self.SymbolTable.insert([n, addr])

    def name_list(self, node):
        if len(node.children) <= 1:
            name_array = list()
        else:
            name_array = self.name_list(node.children[0])
        n = [node.children[-1].name]
        return name_array + n

    def record_type_decl(self, node):
        return ["record", self.triggerFuncByName(node.children[1])]

    def field_decl_list(self, n):
        ty_array = list()
        for i in range(len(n.children)):
            ty_array += self.triggerFuncByName(n.children[i])
        return ty_array

    def field_decl(self, node):
        tp = self.type_decl(node.children[2])
        ty_array = list()
        name_array = self.name_list(node.children[0])
        for n in name_array:
            ty_array += [[n, tp]]
        return ty_array

    def procedure_decl(self, node):
        name, arg_array = self.procedure_head(node.children[0])
        name_array, irtp_array = list(), list()
        for t in arg_array:
            if t[0][0] != "var":
                for i in range(1, len(t[0])):
                    irtp_array.append(t[1])
                    name_array.append(("val", t[0][i]))
            else:
                for i in range(1, len(t[0])):
                    irtp_array.append(t[1].as_pointer())
                    name_array.append(("var", t[0][i]))
        func_type = ir.FunctionType(ir.VoidType(), irtp_array)
        func = ir.Function(self.module, func_type, name=name)
        self.FuncList.append(func)
        self.SymbolTable.insert([name, func])
        self.SymbolTable.initial()
        stored_builder = self.builder
        b = func.append_basic_block(name=name)
        self.builder = ir.IRBuilder(b)
        f_params = func.args
        for i in range(len(f_params)):
            if name_array[i][0] == "val":
                addr = self.builder.alloca(irtp_array[i])
                self.builder.store(f_params[i], addr)
                self.SymbolTable.insert([name_array[i][1], addr])

            if name_array[i][0] == "var":
                addr = f_params[i]
                self.SymbolTable.insert([name_array[i][1], addr])
        self.subroutine(node.children[2])
        self.builder.ret_void()
        self.builder = stored_builder

        self.SymbolTable.SymTables.pop()

    def procedure_head(self, node):
        arg_array = self.triggerFuncByName(node.children[2])
        n = node.children[1].name
        return n, arg_array

    def val_para_list(self, node):
        return self.triggerFuncByName(node.children[0])

    def var_para_list(self, node):
        return self.triggerFuncByName(node.children[1])

    def routine_body(self, node):
        self.compound_stmt(node.children[0])

    def compound_stmt(self, node):
        self.stmt_list(node.children[1])

    def func_decl(self, node):
        name, arg_array, ret = self.func_head(node.children[0])
        name_array = list()
        irtp_array = list()
        for t in arg_array:
            if t[0][0] == "var":
                for i in range(1, len(t[0])):
                    irtp_array.append(t[1].as_pointer())
                    name_array.append(("var", t[0][i]))
            else:
                for i in range(1, len(t[0])):
                    irtp_array.append(t[1])
                    name_array.append(("val", t[0][i]))
        ret_ir_type = type_t[node.children[0].children[-1].children[0].name.upper()]
        func_type = ir.FunctionType(ret_ir_type, irtp_array)
        func = ir.Function(self.module, func_type, name=name)
        self.FuncList.append(func)
        self.SymbolTable.insert([name, func])
        self.SymbolTable.initial()
        stored_builder = self.builder
        block = func.append_basic_block(name=name)
        self.builder = ir.IRBuilder(block)
        retaddr = self.builder.alloca(ret_ir_type)
        self.SymbolTable.insert([name + "_return", retaddr])
        f_params = func.args
        for i in range(len(f_params)):
            if name_array[i][0] == "val":
                addr = self.builder.alloca(irtp_array[i])
                self.builder.store(f_params[i], addr)
                self.SymbolTable.insert([name_array[i][1], addr])
            if name_array[i][0] == "var":
                addr = f_params[i]
                self.SymbolTable.insert([name_array[i][1], addr])
        self.subroutine(node.children[2])
        retval = self.builder.load(retaddr)
        self.builder.ret(retval)
        self.builder = stored_builder
        self.SymbolTable.SymTables.pop()

    def stmt(self, node):
        self.triggerFuncByName(node.children[-1])

    def unlabelled_stmt(self, node):
        self.triggerFuncByName(node.children[0])

    def stmt_list(self, node):
        if len(node.children) <= 1:
            self.epsilon(node.children[0])
        else:
            self.triggerFuncByName(node.children[0])
            self.triggerFuncByName(node.children[1])

    def parameters(self, node):
        return self.triggerFuncByName(node.children[1])

    def func_head(self, node):
        name = node.children[1].name
        arg_array = self.triggerFuncByName(node.children[2])
        ret = self.triggerFuncByName(node.children[4])
        return name, arg_array, ret

    def expression_list(self, node):
        if len(node.children) == 1:
            return self.triggerFuncByName(node.children[0])
        else:
            pass
    def assign_stmt(self, node):
        tp = node.children[1].type
        if tp == "SYM_ASSIGN":
            name = node.children[0].name
            lhs = self.SymbolTable.find(name)['entry']
            rhs = self.expression(node.children[2])
            if type(lhs) == ir.Function:
                lhs = self.SymbolTable.find(name + '_return')['entry']
                self.builder.store(rhs, lhs)
            else:
                if str(lhs.type)[:-1] != str(rhs.type):
                    raise InTypeException(["Cannot assign %s to %s" % (str(rhs.type), str(lhs.type)[:-1])])
                self.builder.store(rhs, lhs)
        elif tp == "SYM_LBRAC":
            name = node.children[0].name
            lhs = self.SymbolTable.find(name)['entry']
            rhs = self.triggerFuncByName(node.children[5])
            i32 = ir.IntType(32)
            i32_0 = ir.Constant(i32, 0)
            if len(node.children[2].children) > 1:
                row = self.triggerFuncByName(node.children[2].children[0])
                col = self.triggerFuncByName(node.children[2].children[2])
                addr1 = self.builder.gep(lhs, [i32_0, row])
                pointer_to_index = self.builder.gep(addr1, [i32_0, col])
            else:
                index = self.triggerFuncByName(node.children[2])
                pointer_to_index = self.builder.gep(lhs, [i32_0, index])
            if str(pointer_to_index.type)[:-1] != str(rhs.type):
                raise InTypeException(["Cannot assign %s to %s" % (str(rhs.type), str(pointer_to_index.type)[:-1])])
            self.builder.store(rhs, pointer_to_index)
        elif tp == "SYM_DOT":
            name = node.children[0].name
            lhs = self.SymbolTable.find(name)['entry']
            rhs = self.expression(node.children[4])
            index = node.children[2].name
            offset = self.SymbolTable.find(name + "." + index)["entry"]
            i32 = ir.IntType(32)
            i32_0 = ir.Constant(i32, 0)
            pointer_to_index = self.builder.gep(lhs, [i32_0, offset])
            if str(pointer_to_index.type)[:-1] != str(rhs.type):
                raise InTypeException(["Cannot assign %s to %s" % (str(rhs.type), str(pointer_to_index.type)[:-1])])
            self.builder.store(rhs, pointer_to_index)

    def para_decl_list(self, node):
        if len(node.children) <= 1:
            pre_list = list()

        else:
            pre_list = self.para_decl_list(node.children[0])
        arg_array = pre_list + [self.para_type_list(node.children[-1])]
        return arg_array

    def para_type_list(self, node):
        paraname_list = self.triggerFuncByName(node.children[0])
        ir_type = self.triggerFuncByName(node.children[-1])
        tp = node.children[0].type
        if tp == "var_para_list":
            paraname_list.insert(0, "var")
        else:
            paraname_list.insert(0, "val")
        return paraname_list, ir_type

    def proc_stmt(self, node):
        if node.children[0].type == 'READ':
            factor = node.children[2]
            if len(factor.children) > 1:
                tp = factor.children[1].type
                if tp == "SYM_LBRAC":
                    name = factor.children[0].name
                    lhs = self.SymbolTable.find(name)['entry']
                    array_part = factor.children[2]
                    if len(array_part.children) == 3 :
                        tp1 = array_part.children[1].name
                        if tp1 == ',':
                            # i = array_part.children[0].children[0].children[0].children[0].children[0].name
                            # # 寻找全局变量？ 调用ID
                            # j = array_part.children[2].children[0].children[0].children[0].name
                            col_value = 1
                            # 寻找全局变量
                            #TODO: index值获取
                            i = self.expression(array_part.children[0])
                            j = self.expr(array_part.children[2])
                            i32 = ir.IntType(32)
                            i32_0 = ir.Constant(i32, 0)
                            row_addr = self.builder.gep(lhs, [i32_0, i])
                            addr = self.builder.gep(row_addr, [i32_0, j])
                    elif len(array_part.children) == 1:
                        index = self.expression(factor.children[2])
                        i32 = ir.IntType(32)
                        i32_0 = ir.Constant(i32, 0)
                        addr = self.builder.gep(lhs, [i32_0, index])
                else:
                    addr = self.SymbolTable.find(node.children[2].children[0].name)['entry']
            else:
                addr = self.SymbolTable.find(node.children[2].children[0].name)['entry']

            python_sca = ""
            ran = str(randint(0, 0x7FFFFFFF))
            emptyptr = ir.IntType(8).as_pointer()
            scanf = self.module.globals.get('scanf', None)
            if not scanf:
                scanf_ty = ir.FunctionType(ir.IntType(32), [emptyptr], var_arg=True)
                scanf = ir.Function(self.module, scanf_ty, name="scanf")
            if addr.type.pointee.intrinsic_name == 'i32':
                python_sca = python_sca + '%d\0'
            elif addr.type.pointee.intrinsic_name == 'i8':
                python_sca = python_sca + '%c\0'

            elif addr.type.pointee.intrinsic_name == 'f64':
                python_sca = python_sca + '%f\0'

            else:
                python_sca = python_sca + '%s\0'
            fmt_sca = ir.Constant(ir.ArrayType(ir.IntType(8), len(python_sca)), bytearray(python_sca.encode("utf8")))
            sca_var = ir.GlobalVariable(self.module, fmt_sca.type, name='sca' + ran)
            sca_var.linkage = 'internal'
            sca_var.global_constant = True
            sca_var.initializer = fmt_sca
            sca_arg = self.builder.bitcast(sca_var, emptyptr)
            self.builder.call(scanf, [sca_arg, addr])
            self.builder.load(addr)
            return
        if node.children[0].name == 'write':
            args = self.args_list(node.children[2])
            ran = str(randint(0, 0x7FFFFFFF))
            emptyptr = ir.IntType(8).as_pointer()
            printf = self.module.globals.get('printf', None)
            if not printf:
                printf_ty = ir.FunctionType(ir.IntType(32), [emptyptr], var_arg=True)
                printf = ir.Function(self.module, printf_ty, name="printf")
            python_str = ""
            offset = '1'
            if len(node.children) >= 5:
                offset = node.children[4].name
            for i in args:
                if i.type.intrinsic_name == 'i8':
                    python_str = python_str + "%+" +offset+ "c"
                elif i.type.intrinsic_name == 'i32':
                    python_str = python_str + "%+" +offset+ "d"
                elif i.type.intrinsic_name == 'f64':
                    python_str = python_str + "%+" +offset+ "f"
                else:
                    python_str = python_str + "%s"
            python_str = python_str + "\0"
            fmt_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(python_str)), bytearray(python_str.encode("utf8")))
            global_fmt = ir.GlobalVariable(self.module, fmt_str.type, name='fmt' + ran)
            global_fmt.linkage = 'internal'
            global_fmt.global_constant = True
            global_fmt.initializer = fmt_str
            fmt_arg = self.builder.bitcast(global_fmt, emptyptr)
            self.builder.call(printf, [fmt_arg] + args)
        elif node.children[0].name == 'writeln':
            ran = str(randint(0, 0x7FFFFFFF))
            emptyptr = ir.IntType(8).as_pointer()
            printf = self.module.globals.get('printf', None)
            if not printf:
                printf_ty = ir.FunctionType(ir.IntType(32), [emptyptr], var_arg=True)
                printf = ir.Function(self.module, printf_ty, name="printf")
            if len(node.children) > 2:
                args = self.args_list(node.children[2])
                python_str = ""
                for i in args:
                    if i.type.intrinsic_name == 'i32':
                        python_str = python_str + "%d "
                    elif i.type.intrinsic_name == 'f64':
                        python_str = python_str + "%f "
                    else:
                        python_str = python_str + "%s "
                python_str = python_str + "\n\0"
            else:
                args = []
                python_str = "\n\0"
            fmt_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(python_str)), bytearray(python_str.encode("utf8")))
            global_fmt = ir.GlobalVariable(self.module, fmt_str.type, name='fmt' + ran)
            global_fmt.linkage = 'internal'
            global_fmt.global_constant = True
            global_fmt.initializer = fmt_str
            fmt_arg = self.builder.bitcast(global_fmt, emptyptr)
            self.builder.call(printf, [fmt_arg] + args)
        else:
            args = self.args_list(node.children[2])
            func = self.SymbolTable.find(node.children[0].name)["entry"]
            args_type = func.args
            for i in range(len(args_type)):
                if args_type[i].type.is_pointer:
                    args[i] = self.find_addr(node.children[2], len(args) - i - 1)
            return self.builder.call(func, args)

    def find_addr(self, node, n):
        cur = node
        for i in range(n):
            cur = cur.children[0]
        return self.SymbolTable.find(cur.children[-1].children[-1].children[-1].children[-1].children[-1].name)[
            'entry']

    def if_stmt(self, node):
        pred = self.triggerFuncByName(node.children[1])
        with self.builder.if_else(pred) as (then, otherwise):
            with then:
                self.triggerFuncByName(node.children[3])
            with otherwise:
                self.triggerFuncByName(node.children[4])

    def else_clause(self, node):
        if len(node.children) > 1:
            self.triggerFuncByName(node.children[-1])
        else:
            return

    def for_stmt(self, node):
        ran = str(randint(0, 0x7FFFFFFF))
        self.SymbolTable.initial()
        addr = self.builder.alloca(ir.IntType(32))
        init_value = self.expression(node.children[3])
        self.SymbolTable.insert([node.children[1].name, addr])
        final_value = self.expression(node.children[5])
        self.builder.store(init_value, addr)
        forblock = self.builder.append_basic_block("for_" + ran)
        self.builder.branch(forblock)
        f_builder = ir.IRBuilder(forblock)
        stmt_block = f_builder.append_basic_block("stmt_" + ran)
        jumpout = f_builder.append_basic_block("jumpout_" + ran)
        init_value = f_builder.load(addr)
        direct = node.children[4].children[0].type
        if direct == "TO":
            cmp = ">"
        else:
            cmp = "<"
        cond = f_builder.icmp_signed(cmp, init_value, final_value)
        f_builder.cbranch(cond, jumpout, stmt_block)
        stmt_builder = ir.IRBuilder(stmt_block)
        stored_builder = self.builder
        self.builder = stmt_builder
        self.triggerFuncByName(node.children[-1])
        self.builder = stored_builder
        one = ir.IntType(32)(1)
        if direct == "TO":
            inc_dec = stmt_builder.add(init_value, one)
        elif direct == "DOWNTO":
            inc_dec = stmt_builder.sub(init_value, one)
        else:
            raise DefMissingException([direct])
        stmt_builder.store(inc_dec, addr)
        stmt_builder.branch(forblock)
        self.builder.position_at_end(jumpout)
        self.SymbolTable.SymTables.pop()

    def repeat_stmt(self, n):
        pass

    def case_stmt(self, node):
        ran = str(randint(0, 0x7FFFFFFF))
        expr = self.triggerFuncByName(node.children[1])
        othercase = self.triggerFuncByName(node.children[3])
        default = self.builder.append_basic_block('default_' + ran)
        self.default = default
        case_part = self.builder.switch(expr, default)
        for val, block in othercase:
            case_part.add_case(val, block)
            builder = ir.IRBuilder(block)
            builder.position_at_end(block)
            builder.branch(self.default)
        self.builder.position_at_end(default)

    def case_expr_list(self, node):
        if len(node.children) > 1:
            return self.triggerFuncByName(node.children[0]) + [self.triggerFuncByName(node.children[1])]
        else:
            return [self.triggerFuncByName(node.children[0])]

    def case_expr(self, node):
        ran = str(randint(0, 0x7FFFFFFF))
        val = self.triggerFuncByName(node.children[0])
        block = self.builder.append_basic_block('case_' + ran)
        stored_builder = self.builder
        self.builder = ir.IRBuilder(block)
        self.triggerFuncByName(node.children[2])
        self.builder = stored_builder
        return val, block

    def while_stmt(self, node):
        ran = str(randint(0, 0x7FFFFFFF))
        whileblock = self.builder.append_basic_block("while_" + ran)
        stmt = self.builder.append_basic_block("stmt_" + ran)
        jumpout = self.builder.append_basic_block("jumpout")
        self.builder.branch(whileblock)
        w_builder = ir.IRBuilder(whileblock)
        stored = self.builder
        self.builder = w_builder
        cond = self.triggerFuncByName(node.children[1])
        self.builder.cbranch(cond, stmt, jumpout)
        s_builder = ir.IRBuilder(stmt)
        self.builder = s_builder
        self.triggerFuncByName(node.children[3])
        self.builder.branch(whileblock)
        self.builder = stored
        self.builder.position_at_end(jumpout)

    def expression(self, node):
        if len(node.children) > 1:
            lhs = self.expression(node.children[0])
            rhs = self.expr(node.children[-1])
            op = node.children[1].name
            if op == "<>":
                op = "!="
            elif op == "=":
                op = "=="
            else:
                pass
            if lhs.type == rhs.type:
                if lhs.type == ir.IntType(32):
                    return self.builder.icmp_signed(op, lhs, rhs)
                elif lhs.type == ir.DoubleType():
                    return self.builder.fcmp_ordered(op, lhs, rhs)
                else:
                    raise InTypeException(["None type %s" % (lhs.type)])
            else:
                raise InTypeException(["types not equal %s â‰  %s" % (lhs.type, rhs.type)])
        elif len(node.children) == 1:
            return self.expr(node.children[-1])
        else:
            raise AnalysisException(["Expression error Num %d" % (len(node.children))])

    def expr(self, node):
        if len(node.children) > 1:
            lhs = self.triggerFuncByName(node.children[0])
            rhs = self.triggerFuncByName(node.children[2])
            op = node.children[1].name
            if lhs.type != rhs.type:
                raise InTypeException(["types not equal %s â‰  %s" % (lhs.type, rhs.type)])
            if lhs.type == ir_type_t["UNSIGNEDINTEGER"]:
                if op == "+":
                    try:
                        if (lhs.constant) and (rhs.constant):
                            return ir.Constant(ir.IntType(32), int(lhs.constant) + int(rhs.constant))
                    except:
                        return self.builder.add(lhs, rhs)
                elif op == "-":
                    return self.builder.sub(lhs, rhs)
                elif op == "or":
                    return self.builder.or_(lhs, rhs)
                elif op == "and":
                    return self.builder.and_(lhs, rhs)
                elif op == "*":
                    return self.builder.mul(lhs, rhs)
                elif op == "div" or op == '/':
                    return self.builder.sdiv(lhs, rhs)
                elif op == "mod":
                    return self.builder.urem(lhs, rhs)
                else:
                    raise InTypeException(["%s on two different types, %s and %s" % (op, lhs.type, rhs.type)])
            if lhs.type == ir_type_t["UNSIGNEDREAL"]:
                if op == "+":
                    return self.builder.fadd(lhs, rhs)
                elif op == "-":
                    return self.builder.fsub(lhs, rhs)
                elif op == "*":
                    return self.builder.fmul(lhs, rhs)
                elif op == "/" or op == 'div':
                    return self.builder.fdiv(lhs, rhs)
                elif op == "mod":
                    return self.builder.frem(lhs, rhs)
                else:
                    raise InTypeException(["%s on two different types, %s and %s" % (op, lhs.type, rhs.type)])
            elif lhs.type == ir_type_t["BOOLEAN"]:
                if op == "or":
                    return self.builder.or_(lhs, rhs)
                elif op == "and":
                    return self.builder.and_(lhs, rhs)
                else:
                    raise OperationException(["Error Operation %s" % (op)])
            else:
                raise InTypeException(["None type %s" % (lhs.type)])
        else:
            return self.triggerFuncByName(node.children[0])

    def term(self, node):
        if len(node.children) > 1:
            lhs = self.triggerFuncByName(node.children[0])
            rhs = self.triggerFuncByName(node.children[2])
            op = node.children[1].name
            if lhs.type != rhs.type:
                raise InTypeException(["%s on two different types, %s and %s" % (op, lhs.type, rhs.type)])
            if lhs.type == ir_type_t["UNSIGNEDINTEGER"]:
                if op == "*":
                    return self.builder.mul(lhs, rhs)
                elif op == "div" or op == '/':
                    return self.builder.sdiv(lhs, rhs)
                elif op == "mod":
                    return self.builder.urem(lhs, rhs)
                else:
                    raise OperationException(["Undefined op %s" % op])
            elif lhs.type == "double":
                if op == "*":
                    return self.builder.fmul(lhs, rhs)
                elif op == "div" or op == '/':
                    return self.builder.fdiv(lhs, rhs)
                elif op == "mod":
                    return self.builder.frem(lhs, rhs)
                else:
                    raise OperationException(["Undefined op %s" % op])
            else:
                raise OperationException(["Error Operation %s" % (op)])
        else:
            return self.triggerFuncByName(node.children[0])

    def factor(self, node):
        if len(node.children) == 1:
            return self.triggerFuncByName(node.children[0])
        elif len(node.children) == 3:
            if node.children[1].type == "SYM_DOT":
                name = node.children[0].name
                lhs = self.SymbolTable.find(name)['entry']
                index = node.children[2].name
                offset = self.SymbolTable.find(name + "." + index)["entry"]
                i32 = ir.IntType(32)
                i32_0 = ir.Constant(i32, 0)
                pointer_to_index = self.builder.gep(lhs, [i32_0, offset])  # gets address of array[0]
                return self.builder.load(pointer_to_index)
            else:
                return self.triggerFuncByName(node.children[1])
        elif len(node.children) == 4:
            if node.children[1].type == "SYM_LPAREN":
                args = self.args_list(node.children[2])
                func = self.SymbolTable.find(node.children[0].name)["entry"]
                args_type = func.args
                for i in range(len(args_type)):
                    if args_type[i].type.is_pointer:
                        args[i] = self.find_addr(node.children[2], len(args) - i - 1)
                ret = self.builder.call(func, args)
                return ret
            elif node.children[1].type == "SYM_LBRAC":
                expression = node.children[2]
                if len(expression.children) == 3 and expression.children[1].name == ',':
                    lhs = self.expression(expression.children[0])
                    rhs = self.expr(expression.children[-1])
                    i32 = ir.IntType(32)
                    i32_0 = ir.Constant(i32, 0)
                    head = self.SymbolTable.find(node.children[0].name)["entry"]
                    row_addr = self.builder.gep(head, [i32_0, lhs])
                    addr = self.builder.gep(row_addr, [i32_0, rhs])
                    return self.builder.load(addr)
                name = node.children[0].name
                lhs = self.SymbolTable.find(name)['entry']
                index = self.expression(node.children[2])
                i32 = ir.IntType(32)
                i32_0 = ir.Constant(i32, 0)
                pointer_to_index = self.builder.gep(lhs, [i32_0, index])  # gets address of array[0]
                return self.builder.load(pointer_to_index)

    def args_list(self, node):
        if len(node.children) > 1:
            pre_list = self.args_list(node.children[0])
        else:
            pre_list = list()
        current = [self.triggerFuncByName(node.children[-1])]
        return pre_list + current

    def ID(self, node):
        name = node.name
        addr = self.SymbolTable.find(name)['entry']
        if type(addr) != ir.Function:
            var = self.builder.load(addr)
            return var
        else:
            addr = self.SymbolTable.find(name + '_return')['entry']
            var = self.builder.load(addr)
            return var

    def epsilon(self, n):
        # epsilon do noting
        pass
        return

if __name__ == "__main__":
    f = open('Test/matrix.pas', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    astroot = parser.parse(data)
    ir_code_gen = IntRepGen()
    ir_code_gen.initial(astroot)
    ir_code_gen.Generation()