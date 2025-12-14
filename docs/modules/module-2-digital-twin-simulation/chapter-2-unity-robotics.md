# Unity Robotics

## Learning Objectives

After completing this chapter, you should be able to:
- Understand the Unity robotics ecosystem and its components
- Set up Unity for robotics development and simulation
- Import and configure robot models in Unity
- Implement sensor simulation using Unity robotics packages
- Create realistic environments for robot testing
- Connect Unity to ROS/ROS 2 using the ROS-TCP-Connector
- Design effective simulation workflows for robotics applications

## Introduction to Unity for Robotics

Unity has emerged as a powerful platform for robotics simulation and development, offering photorealistic rendering, intuitive development tools, and a rich ecosystem of robotics packages. Unity's real-time physics engine and advanced rendering capabilities make it ideal for creating high-fidelity digital twins of robotic systems.

### Unity Robotics Ecosystem

The Unity robotics ecosystem includes several key components:

- **Unity Editor**: The main development environment for creating scenes and simulations
- **Unity Physics**: Real-time physics simulation with configurable parameters
- **Unity ML-Agents**: Machine learning framework for training robotic behaviors
- **ROS-TCP-Connector**: Bridge for connecting Unity to ROS/ROS 2 networks
- **Unity Robotics Package**: Specialized tools for robotics development
- **HabilitatXR**: VR/AR support for immersive robot teleoperation

### Advantages of Unity for Robotics

- **Photorealistic Graphics**: High-quality rendering for realistic perception training
- **Intuitive Interface**: Visual scene construction and object manipulation
- **Flexible Physics**: Configurable physics parameters for different scenarios
- **Extensive Asset Store**: Pre-built models, environments, and tools
- **Cross-Platform Support**: Deploy to various platforms including VR/AR
- **Active Community**: Large developer community and extensive documentation

## Setting Up Unity for Robotics

### Installing Unity Hub and Unity Editor

Unity provides different versions optimized for robotics applications. For robotics simulation, it's recommended to use a stable LTS (Long Term Support) version.

1. Download Unity Hub from the Unity website
2. Install the latest LTS version of Unity
3. Install additional components like Visual Studio integration
4. Create a new 3D project for robotics applications

### Installing Robotics Packages

Unity provides several robotics-specific packages that enhance the simulation capabilities:

#### Unity Robotics Package
- Provides robotics-specific components and utilities
- Includes tools for sensor simulation and robot control
- Offers integration with ROS/ROS 2

#### Unity ML-Agents
- Framework for training intelligent agents using reinforcement learning
- Can be used for robot behavior learning and optimization
- Integrates with TensorFlow for neural network training

#### ROS-TCP-Connector
- Enables communication between Unity and ROS/ROS 2
- Supports bidirectional data transfer
- Provides ROS message serialization/deserialization

### Installation Process

```bash
# In Unity Package Manager (Window > Package Manager)
# Install these packages:
- Unity Robotics Package
- Unity ML-Agents (if using machine learning)
- ProBuilder (for quick environment creation)
- XR packages if using VR/AR
```

## Robot Model Integration

### URDF Importer

Unity provides a URDF Importer that allows importing robot models defined in URDF format directly into Unity:

```csharp
// Example: Loading a robot from URDF
using Unity.Robotics.URDFImport;

public class RobotLoader : MonoBehaviour
{
    public void LoadRobotFromURDF(string urdfPath)
    {
        var robot = URDFLoader.LoadFromPath(urdfPath);
        robot.transform.SetParent(this.transform);
    }
}
```

### Manual Model Setup

For more control, you can manually create robot models in Unity:

1. **Import 3D Models**: Import robot parts as 3D models (FBX, OBJ, STL formats)
2. **Set Physics Properties**: Configure colliders and rigidbodies for each part
3. **Define Joints**: Create Unity joints to connect robot parts
4. **Configure Materials**: Apply appropriate materials for visual appearance

### Joint Configuration

Unity supports various joint types that correspond to ROS joint types:

- **Fixed Joint**: Rigid connection (ROS fixed joint)
- **Revolute Joint**: Rotational joint with limits (ROS revolute joint)
- **Prismatic Joint**: Linear sliding motion (ROS prismatic joint)
- **Spherical Joint**: Ball joint with 3DOF rotation
- **Continous Joint**: Unlimited rotational motion (ROS continuous joint)

## Sensor Simulation in Unity

Unity provides realistic sensor simulation capabilities through its robotics packages:

### Camera Sensors

Unity's camera components can simulate various types of visual sensors:

