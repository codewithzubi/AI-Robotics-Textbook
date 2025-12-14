---
title: "Capstone Implementation Guide"
sidebar_position: 2
---

# Capstone Implementation Guide: Autonomous Humanoid Robotics System

## Implementation Overview

This guide provides detailed instructions for implementing the integrated autonomous humanoid robotics system. The implementation follows an iterative, test-driven approach that builds upon the foundational concepts from all four textbook modules while ensuring proper integration between components.

## Prerequisites and Setup

### System Requirements
- **Operating System**: Ubuntu 22.04 LTS with real-time kernel (recommended)
- **GPU**: NVIDIA GPU with CUDA compute capability 6.0+ (RTX 3080 or better recommended)
- **RAM**: 32GB minimum, 64GB recommended
- **Storage**: 500GB SSD minimum for models and datasets
- **Network**: Reliable network connection for package management and API access

### Software Dependencies

#### ROS 2 Environment
```bash
# Install ROS 2 Humble Hawksbill
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential

# Initialize rosdep
sudo rosdep init
rosdep update

# Source ROS 2
source /opt/ros/humble/setup.bash
```

#### Python Environment
```bash
# Create virtual environment
python3 -m venv capstone_env
source capstone_env/bin/activate
pip install --upgrade pip

# Install Python dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers openai-whisper
pip install numpy scipy matplotlib
pip install opencv-python
pip install pyquaternion
```

#### Isaac ROS Components
```bash
# Install Isaac ROS common components
sudo apt install ros-humble-isaac-ros-common
sudo apt install ros-humble-isaac-ros-apriltag
sudo apt install ros-humble-isaac-ros-visual-slam
sudo apt install ros-humble-isaac-ros-detection2d
```

## Project Structure

Create the following directory structure for the capstone project:

```
capstone_project/
├── src/
│   ├── vla_integration/
│   │   ├── vla_perception/
│   │   ├── vla_planning/
│   │   └── vla_control/
│   ├── humanoid_control/
│   │   ├── balance_control/
│   │   ├── walking_pattern/
│   │   └── manipulation/
│   ├── simulation_bridge/
│   │   ├── gazebo_bridge/
│   │   └── unity_bridge/
│   └── system_integration/
│       ├── message_types/
│       ├── state_manager/
│       └── coordinator/
├── config/
├── launch/
├── test/
└── docs/
```

## Implementation Phase 1: System Architecture and Integration Framework

### 1.1 Create the System Coordinator Node

Create `src/system_integration/coordinator/capstone_coordinator.py`:

