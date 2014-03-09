#!/usr/bin/env python2
# -*- coding: utf8 -*-
#
# Copyright 2013 Jiří Pinkava <j-pi@seznam.cz>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

from gnuradio import gr, gr_unittest, blocks
from rstt_swig import bytes2frames

class qa_bytes2frames(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block ()

    def tearDown(self):
        self.tb = None

    def do(self, data_src, data_exp, test_block):
        src = blocks.vector_source_s(data_src)
        self.tb.connect(src, test_block)
        dst = blocks.vector_sink_s(vlen=240)
        self.tb.connect(test_block, dst)
        self.tb.run()
        result_data = tuple([int(x) for x in dst.data()])
        self.assertEqual(data_exp, result_data)

    # trivial valid sync
    def test_00(self):
        data_src =(0x2A, )*5 + (0x10, 0x65, 0x10) + (0, )*34 + \
                (0x69, 0x0C, ) + (0, )*26 + \
                (0x67, 0x3D, ) + (0, )*124 + \
                (0x68, 0x05, ) + (0, )*12 + \
                (0xff, 0x02, 0x02, 0x00, 0x02, ) + (0, )*25
        data_exp = data_src
        #data_src = data_src + data_src
        test_block = bytes2frames()
        self.do(data_src, data_exp, test_block)

    # sync with offset
    def test_01(self):
        data_src = (0x2A, )*5 + (0x10, 0x65, 0x10) + (0, )*34 + \
                (0x69, 0x0C, ) + (0, )*26 + \
                (0x67, 0x3D, ) + (0, )*124 + \
                (0x68, 0x05, ) + (0, )*12 + \
                (0xff, 0x02, 0x02, 0x00, 0x02, ) + (0, )*25
        data_exp = \
                (0x700,)*6 + (0x700, 0x700, ) + (0x700, )*34 + \
                (0x700, 0x700, ) + (0x700, )*26 + \
                (0x700, 0x700, ) + (0x700, )*124 + \
                (0x700, 0x700, ) + (0x700, )*12 + \
                (0x700, 0x700, 0x700, 0x700, 0x700, ) + (0x700, )*15 + (0x01, )*10 + \
                data_src + \
                data_src
        data_src = (0x01,)* 10 + data_src + data_src
        #data_src = data_src + data_src
        test_block = bytes2frames()
        self.do(data_src, data_exp, test_block)


if __name__ == '__main__':
    gr_unittest.run(qa_bytes2frames, "qa_bytes2frames.xml")

