cmake_minimum_required(VERSION 2.8.3)
project(imu)

find_package(Boost REQUIRED COMPONENTS thread)

find_package(catkin REQUIRED COMPONENTS
  cmake_modules
  message_filters
  roscpp
  sensor_msgs
  std_msgs
  tf
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES complementary_filter
  CATKIN_DEPENDS message_filters roscpp sensor_msgs std_msgs tf
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
)

## Declare a cpp library
add_library(complementary_filter
  src/complementary_filter.cpp
  src/complementary_filter_ros.cpp
  include/imu_complementary_filter/complementary_filter.h
  include/imu_complementary_filter/complementary_filter_ros.h
)
target_link_libraries(complementary_filter ${catkin_LIBRARIES} ${Boost_LIBRARIES})

# create complementary_filter_node executable
add_executable(complementary_filter_node src/complementary_filter_node.cpp)
target_link_libraries(complementary_filter_node complementary_filter ${catkin_LIBRARIES})

# create imu_raw_node executable
add_executable(imu_raw_node src/imu_raw_node.cpp)
target_link_libraries(imu_raw_node ${catkin_LIBRARIES} wiringPi)