```python
#!/usr/bin/env python3
"""
Capstone Project System Coordinator
Manages communication between all system modules
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped, Twist
from capstone_msgs.msg import SystemStatus, Command, ExecutionResult

class CapstoneCoordinator(Node):
    def __init__(self):
        super().__init__('capstone_coordinator')

        # Publishers for system status
        self.status_pub = self.create_publisher(SystemStatus, '/capstone/system_status', 10)
        self.command_pub = self.create_publisher(Command, '/capstone/commands', 10)

        # Subscribers for system feedback
        self.vision_feedback_sub = self.create_subscription(
            String, '/vla/vision_feedback', self.vision_feedback_callback, 10
        )
        self.navigation_feedback_sub = self.create_subscription(
            String, '/navigation/feedback', self.navigation_feedback_callback, 10
        )
        self.manipulation_feedback_sub = self.create_subscription(
            String, '/manipulation/feedback', self.manipulation_feedback_callback, 10
        )
        self.balance_feedback_sub = self.create_subscription(
            String, '/balance/feedback', self.balance_feedback_callback, 10
        )

        # System state
        self.system_state = {
            'vision_ready': False,
            'navigation_ready': False,
            'manipulation_ready': False,
            'balance_stable': True,
            'language_processing': False,
            'current_task': None,
            'task_queue': []
        }

        # Timer for status updates
        self.status_timer = self.create_timer(1.0, self.publish_system_status)

        self.get_logger().info('Capstone Coordinator initialized')

    def vision_feedback_callback(self, msg):
        """Handle vision system feedback"""
        if 'ready' in msg.data.lower():
            self.system_state['vision_ready'] = True
        elif 'error' in msg.data.lower():
            self.system_state['vision_ready'] = False

    def navigation_feedback_callback(self, msg):
        """Handle navigation system feedback"""
        if 'ready' in msg.data.lower():
            self.system_state['navigation_ready'] = True
        elif 'error' in msg.data.lower():
            self.system_state['navigation_ready'] = False

    def manipulation_feedback_callback(self, msg):
        """Handle manipulation system feedback"""
        if 'ready' in msg.data.lower():
            self.system_state['manipulation_ready'] = True
        elif 'error' in msg.data.lower():
            self.system_state['manipulation_ready'] = False

    def balance_feedback_callback(self, msg):
        """Handle balance system feedback"""
        if 'stable' in msg.data.lower():
            self.system_state['balance_stable'] = True
        elif 'unstable' in msg.data.lower():
            self.system_state['balance_stable'] = False

    def publish_system_status(self):
        """Publish system status at regular intervals"""
        status_msg = SystemStatus()
        status_msg.timestamp = self.get_clock().now().to_msg()
        status_msg.vision_ready = self.system_state['vision_ready']
        status_msg.navigation_ready = self.system_state['navigation_ready']
        status_msg.manipulation_ready = self.system_state['manipulation_ready']
        status_msg.balance_stable = self.system_state['balance_stable']
        status_msg.language_processing = self.system_state['language_processing']
        status_msg.current_task = self.system_state['current_task'] if self.system_state['current_task'] else ""

        self.status_pub.publish(status_msg)

    def process_command(self, command_msg):
        """Process high-level commands"""
        if not self.system_ready():
            self.get_logger().warn('System not ready, queuing command')
            self.system_state['task_queue'].append(command_msg)
            return False

        self.system_state['language_processing'] = True
        self.system_state['current_task'] = command_msg.command

        # Route command to appropriate subsystem
        if any(keyword in command_msg.command.lower() for keyword in ['go to', 'navigate', 'move to']):
            # Send to navigation system
            nav_cmd = Command()
            nav_cmd.command = command_msg.command
            nav_cmd.target_system = 'navigation'
            self.command_pub.publish(nav_cmd)
        elif any(keyword in command_msg.command.lower() for keyword in ['pick', 'grasp', 'place', 'take']):
            # Send to manipulation system
            manip_cmd = Command()
            manip_cmd.command = command_msg.command
            manip_cmd.target_system = 'manipulation'
            self.command_pub.publish(manip_cmd)
        else:
            # Send to VLA system for processing
            vla_cmd = Command()
            vla_cmd.command = command_msg.command
            vla_cmd.target_system = 'vla'
            self.command_pub.publish(vla_cmd)

        return True

    def system_ready(self):
        """Check if system is ready to accept commands"""
        return (self.system_state['vision_ready'] and
                self.system_state['navigation_ready'] and
                self.system_state['manipulation_ready'] and
                self.system_state['balance_stable'])

def main(args=None):
    rclpy.init(args=args)

    coordinator = CapstoneCoordinator()

    try:
        rclpy.spin(coordinator)
    except KeyboardInterrupt:
        pass
    finally:
        coordinator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 1.2 Create Custom Message Types

Create `src/system_integration/message_types/CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.8)
project(capstone_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)

