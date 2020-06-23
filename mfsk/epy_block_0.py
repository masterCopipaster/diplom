"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import sys


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Text Logger"""

    def __init__(self, filename = "log.txt", open_param = "w", num_inputs = 2):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Float Text Logger',   # will show up in GRC
            in_sig=[np.float32] * num_inputs,
            out_sig = []
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.file = sys.stdout #open(filename, open_param)
        self.num_inputs = num_inputs

    def work(self, input_items, output_items):
        try:
            i = 0
            while 1:
                s = ""
                for k in range(self.num_inputs):
                    s += str(input_items[k][i]) + "\t"
                s += "\n"
                self.file.write(s)
                i += 1
        except:
            pass
        return 0
