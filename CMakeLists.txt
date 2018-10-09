project(cmake_wrapper)

message(STATUS "CMake Conan Wrapper")
include(conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(source_subfolder)
