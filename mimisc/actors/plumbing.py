from migen.fhdl.std import *
from migen.genlib.record import *
from migen.flow.actor import *


class Relax(Module):
    def __init__(self, layout):
        self.d = Sink(layout)
        self.q = Source(layout)
        self.busy = Signal()

        ###

        reg_a = Record(layout)
        reg_a_full = Signal(reset=0)
        reg_b = Record(layout)
        reg_b_full = Signal(reset=0)

        tx_out = Signal()
        tx_in = Signal()

        self.comb += [
            If(reg_a_full,
                self.q.payload.eq(reg_a)
            ).Else(
                self.q.payload.eq(reg_b)
            ),
            self.d.ack.eq(~(reg_b_full & reg_a_full)),
            self.q.stb.eq(reg_a_full | reg_b_full),
            self.busy.eq(self.q.stb),
            tx_out.eq(self.q.stb & self.q.ack),
            tx_in.eq(self.d.stb & self.d.ack),
        ]

        self.sync += [
            If(tx_in,
                reg_b.eq(self.d.payload),
                reg_b_full.eq(1),
                If(tx_out,
                    reg_a_full.eq(0)
                ).Else(
                    If(reg_b_full,
                        reg_a_full.eq(1),
                        reg_a.eq(reg_b)
                    )
                )
            ).Elif(tx_out,
                If(reg_a_full,
                    reg_a_full.eq(0)
                ).Else(
                    reg_b_full.eq(0)
                )
            )
        ]


class Schedule(Module):
    def __init__(self, layout):
        self.sink = Sink(layout)
        self.source_a = Source(layout)
        self.source_b = Source(layout)
        self.busy = Signal()

        ###

        priority = Signal()

        en = Signal()
        en_a = Signal()
        en_b = Signal()

        self.comb += [
            self.busy.eq(0),
            en.eq((self.source_a.ack | self.source_b.ack) & self.sink.stb),
            self.sink.ack.eq(en),
            If(priority,
                en_a.eq(en & self.source_a.ack),
                en_b.eq(en & ~self.source_a.ack),
            ).Else(
                en_a.eq(en & ~self.source_b.ack),
                en_b.eq(en & self.source_b.ack),
            ),
            self.source_a.stb.eq(en_a),
            self.source_b.stb.eq(en_b),
            self.source_a.payload.eq(self.sink.payload),
            self.source_b.payload.eq(self.sink.payload),
        ]

        self.sync += If(en, priority.eq(~priority))


class Gather(Module):
    def __init__(self, layout):
        self.sink_a = Sink(layout)
        self.sink_b = Sink(layout)
        self.source = Source(layout)
        self.busy = Signal()

        ###

        priority = Signal()

        en = Signal()
        en_a = Signal()
        en_b = Signal()

        self.comb += [
            self.busy.eq(0),
            en.eq((self.sink_a.stb | self.sink_b.stb) & self.source.ack),
            self.source.stb.eq(en),
            If(priority,
                en_a.eq(en & self.sink_a.stb),
                en_b.eq(en & ~self.sink_a.stb),
            ).Else(
                en_a.eq(en & ~self.sink_b.stb),
                en_b.eq(en & self.sink_b.stb),
            ),
            self.sink_a.ack.eq(en_a),
            self.sink_b.ack.eq(en_b),
            If(en_a,
                self.source.payload.eq(self.sink_a.payload),
            ).Else(
                self.source.payload.eq(self.sink_b.payload),
            ),
        ]

        self.sync += If(en, priority.eq(~priority))
