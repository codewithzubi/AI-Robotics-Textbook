---
title: "Consistent Terminology"
sidebar_position: 101
---

# Consistent Terminology Across All Modules

This document establishes consistent terminology to ensure clarity and reduce ambiguity throughout the Physical AI & Humanoid Robotics textbook. All modules should adhere to these definitions and naming conventions.

## Robot and System Terminology

### Robot Types
- **Humanoid Robot**: A robot with human-like form, typically bipedal with arms and a head
- **Mobile Robot**: A robot capable of locomotion in its environment
- **Manipulator**: A robot arm or similar device designed for manipulation tasks
- **Autonomous Robot**: A robot capable of performing tasks without human intervention
- **Semi-Autonomous Robot**: A robot that requires some level of human oversight or intervention

### Robot Components
- **End-Effector**: The tool or device at the end of a robot arm that interacts with the environment
- **Joint**: A connection between two robot links that allows relative motion
- **Link**: A rigid body component of a robot manipulator
- **Actuator**: A component that moves or controls a mechanism or system
- **Sensor**: A device that detects or measures a physical property and records, indicates, or otherwise responds to it
- **Controller**: A device or algorithm that manages and regulates the behavior of a system

## Software and Computing Terminology

### ROS 2 Specific
- **Node**: A process that performs computation in ROS 2
- **Topic**: An asynchronous message-passing mechanism for communication between ROS 2 nodes
- **Service**: A synchronous request/reply communication pattern in ROS 2
- **Action**: A communication pattern for long-running tasks with feedback in ROS 2
- **Parameter**: Configuration values that can be set and retrieved by ROS 2 nodes
- **Package**: A modular unit of ROS 2 software containing libraries, executables, and other resources
- **Launch File**: XML or Python files that specify which nodes to run and with what parameters
- **TF (Transforms)**: A system for tracking coordinate frame relationships over time

### AI and Machine Learning
- **Model**: A mathematical representation of a system, process, or relationship
- **Training**: The process of teaching a machine learning model using data
- **Inference**: The process of using a trained model to make predictions
- **Dataset**: A collection of data used for training or evaluating models
- **Feature**: An individual measurable property or characteristic of a phenomenon
- **Label**: The target variable in supervised learning
- **Algorithm**: A set of rules or procedures for solving a problem

### Vision and Perception
- **Image**: A 2D representation of visual information
- **Point Cloud**: A set of data points in 3D space, typically representing the external surface of an object
- **Depth Image**: An image where each pixel value represents the distance from the camera to the object
- **Segmentation**: The process of partitioning a digital image into multiple segments
- **Object Detection**: The computer technology related to identifying objects in images or videos
- **Pose Estimation**: Determining the position and orientation of an object

## Control and Navigation Terminology

### Control Systems
- **Open-Loop Control**: A control system without feedback
- **Closed-Loop Control**: A control system with feedback to correct errors
- **Feedforward Control**: Control based on anticipated disturbances or reference changes
- **PID Controller**: A control loop mechanism employing proportional, integral, and derivative terms
- **Setpoint**: The desired value of a controlled variable
- **Process Variable**: The actual value of the controlled variable
- **Error**: The difference between the setpoint and process variable

### Navigation
- **Localization**: Determining the robot's position and orientation in the environment
- **Mapping**: Creating a representation of the environment
- **SLAM (Simultaneous Localization and Mapping)**: The computational problem of constructing or updating a map of an unknown environment while simultaneously keeping track of an agent's location
- **Path Planning**: Finding a route from start to goal
- **Path Following**: Executing a planned path
- **Obstacle Avoidance**: Navigating around obstacles in the environment
- **Waypoint**: A reference point on a path
- **Goal**: The desired destination or target state

## Simulation and Digital Twin Terminology

### Simulation Concepts
- **Digital Twin**: A virtual replica of a physical system that enables real-time synchronization and bidirectional data flow
- **Simulation**: The imitation of the operation of a real-world process or system over time
- **Physics Engine**: Software that simulates physical systems
- **Collision Detection**: The computational problem of detecting when two or more bodies come into contact
- **Sensor Simulation**: The process of creating virtual sensors that generate realistic data
- **Real-time Simulation**: Simulation that runs at the same rate as real time
- **Fidelity**: The accuracy with which a simulation represents the real system

### Rendering and Visualization
- **Rendering**: The process of generating an image from a model
- **Ray Tracing**: A rendering technique that simulates the physical behavior of light
- **Polygon Count**: The number of polygons used to represent a 3D object
- **Texture**: A bitmap image applied to the surface of a shape
- **Lighting**: The simulation of light behavior in a virtual environment

## AI and Language Processing Terminology

### Language Processing
- **Natural Language Processing (NLP)**: The ability of a computer program to understand human language as it is spoken
- **Tokenization**: The process of converting text into smaller units called tokens
- **Embedding**: A representation of words or phrases as vectors of numbers
- **Context Window**: The maximum amount of text an LLM can process at once
- **Prompt**: Input provided to a language model to generate a response
- **Generation**: The process of creating new text based on input and training

### Vision-Language Integration
- **Multimodal**: Processing and integrating information from multiple sensory modalities
- **Cross-Modal**: Relating to or integrating different sensory modalities
- **Alignment**: The correspondence between different modalities
- **Fusion**: The process of combining information from multiple modalities
- **Attention**: A mechanism that allows models to focus on relevant information

## Humanoid-Specific Terminology

### Humanoid Control
- **Center of Mass (CoM)**: The point where the robot's mass is concentrated for balance control
- **Zero Moment Point (ZMP)**: Point where the moment of the ground reaction force is zero
- **Support Polygon**: Area defined by the points of contact between the robot and ground
- **Gait**: The pattern of limb movements during locomotion
- **Stride**: A complete gait cycle from initial contact of one foot to the next contact of the same foot
- **Step**: The period from initial contact of one foot to initial contact of the other foot
- **Double Support Phase**: When both feet are on the ground during walking
- **Single Support Phase**: When only one foot is on the ground during walking

### Balance and Stability
- **Stability**: The ability to maintain balance and resist falling
- **Equilibrium**: A state of balance where all forces and moments are balanced
- **Posture**: The position of the body or a body part
- **Stance**: The position of the feet and legs relative to the body
- **Swing Phase**: The phase of gait when the foot is off the ground
- **Stance Phase**: The phase of gait when the foot is in contact with the ground

## Consistency Guidelines

### Naming Conventions
- Use consistent abbreviations: ROS 2 (not ROS2 or ros2)
- Use consistent capitalization: NVIDIA Isaac (not nvidia isaac or Nvidia Isaac)
- Use consistent terminology: "humanoid robot" (not "humanoid" or "human-like robot" when referring to the same concept)

### Technical Accuracy
- Use precise technical terms rather than colloquialisms
- Define terms when first introduced in each module
- Link to the glossary overview when introducing new terms
- Maintain consistency with official documentation for tools and frameworks

### Writing Style
- Use active voice when describing robot actions
- Be specific about coordinate frames and reference systems
- Include units of measurement when specifying physical quantities
- Use consistent terminology for similar concepts across modules