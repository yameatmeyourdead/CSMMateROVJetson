# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.19

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\CMake\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\CMake\bin\cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = D:\Desktop\Programming\CPP-Rewrite

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = D:\Desktop\Programming\CPP-Rewrite\build

# Include any dependencies generated for this target.
include CMakeFiles/ROV.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/ROV.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/ROV.dir/flags.make

CMakeFiles/ROV.dir/ROV.cpp.obj: CMakeFiles/ROV.dir/flags.make
CMakeFiles/ROV.dir/ROV.cpp.obj: CMakeFiles/ROV.dir/includes_CXX.rsp
CMakeFiles/ROV.dir/ROV.cpp.obj: ../ROV.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\Desktop\Programming\CPP-Rewrite\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/ROV.dir/ROV.cpp.obj"
	C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\ROV.dir\ROV.cpp.obj -c D:\Desktop\Programming\CPP-Rewrite\ROV.cpp

CMakeFiles/ROV.dir/ROV.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ROV.dir/ROV.cpp.i"
	C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\Desktop\Programming\CPP-Rewrite\ROV.cpp > CMakeFiles\ROV.dir\ROV.cpp.i

CMakeFiles/ROV.dir/ROV.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ROV.dir/ROV.cpp.s"
	C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\Desktop\Programming\CPP-Rewrite\ROV.cpp -o CMakeFiles\ROV.dir\ROV.cpp.s

# Object files for target ROV
ROV_OBJECTS = \
"CMakeFiles/ROV.dir/ROV.cpp.obj"

# External object files for target ROV
ROV_EXTERNAL_OBJECTS =

ROV.exe: CMakeFiles/ROV.dir/ROV.cpp.obj
ROV.exe: CMakeFiles/ROV.dir/build.make
ROV.exe: src/libsrc.a
ROV.exe: src/Components/libcomponents.a
ROV.exe: CMakeFiles/ROV.dir/linklibs.rsp
ROV.exe: CMakeFiles/ROV.dir/objects1.rsp
ROV.exe: CMakeFiles/ROV.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=D:\Desktop\Programming\CPP-Rewrite\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ROV.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\ROV.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/ROV.dir/build: ROV.exe

.PHONY : CMakeFiles/ROV.dir/build

CMakeFiles/ROV.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\ROV.dir\cmake_clean.cmake
.PHONY : CMakeFiles/ROV.dir/clean

CMakeFiles/ROV.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" D:\Desktop\Programming\CPP-Rewrite D:\Desktop\Programming\CPP-Rewrite D:\Desktop\Programming\CPP-Rewrite\build D:\Desktop\Programming\CPP-Rewrite\build D:\Desktop\Programming\CPP-Rewrite\build\CMakeFiles\ROV.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/ROV.dir/depend