set(msg_files
  "msg/SystemStatus.msg"
  "msg/Command.msg"
  "msg/ExecutionResult.msg"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES std_msgs geometry_msgs builtin_interfaces
  ADD_LINTER_TESTS
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
```

Create `src/system_integration/message_types/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>capstone_msgs</name>
  <version>0.0.0</version>
  <description>Custom messages for capstone project</description>
  <maintainer email="student@university.edu">Student</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>builtin_interfaces</depend>

  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

Create message files in `src/system_integration/message_types/msg/`:

**SystemStatus.msg**:
```
builtin_interfaces/Time timestamp
bool vision_ready
bool navigation_ready
bool manipulation_ready
bool balance_stable
bool language_processing
string current_task
```

**Command.msg**:
```
builtin_interfaces/Time timestamp
string command
string target_system
string priority  # low, medium, high, emergency
```

**ExecutionResult.msg**:
```
builtin_interfaces/Time timestamp
string command_executed
bool success
string error_message
float64 execution_time
string result_details
```

### 1.3 Build the Message Package

```bash
cd capstone_project/src/system_integration/message_types
colcon build --packages-select capstone_msgs
source install/setup.bash
```

## Implementation Phase 2: VLA Integration Layer

### 2.1 Create VLA Perception Node

Create `src/vla_integration/vla_perception/vla_perception_node.py`:

```python
#!/usr/bin/env python3
"""
VLA Perception Node
Integrates vision, language, and action perception systems
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge
import numpy as np
import cv2
from transformers import CLIPProcessor, CLIPModel
import torch

class VLAPerceptionNode(Node):
    def __init__(self):
        super().__init__('vla_perception_node')

        # Initialize CV bridge
        self.cv_bridge = CvBridge()

        # Initialize CLIP model for vision-language integration
        try:
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_model.eval()
            self.get_logger().info('CLIP model loaded successfully')
        except Exception as e:
            self.get_logger().error(f'Failed to load CLIP model: {e}')
            self.clip_model = None

        # Publishers and subscribers
        self.image_sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        self.camera_info_sub = self.create_subscription(
            CameraInfo, '/camera/camera_info', self.camera_info_callback, 10
        )
        self.language_sub = self.create_subscription(
            String, '/vla/language_command', self.language_callback, 10
        )

        self.object_detection_pub = self.create_publisher(
            String, '/vla/detected_objects', 10
        )
        self.saliency_map_pub = self.create_publisher(
            Image, '/vla/saliency_map', 10
        )
        self.attention_pub = self.create_publisher(
            PointStamped, '/vla/attention_point', 10
        )

        # Internal state
        self.latest_image = None
        self.camera_matrix = None
        self.current_command = None

        # Timer for processing
        self.process_timer = self.create_timer(0.1, self.process_callback)

        self.get_logger().info('VLA Perception Node initialized')

    def image_callback(self, msg):
        """Process incoming image data"""
        try:
            self.latest_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def camera_info_callback(self, msg):
        """Process camera calibration data"""
        self.camera_matrix = np.array(msg.k).reshape(3, 3)

    def language_callback(self, msg):
        """Process incoming language commands"""
        self.current_command = msg.data
        self.get_logger().info(f'Received language command: {msg.data}')

    def process_callback(self):
        """Process perception pipeline"""
        if self.latest_image is not None and self.current_command is not None:
            # Perform vision-language integration
            objects = self.detect_objects_by_command(self.latest_image, self.current_command)

            # Publish detected objects
            obj_msg = String()
            obj_msg.data = str(objects)
            self.object_detection_pub.publish(obj_msg)

            # Generate saliency map based on command
            saliency_map = self.generate_saliency_map(self.latest_image, self.current_command)

            if saliency_map is not None:
                saliency_msg = self.cv_bridge.cv2_to_imgmsg(saliency_map, encoding='mono8')
                self.saliency_map_pub.publish(saliency_msg)

            # Find attention point
            attention_point = self.find_attention_point(saliency_map)
            if attention_point is not None:
                point_msg = PointStamped()
                point_msg.header.stamp = self.get_clock().now().to_msg()
                point_msg.header.frame_id = 'camera_link'
                point_msg.point.x = attention_point[0]
                point_msg.point.y = attention_point[1]
                point_msg.point.z = 0.0  # Will be computed from depth
                self.attention_pub.publish(point_msg)

    def detect_objects_by_command(self, image, command):
        """Detect objects relevant to the command using CLIP"""
        if self.clip_model is None:
            return []

        # Use CLIP to find objects related to command
        # This is a simplified implementation - in practice, you'd use more sophisticated methods
        possible_objects = ['cup', 'bottle', 'chair', 'table', 'person', 'box', 'phone', 'book']

        # Process with CLIP
        inputs = self.clip_processor(
            text=possible_objects,
            images=[image] * len(possible_objects),
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():
            outputs = self.clip_model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]

        # Find objects with high probability
        detected_objects = []
        for i, (obj, prob) in enumerate(zip(possible_objects, probs)):
            if prob > 0.1:  # Threshold for detection
                detected_objects.append({
                    'object': obj,
                    'confidence': float(prob),
                    'bbox': self.find_object_bbox(image, obj)  # Simplified
                })

        return detected_objects

    def find_object_bbox(self, image, object_name):
        """Find bounding box for object (simplified implementation)"""
        # This would use object detection in a real implementation
        # For now, return a center-based bounding box
        h, w = image.shape[:2]
        center_x, center_y = w // 2, h // 2
        return {
            'xmin': max(0, center_x - 50),
            'ymin': max(0, center_y - 50),
            'xmax': min(w, center_x + 50),
            'ymax': min(h, center_y + 50)
        }

    def generate_saliency_map(self, image, command):
        """Generate saliency map highlighting relevant regions"""
        if self.clip_model is None:
            return None

        # This is a simplified saliency implementation
        # In practice, you'd use more sophisticated methods like gradient-based saliency
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply basic saliency based on CLIP features
        # This is a placeholder - real implementation would use attention maps
        saliency = np.zeros_like(gray, dtype=np.float32)

        # Highlight center region as an example
        h, w = gray.shape
        center_h, center_w = h // 2, w // 2
        cv2.circle(saliency, (center_w, center_h), min(h, w) // 4, 255, -1)

        # Normalize to 0-255 range
        saliency = ((saliency - saliency.min()) / (saliency.max() - saliency.min()) * 255).astype(np.uint8)

        return saliency

    def find_attention_point(self, saliency_map):
        """Find the point of highest attention in the saliency map"""
        if saliency_map is None:
            return None

        # Find the point with maximum saliency
        max_idx = np.unravel_index(np.argmax(saliency_map), saliency_map.shape)
        return (float(max_idx[1]), float(max_idx[0]))  # x, y coordinates

def main(args=None):
    rclpy.init(args=args)

    perception_node = VLAPerceptionNode()

    try:
        rclpy.spin(perception_node)
    except KeyboardInterrupt:
        pass
    finally:
        perception_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2.2 Create VLA Planning Node

Create `src/vla_integration/vla_planning/vla_planning_node.py`:

```python
#!/usr/bin/env python3
"""
VLA Planning Node
Translates language commands into executable action plans
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from capstone_msgs.msg import Command, ExecutionResult
import json
import time

class VLAPlanningNode(Node):
    def __init__(self):
        super().__init__('vla_planning_node')

        # Publishers and subscribers
        self.command_sub = self.create_subscription(
            Command, '/capstone/commands', self.command_callback, 10
        )
        self.plan_pub = self.create_publisher(
            String, '/vla/action_plan', 10
        )
        self.result_pub = self.create_publisher(
            ExecutionResult, '/vla/execution_result', 10
        )

        # Action vocabulary
        self.action_vocabulary = {
            'navigation': ['go to', 'move to', 'navigate to', 'walk to', 'approach'],
            'manipulation': ['pick', 'grasp', 'take', 'lift', 'place', 'put', 'drop'],
            'interaction': ['open', 'close', 'push', 'pull', 'press', 'turn'],
            'perception': ['find', 'locate', 'look for', 'search for', 'identify']
        }

        # Object vocabulary
        self.object_vocabulary = [
            'cup', 'bottle', 'chair', 'table', 'person', 'box', 'phone', 'book',
            'door', 'window', 'light', 'remote', 'keys', 'wallet', 'food', 'water'
        ]

        # Location vocabulary
        self.location_vocabulary = [
            'kitchen', 'living room', 'bedroom', 'bathroom', 'office', 'dining room',
            'hallway', 'entrance', 'table', 'counter', 'shelf', 'couch'
        ]

        self.get_logger().info('VLA Planning Node initialized')

    def command_callback(self, msg):
        """Process incoming commands and generate action plans"""
        if msg.target_system != 'vla':
            return

        self.get_logger().info(f'Processing command: {msg.command}')

        try:
            # Parse the command and generate plan
            plan = self.parse_command_to_plan(msg.command)

            # Publish the plan
            plan_msg = String()
            plan_msg.data = json.dumps(plan)
            self.plan_pub.publish(plan_msg)

            # Publish execution result
            result_msg = ExecutionResult()
            result_msg.timestamp = self.get_clock().now().to_msg()
            result_msg.command_executed = msg.command
            result_msg.success = True
            result_msg.error_message = ""
            result_msg.execution_time = 0.1  # Placeholder
            result_msg.result_details = f"Generated plan with {len(plan['actions'])} actions"

            self.result_pub.publish(result_msg)

        except Exception as e:
            self.get_logger().error(f'Error processing command: {e}')

            # Publish failure result
            result_msg = ExecutionResult()
            result_msg.timestamp = self.get_clock().now().to_msg()
            result_msg.command_executed = msg.command
            result_msg.success = False
            result_msg.error_message = str(e)
            result_msg.execution_time = 0.0
            result_msg.result_details = "Plan generation failed"

            self.result_pub.publish(result_msg)

    def parse_command_to_plan(self, command):
        """Parse natural language command and generate action plan"""
        command_lower = command.lower()

        # Initialize plan structure
        plan = {
            'original_command': command,
            'parsed_command': self.parse_command_structure(command_lower),
            'actions': [],
            'constraints': [],
            'safety_checks': []
        }

        # Determine primary action type
        action_type = self.identify_action_type(command_lower)

        if action_type == 'navigation':
            plan['actions'] = self.generate_navigation_plan(command_lower)
        elif action_type == 'manipulation':
            plan['actions'] = self.generate_manipulation_plan(command_lower)
        elif action_type == 'interaction':
            plan['actions'] = self.generate_interaction_plan(command_lower)
        elif action_type == 'perception':
            plan['actions'] = self.generate_perception_plan(command_lower)
        else:
            # Default to general plan
            plan['actions'] = self.generate_general_plan(command_lower)

        # Add safety constraints
        plan['safety_checks'] = self.generate_safety_constraints(plan['actions'])

        return plan

    def identify_action_type(self, command):
        """Identify the primary action type from command"""
        for action_type, keywords in self.action_vocabulary.items():
            for keyword in keywords:
                if keyword in command:
                    return action_type
        return 'general'

    def parse_command_structure(self, command):
        """Parse the grammatical structure of the command"""
        # Simple parsing - in practice, use NLP libraries
        words = command.split()

        parsed = {
            'verb': None,
            'object': None,
            'location': None,
            'modifiers': []
        }

        # Extract verb (action word)
        for i, word in enumerate(words):
            if any(action_type in word for action_type in ['go', 'move', 'pick', 'grasp', 'place', 'find']):
                parsed['verb'] = word
                break

        # Extract object
        for obj in self.object_vocabulary:
            if obj in command:
                parsed['object'] = obj
                break

        # Extract location
        for loc in self.location_vocabulary:
            if loc in command:
                parsed['location'] = loc
                break

        return parsed

    def generate_navigation_plan(self, command):
        """Generate navigation-specific action plan"""
        actions = []

        # Extract destination
        destination = None
        for loc in self.location_vocabulary:
            if loc in command:
                destination = loc
                break

        if destination:
            actions.append({
                'action': 'navigate_to_location',
                'parameters': {
                    'destination': destination,
                    'precision': 'high' if 'precisely' in command else 'medium'
                }
            })
        else:
            # If no specific location, use general navigation
            actions.append({
                'action': 'explore_environment',
                'parameters': {
                    'duration': 30  # seconds
                }
            })

        return actions

    def generate_manipulation_plan(self, command):
        """Generate manipulation-specific action plan"""
        actions = []

        # Identify object to manipulate
        target_object = None
        for obj in self.object_vocabulary:
            if obj in command:
                target_object = obj
                break

        # Determine action type
        if any(word in command for word in ['pick', 'grasp', 'take', 'lift']):
            action = 'grasp_object'
        elif any(word in command for word in ['place', 'put', 'drop']):
            action = 'place_object'
        else:
            action = 'manipulate_object'

        if target_object:
            actions.append({
                'action': action,
                'parameters': {
                    'object': target_object,
                    'grasp_type': 'precision' if 'carefully' in command else 'power'
                }
            })

        return actions

    def generate_interaction_plan(self, command):
        """Generate interaction-specific action plan"""
        actions = []

        # Identify target for interaction
        target = None
        for obj in self.object_vocabulary:
            if obj in command:
                target = obj
                break

        if not target:
            for loc in self.location_vocabulary:
                if loc in command:
                    target = loc
                    break

        if target:
            # Determine interaction type
            interaction_type = 'interact'
            if any(word in command for word in ['open', 'close']):
                interaction_type = 'open_close'
            elif any(word in command for word in ['push', 'pull']):
                interaction_type = 'push_pull'
            elif any(word in command for word in ['press', 'turn']):
                interaction_type = 'press_turn'

            actions.append({
                'action': interaction_type,
                'parameters': {
                    'target': target,
                    'force': 'light' if 'gently' in command else 'normal'
                }
            })

        return actions

    def generate_perception_plan(self, command):
        """Generate perception-specific action plan"""
        actions = []

        # Identify object to find
        target_object = None
        for obj in self.object_vocabulary:
            if obj in command:
                target_object = obj
                break

        if target_object:
            actions.append({
                'action': 'search_for_object',
                'parameters': {
                    'object': target_object,
                    'search_method': 'systematic' if 'thoroughly' in command else 'efficient'
                }
            })
            actions.append({
                'action': 'localize_object',
                'parameters': {
                    'object': target_object
                }
            })

        return actions

    def generate_general_plan(self, command):
        """Generate general action plan when specific type is unclear"""
        actions = []

        # Use keywords to determine appropriate actions
        if any(word in command for word in ['find', 'look', 'search']):
            actions.extend(self.generate_perception_plan(command))
        elif any(word in command for word in ['go', 'move', 'walk']):
            actions.extend(self.generate_navigation_plan(command))
        elif any(word in command for word in ['pick', 'grasp', 'place']):
            actions.extend(self.generate_manipulation_plan(command))
        else:
            # Default action - observe and report
            actions.append({
                'action': 'observe_environment',
                'parameters': {
                    'duration': 10
                }
            })
            actions.append({
                'action': 'report_observation',
                'parameters': {
                    'content': command
                }
            })

        return actions

    def generate_safety_constraints(self, actions):
        """Generate safety constraints for the action plan"""
        constraints = []

        for action in actions:
            if action['action'] in ['navigate_to_location', 'explore_environment']:
                constraints.append({
                    'constraint': 'maintain_balance',
                    'priority': 'high'
                })
                constraints.append({
                    'constraint': 'avoid_obstacles',
                    'priority': 'high'
                })
            elif action['action'] in ['grasp_object', 'place_object', 'manipulate_object']:
                constraints.append({
                    'constraint': 'check_object_weight',
                    'priority': 'medium'
                })
                constraints.append({
                    'constraint': 'maintain_balance_during_manipulation',
                    'priority': 'high'
                })
            elif action['action'] in ['open_close', 'push_pull', 'press_turn']:
                constraints.append({
                    'constraint': 'apply_appropriate_force',
                    'priority': 'medium'
                })

        return constraints

def main(args=None):
    rclpy.init(args=args)

    planning_node = VLAPlanningNode()

    try:
        rclpy.spin(planning_node)
    except KeyboardInterrupt:
        pass
    finally:
        planning_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Implementation Phase 3: Humanoid Control Integration

### 3.1 Create Humanoid Balance Controller

Create `src/humanoid_control/balance_control/balance_controller_node.py`:

```python
#!/usr/bin/env python3
"""
Humanoid Balance Controller Node
Maintains balance during humanoid robot operation
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Vector3Stamped, PointStamped
from std_msgs.msg import Float64MultiArray
from builtin_interfaces.msg import Time
import numpy as np
from scipy.spatial.transform import Rotation as R
import math

class BalanceControllerNode(Node):
    def __init__(self):
        super().__init__('balance_controller_node')

        # Robot parameters
        self.robot_mass = 70.0  # kg
        self.com_height = 0.8  # m
        self.gravity = 9.81  # m/s^2

        # Balance controller parameters
        self.zmp_kp = 10.0
        self.zmp_kd = 2.0
        self.com_kp = 8.0
        self.com_kd = 1.5

        # Support polygon (simplified - rectangle)
        self.support_polygon = np.array([
            [-0.1, 0.1],   # left foot front-left
            [-0.1, -0.1],  # left foot front-right
            [0.1, -0.1],   # right foot back-right
            [0.1, 0.1]     # right foot back-left
        ])

        # Publishers and subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10
        )
        self.com_reference_sub = self.create_subscription(
            PointStamped, '/balance/com_reference', self.com_reference_callback, 10
        )

        self.balance_cmd_pub = self.create_publisher(
            Float64MultiArray, '/balance/commands', 10
        )
        self.zmp_pub = self.create_publisher(
            PointStamped, '/balance/zmp', 10
        )
        self.com_pub = self.create_publisher(
            PointStamped, '/balance/com', 10
        )
        self.balance_status_pub = self.create_publisher(
            Vector3Stamped, '/balance/status', 10
        )

        # Robot state
        self.current_joint_positions = {}
        self.current_joint_velocities = {}
        self.current_joint_efforts = {}
        self.current_imu_orientation = np.array([0, 0, 0, 1])  # quaternion
        self.current_imu_angular_velocity = np.array([0, 0, 0])
        self.current_imu_linear_acceleration = np.array([0, 0, 0])
        self.current_com = np.array([0.0, 0.0, self.com_height])
        self.current_com_velocity = np.array([0.0, 0.0, 0.0])
        self.current_com_acceleration = np.array([0.0, 0.0, 0.0])
        self.desired_com = np.array([0.0, 0.0, self.com_height])

        # Control timer
        self.control_timer = self.create_timer(0.02, self.balance_control_callback)  # 50 Hz

        self.get_logger().info('Balance Controller Node initialized')

    def joint_state_callback(self, msg):
        """Process joint state updates"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.current_joint_positions[name] = msg.position[i]
            if i < len(msg.velocity):
                self.current_joint_velocities[name] = msg.velocity[i]
            if i < len(msg.effort):
                self.current_joint_efforts[name] = msg.effort[i]

    def imu_callback(self, msg):
        """Process IMU data"""
        self.current_imu_orientation = np.array([
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        ])
        self.current_imu_angular_velocity = np.array([
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ])
        self.current_imu_linear_acceleration = np.array([
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z
        ])

    def com_reference_callback(self, msg):
        """Process desired center of mass reference"""
        self.desired_com = np.array([
            msg.point.x,
            msg.point.y,
            msg.point.z
        ])

    def balance_control_callback(self):
        """Main balance control loop"""
        try:
            # Estimate current CoM position (simplified)
            self.estimate_com_position()

            # Calculate ZMP
            current_zmp = self.compute_zmp(self.current_com, self.current_com_acceleration)

            # Calculate desired ZMP
            desired_zmp = self.compute_zmp(self.desired_com, np.array([0, 0, 0]))

            # Balance control law
            zmp_error = desired_zmp[:2] - current_zmp[:2]
            com_error = self.desired_com[:2] - self.current_com[:2]

            # Combine ZMP and CoM control
            control_output = (
                self.zmp_kp * zmp_error +
                self.com_kp * com_error
            )

            # Check if in support polygon
            in_support = self.is_in_support_polygon(current_zmp[:2])

            # Publish balance status
            status_msg = Vector3Stamped()
            status_msg.header.stamp = self.get_clock().now().to_msg()
            status_msg.header.frame_id = 'base_link'
            status_msg.vector.x = float(control_output[0])
            status_msg.vector.y = float(control_output[1])
            status_msg.vector.z = 1.0 if in_support else 0.0  # z component indicates stability
            self.balance_status_pub.publish(status_msg)

            # Publish ZMP
            zmp_msg = PointStamped()
            zmp_msg.header.stamp = self.get_clock().now().to_msg()
            zmp_msg.header.frame_id = 'map'
            zmp_msg.point.x = float(current_zmp[0])
            zmp_msg.point.y = float(current_zmp[1])
            zmp_msg.point.z = 0.0
            self.zmp_pub.publish(zmp_msg)

            # Publish CoM
            com_msg = PointStamped()
            com_msg.header.stamp = self.get_clock().now().to_msg()
            com_msg.header.frame_id = 'map'
            com_msg.point.x = float(self.current_com[0])
            com_msg.point.y = float(self.current_com[1])
            com_msg.point.z = float(self.current_com[2])
            self.com_pub.publish(com_msg)

            # Generate balance commands
            balance_cmd = Float64MultiArray()
            balance_cmd.data = [float(x) for x in control_output]
            self.balance_cmd_pub.publish(balance_cmd)

        except Exception as e:
            self.get_logger().error(f'Balance control error: {e}')

    def estimate_com_position(self):
        """Estimate current center of mass position"""
        # Simplified CoM estimation - in practice, use kinematic model
        # For now, use IMU data and joint positions to estimate CoM

        # This is a placeholder - real implementation would use forward kinematics
        # and a detailed robot model
        self.current_com[2] = self.com_height  # Maintain approximate height

        # Add small adjustments based on joint angles if available
        # This is where you'd implement actual CoM calculation

    def compute_zmp(self, com_pos, com_acc):
        """Compute Zero Moment Point from CoM position and acceleration"""
        zmp_x = com_pos[0] - (self.com_height / self.gravity) * com_acc[0]
        zmp_y = com_pos[1] - (self.com_height / self.gravity) * com_acc[1]

        return np.array([zmp_x, zmp_y, 0.0])

    def is_in_support_polygon(self, point):
        """Check if point is within support polygon using ray casting"""
        x, y = point
        n = len(self.support_polygon)
        inside = False

        p1x, p1y = self.support_polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = self.support_polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

def main(args=None):
    rclpy.init(args=args)

    balance_controller = BalanceControllerNode()

    try:
        rclpy.spin(balance_controller)
    except KeyboardInterrupt:
        pass
    finally:
        balance_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Implementation Phase 4: Simulation Bridge

### 4.1 Create Gazebo Bridge Node

Create `src/simulation_bridge/gazebo_bridge/gazebo_bridge_node.py`:

```python
#!/usr/bin/env python3
"""
Gazebo Bridge Node
Interfaces between ROS 2 and Gazebo simulation
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist, Pose
from gazebo_msgs.srv import SetEntityState, GetEntityState
from gazebo_msgs.msg import ModelState
from builtin_interfaces.msg import Time
import numpy as np

