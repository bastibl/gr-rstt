# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of gr-rstt
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

list(APPEND rstt_sources
    symbols2bits_impl.cc
    bits2bytes_impl.cc
    bytes2frames_impl.cc
    error_correction_guess.cc
    error_correction_impl.cc
    decoder_impl.cc
    noise_level_estimator_impl.cc
    noise_level_estimator2_impl.cc
    clip_impl.cc
)

set(rstt_sources "${rstt_sources}" PARENT_SCOPE)
if(NOT rstt_sources)
    MESSAGE(STATUS "No C++ sources... skipping lib/")
    return()
endif(NOT rstt_sources)

add_library(gnuradio-rstt SHARED ${rstt_sources})
target_link_libraries(gnuradio-rstt gnuradio::gnuradio-runtime gnuradio::gnuradio-fec)
target_include_directories(gnuradio-rstt
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
    PUBLIC $<INSTALL_INTERFACE:include>
  )
set_target_properties(gnuradio-rstt PROPERTIES DEFINE_SYMBOL "gnuradio_rstt_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-rstt PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-rstt)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

# If your unit tests require special include paths, add them here
#include_directories()
# List all files that contain Boost.UTF unit tests here
list(APPEND test_rstt_sources
)
# Anything we need to link to for the unit tests go here
list(APPEND GR_TEST_TARGET_DEPS gnuradio-rstt cppunit)

if(NOT test_rstt_sources)
    MESSAGE(STATUS "No C++ unit tests... skipping")
    return()
endif(NOT test_rstt_sources)

foreach(qa_file ${test_rstt_sources})
    GR_ADD_CPP_TEST("rstt_${qa_file}"
        ${CMAKE_CURRENT_SOURCE_DIR}/${qa_file}
    )
endforeach(qa_file)
