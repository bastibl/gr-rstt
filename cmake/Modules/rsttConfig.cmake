INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_RSTT rstt)

FIND_PATH(
    RSTT_INCLUDE_DIRS
    NAMES rstt/api.h
    HINTS $ENV{RSTT_DIR}/include
        ${PC_RSTT_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    RSTT_LIBRARIES
    NAMES gnuradio-rstt
    HINTS $ENV{RSTT_DIR}/lib
        ${PC_RSTT_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/rsttTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(RSTT DEFAULT_MSG RSTT_LIBRARIES RSTT_INCLUDE_DIRS)
MARK_AS_ADVANCED(RSTT_LIBRARIES RSTT_INCLUDE_DIRS)
