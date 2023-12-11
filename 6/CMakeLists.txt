cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

find_package(fmt)

project(six_one)
add_executable(six_one six_one.cpp)
set_property(TARGET six_one PROPERTY CXX_STANDARD 20)
target_link_libraries(six_one PRIVATE fmt::fmt)

project(six_two)
add_executable(six_two six_two.cpp)
set_property(TARGET six_two PROPERTY CXX_STANDARD 20)
target_link_libraries(six_two PRIVATE fmt::fmt)
