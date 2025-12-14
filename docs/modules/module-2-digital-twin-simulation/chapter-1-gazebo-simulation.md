# Gazebo Simulation

## Learning Objectives

After completing this chapter, you should be able to:
- Explain the fundamental concepts and architecture of Gazebo simulation
- Set up a basic Gazebo simulation environment
- Create and configure simple worlds and models in Gazebo
- Understand the physics engine and its parameters
- Implement basic robot simulation with sensors
- Control and interact with the simulation environment

## Introduction to Gazebo

Gazebo is a powerful robotics simulation environment that provides high-fidelity physics simulation and realistic rendering. It is widely used in robotics research and development to test algorithms and robot designs in a virtual environment before deployment on real robots.

### Key Features of Gazebo

- **High-Fidelity Physics**: Accurate simulation of rigid body dynamics, collisions, and contacts
- **Realistic Rendering**: High-quality graphics rendering with support for lighting and shadows
- **Sensor Simulation**: Support for various sensor types including cameras, LIDAR, IMU, and GPS
- **Plugin Architecture**: Extensible through plugins for custom behaviors and interfaces
- **ROS Integration**: Seamless integration with ROS and ROS 2 for robotics development

### Gazebo Architecture

Gazebo consists of several core components:

1. **Physics Engine**: Handles collision detection and dynamics simulation
2. **Rendering Engine**: Manages the visual representation of the world
3. **Server**: Runs the simulation and handles communications
4. **Client**: Provides the user interface for visualization and interaction
5. **Transport Layer**: Enables communication between components

## Setting Up Gazebo

### Installation

Gazebo can be installed in various ways depending on your system. For robotics development, it's often installed as part of a ROS distribution:

```bash
# For ROS 2 Humble Hawksbill on Ubuntu 22.04
sudo apt update
sudo apt install ros-humble-gazebo-*
```

### Basic Gazebo Commands

```bash
# Launch Gazebo with an empty world
gazebo

# Launch Gazebo with a specific world file
gazebo my_world.world

# Launch Gazebo in headless mode (no GUI)
gz sim -s -r my_world.sdf
```

## Creating Worlds in Gazebo

A world file in Gazebo defines the environment, including models, lighting, and physics properties. World files are typically written in SDF (Simulation Description Format).

### Basic World Structure

```xml
<?xml version="1.0"?>
<sdf version="1.7">
  <world name="my_world">
    <!-- Include models -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Define physics engine -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <!-- Define models -->
    <model name="my_robot">
      <!-- Model definition goes here -->
    </model>
  </world>
</sdf>
```

### World Properties

- **Gravity**: Defines the gravitational acceleration (default: 0, 0, -9.8)
- **Physics Engine**: Configures the physics simulation parameters
- **Lighting**: Sets up sun and other light sources
- **Models**: Includes predefined models or custom robot models

## Model Definition in Gazebo

Models in Gazebo are described using SDF and can include:

- **Links**: Rigid bodies with visual and collision properties
- **Joints**: Connections between links allowing relative motion
- **Sensors**: Virtual sensors attached to links
- **Plugins**: Custom behaviors and control logic

### Example Model Structure

```xml
<sdf version="1.7">
  <model name="simple_robot">
    <!-- Base link -->
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.01</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.01</iyy>
          <iyz>0.0</iyz>
          <izz>0.01</izz>
        </inertia>
      </inertial>

      <visual name="chassis_visual">
        <geometry>
          <box>
            <size>0.5 0.3 0.2</size>
          </box>
        </geometry>
        <material>
          <ambient>0.8 0.8 0.8 1</ambient>
          <diffuse>0.8 0.8 0.8 1</diffuse>
        </material>
      </visual>

      <collision name="chassis_collision">
        <geometry>
          <box>
            <size>0.5 0.3 0.2</size>
          </box>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
```

## Physics Simulation

Gazebo provides realistic physics simulation through various physics engines:

### ODE (Open Dynamics Engine)
- Most commonly used in Gazebo
- Good balance of speed and accuracy
- Supports rigid body dynamics

### Bullet
- Used in some robotics applications
- Good for complex collision detection
- Stable for complex interactions

### Simbody
- Suitable for biomechanics applications
- Advanced constraint solving

### Physics Parameters

Important physics parameters to tune for realistic simulation:

