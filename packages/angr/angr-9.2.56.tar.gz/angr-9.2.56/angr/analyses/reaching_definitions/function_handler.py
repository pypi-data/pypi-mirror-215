from typing import TYPE_CHECKING, List, Set, Optional, Union
from dataclasses import dataclass, field
import logging

from cle import Symbol
from cle.backends import ELF

from angr.storage.memory_mixins.paged_memory.pages.multi_values import MultiValues
from angr.sim_type import SimTypeBottom
from angr.knowledge_plugins.key_definitions.atoms import Atom, Register, MemoryLocation, SpOffset
from angr.calling_conventions import SimCC
from angr.sim_type import SimTypeFunction
from angr.knowledge_plugins.key_definitions.definition import Definition
from angr.knowledge_plugins.functions import Function
from angr.analyses.reaching_definitions.dep_graph import FunctionCallRelationships
from angr.code_location import CodeLocation

if TYPE_CHECKING:
    from angr.analyses.reaching_definitions.rd_state import ReachingDefinitionsState
    from angr.analyses.reaching_definitions.reaching_definitions import ReachingDefinitionsAnalysis

l = logging.getLogger(__name__)


@dataclass
class FunctionEffect:
    """
    A single effect that a function summary may apply to the state. This is largely an implementation detail; use
    `FunctionCallData.depends` instead.
    """

    dest: Optional[Atom]
    sources: Set[Atom]
    value: Optional[MultiValues] = None
    sources_defns: Optional[Set[Definition]] = None
    apply_at_callsite: bool = False


@dataclass
class FunctionCallData:
    """
    A bundle of intermediate data used when computing the sum effect of a function during ReachingDefinitionsAnalysis.

    RDA engine contract:

    - Construct one of these before calling `FunctionHandler.handle_function`. Fill it with as many fields as you can
      realistically provide without duplicating effort.
    - Provide `callsite_codeloc` as either the call statement (AIL) or the default exit of the default statement of the
      calling block (VEX)
    - Provide `function_codeloc` as the callee address with `stmt_idx=0``.

    Function handler contract:

    - If redefine_locals is unset, do not adjust any artifacts of the function call abstration, such as the stack
      pointer, the caller saved registers, etc.
    - If caller_will_handle_single_ret is set, and there is a single entry in `ret_atoms`, do not apply to the state
      effects modifying this atom. Instead, set `ret_values` and `ret_values_deps` to the values and deps which are
      used constructing these values.
    """

    callsite_codeloc: CodeLocation
    function_codeloc: CodeLocation
    address_multi: Optional[MultiValues]
    address: Optional[int] = None
    symbol: Optional[Symbol] = None
    function: Optional[Function] = None
    name: Optional[str] = None
    cc: Optional[SimCC] = None
    prototype: Optional[SimTypeFunction] = None
    args_atoms: Optional[List[Set[Atom]]] = None
    args_values: Optional[List[MultiValues]] = None
    ret_atoms: Optional[Set[Atom]] = None
    redefine_locals: bool = True
    visited_blocks: Optional[Set[int]] = None
    effects: List[FunctionEffect] = field(default_factory=lambda: [])
    ret_values: Optional[MultiValues] = None
    ret_values_deps: Optional[Set[Definition]] = None
    caller_will_handle_single_ret: bool = False
    guessed_cc: bool = False
    guessed_prototype: bool = False
    retaddr_popped: bool = False

    def has_clobbered(self, dest: Atom) -> bool:
        """
        Determines whether the given atom already has effects applied
        """
        if isinstance(dest, Register):
            for effect in self.effects:
                if not isinstance(effect.dest, Register):
                    continue
                reg = effect.dest
                if dest.reg_offset + dest.size <= reg.reg_offset or dest.reg_offset >= reg.reg_offset + reg.size:
                    # no overlap
                    continue
                return True
            return False
        if isinstance(dest, MemoryLocation) and isinstance(dest.addr, SpOffset):
            for effect in self.effects:
                if not isinstance(effect.dest, MemoryLocation) or not isinstance(effect.dest.addr, SpOffset):
                    continue
                stkarg = effect.dest
                if (
                    dest.addr.offset + dest.size <= stkarg.addr.offset
                    or stkarg.addr.offset + stkarg.size <= dest.addr.offset
                ):
                    # no overlap
                    continue
                return True
            return False
        # unsupported
        return False

    def depends(
        self,
        dest: Optional[Atom],
        *sources: Atom,
        value: Optional[MultiValues] = None,
        apply_at_callsite: bool = False,
    ):
        """
        Mark a single effect of the current function, including the atom being modified, the input atoms on which that
        output atom depends, the precise (or imprecise!) value to store, and whether the effect should be applied
        during the function or afterwards, at the callsite.

        The atom being modified may be None to mark uses of the source atoms which do not have any explicit sinks.
        """
        if dest is not None and self.has_clobbered(dest):
            l.warning(
                "Function handler for %s seems to be implemented incorrectly - "
                "you're supposed to call depends() exactly once per dependant atom",
                self.address,
            )
        else:
            self.effects.append(FunctionEffect(dest, set(sources), value=value, apply_at_callsite=apply_at_callsite))


