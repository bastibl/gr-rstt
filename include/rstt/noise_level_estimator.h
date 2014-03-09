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

#ifndef INCLUDED_RSTT_NOISE_LEVEL_ESTIMATOR_H
#define INCLUDED_RSTT_NOISE_LEVEL_ESTIMATOR_H

#include <rstt/api.h>
#include <boost/shared_ptr.hpp>
#include <rstt/noise_model.h>

namespace gr {
  namespace rstt {

    /*!
     * Estimate noise level value in signal.

     * It does so by spliting input signal power spectrum into chunks.
     * Then are identified chunks which contains only noise and
     * from which noise level (mean and dispersion) are estimated.
     */
    class RSTT_API noise_level_estimator {
     protected:
       noise_level_estimator()
       {}

     public:
      typedef boost::shared_ptr<noise_level_estimator> sptr;

      /*!
       * @param coverage is value in range from 0. to 1. It represents amount of
       *   signal power spectrum used for noise estimation. 0.2 is good value.
       * @param nsplits numer of fragmens generated for noise estimation.
       */
      static sptr
      make(float coverage, int nsplits);

      virtual ~noise_level_estimator()
      { }

      /*!
       * Do noise level estimation.
       *
       * @param data (natural) logarithm of signal power spectrum.
       * @param data_items length of input data.
       */
      virtual noise_model estimate(const float *data, int data_items) const = 0;
    };

  } // namespace rstt
} // namespace gr

#endif /* INCLUDED_RSTT_NOISE_LEVEL_ESTIMATOR_H */

