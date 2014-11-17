from mibuild.generic_platform import *
from mibuild.xilinx_ise import XilinxISEPlatform
from mibuild.crg import SimpleCRG


_io = [
        ("clk_if", 0, Pins("K20"), IOStandard("LVCMOS33")),
        ("fx2_fifo", 0,
            Subsignal("sloe", Pins("U15"), Drive(12)),
            Subsignal("slrd", Pins("N22"), Drive(12)),
            Subsignal("slwr", Pins("M22"), Drive(12)),
            Subsignal("pktend", Pins("AB5"), Drive(12)),
            Subsignal("fifoadr", Pins("W17 Y18"), Drive(12)),
            Subsignal("fd", Pins("Y17 V13 W13 AA8 AB8 W6 Y6 Y9 "
                "V21 V22 U20 U22 R20 R22 P18 P19")),
            Subsignal("flag", Pins("F20 F19 F18 AB17")),
            IOStandard("LVCMOS33")),
]

class Platform(XilinxISEPlatform):
    def __init__(self, manual_timing=False):
        self.manual_timing = manual_timing
        XilinxISEPlatform.__init__(self, "xc6slx150-3csg484", _io,
                lambda p: SimpleCRG(p, "clk_if", None))
        self.add_platform_command("""
CONFIG VCCAUX = "2.5";
""")

    def do_finalize(self, fragment):
        if self.manual_timing:
            return
        try:
            self.add_platform_command("""
NET "{clk_if}" TNM_NET = "GRP_clk_if";
TIMESPEC "TS_clk_if" = PERIOD "GRP_clk_if" 33.33 ns HIGH 50%;

OFFSET = IN 15 ns VALID 30 ns BEFORE "{clk_if}";
OFFSET = OUT 15 ns AFTER "{clk_if}";

""", clk_if=self.lookup_request("clk_if"))
        except ConstraintError:
            pass
