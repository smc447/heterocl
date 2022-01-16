import hcl_mlir


class WithScope(object):
    """Auxiliary scope with"""

    def __init__(self, enter_value, exit_cb):
        self._enter_value = enter_value
        self._exit_cb = exit_cb

    def __enter__(self):
        return self._enter_value

    def __exit__(self, ptype, value, trace):
        self._exit_cb()


def for_(begin, end, step=1, name="i"):
    """Construct a FOR loop.

    Be careful: should not be used with other compute APIs like sum
    """
    hcl_mlir.enable_build_inplace()
    if isinstance(begin, int) and isinstance(end, int):
        loop = hcl_mlir.make_constant_for(begin, end, step, name=name, ip=hcl_mlir.GlobalInsertionPoint.get())
    else:
        raise RuntimeError("Not implemented")
    iter_var = hcl_mlir.IterVar(loop.induction_variable)
    hcl_mlir.GlobalInsertionPoint.save(loop.body)

    def _exit_cb():
        hcl_mlir.GlobalInsertionPoint.restore()

    return WithScope(iter_var, _exit_cb)