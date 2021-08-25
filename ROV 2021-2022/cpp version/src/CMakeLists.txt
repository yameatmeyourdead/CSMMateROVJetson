add_library(src 
Tools/Vector3D.cpp
Tools/Vector3D.h
Logger/Logger.cpp
Logger/Logger.h
Controller.cpp
Controller.h

)
add_subdirectory(Components)
target_link_libraries(src components)