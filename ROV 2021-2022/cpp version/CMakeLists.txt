cmake_minimum_required(VERSION 3.19)

project(
    ROV
    VERSION 0.1
    DESCRIPTION "Colorado School of Mines MATE ROV"
    LANGUAGES CXX
)

add_subdirectory(src)

add_executable(${PROJECT_NAME} ROV.cpp)

target_include_directories(${PROJECT_NAME} PUBLIC src)
target_link_directories(${PROJECT_NAME} PRIVATE src)
target_link_libraries(${PROJECT_NAME} src)