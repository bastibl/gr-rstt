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


#ifndef INCLUDED_RSTT_ERROR_CORRECTION_H
#define INCLUDED_RSTT_ERROR_CORRECTION_H

#include <rstt/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace rstt {

    /*!
     * \brief Correct errors in recieved radisonde frames.
     * \ingroup rstt
     *
     */
    class RSTT_API error_correction : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<error_correction> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of rstt::error_correction.
       *
       * \param drop_invalid Drop totaly broken frames (keep partialy broken).
       * \param guess_level Enable error correction by guessing byte values,
       *    based on content of previous frames.
       *    0 - guessing disables, 1 - known for sure, 4/6/8 - safe and usefull
       *    256 - maximum (nonsense, try guess all bytes!).
       *
       * To avoid accidental use of raw pointers, rstt::error_correction's
       * constructor is in a private implementation
       * class. rstt::error_correction::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool drop_invalid = false, int guess_level = 1);
    };

  } // namespace rstt
} // namespace gr

#endif /* INCLUDED_RSTT_ERROR_CORRECTION_H */