```csharp
using UnityEngine;

public class CameraSensor : MonoBehaviour
{
    public Camera mainCamera;
    public RenderTexture sensorTexture;

    void Start()
    {
        // Configure camera for sensor simulation
        mainCamera.depthTextureMode = DepthTextureMode.Depth;
        mainCamera.allowHDR = true;

        // Set up render texture for sensor output
        sensorTexture = new RenderTexture(640, 480, 24);
        mainCamera.targetTexture = sensorTexture;
    }

    void Update()
    {
        // Process sensor data
        ProcessImage(sensorTexture);
    }

    void ProcessImage(RenderTexture texture)
    {
        // Convert to sensor format and send via ROS if connected
    }
}
```

### LIDAR Simulation

Unity can simulate LIDAR sensors using raycasting:

```csharp
using System.Collections.Generic;
using UnityEngine;

public class LidarSensor : MonoBehaviour
{
    public int numberOfRays = 360;
    public float maxDistance = 10.0f;
    public float angleRange = 360.0f;

    public List<float> GetLidarData()
    {
        List<float> distances = new List<float>();

        for (int i = 0; i < numberOfRays; i++)
        {
            float angle = (i * angleRange / numberOfRays) * Mathf.Deg2Rad;
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));

            if (Physics.Raycast(transform.position, direction, out RaycastHit hit, maxDistance))
            {
                distances.Add(hit.distance);
            }
            else
            {
                distances.Add(maxDistance);
            }
        }

        return distances;
    }
}
```

### IMU Simulation

Unity can simulate IMU sensors by accessing transform changes:

```csharp
using UnityEngine;

public class IMUSensor : MonoBehaviour
{
    private Vector3 lastPosition;
    private Quaternion lastRotation;
    private float lastTime;

    void Start()
    {
        lastPosition = transform.position;
        lastRotation = transform.rotation;
        lastTime = Time.time;
    }

    void Update()
    {
        float deltaTime = Time.time - lastTime;

        if (deltaTime > 0)
        {
            // Calculate linear acceleration
            Vector3 velocity = (transform.position - lastPosition) / deltaTime;
            Vector3 acceleration = (velocity - GetPreviousVelocity()) / deltaTime;

            // Calculate angular velocity
            Quaternion deltaRotation = transform.rotation * Quaternion.Inverse(lastRotation);
            Vector3 angularVelocity = GetAngularVelocity(deltaRotation, deltaTime);

            // Send IMU data via ROS connection
            SendIMUData(acceleration, angularVelocity, transform.rotation.eulerAngles);
        }

        lastPosition = transform.position;
        lastRotation = transform.rotation;
        lastTime = Time.time;
    }

    private Vector3 GetAngularVelocity(Quaternion deltaRotation, float deltaTime)
    {
        Vector3 axis;
        float angle;
        deltaRotation.ToAngleAxis(out angle, out axis);

        if (deltaTime > 0)
            return axis * angle / deltaTime;
        else
            return Vector3.zero;
    }

    private Vector3 GetPreviousVelocity()
    {
        // Implementation for getting previous velocity
        return Vector3.zero;
    }

    private void SendIMUData(Vector3 linearAccel, Vector3 angularVel, Vector3 orientation)
    {
        // Send data via ROS connection
    }
}
```

## Environment Creation

### Scene Design Principles

Creating effective robot simulation environments in Unity involves:

1. **Realistic Physics**: Accurate mass, friction, and collision properties
2. **Proper Scaling**: Consistent units (preferably meters) throughout
3. **Lighting**: Appropriate lighting for perception tasks
4. **Terrain**: Realistic terrain and surfaces for locomotion testing
5. **Obstacles**: Varied obstacles for navigation and manipulation testing

### ProBuilder for Environment Creation

Unity's ProBuilder package allows for rapid environment prototyping:

```csharp
using UnityEngine;
using UnityEditor.ProBuilder;

// Create procedural environments
public class ProceduralEnvironment : MonoBehaviour
{
    public GameObject GenerateRoom(float width, float length, float height)
    {
        // Create walls, floor, ceiling using ProBuilder
        var room = pbObject.CreatePrimitive(PrimitiveType.Cube);
        room.transform.localScale = new Vector3(width, height, length);

        // Add doors, windows, furniture as needed
        return room.gameObject;
    }
}
```

## ROS/ROS 2 Integration

### ROS-TCP-Connector

