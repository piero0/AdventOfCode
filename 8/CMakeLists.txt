cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

find_package(fmt)
set(name "eight")

project(${name})
add_executable(${name} ${name}.cpp)
set_property(TARGET ${name} PROPERTY CXX_STANDARD 20)
target_link_libraries(${name} PRIVATE fmt::fmt)
