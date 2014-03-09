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

#ifndef INCLUDED_RSTT_ERROR_CORRECTION_IMPL_H
#define INCLUDED_RSTT_ERROR_CORRECTION_IMPL_H

#include <rstt/error_correction.h>
#include "error_correction_guess.h"

namespace gr {
  namespace rstt {

    class error_correction_impl : public error_correction
    {
     private:
      typedef unsigned short in_t;
      typedef unsigned short out_t;

      /** Reed-Solomon codec private data. */
      void *rs;

      bool drop_invalid;
      int guess_level;

      struct pred_byte_err;
      struct pred_recv_err;

      error_correction_guess guess_correction;

      /** Try serveral correction algorithms. */
      bool do_corrections(const in_t *in, out_t *out) const;

      /** Try process correction for specified value algorithm. */
      template <class GetValue>
      bool do_correction(const in_t *in, out_t *out, GetValue get_value) const;

      /** Evaluate Reed-Solomon correction code. */
      template <class GetValue>
      int do_rs_correction(const in_t *in, unsigned char *rs_data,
              GetValue get_value) const;

      /** copy back corrected data and (correct) header */
      void copy_corrected(unsigned char *rs_data, out_t *out) const;

      static bool chech_crc(const in_t *in, int len);

     public:
      error_correction_impl(bool drop_invalid, int guess_level);
      ~error_correction_impl();

      /**
        Check subframes CRC.
        Returns positive number if all subframes are valid,
        negative number if some subframes are invalid, or zero
        if no valid subframe is found.
      **/
      static int is_frame_valid(const in_t *in);

      int work(int noutput_items,
	       gr_vector_const_void_star &input_items,
	       gr_vector_void_star &output_items);
    };

  } // namespace rstt
} // namespace gr

#endif /* INCLUDED_RSTT_ERROR_CORRECTION_IMPL_H */