class GazeboBridgeNode(Node):
    def __init__(self):
        super().__init__('gazebo_bridge_node')

        # Publishers and subscribers
        self.joint_cmd_pub = self.create_publisher(
            JointState, '/gazebo/joint_commands', 10
        )
        self.model_state_pub = self.create_publisher(
            ModelState, '/gazebo/model_states', 10
        )

        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_commands', self.joint_command_callback, 10
        )
        self.twist_sub = self.create_subscription(
            Twist, '/cmd_vel', self.velocity_command_callback, 10
        )

        # Services
        self.set_entity_state_cli = self.create_client(
            SetEntityState, '/set_entity_state'
        )
        self.get_entity_state_cli = self.create_client(
            GetEntityState, '/get_entity_state'
        )

        # Robot configuration
        self.robot_name = 'humanoid_robot'
        self.joint_names = [
            'left_hip_pitch', 'left_hip_roll', 'left_hip_yaw',
            'left_knee', 'left_ankle_pitch', 'left_ankle_roll',
            'right_hip_pitch', 'right_hip_roll', 'right_hip_yaw',
            'right_knee', 'right_ankle_pitch', 'right_ankle_roll',
            'left_shoulder_pitch', 'left_shoulder_roll', 'left_elbow',
            'right_shoulder_pitch', 'right_shoulder_roll', 'right_elbow'
        ]

        # Wait for services
        while not self.set_entity_state_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for set_entity_state service...')

        while not self.get_entity_state_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for get_entity_state service...')

        self.get_logger().info('Gazebo Bridge Node initialized')

    def joint_command_callback(self, msg):
        """Process joint commands and forward to Gazebo"""
        # Create joint state message for Gazebo
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = msg.name
        joint_state.position = msg.position
        joint_state.velocity = msg.velocity if msg.velocity else [0.0] * len(msg.position)
        joint_state.effort = msg.effort if msg.effort else [0.0] * len(msg.position)

        # Publish to Gazebo
        self.joint_cmd_pub.publish(joint_state)

    def velocity_command_callback(self, msg):
        """Process velocity commands for base movement"""
        # Convert twist command to Gazebo model state
        model_state = ModelState()
        model_state.model_name = self.robot_name
        model_state.pose = Pose()  # Keep current pose
        model_state.twist.linear.x = msg.linear.x
        model_state.twist.linear.y = msg.linear.y
        model_state.twist.linear.z = msg.linear.z
        model_state.twist.angular.x = msg.angular.x
        model_state.twist.angular.y = msg.angular.y
        model_state.twist.angular.z = msg.angular.z
        model_state.reference_frame = 'world'

        # Publish model state
        self.model_state_pub.publish(model_state)

    def set_robot_pose(self, x, y, z, roll, pitch, yaw):
        """Set robot pose in Gazebo"""
        req = SetEntityState.Request()
        req.state.name = self.robot_name
        req.state.pose.position.x = x
        req.state.pose.position.y = y
        req.state.pose.position.z = z

        # Convert Euler to quaternion
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x_q = sr * cp * cy - cr * sp * sy
        y_q = cr * sp * cy + sr * cp * sy
        z_q = cr * cp * sy - sr * sp * cy

        req.state.pose.orientation.w = w
        req.state.pose.orientation.x = x_q
        req.state.pose.orientation.y = y_q
        req.state.pose.orientation.z = z_q

        future = self.set_entity_state_cli.call_async(req)
        return future

    def get_robot_state(self):
        """Get current robot state from Gazebo"""
        req = GetEntityState.Request()
        req.name = self.robot_name
        req.relative_entity_name = 'world'

        future = self.get_entity_state_cli.call_async(req)
        return future

