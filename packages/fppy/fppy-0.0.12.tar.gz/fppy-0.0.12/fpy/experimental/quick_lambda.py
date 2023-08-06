import sys
import types
import dis
import bytecode as bc
from importlib._bootstrap_external import (
    PathFinder,
    FileLoader,
    SourceFileLoader,
    SourcelessFileLoader,
    ExtensionFileLoader,
)

from dataclasses import dataclass


__all__ = []


@dataclass
class QLVar:
    name: str

    def pre_and_post_stack_effect(self):
        return 1, 0


def partitionInst(insts, n):
    if not insts:
        return [], []
    head = insts[-1]
    print(f"{n = }")
    print(f"{head = }")
    print(f"{head.pre_and_post_stack_effect() = }")
    pre, post = head.pre_and_post_stack_effect()
    if pre < 0:
        nxt, rst = partitionInst(insts[:-1], n - pre)
        return nxt + [head], rst
    if n == 0:
        return [], insts
    if pre >= 0:
        if pre == n:
            return [head], insts[:-1]
        if pre < n:
            nxt, rst = partitionInst(insts[:-1], n - pre)
            return nxt + [head], rst
    pre = abs(pre)
    nxt, rst = partitionInst(insts[:-1], pre)
    if post == n:
        return nxt + [head], rst
    if post < n:
        head = nxt + [head]
        nxt, rst = partitionInst(rst, n - post)
        return nxt + head, rst
    return [], []


def transform_block(raw_bc):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(f"block {raw_bc = }")
    trans_bc = []
    for instr in raw_bc:
        if not isinstance(instr, bc.Instr):
            trans_bc.append(instr)
            continue
        if instr.name == "LOAD_CONST":
            if isinstance(instr.arg, types.CodeType):
                transformed_co = transform(instr.arg)
                trans_bc.append(
                    bc.Instr("LOAD_CONST", transformed_co, lineno=instr.lineno)
                )
                continue
        elif instr.name in ("LOAD_NAME", "LOAD_GLOBAL"):
            name = instr.arg
            if name.startswith("_") and name[1:].isdigit():
                trans_bc.append(QLVar(name))
                continue

        trans_bc.append(instr)
    res_bc = []
    parts = []
    print(f"{trans_bc = }")
    print("------------------------------")
    while trans_bc:
        last_instr = trans_bc[-1]
        if last_instr.has_jump():
            part, trans_bc = partitionInst(trans_bc[:-1], 1)
            part.append(last_instr)
        else:
            part, trans_bc = partitionInst(trans_bc, 0)
        parts.append(part)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(f"{part = }")
    return res_bc


def transform(co):
    raw_bc = bc.Bytecode.from_code(co)
    cfg = bc.ControlFlowGraph.from_bytecode(raw_bc)
    res_cfg = bc.ControlFlowGraph()
    for block in cfg:
        transform_block(block)

    return cfg.to_code()


class ProxySourceFileLoader(SourceFileLoader):
    def __init__(self, loader: SourceFileLoader):
        SourceFileLoader.__init__(self, loader.name, loader.path)

    def get_data(self, path: str):
        data = SourceFileLoader.get_data(self, path)
        print(f"SourceFileLoader {data = }")
        return data

    def get_code(self, fullname):
        co = SourceFileLoader.get_code(self, fullname)
        return transform(co)


class ProxySourcelessLoader(SourcelessFileLoader):
    def __init__(self, loader: SourcelessFileLoader):
        SourcelessFileLoader.__init__(self, loader.name, loader.path)

    def get_data(self, path: str):
        data = SourcelessFileLoader.get_data(self, path)
        print(f"SourcelessFileLoader {data = }")
        return data

    def get_code(self, fullname):
        co = SourcelessFileLoader.get_code(self, fullname)
        return transform(co)


class QLFinder(PathFinder):
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        spec = PathFinder.find_spec(fullname, path, target)
        if spec and spec.loader and isinstance(spec.loader, FileLoader):
            loader = spec.loader
            loader_ty = loader.__class__
            print(f"{loader_ty = }")
            loader_ = {
                SourcelessFileLoader: lambda: ProxySourcelessLoader(loader),
                SourceFileLoader: lambda: ProxySourceFileLoader(loader),
            }.get(loader_ty, lambda: loader)()
            spec.loader = loader_
        return spec


sys.meta_path.insert(0, QLFinder)
