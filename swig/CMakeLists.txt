# Copyright 2011 Free Software Foundation, Inc.
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
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT rstt_sources)
    MESSAGE(STATUS "No C++ sources... skipping swig/")
    return()
endif(NOT rstt_sources)

########################################################################
# Include swig generation macros
########################################################################
find_package(SWIG)
find_package(PythonLibs)
if(NOT SWIG_FOUND OR NOT PYTHONLIBS_FOUND)
    return()
endif()
include(GrSwig)
include(GrPython)

########################################################################
# Setup swig generation
########################################################################
set(GR_SWIG_INCLUDE_DIRS $<TARGET_PROPERTY:gnuradio::runtime_swig,INTERFACE_INCLUDE_DIRECTORIES>)
set(GR_SWIG_TARGET_DEPS gnuradio::runtime_swig)

set(GR_SWIG_LIBRARIES gnuradio-rstt)

set(GR_SWIG_DOC_FILE ${CMAKE_CURRENT_BINARY_DIR}/rstt_swig_doc.i)
set(GR_SWIG_DOC_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../include)

GR_SWIG_MAKE(rstt_swig rstt_swig.i)

########################################################################
# Install the build swig module
########################################################################
GR_SWIG_INSTALL(TARGETS rstt_swig DESTINATION ${GR_PYTHON_DIR}/rstt)

########################################################################
# Install swig .i files for development
########################################################################
install(
    FILES
    rstt_swig.i
    ${CMAKE_CURRENT_BINARY_DIR}/rstt_swig_doc.i
    DESTINATION ${GR_INCLUDE_DIR}/rstt/swig
)