def main(args=None):
    rclpy.init(args=args)

    gazebo_bridge = GazeboBridgeNode()

    try:
        rclpy.spin(gazebo_bridge)
    except KeyboardInterrupt:
        pass
    finally:
        gazebo_bridge.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Implementation Phase 5: System Integration and Launch

### 5.1 Create Main Launch File

Create `launch/capstone_system.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # Capstone Coordinator Node
    coordinator_node = Node(
        package='capstone_project',
        executable='capstone_coordinator',
        name='capstone_coordinator',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # VLA Perception Node
    vla_perception_node = Node(
        package='capstone_project',
        executable='vla_perception_node',
        name='vla_perception_node',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # VLA Planning Node
    vla_planning_node = Node(
        package='capstone_project',
        executable='vla_planning_node',
        name='vla_planning_node',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Balance Controller Node
    balance_controller_node = Node(
        package='capstone_project',
        executable='balance_controller_node',
        name='balance_controller_node',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Gazebo Bridge Node
    gazebo_bridge_node = Node(
        package='capstone_project',
        executable='gazebo_bridge_node',
        name='gazebo_bridge_node',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        use_sim_time_arg,
        coordinator_node,
        vla_perception_node,
        vla_planning_node,
        balance_controller_node,
        gazebo_bridge_node
    ])
```

