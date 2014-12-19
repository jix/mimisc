from migen.fhdl.std import *
from migen.genlib.record import *
from migen.flow.actor import *
from migen.actorlib.sim import *


class ListSource(SimActor):
    def __init__(self, layout):
        self.source = Source(layout)
        self.tokens = []
        super().__init__(self._source_gen())
        self.comb += self.busy.eq(0)

    def _source_gen(self):
        while True:
            if self.tokens:
                token = self.tokens.pop(0)
                if token:
                    yield Token('source', token)
                else:
                    yield None
            else:
                yield None


class ListSink(SimActor):
    def __init__(self, layout, limit=None):
        self.sink = Sink(layout)
        self.tokens = []
        super().__init__(self._sink_gen())
        self.comb += self.busy.eq(0)
        self.limit = limit

    def _sink_gen(self):
        while True:
            if self.limit is None or len(self.tokens) < self.limit:
                tk = Token('sink')
                yield tk
                if tk.value is not None:
                    self.tokens.append(tk.value)
            else:
                yield None
