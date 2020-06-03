"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """aliexpress relay remote control PWM decoder"""

    def __init__(self, packet_separator = 10, glitch_max_width = 1, packet_length = 24):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='remote_basic_decoder',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[]#np.int32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.packet_separator = packet_separator
        self.glitch_max_width = glitch_max_width
        self.packet_length = packet_length
        
        self.cur_state = False
        self.sample_counter = 0
        self.posedge_counter = 0
        self.negedge_counter = 0

        self.bit_index = 0
        self.result = 0

    def work(self, input_items, output_items):
    
        tobit = lambda s: True if s > 0.5 else False
        
        highper = self.negedge_counter - self.posedge_counter
        lowper = self.sample_counter - self.negedge_counter
        out = []
        
        for sample in input_items[0]:
            
            
            bit = tobit(sample)
            lowper = self.sample_counter - self.negedge_counter     
            
            if lowper > self.packet_separator and self.bit_index != 0:
                if self.packet_length == self.bit_index:
                    print(format(self.result, "X"))
                #out.append(np.int32(self.result))
                self.bit_index = 0
                self.result = 0
                
            if bit and not self.cur_state:
                if self.sample_counter - self.negedge_counter > self.glitch_max_width :
                    highper = self.negedge_counter - self.posedge_counter
                    res = highper > lowper
                    
                    if lowper < self.packet_separator:
                        self.result = (self.result << 1) | res
                        self.bit_index += 1
                    
                    self.posedge_counter_buffer = self.posedge_counter
                    self.posedge_counter = self.sample_counter
                else:
                    self.negedge_counter = self.negedge_counter_buffer
                
            if (not bit) and self.cur_state:
                if self.sample_counter - self.posedge_counter > self.glitch_max_width :
                    self.negedge_counter_buffer = self.negedge_counter
                    self.negedge_counter = self.sample_counter
                else:
                    self.posedge_counter = self.posedge_counter_buffer
                
            self.sample_counter += 1
            self.cur_state = bit
        #output_items = np.array([out])
        return len(input_items[0])



