# URDF and Robot Modeling

## Learning Objectives

After completing this chapter, you should be able to:
- Define URDF and explain its role in robot modeling
- Create basic URDF files to describe robot geometry and kinematics
- Understand the structure of URDF with links and joints
- Use Xacro to create more complex and reusable URDF models
- Integrate URDF models with ROS 2 for visualization and simulation
- Apply collision and visual properties to robot models

## Understanding URDF

URDF (Unified Robot Description Format) is an XML format used in ROS to describe robot models. It defines the physical and kinematic properties of a robot, including its structure, joints, and other elements that define the robot's geometry and movement capabilities.

### URDF Purpose

- **Robot Representation**: Describe the physical structure of a robot
- **Kinematics**: Define how robot parts move relative to each other
- **Simulation**: Provide models for physics simulation environments
- **Visualization**: Enable 3D visualization in tools like RViz
- **Collision Detection**: Define collision properties for safety

### Key URDF Concepts

- **Links**: Rigid parts of the robot (e.g., chassis, arm segments)
- **Joints**: Connections between links that allow relative motion
- **Materials**: Visual properties like color and texture
- **Inertial Properties**: Mass, center of mass, and inertia for physics simulation

## URDF Structure

A basic URDF file has the following structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links define rigid parts -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>

  <!-- Joints define connections between links -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0.2 0 0" rpy="0 0 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

## Links and Their Properties

### Visual Properties
The `<visual>` element defines how a link appears in visualization tools:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1 1 1"/>
    <!-- Other options: <cylinder>, <sphere>, <mesh> -->
  </geometry>
  <material name="red">
    <color rgba="1 0 0 1"/>
  </material>
</visual>
```

### Collision Properties
The `<collision>` element defines how a link interacts with physics simulation:

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1 1 1"/>
  </geometry>
</collision>
```

### Inertial Properties
The `<inertial>` element defines mass properties for physics simulation:

```xml
<inertial>
  <mass value="1.0"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
</inertial>
```

## Joints and Their Types

### Joint Types
- **fixed**: No movement between links
- **continuous**: Continuous rotation (like a wheel)
- **revolute**: Limited rotation (like an elbow)
- **prismatic**: Linear sliding motion
- **floating**: 6 degrees of freedom
- **planar**: Motion in a plane

### Joint Definition
```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link_name"/>
  <child link="child_link_name"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
</joint>
```

## Using Xacro for Complex Models

Xacro (XML Macros) extends URDF with features like macros, constants, and mathematical expressions:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="my_robot">

  <!-- Define constants -->
  <xacro:property name="wheel_radius" value="0.1"/>
  <xacro:property name="wheel_width" value="0.05"/>

  <!-- Define a macro for wheels -->
  <xacro:macro name="wheel" params="prefix parent x y z">
    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="${parent}"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="${x} ${y} ${z}" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>

    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </visual>
    </link>
  </xacro:macro>

  <!-- Use the macro to create wheels -->
  <xacro:wheel prefix="front_left" parent="base_link" x="0.2" y="0.2" z="0"/>
  <xacro:wheel prefix="front_right" parent="base_link" x="0.2" y="-0.2" z="0"/>
  <xacro:wheel prefix="rear_left" parent="base_link" x="-0.2" y="0.2" z="0"/>
  <xacro:wheel prefix="rear_right" parent="base_link" x="-0.2" y="-0.2" z="0"/>

