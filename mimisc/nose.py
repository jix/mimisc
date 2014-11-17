from migen.sim.generic import *
from migen.fhdl.structure import _Fragment
from migen.sim.upper import gen_sim, proxy_sim
import nose.tools
import os


def simulation(f):
    def wrapper(self, *args, **kwds):
        self.finalize()
        self._fragment.sim.append(proxy_sim(self, gen_sim(
            lambda tb_values: f(self, tb_values, *args, **kwds))))
        run_simulation(self,
            keep_files=bool(os.getenv('MIGEN_KEEP_FILES', False)))
    return nose.tools.make_decorator(f)(wrapper)
