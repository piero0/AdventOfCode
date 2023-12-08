cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

project(five_one)
add_executable(five_one five_one.cpp)
set_property(TARGET five_one PROPERTY CXX_STANDARD 20)

project(five_two)
add_executable(five_two five_two.cpp)
set_property(TARGET five_two PROPERTY CXX_STANDARD 20)

find_package(fmt)
target_link_libraries(five_two PRIVATE fmt::fmt)