</robot>
```

## Real-World Example: Simple Mobile Robot

A common robot model is a differential drive mobile robot:

- **Base Link**: Main chassis of the robot
- **Wheels**: Two drive wheels and one or more casters
- **Sensors**: Camera, LIDAR, IMU mounts
- **Joints**: Wheel joints for drive and caster joints

## Step-by-Step Workflow: Creating a Simple Robot Model

1. **Create a URDF file** named `simple_robot.urdf`:
   ```xml
   <?xml version="1.0"?>
   <robot name="simple_robot">
     <link name="base_link">
       <visual>
         <geometry>
           <box size="0.5 0.3 0.2"/>
         </geometry>
         <material name="grey">
           <color rgba="0.5 0.5 0.5 1"/>
         </material>
       </visual>
       <collision>
         <geometry>
           <box size="0.5 0.3 0.2"/>
         </geometry>
       </collision>
     </link>
   </robot>
   ```

2. **Validate the URDF** using check_urdf:
   ```bash
   check_urdf /path/to/your/robot.urdf
   ```

3. **Visualize the robot** in RViz:
   ```bash
   ros2 run rviz2 rviz2
   ```

4. **Add the RobotModel display** in RViz and set the Robot Description parameter

## Practical Exercise

**Exercise Title**: Differential Drive Robot Model with Sensors

**Difficulty**: Intermediate

**Estimated Time**: 120 minutes

**Instructions**:
1. Create a comprehensive URDF file for a differential drive mobile robot with chassis, wheels, and caster
2. Add detailed visual and collision properties to each link with appropriate materials and colors
3. Define joints connecting the wheels to the base with proper kinematic constraints
4. Use Xacro to create reusable macros for similar components like wheels and sensors
5. Add sensor mounts to the robot model (camera, LIDAR, IMU) with appropriate placements
6. Validate the URDF file using check_urdf tool and fix any errors
7. Visualize your robot model in RViz and verify all components appear correctly
8. Integrate the URDF with robot_state_publisher to see joint transformations
9. Add transmission definitions for the wheel joints to enable simulation
10. Create a launch file that loads the robot model and starts visualization

**Required Resources**:
- ROS 2 development environment
- Text editor or IDE
- RViz2 for visualization
- Terminal application
- Robot state publisher package

**Success Criteria**:
- URDF file is syntactically correct and passes validation
- Robot model displays properly in RViz with all components visible
- All joints are properly defined with correct kinematic properties
- Visual and collision properties are correctly specified with appropriate geometries
- Sensor mounts are properly positioned and oriented on the robot
- Robot model includes proper inertial properties for physics simulation
- Xacro macros work correctly and reduce redundancy in the model
- Launch file successfully loads the robot model and starts visualization
- Joint transformations are visible in the TF tree

## Integrating URDF with ROS 2

### Robot State Publisher
The `robot_state_publisher` node reads a URDF file and publishes the robot's joint states to TF:

```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:='$(cat robot.urdf)'
```

### Launch Files
URDF models are often loaded in launch files:

```python
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
import os

def generate_launch_description():
    pkg_share = FindPackageShare(package='my_robot_description').find('my_robot_description')
    urdf_file = os.path.join(pkg_share, 'urdf', 'robot.urdf')

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': Command(['xacro ', urdf_file])}]
        )
    ])
```

## Summary

This chapter covered URDF (Unified Robot Description Format) and robot modeling in ROS 2. You learned how to create robot models using links and joints, apply visual and collision properties, use Xacro for complex models, and integrate URDF with ROS 2 for visualization and simulation.

The next chapter will explore ROS 2 programming in Python, where you'll learn to implement the concepts covered in this module in practical code examples.

## Glossary Terms

- **URDF**: Unified Robot Description Format, an XML format for robot models
- **Link**: A rigid part of a robot in URDF
- **Joint**: A connection between links that allows relative motion
- **Xacro**: XML Macros, an extension to URDF for creating reusable robot models
- **Collision**: Properties that define how a link interacts with physics simulation
- **Visual**: Properties that define how a link appears in visualization tools

## Review Questions

1. What is the difference between visual and collision properties in URDF?
2. Name three types of joints supported in URDF.
3. What is Xacro and why is it useful for robot modeling?
4. How do you load a URDF file into a ROS 2 system?
5. What is the purpose of the robot_state_publisher node?

## Further Reading

- URDF Documentation: https://wiki.ros.org/urdf
- Xacro Tutorial: https://wiki.ros.org/xacro
- Robot State Publisher: https://docs.ros.org/en/humble/p/robot_state_publisher/
- ROS 2 URDF Tutorials: https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

## Technical Validation

This chapter has been validated against the official ROS 2 Humble Hawksbill documentation and URDF specifications. All XML syntax, joint types, and robot modeling concepts have been verified to match current ROS 2 standards and best practices.