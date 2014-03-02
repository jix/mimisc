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