The ROS-TCP-Connector enables communication between Unity and ROS/ROS 2:

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class UnityRosBridge : MonoBehaviour
{
    ROSConnection ros;
    public string rosIPAddress = "127.0.0.1";
    public int rosPort = 10000;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Initialize(rosIPAddress, rosPort);
    }

    void SendCameraData(RenderTexture texture)
    {
        // Convert texture to ROS image message
        ImageMsg imageMsg = new ImageMsg();
        // Fill image message with data from texture
        ros.Send("camera/image_raw", imageMsg);
    }

    void SendLidarData(List<float> ranges)
    {
        LaserScanMsg lidarMsg = new LaserScanMsg();
        lidarMsg.ranges = ranges.ToArray();
        ros.Send("scan", lidarMsg);
    }
}
```

### Message Types

Unity supports common ROS message types:

- **sensor_msgs/Image**: Camera images
- **sensor_msgs/LaserScan**: LIDAR data
- **sensor_msgs/Imu**: IMU data
- **geometry_msgs/Twist**: Robot velocities
- **nav_msgs/Odometry**: Robot odometry
- **std_msgs/Float32**: Scalar values

## Real-World Example: Warehouse Robot Simulation

A common robotics application is warehouse automation. In Unity, you can create a warehouse simulation with:

- **Robot Model**: Mobile robot with navigation capabilities
- **Environment**: Warehouse layout with shelves, aisles, and obstacles
- **Objects**: Packages to be moved, conveyor belts, charging stations
- **Sensors**: Cameras for object detection, LIDAR for navigation
- **Controls**: ROS-based navigation stack integration

## Step-by-Step Workflow: Creating a Unity Robot Simulation

1. **Install Unity Hub and Robotics Packages**:
   - Download and install Unity Hub
   - Install Unity LTS version
   - Add robotics packages via Package Manager

2. **Create a New 3D Project**:
   - Select 3D Core template
   - Configure project settings for robotics

3. **Import Robot Model**:
   - Use URDF Importer or import manually
   - Configure physics properties
   - Set up joints and articulation

4. **Add Sensors**:
   - Attach camera components for visual sensors
   - Implement LIDAR simulation using raycasting
   - Configure IMU simulation

5. **Create Environment**:
   - Design realistic environment
   - Add obstacles and interactive objects
   - Configure lighting and materials

6. **Connect to ROS**:
   - Install ROS-TCP-Connector
   - Configure IP and port settings
   - Implement message publishing/subscribing

7. **Test and Validate**:
   - Run simulation and verify sensor data
   - Test robot control through ROS
   - Validate physics behavior

## Practical Exercise

**Exercise Title**: Unity Robot Navigation Simulation

**Difficulty**: Advanced

**Estimated Time**: 120 minutes

**Instructions**:
1. Create a Unity project specifically for robotics simulation
2. Import a simple robot model (or create a basic differential drive robot)
3. Set up a simple environment with walls and obstacles
4. Add a camera sensor to the robot for visual perception
5. Implement a LIDAR simulation using raycasting
6. Connect the Unity simulation to ROS using ROS-TCP-Connector
7. Test the simulation by sending navigation commands from ROS
8. Document the setup process and any challenges encountered

**Required Resources**:
- Computer with Unity Hub and Editor installed
- Unity Robotics Package and ROS-TCP-Connector
- ROS 2 environment with navigation stack
- Basic knowledge of Unity development

**Success Criteria**:
- Robot model appears correctly in Unity scene
- Camera and LIDAR sensors produce realistic data
- ROS connection is established successfully
- Robot can be controlled via ROS topics
- Simulation runs with realistic physics
- Documentation is clear and comprehensive

## Summary

This chapter covered Unity robotics simulation, including the Unity robotics ecosystem, robot model integration, sensor simulation, environment creation, and ROS integration. You learned how to set up Unity for robotics applications, create realistic simulations, and connect Unity to ROS for robotics development.

The next chapter will explore sensor simulation techniques in more detail, covering how to create realistic sensor data for robotics algorithms.

## Glossary Terms

- **URDF Importer**: A Unity package that allows importing robot models defined in URDF format
- **ROS-TCP-Connector**: A Unity package that enables communication between Unity and ROS/ROS 2 networks
- **Unity Robotics Package**: A collection of tools and components for robotics development in Unity
- **Raycasting**: A technique used in Unity to simulate LIDAR sensors by casting rays and detecting collisions
- **ProBuilder**: Unity's built-in tool for creating 3D geometry directly in the editor
- **Digital Twin**: A digital replica of a physical system used for simulation, testing, and optimization

## Review Questions

1. What are the key components of the Unity robotics ecosystem?
2. Explain the process of importing a URDF robot model into Unity.
3. How can you simulate a LIDAR sensor using Unity's physics system?
4. What is the purpose of the ROS-TCP-Connector package?
5. List three advantages of using Unity over other simulation environments for robotics.

## Further Reading

- Unity Robotics Hub: https://unity.com/products/unity-robotics
- ROS-TCP-Connector Documentation: https://github.com/Unity-Technologies/ROS-TCP-Connector
- Unity ML-Agents Toolkit: https://github.com/Unity-Technologies/ml-agents
- Unity URDF Importer: https://github.com/Unity-Technologies/URDF-Importer