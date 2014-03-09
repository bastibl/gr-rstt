/* -*- c++ -*- */
/* 
 * Copyright 2013 Jiří Pinkava <j-pi@seznam.cz>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */

#ifndef INCLUDED_RSTT_BITS2BYTES_IMPL_H
#define INCLUDED_RSTT_BITS2BYTES_IMPL_H

#include <rstt/bits2bytes.h>

namespace gr {
  namespace rstt {

    class bits2bytes_impl : public bits2bytes
    {
     private:
      typedef signed char in_t;
      typedef unsigned short out_t;

      enum {
          STATUS_INVALID_START = 0x100,
          STATUS_INVALID_BYTE = 0x200,
          STATUS_INVALID_STOP = 0x400
      };

      /** Lenght of sync window in bits, */
      int sync_nbits;
      /** Number of bits to fill in, before normal work can start. */
      int fill_in_bits;
      /** Index to firts input bit which was not processed at all. */
      int in_idx;

      /** If true, bits are droppend until synchronization is achieved. */
      bool do_bit_resync;
      /** Bytes remaining to send before normal operation can continue. */
      int send_bytes_remain;
      /** Lenght of sync window in bits. */
      int sync_win[10];
      int sync_win_idx;
      int sync_offs;

      out_t get_byte(const in_t *in, bool start_bite_missing = false) const;
      int get_sync_offs() const;
      int resync_stream(int out_len, int produced, int in_len, const in_t *in, out_t *out);
      void shift_bits(const in_t *in, int nbits = 10);

      /** Update current sync value by 'inc' and move to next sync window
        position. */
      void sync_win_idx_pp(int inc = 0);

      int work_convert(int out_len,
              int in_len,
              const in_t *in,
              out_t *out);

      bool work_fill(int in_len, const in_t *in);

     public:
      bits2bytes_impl(int sync_nbytes);
      ~bits2bytes_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
    };

  } // namespace rstt
} // namespace gr

#endif /* INCLUDED_RSTT_BITS2BYTES_IMPL_H */

