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


#ifndef INCLUDED_RSTT_DECODER_H
#define INCLUDED_RSTT_DECODER_H

#include <rstt/api.h>
#include <gnuradio/hier_block2.h>

namespace gr {
  namespace rstt {

    /*!
     * \brief Convert demodulated symbols to frames.
     * \ingroup rstt
     *
     */
    class RSTT_API decoder : virtual public gr::hier_block2
    {
     public:
      typedef boost::shared_ptr<decoder> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of rstt::decoder.
       *
       * \param sync_nbits Use N bits for bite stream synchronization.
       * \param sync_nbytes Use N bytes for byte stream synchronization.
       * \param drop_invalid Drop invalid frames (keep partialy valid).
       * \param guess_level Error correction based on byte value distribution
       * probability. 0 - disabled, 1 - correct only well known bytes,
       * 4/6/8 - good values for value guessing (with error probability N/256)
       * 256 - try guess all bytes (nonsens)
       *
       * To avoid accidental use of raw pointers, rstt::decoder's
       * constructor is in a private implementation
       * class. rstt::decoder::make is the public interface for
       * creating new instances.
       */
      static sptr make(int sync_nbits = 20*10, int sync_nbytes = 32,
              bool drop_invalid = true, int guess_level = 1);
    };

  } // namespace rstt
} // namespace gr

#endif /* INCLUDED_RSTT_DECODER_H */

