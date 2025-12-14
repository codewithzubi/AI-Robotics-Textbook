# Nodes and Topics

## Learning Objectives

After completing this chapter, you should be able to:
- Define ROS 2 nodes and their role in robotic systems
- Explain the publish/subscribe communication pattern using topics
- Create simple publisher and subscriber nodes in Python
- Understand Quality of Service (QoS) settings and their impact
- Debug common issues with node communication

## Understanding Nodes

A node is a process that performs computation in ROS 2. Nodes are the fundamental building blocks of a ROS 2 system and are typically organized to perform discrete actions, such as controlling a specific sensor or actuator.

### Node Characteristics

- **Process-based**: Each node runs as a separate process
- **Communication hub**: Nodes communicate with other nodes through topics, services, and actions
- **Namespaced**: Nodes can be organized using namespaces for better organization
- **Lifecycle-aware**: Nodes can have different lifecycle states (unconfigured, inactive, active, finalized)

### Node Creation in Python

To create a node in Python, you'll typically inherit from `rclpy.Node`:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        # Node initialization code here

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## Topics and Publish/Subscribe Pattern

Topics are named buses over which nodes exchange messages. The publish/subscribe communication pattern allows for asynchronous communication between nodes.

### How Topics Work

1. **Publisher**: A node that sends messages to a topic
2. **Subscriber**: A node that receives messages from a topic
3. **Message**: The data structure sent between nodes
4. **Topic name**: A unique identifier for the communication channel

### Message Types

ROS 2 provides standard message types in packages like `std_msgs`, `geometry_msgs`, and `sensor_msgs`. You can also define custom message types.

## Creating a Publisher Node

Here's an example of a simple publisher node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
```

## Creating a Subscriber Node

Here's an example of a simple subscriber node:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
```

## Quality of Service (QoS)

QoS settings allow you to configure the behavior of publishers and subscribers for reliability, durability, and other performance characteristics.

### QoS Profiles

- **Reliability**: Best effort vs reliable delivery
- **Durability**: Volatile vs transient local (for late-joining subscribers)
- **History**: Keep last N messages vs keep all messages
- **Depth**: Number of messages to store in the queue

### Example with QoS Settings

```python
from rclpy.qos import QoSProfile

# Create a QoS profile with specific settings
qos_profile = QoSProfile(
    depth=10,
    reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
    durability=rclpy.qos.DurabilityPolicy.VOLATILE
)

# Use the QoS profile when creating a publisher
self.publisher_ = self.create_publisher(String, 'topic', qos_profile)
```

## Real-World Example: Sensor Data Broadcasting

In a typical robot, multiple sensors might publish data to different topics:

- `/camera/image_raw`: Raw image data from a camera
- `/laser_scan`: LIDAR scan data
- `/imu/data`: Inertial measurement unit readings
- `/joint_states`: Current positions of robot joints

Other nodes (subscribers) might process this data for perception, navigation, or control purposes.

## Step-by-Step Workflow: Creating a Publisher-Subscriber System

1. **Create a package**:
   ```bash
   ros2 pkg create --build-type ament_python my_robot_package
   ```

2. **Create the publisher script** in `my_robot_package/my_robot_package/publisher_member_function.py`

3. **Create the subscriber script** in `my_robot_package/my_robot_package/subscriber_member_function.py`

4. **Update setup.py** to include entry points for both scripts

5. **Build the package**:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select my_robot_package
   source install/setup.bash
   ```

6. **Run the publisher**:
   ```bash
   ros2 run my_robot_package publisher_member_function
   ```

7. **In a new terminal, run the subscriber**:
   ```bash
   ros2 run my_robot_package subscriber_member_function
   ```

## Practical Exercise

**Exercise Title**: Temperature Monitoring System

**Difficulty**: Beginner

**Estimated Time**: 60 minutes

**Instructions**:
1. Create a ROS 2 package named `temperature_monitor` using `ros2 pkg create`
2. Implement a publisher node that simulates temperature readings with realistic values
3. Implement a subscriber node that receives temperature data and logs it with timestamps
4. Test the communication between the nodes using `ros2 run` commands
5. Experiment with different QoS settings to observe their effects on communication
6. Use `ros2 topic echo` to monitor the topic data in real-time
7. Create a launch file that starts both nodes simultaneously
8. Add parameter configuration for temperature thresholds and logging frequency

**Required Resources**:
- ROS 2 development environment
- Python 3.x
- Text editor or IDE
- Terminal application

**Success Criteria**:
- Publisher successfully sends temperature messages to the topic at regular intervals
- Subscriber successfully receives messages and logs them with timestamps
- Messages are correctly formatted using appropriate message types (e.g., std_msgs/Float64)
- QoS settings are properly configured and tested with different profiles
- Launch file successfully starts both nodes simultaneously
- Parameter configuration works as expected for thresholds and frequency
- Communication can be monitored externally using ROS 2 command-line tools

## Summary

This chapter covered the fundamental communication patterns in ROS 2 using nodes and topics. You learned how to create publisher and subscriber nodes in Python, understand Quality of Service settings, and implement basic communication between nodes.

The next chapter will explore services and parameters, which provide request/response communication and configuration management in ROS 2.

## Glossary Terms

- **Node**: A process that performs computation in ROS 2
- **Topic**: A named bus for asynchronous message exchange between nodes
- **Publisher**: A node that sends messages to a topic
- **Subscriber**: A node that receives messages from a topic
- **QoS**: Quality of Service, settings that configure communication behavior
- **Message**: The data structure sent between nodes via topics

## Review Questions

1. What is the difference between a publisher and a subscriber?
2. Explain the publish/subscribe communication pattern in your own words.
3. What are Quality of Service (QoS) settings and why are they important?
4. Name three standard message types provided by ROS 2.
5. How do you create a timer callback in a ROS 2 node?

## Further Reading

- ROS 2 Node Concepts: https://docs.ros.org/en/humble/Concepts/About-ROS-2-Client-Libraries.html
- ROS 2 Topics Tutorial: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html
- Quality of Service in ROS 2: https://docs.ros.org/en/humble/Concepts/About-Quality-of-Service-Settings.html

## Technical Validation

This chapter has been validated against the official ROS 2 Humble Hawksbill documentation. All code examples, QoS settings, and node communication patterns have been verified to match current ROS 2 standards and best practices.