### 5.2 Create Package Configuration

Create `package.xml` in the project root:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>capstone_project</name>
  <version>0.0.0</version>
  <description>Capstone project for autonomous humanoid robotics system</description>
  <maintainer email="student@university.edu">Student</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>nav_msgs</depend>
  <depend>builtin_interfaces</depend>
  <depend>cv_bridge</depend>
  <depend>gazebo_msgs</depend>
  <depend>capstone_msgs</depend>

  <exec_depend>ros2launch</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

Create `setup.py` in the project root:

```python
from setuptools import setup
import os
from glob import glob

package_name = 'capstone_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Student',
    maintainer_email='student@university.edu',
    description='Capstone project for autonomous humanoid robotics system',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'capstone_coordinator = capstone_project.capstone_coordinator:main',
            'vla_perception_node = capstone_project.vla_perception_node:main',
            'vla_planning_node = capstone_project.vla_planning_node:main',
            'balance_controller_node = capstone_project.balance_controller_node:main',
            'gazebo_bridge_node = capstone_project.gazebo_bridge_node:main',
        ],
    },
)
```

## Implementation Phase 6: Testing and Validation

### 6.1 Create Test Scripts

Create `test/test_integration.py`:

```python
#!/usr/bin/env python3
"""
Integration tests for capstone system
"""

import unittest
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

class TestCapstoneIntegration(unittest.TestCase):
    def setUp(self):
        rclpy.init()
        self.node = Node('test_capstone_integration')

    def tearDown(self):
        self.node.destroy_node()
        rclpy.shutdown()

    def test_system_communication(self):
        """Test that all system components can communicate"""
        # This would test actual communication between nodes
        self.assertTrue(True)  # Placeholder

    def test_command_processing(self):
        """Test command processing pipeline"""
        # This would test the full pipeline from command to action
        self.assertTrue(True)  # Placeholder

    def test_balance_maintenance(self):
        """Test balance control system"""
        # This would test balance control functionality
        self.assertTrue(True)  # Placeholder

if __name__ == '__main__':
    unittest.main()
```

Now let me create the evaluation criteria document:
