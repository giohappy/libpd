cmake_minimum_required(VERSION 3.25)
project(pylibpd_project C)

# Set policies for UseSWIG
cmake_policy(SET CMP0078 NEW)
cmake_policy(SET CMP0086 NEW)

# Force settings for the libpd subproject to build the static library
set(LIBPD_STATIC ON CACHE BOOL "Build static library" FORCE)
set(LIBPD_SHARED OFF CACHE BOOL "Build shared library" FORCE)
set(PD_UTILS OFF CACHE BOOL "Compile utilities" FORCE)
set(PD_EXTRA ON CACHE BOOL "Compile extras" FORCE)

# Add the main libpd repository as a subdirectory
add_subdirectory(.. "${CMAKE_CURRENT_BINARY_DIR}/libpd_build")

# Find Python and SWIG
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

# Configure SWIG for Python
set_property(SOURCE pylibpd.i PROPERTY CPLUSPLUS OFF)

# Add the SWIG python library target
swig_add_library(_pylibpd
    TYPE SHARED
    LANGUAGE python
    SOURCES pylibpd.i
)

# Link the SWIG module to the static libpd library and Python
target_link_libraries(_pylibpd PRIVATE libpd_static Python::Python)

# Configure MSVC-specific warnings/definitions for the wrapper target
if(MSVC)
    target_compile_options(_pylibpd PRIVATE /wd4091 /wd4996)
    target_compile_definitions(_pylibpd PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

# Set output properties so it is built as a .pyd file with no "lib" prefix
set_target_properties(_pylibpd PROPERTIES
    PREFIX ""
    SUFFIX ".pyd"
)

# Copy generated Python module and binary to the source directory for easy development/testing
add_custom_command(TARGET _pylibpd POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:_pylibpd> "${CMAKE_CURRENT_SOURCE_DIR}/"
    COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/pylibpd.py" "${CMAKE_CURRENT_SOURCE_DIR}/"
    COMMENT "Copying compiled Python bindings to python/ source directory"
)

