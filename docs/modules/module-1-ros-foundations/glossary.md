# Glossary of ROS 2 Concepts

This glossary contains key terms used in the ROS 2 Foundations module, with definitions specific to the context of ROS 2 development.

## A

### Action
A goal-based communication pattern in ROS 2 that allows for long-running tasks with feedback and status updates. Actions extend the basic request/response pattern of services by adding support for ongoing feedback during execution and the ability to cancel goals.

### Ament
The build system used by ROS 2, which replaces the catkin build system from ROS 1. Ament provides better support for modern CMake practices and improved dependency management.

## C

### Client Library
A software library that provides the APIs needed to create ROS 2 nodes in a particular programming language (e.g., rclpy for Python, rclcpp for C++).

### Communication Primitive
The fundamental ways nodes can exchange information in ROS 2: topics (publish/subscribe), services (request/response), and actions (goal-based with feedback).

## D

### DDS (Data Distribution Service)
The middleware that ROS 2 uses for communication between nodes. DDS provides a standardized way for applications to communicate in a distributed system, offering features like Quality of Service (QoS) policies.

## J

### Joint
In URDF, a connection between two links that allows relative motion. Joints define the kinematic and dynamic properties of how robot parts move relative to each other.

## L

### Link
In URDF, a rigid part of a robot model. Links define the geometry, collision properties, and inertial properties of robot components.

### Lifecycle Node
A node that follows a well-defined state machine with states like unconfigured, inactive, active, and finalized, allowing for better resource management and system control.

## M

### Message
The data structure used in ROS 2 for communication between nodes. Messages are defined in .msg files and are used with topics and services.

## N

### Node
A process that performs computation in ROS 2. Nodes are the fundamental building blocks of a ROS 2 system and communicate with other nodes through topics, services, and actions.

## P

### Parameter
A configuration value that can be set for a ROS 2 node at runtime. Parameters provide a way to configure node behavior without recompiling code.

### Publisher
A component of a node that sends messages to a topic. Publishers implement the "publish" side of the publish/subscribe communication pattern.

## Q

### QoS (Quality of Service)
Settings that define the behavior of communication between ROS 2 nodes, including reliability, durability, history, and liveliness policies.

## R

### ROS 2 (Robot Operating System 2)
The second generation of the Robot Operating System, designed to be suitable for real-world applications with improved security, real-time support, and better architecture for distributed systems.

### rclpy
The Python client library for ROS 2, providing the APIs needed to create ROS 2 nodes and use ROS 2 concepts in Python.

### Robot State Publisher
A ROS 2 node that reads a robot description (URDF) and joint positions, then publishes the 3D poses of the robot's links to the TF system.

## S

### Service
A synchronous communication pattern in ROS 2 where a client sends a request to a server and waits for a response. Services use a request/response model.

### Subscriber
A component of a node that receives messages from a topic. Subscribers implement the "subscribe" side of the publish/subscribe communication pattern.

## T

### Topic
A named bus over which nodes exchange messages in ROS 2. Topics implement an asynchronous publish/subscribe communication pattern.

## U

### URDF (Unified Robot Description Format)
An XML format used in ROS to describe robot models, defining the physical and kinematic properties of a robot including its structure, joints, and other elements.

## X

### Xacro (XML Macros)
An XML macro language that extends URDF, allowing for more complex and reusable robot descriptions through features like macros, constants, and mathematical expressions.