- **Max Step Size**: Time step for the physics solver (typically 0.001s)
- **Real Time Factor**: Ratio of simulation time to real time (1.0 = real-time)
- **Update Rate**: How frequently the physics engine updates (Hz)

## Sensor Simulation

Gazebo includes realistic simulation of various sensor types:

### Camera Sensors
- RGB cameras for visual perception
- Depth cameras for 3D reconstruction
- Wide-angle and narrow-angle configurations

### Range Sensors (LIDAR)
- 2D and 3D LIDAR simulation
- Adjustable resolution and range
- Noise modeling for realistic data

### IMU Sensors
- Accelerometer and gyroscope simulation
- Bias and noise modeling
- Gravity compensation

### GPS Sensors
- Position and velocity estimation
- Atmospheric modeling
- Multipath and signal noise

## Real-World Example: TurtleBot3 Simulation

One of the most common examples in robotics education is the TurtleBot3 simulation in Gazebo. The TurtleBot3 simulation demonstrates:

- Complete robot model with URDF/SDF conversion
- Sensor integration (camera, LIDAR, IMU)
- Control interfaces through ROS
- Navigation and mapping in simulation

## Step-by-Step Workflow: Creating a Simple Robot Simulation

1. **Create a model directory**:
   ```bash
   mkdir -p ~/.gazebo/models/simple_robot
   ```

2. **Create the model.config file**:
   ```xml
   <?xml version="1.0"?>
   <model>
     <name>simple_robot</name>
     <version>1.0</version>
     <sdf version="1.7">model.sdf</sdf>
     <author>
       <name>Your Name</name>
       <email>your.email@example.com</email>
     </author>
     <description>A simple robot model for simulation.</description>
   </model>
   ```

3. **Create the model.sdf file** with the SDF structure shown above

4. **Create a world file** that includes your robot model

5. **Launch the simulation**:
   ```bash
   gazebo my_world.world
   ```

6. **Interact with the simulation** using ROS topics and services

## Practical Exercise

**Exercise Title**: Basic Gazebo Robot Simulation

**Difficulty**: Intermediate

**Estimated Time**: 90 minutes

**Instructions**:
1. Create a simple wheeled robot model with 2 links (chassis and wheel) and 1 joint
2. Define visual and collision properties for each link
3. Create a world file that includes your robot and a ground plane
4. Add a camera sensor to the robot to simulate visual perception
5. Launch the simulation and verify that the robot appears correctly
6. Test the physics by observing how the robot interacts with the environment
7. Document the SDF files and explain the key components

**Required Resources**:
- Computer with Gazebo installed
- Text editor for creating SDF files
- Basic understanding of 3D coordinate systems

**Success Criteria**:
- Robot model loads correctly in Gazebo
- Physics simulation behaves realistically
- Camera sensor produces visual output
- SDF files are properly structured and documented
- Simulation runs without errors

## Summary

This chapter introduced you to Gazebo simulation, the powerful robotics simulation environment. You learned about the architecture, world creation, model definition, physics simulation, and sensor integration in Gazebo. You also practiced creating a simple robot simulation from scratch.

The next chapter will explore Unity-based robotics simulation, providing an alternative approach to digital twin creation.

## Glossary Terms

- **SDF**: Simulation Description Format, the XML-based format used by Gazebo to describe worlds and models
- **Gazebo**: A robotics simulation environment that provides high-fidelity physics simulation and realistic rendering
- **Physics Engine**: The component responsible for simulating rigid body dynamics, collisions, and contacts
- **Sensor Simulation**: The process of modeling virtual sensors to generate realistic data for robotics algorithms
- **Digital Twin**: A digital replica of a physical system used for simulation, testing, and optimization

## Review Questions

1. What are the main components of the Gazebo architecture?
2. Explain the difference between visual and collision properties in a Gazebo model.
3. What are the key physics parameters that affect simulation accuracy?
4. List three types of sensors that can be simulated in Gazebo.
5. How does Gazebo integrate with ROS for robotics development?

## Further Reading

- Gazebo Harmonic Documentation: http://gazebosim.org/docs/harmonic
- SDF Specification: http://sdformat.org/spec
- ROS 2 Gazebo Integration: https://github.com/ros-simulation/gazebo_ros_pkgs