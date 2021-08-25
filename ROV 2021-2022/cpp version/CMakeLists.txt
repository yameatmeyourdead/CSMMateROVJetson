cmake_minimum_required(VERSION 3.0.0)
project(CPPROV VERSION 0.1.0)

include(CTest)
enable_testing()

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(CPPROV
               Cameras.cpp
               Component.hpp
               Drive.cpp
               Manipulator.cpp
               MicroROV.cpp
               ROV.cpp
               )

target_link_libraries(CPPROV ${OpenCV_LIBS})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)