# pylint: disable=unused-argument, no-self-use
class FunctionHandler:
    """
    A mechanism for summarizing a function call's effect on a program for ReachingDefinitionsAnalysis.
    """

    def hook(self, analysis: "ReachingDefinitionsAnalysis") -> "FunctionHandler":
        """
        Attach this instance of the function handler to an instance of RDA.
        """
        return self

    def make_function_codeloc(
        self, target: Union[None, int, MultiValues], callsite: CodeLocation, callsite_func_addr: Optional[int]
    ):
        """
        The RDA engine will call this function to transform a callsite CodeLocation into a callee CodeLocation.
        """
        if isinstance(target, MultiValues):
            target_bv = target.one_value()
            if target_bv is not None and target_bv.op == "BVV":
                target_int = target_bv.args[0]
            else:
                target_int = None
        else:
            target_int = target
        if callsite.context is None:
            return CodeLocation(target_int, stmt_idx=None, context=None)
        elif type(callsite.context) is tuple and callsite_func_addr is not None:
            return CodeLocation(target_int, stmt_idx=None, context=(callsite.block_addr,) + callsite.context)
        else:
            raise TypeError(
                "Please implement FunctionHandler.make_function_codeloc for your special context sensitivity"
            )

    def handle_function(self, state: "ReachingDefinitionsState", data: FunctionCallData):
        """
        The main entry point for the function handler. Called with a RDA state and a FunctionCallData, it is expected
        to update the state and the data as per the contracts described on FunctionCallData.

        You can override this method to take full control over how data is processed, or override any of the following
        to use the higher-level interface (data.depends()):

        - `handle_impl_<function name>` - used for `<function name>`.
        - `handle_local_function` - used for any function (excluding plt stubs) whose address is inside the main binary.
        - `handle_external_function` - used for any function or plt stub whose address is outside the main binary.
        - `handle_indirect_function` - used for any function whose target cannot be resolved.
        - `handle_generic_function` - used as a default if none of the above are overridden.

        Each of them take the same signature as `handle_function`.
        """
        # META
        assert state.analysis is not None
        assert state.analysis.project.loader.main_object is not None
        if data.address is None and data.address_multi is not None:
            for vs in data.address_multi.values():
                for val in vs:
                    if val is not None and val.op == "BVV":
                        data.address = val.args[0]
                        break
                if data.address is not None:
                    break
        if data.symbol is None and data.address is not None:
            data.symbol = state.analysis.project.loader.find_symbol(data.address)
        if data.function is None and data.address is not None:
            data.function = state.analysis.project.kb.functions.get(data.address, None)
        if data.name is None and data.function is not None:
            data.name = data.function.name
        if data.name is None and data.symbol is not None:
            data.name = data.symbol.name
        if data.cc is None and data.function is not None:
            data.cc = data.function.calling_convention
        if data.prototype is None and data.function is not None:
            data.prototype = data.function.prototype
        if data.address is not None and (data.cc is None or data.prototype is None):
            hook = (
                None
                if not state.analysis.project.is_hooked(data.address)
                else state.analysis.project.hooked_by(data.address)
            )
            if (
                hook is None
                and isinstance(state.analysis.project.loader.main_object, ELF)
                and data.address in state.analysis.project.loader.main_object.reverse_plt
            ):
                plt_name = state.analysis.project.loader.main_object.reverse_plt[data.address]
                if state.analysis.project.loader.find_symbol(plt_name) is not None:
                    hook = state.analysis.project.symbol_hooked_by(plt_name)
            if data.cc is None and hook is not None:
                data.cc = hook.cc
            if data.prototype is None and hook is not None:
                data.prototype = hook.prototype.with_arch(state.arch)
                data.guessed_prototype = hook.guessed_prototype

        # fallback to the default calling convention and prototype
        if data.cc is None:
            data.cc = state.analysis.project.factory.cc()
            data.guessed_cc = True
        if data.prototype is None:
            data.prototype = state.analysis.project.factory.function_prototype()
            data.guessed_prototype = True

        args_atoms_from_values = set()
        if data.args_atoms is None and data.args_values is not None:
            data.args_atoms = [
                set().union(
                    *({defn.atom for defn in state.extract_defs(value)} for values in mv.values() for value in values)
                )
                for mv in data.args_values
            ]
            for atoms_set in data.args_atoms:
                args_atoms_from_values |= atoms_set
        elif data.args_atoms is None and data.cc is not None and data.prototype is not None:
            data.args_atoms = self.c_args_as_atoms(state, data.cc, data.prototype)
        if data.ret_atoms is None and data.cc is not None and data.prototype is not None:
            if data.prototype.returnty is not None:
                data.ret_atoms = self.c_return_as_atoms(state, data.cc, data.prototype)

        # PROCESS
        state.move_codelocs(data.function_codeloc)
        if data.name is not None and hasattr(self, f"handle_impl_{data.name}"):
            handler = getattr(self, f"handle_impl_{data.name}")
        elif data.address is not None:
            if (data.symbol is None and state.analysis.project.loader.main_object.contains_addr(data.address)) or (
                data.symbol is not None and data.symbol.owner is state.analysis.project.loader.main_object
            ):
                handler = self.handle_local_function
            else:
                handler = self.handle_external_function

        else:
            handler = self.handle_indirect_function

        handler(state, data)

        # a call expression does not overwrite or redefine any local registers
        if data.redefine_locals:
            if data.cc is not None:
                for reg in self.caller_saved_regs_as_atoms(state, data.cc):
                    if not data.has_clobbered(reg):
                        data.depends(reg)
            if state.arch.call_pushes_ret and not data.retaddr_popped:
                sp_atom = self.stack_pointer_as_atom(state)
                if not data.has_clobbered(sp_atom):  # let the user override the stack pointer if they want
                    new_sp = None
                    sp_val = state.live_definitions.get_value_from_atom(sp_atom)
                    if sp_val is not None:
                        one_sp_val = sp_val.one_value()
                        if one_sp_val is not None:
                            # call_sp_fix is the sp movement after the call instruction executes, which means it is
                            # usually a negative number if the stack grows towards a lower address. when we return,
                            # we should subtract this negative number from the current stack pointer to keep the stack
                            # balanced.
                            new_sp = MultiValues(one_sp_val - state.arch.call_sp_fix)
                    data.depends(sp_atom, value=new_sp)

        # OUTPUT
        args_defns = [
            set().union(*(state.get_definitions(atom) for atom in atoms)) for atoms in (data.args_atoms or set())
        ]
        all_args_defns = set().union(*args_defns)
        other_input_defns = set()
        ret_defns = set()
        other_output_defns = set()

        # translate all the dep atoms into dep defns
        for effect in data.effects:
            if effect.sources_defns is None and effect.sources:
                effect.sources_defns = set().union(*(set(state.get_definitions(atom)) for atom in effect.sources))
                other_input_defns |= effect.sources_defns - all_args_defns
        # apply the effects, with the ones marked with apply_at_callsite=False applied first
        for effect in sorted(data.effects, key=lambda effect: effect.apply_at_callsite):
            codeloc = data.callsite_codeloc if effect.apply_at_callsite else data.function_codeloc
            state.move_codelocs(codeloc)  # no-op if duplicated
            # mark uses
            for source in effect.sources_defns or set():
                if source.atom not in args_atoms_from_values:
                    state.add_use_by_def(source, expr=None)
            if effect.dest is None:
                continue

            value = effect.value if effect.value is not None else MultiValues(state.top(effect.dest.bits))
            # special case: if there is exactly one ret atom, we expect that the caller will do something
            # with the value, e.g. if this is a call expression.
            if data.caller_will_handle_single_ret and data.ret_atoms == {effect.dest}:
                data.ret_values = value
                data.ret_values_deps = effect.sources_defns
            else:
                # mark definition
                mv, defs = state.kill_and_add_definition(
                    effect.dest,
                    value,
                    endness=state.arch.memory_endness,
                    uses=effect.sources_defns or set(),
                )
                # categorize the output defn as either ret or other based on the atoms
                for defn in defs:
                    if data.ret_atoms is not None and defn.atom not in data.ret_atoms:
                        other_output_defns.add(defn)
                    else:
                        ret_defns.add(defn)

        # record this callsite
        state.analysis.function_calls[data.callsite_codeloc] = FunctionCallRelationships(
            callsite=data.callsite_codeloc,
            target=data.address,
            args_defns=args_defns,
            other_input_defns=other_input_defns,
            ret_defns=ret_defns,
            other_output_defns=other_output_defns,
        )
        # move the current codeloc back to the callsite
        state.move_codelocs(data.callsite_codeloc)

    def handle_generic_function(self, state: "ReachingDefinitionsState", data: FunctionCallData):
        assert data.cc is not None
        assert data.prototype is not None
        if data.prototype.returnty is not None:
            data.ret_values = MultiValues(state.top(data.prototype.returnty.with_arch(state.arch).size))
        if data.guessed_prototype:
            # use all!
            # TODO should we use some number of stack variables as well?
            if data.ret_atoms is not None:
                for ret_atom in data.ret_atoms:
                    data.depends(
                        ret_atom,
                        *(Register(*state.arch.registers[reg_name], arch=state.arch) for reg_name in data.cc.ARG_REGS),
                        apply_at_callsite=True,
                    )
        else:
            sources = {atom for arg in data.args_atoms or [] for atom in arg}
            if not data.ret_atoms:
                data.depends(None, *sources, apply_at_callsite=True)  # controversial
                return
            for atom in data.ret_atoms:
                data.depends(atom, *sources, apply_at_callsite=True)

    handle_indirect_function = handle_generic_function
    handle_local_function = handle_generic_function
    handle_external_function = handle_generic_function

    @staticmethod
    def c_args_as_atoms(state: "ReachingDefinitionsState", cc: SimCC, prototype: SimTypeFunction) -> List[Set[Atom]]:
        if not prototype.variadic:
            sp_value = state.get_one_value(Register(state.arch.sp_offset, state.arch.bytes))
            sp = state.get_stack_offset(sp_value) if sp_value is not None else None
            atoms = []
            for arg in cc.arg_locs(prototype):
                atoms_set = set()
                for footprint_arg in arg.get_footprint():
                    try:
                        atom = Atom.from_argument(
                            footprint_arg,
                            state.arch,
                            full_reg=True,
                            sp=sp,
                        )
                    except ValueError:
                        continue
                    atoms_set.add(atom)
                atoms.append(atoms_set)
            return atoms
        return [{Register(*state.arch.registers[arg_name], arch=state.arch)} for arg_name in cc.ARG_REGS]

    @staticmethod
    def c_return_as_atoms(state: "ReachingDefinitionsState", cc: SimCC, prototype: SimTypeFunction) -> Set[Atom]:
        if prototype.returnty is not None and not isinstance(prototype.returnty, SimTypeBottom):
            retval = cc.return_val(prototype.returnty)
            if retval is not None:
                return {
                    Atom.from_argument(footprint_arg, state.arch, full_reg=True)
                    for footprint_arg in retval.get_footprint()
                }
        return set()

    @staticmethod
    def caller_saved_regs_as_atoms(state: "ReachingDefinitionsState", cc: SimCC) -> Set[Register]:
        return (
            {Register(*state.arch.registers[reg], arch=state.arch) for reg in cc.CALLER_SAVED_REGS}
            if cc.CALLER_SAVED_REGS is not None
            else set()
        )

    @staticmethod
    def stack_pointer_as_atom(state) -> Register:
        return Register(state.arch.sp_offset, state.arch.bytes, state.arch)
