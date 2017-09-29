# Modified for Conan.io library inclusion

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
MESSAGE(${CONAN_LIB_DIRS_OPENBLAS})
find_library(OpenBLAS_LIBRARY
  NAMES ${CONAN_LIBS_OPENBLAS}
  PATHS ${CMAKE_SYSTEM_LIBRARY_PATH} ${CONAN_LIB_DIRS_OPENBLAS}
  )

if(OpenBLAS_LIBRARY)
  set(OpenBLAS_LIBRARIES ${OpenBLAS_LIBRARY})
  set(OpenBLAS_FOUND YES)
else()
  set(OpenBLAS_FOUND NO)
endif()


if(OpenBLAS_FOUND)
  if (NOT OpenBLAS_FIND_QUIETLY)
    message(STATUS "Found OpenBLAS: ${OpenBLAS_LIBRARIES}")
  endif()
else()
  if(OpenBLAS_FIND_REQUIRED)
    message(FATAL_ERROR "Could not find OpenBLAS")
  endif()
endif()


# mark_as_advanced(OpenBLAS_LIBRARY)
