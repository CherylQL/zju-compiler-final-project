import json
import llvmlite.binding as llvm

class Optimization:
    def __init__(self, module):
        self.pmm = llvm.create_module_pass_manager()
        self.pmb = llvm.create_pass_manager_builder()
        self.module = module
        self.fpm = llvm.create_function_pass_manager(self.module)

    def opt_module(self):
        self.pmm.run(self.module)
        return self.module

    def config(self):
        with open("optimization_config.json", "r") as f:
            content = f.read()
            opt = json.loads(content)
            # 全局优化选项
            self.pmb.loop_vectorize = opt["loop_vectorize"]
            self.pmb.slp_vectorize = opt["slp_vectorize"]
            self.pmb.inlining_threshold = opt["inlining_threshold"]
            self.pmb.disable_unroll_loops = opt["disable_unroll_loops"]
            self.pmb.opt_level = opt["opt_level"]
            self.pmb.size_level = opt["size_level"]
            self.pmm = llvm.create_module_pass_manager()
            self.pmb.populate(self.pmm)
            self.pmb.populate(self.fpm)

            # 两种pass manager优化选项
            if opt["const_merge"]:
                self.pmm.add_const_merge_pass()
                self.fpm.add_const_merge_pass()
            if opt["dead_arg_elimination"]:
                self.pmm.add_dead_arg_elimination_pass()
                self.fpm.add_dead_arg_elimination_pass()
            if opt["function_attrs"]:
                self.pmm.add_function_attrs_pass()
                self.fpm.add_function_attrs_pass()
            if opt["function_inlining"]:
                self.pmm.add_function_inlining_pass(opt["function_inlining"])
            if opt["global_dce"]:
                self.pmm.add_global_dce_pass()
                self.fpm.add_global_dce_pass()
            if opt["global_optimizer"]:
                self.pmm.add_global_optimizer_pass()
                self.fpm.add_global_optimizer_pass()
            if opt["ipsccp"]:
                self.pmm.add_ipsccp_pass()
                self.fpm.add_ipsccp_pass()
            if opt["dead_code_elimination"]:
                self.pmm.add_dead_code_elimination_pass()
                self.fpm.add_dead_code_elimination_pass()
            if opt["cfg_simplification"]:
                self.pmm.add_cfg_simplification_pass()
                self.fpm.add_cfg_simplification_pass()
            if opt["gvn"]:
                self.pmm.add_gvn_pass()
                self.fpm.add_gvn_pass()
            if opt["instruction_combining"]:
                self.pmm.add_instruction_combining_pass()
                self.fpm.add_instruction_combining_pass()
            if opt["licm"]:
                self.pmm.add_licm_pass()
                self.fpm.add_licm_pass()
            if opt["sccp"]:
                self.pmm.add_sccp_pass()
                self.fpm.add_sccp_pass()
            if opt["sroa"]:
                self.pmm.add_sroa_pass()
                self.fpm.add_sroa_pass()
            if opt["basicaa"]:
                self.pmm.add_basicaa_pass()
                self.fpm.add_basicaa_pass()
            if opt["type_based_alias_analysis"]:
                self.pmm.add_type_based_alias_analysis_pass()



            

        