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
include src/Components/CMakeFiles/components.dir/depend.make

# Include the progress variables for this target.
include src/Components/CMakeFiles/components.dir/progress.make

# Include the compile flags for this target's objects.
include src/Components/CMakeFiles/components.dir/flags.make

src/Components/CMakeFiles/components.dir/Drive.cpp.obj: src/Components/CMakeFiles/components.dir/flags.make
src/Components/CMakeFiles/components.dir/Drive.cpp.obj: ../src/Components/Drive.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\Desktop\Programming\CPP-Rewrite\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/Components/CMakeFiles/components.dir/Drive.cpp.obj"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\components.dir\Drive.cpp.obj -c D:\Desktop\Programming\CPP-Rewrite\src\Components\Drive.cpp

src/Components/CMakeFiles/components.dir/Drive.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/components.dir/Drive.cpp.i"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\Desktop\Programming\CPP-Rewrite\src\Components\Drive.cpp > CMakeFiles\components.dir\Drive.cpp.i

src/Components/CMakeFiles/components.dir/Drive.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/components.dir/Drive.cpp.s"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\Desktop\Programming\CPP-Rewrite\src\Components\Drive.cpp -o CMakeFiles\components.dir\Drive.cpp.s

src/Components/CMakeFiles/components.dir/Manipulator.cpp.obj: src/Components/CMakeFiles/components.dir/flags.make
src/Components/CMakeFiles/components.dir/Manipulator.cpp.obj: ../src/Components/Manipulator.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\Desktop\Programming\CPP-Rewrite\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object src/Components/CMakeFiles/components.dir/Manipulator.cpp.obj"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\components.dir\Manipulator.cpp.obj -c D:\Desktop\Programming\CPP-Rewrite\src\Components\Manipulator.cpp

src/Components/CMakeFiles/components.dir/Manipulator.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/components.dir/Manipulator.cpp.i"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\Desktop\Programming\CPP-Rewrite\src\Components\Manipulator.cpp > CMakeFiles\components.dir\Manipulator.cpp.i

src/Components/CMakeFiles/components.dir/Manipulator.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/components.dir/Manipulator.cpp.s"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && C:\PROGRA~1\MINGW-~1\X86_64~1.0-P\mingw64\bin\G__~1.EXE $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\Desktop\Programming\CPP-Rewrite\src\Components\Manipulator.cpp -o CMakeFiles\components.dir\Manipulator.cpp.s

# Object files for target components
components_OBJECTS = \
"CMakeFiles/components.dir/Drive.cpp.obj" \
"CMakeFiles/components.dir/Manipulator.cpp.obj"

# External object files for target components
components_EXTERNAL_OBJECTS =

src/Components/libcomponents.a: src/Components/CMakeFiles/components.dir/Drive.cpp.obj
src/Components/libcomponents.a: src/Components/CMakeFiles/components.dir/Manipulator.cpp.obj
src/Components/libcomponents.a: src/Components/CMakeFiles/components.dir/build.make
src/Components/libcomponents.a: src/Components/CMakeFiles/components.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=D:\Desktop\Programming\CPP-Rewrite\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX static library libcomponents.a"
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && $(CMAKE_COMMAND) -P CMakeFiles\components.dir\cmake_clean_target.cmake
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\components.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/Components/CMakeFiles/components.dir/build: src/Components/libcomponents.a

.PHONY : src/Components/CMakeFiles/components.dir/build

src/Components/CMakeFiles/components.dir/clean:
	cd /d D:\Desktop\Programming\CPP-Rewrite\build\src\Components && $(CMAKE_COMMAND) -P CMakeFiles\components.dir\cmake_clean.cmake
.PHONY : src/Components/CMakeFiles/components.dir/clean

src/Components/CMakeFiles/components.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" D:\Desktop\Programming\CPP-Rewrite D:\Desktop\Programming\CPP-Rewrite\src\Components D:\Desktop\Programming\CPP-Rewrite\build D:\Desktop\Programming\CPP-Rewrite\build\src\Components D:\Desktop\Programming\CPP-Rewrite\build\src\Components\CMakeFiles\components.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : src/Components/CMakeFiles/components.dir/depend

