"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, sample_rate = 2048000, short_impulse_len = 0.0005, long_impulse_len = 0.001, packet_separator_len = 0.01, packet_len = 24, data = 0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='remote basic coder',   # will show up in GRC
            in_sig=[],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sample_rate = sample_rate
        self.short_impulse_len = short_impulse_len
        self.long_impulse_len = long_impulse_len
        self.packet_len = packet_len
        self.data = data
        self.sl = int(sample_rate * short_impulse_len)
        self.ll = int(sample_rate * long_impulse_len) 
        self.ps = int(sample_rate * packet_separator_len)
        self.transm_index = 0
        
    def generate_bit(self, bit):
        return [np.complex64(1.0) for i in xrange(self.ll if bit else self.sl)] + [np.complex64(0.0) for i in xrange(self.sl if bit else self.ll)]
        
    def generate_packet(self):
        res = []
        for i in xrange(self.packet_len):
            res += self.generate_bit(1 & (self.data >> (self.packet_len - i - 1)))
        res += [np.complex64(1.0) for i in xrange(self.sl)] + [np.complex64(0.0) for i in xrange(self.ps)]
        return res

    def work(self, input_items, output_items):
    
        pack = self.generate_packet()
        for i in range(len(output_items[0])):
            output_items[0][i] = pack[self.transm_index]
            self.transm_index = (self.transm_index + 1) % len(pack)
            
        return len(output_items[0])
