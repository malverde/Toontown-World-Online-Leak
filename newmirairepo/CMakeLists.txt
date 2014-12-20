cmake_minimum_required (VERSION 2.6)
set_property (GLOBAL PROPERTY USE_FOLDERS ON)
project(Mirai)

set(BUILD_STATIC BOOL on)

if (WIN32)
	add_definitions (-D_WIN32_WINDOWS)
endif()

SET(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -D_DEBUG")

link_directories(${CMAKE_CURRENT_LIST_DIR}/p3dbuild/lib)
include_directories(${CMAKE_CURRENT_LIST_DIR}/p3dbuild/include)

link_directories(${CMAKE_CURRENT_LIST_DIR}/Python-2.7.5/PCbuild)
include_directories(${CMAKE_CURRENT_LIST_DIR}/Python-2.7.5/Include)
include_directories(${CMAKE_CURRENT_LIST_DIR}/Python-2.7.5/PC)

link_directories(${CMAKE_CURRENT_LIST_DIR}/panda3d-1.8.1/thirdparty/win-libs-vc9)

include_directories(C:/openssl/include) #CLEANME
link_directories(C:/openssl/lib) #CLEANME


add_executable(mirai
	mirai.cpp
)
target_link_libraries(mirai python27.lib libeay32.lib)