---
title: "Chapter 4: Perception Systems"
sidebar_position: 4
---

# Chapter 4: Perception Systems

## Learning Objectives

By the end of this chapter, students will be able to:
- Design and implement multi-modal perception systems for robotics
- Integrate different sensor types for robust perception
- Apply deep learning techniques for object detection and classification
- Implement sensor fusion algorithms for improved perception accuracy
- Evaluate perception system performance and reliability

## Introduction to Robotics Perception

Perception systems form the sensory foundation of autonomous robotics, enabling robots to understand and interpret their environment. In modern robotics, perception systems must process multiple sensor modalities including cameras, LiDAR, radar, IMU, and other specialized sensors to create a comprehensive understanding of the environment.

Effective perception systems must handle various challenges including sensor noise, environmental conditions, real-time processing requirements, and the integration of multiple data sources. The goal is to create robust, accurate, and efficient perception that enables reliable autonomous operation.

## Sensor Modalities and Characteristics

### Camera Systems

Cameras provide rich visual information that is essential for many robotics applications. Different camera types serve specific purposes:

#### RGB Cameras
- **Strengths**: Rich color and texture information, high resolution
- **Applications**: Object recognition, scene understanding, visual SLAM
- **Limitations**: Performance varies with lighting conditions, no depth information

#### Depth Cameras
- **Strengths**: Direct depth measurements, 3D scene reconstruction
- **Applications**: Obstacle detection, 3D mapping, manipulation
- **Types**: Stereo, structured light, time-of-flight

#### Thermal Cameras
- **Strengths**: Works in low-light conditions, detects heat signatures
- **Applications**: Surveillance, human detection, temperature monitoring
- **Limitations**: Lower resolution, specialized processing requirements

### LiDAR Systems

LiDAR (Light Detection and Ranging) provides accurate 3D spatial information:

#### 2D LiDAR
- **Applications**: Indoor navigation, obstacle detection
- **Characteristics**: Single plane scanning, high accuracy in plane
- **Limitations**: Limited vertical information

#### 3D LiDAR
- **Applications**: 3D mapping, outdoor navigation, object detection
- **Characteristics**: Full 3D point cloud, good range accuracy
- **Types**: Mechanical, solid-state, MEMS

### Other Sensors

#### IMU (Inertial Measurement Unit)
- Provides acceleration and rotation data
- Essential for motion estimation and stabilization
- High-frequency data but prone to drift

#### Radar
- Works in adverse weather conditions
- Good for velocity estimation
- Lower resolution than other sensors

## Isaac ROS Perception Components

### Isaac ROS Detection 2D

Isaac ROS Detection 2D provides GPU-accelerated 2D object detection:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from std_msgs.msg import Header
from builtin_interfaces.msg import Time
import cv2
from cv_bridge import CvBridge

class IsaacObjectDetector(Node):
    def __init__(self):
        super().__init__('isaac_object_detector')

        self.cv_bridge = CvBridge()

        # Publishers and subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_rect_color',
            self.image_callback,
            10
        )

        self.detection_pub = self.create_publisher(
            Detection2DArray,
            '/isaac_ros/detections',
            10
        )

    def image_callback(self, msg):
        """
        Process image and perform object detection using Isaac ROS
        """
        # Convert ROS image to OpenCV format
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # In practice, Isaac ROS Detection 2D node would process this
        # The node uses GPU-accelerated deep learning models
        detections = self.perform_gpu_detection(cv_image)

        # Create detection message
        detection_array = Detection2DArray()
        detection_array.header = msg.header
        detection_array.detections = detections

        # Publish detections
        self.detection_pub.publish(detection_array)

    def perform_gpu_detection(self, image):
        """
        GPU-accelerated object detection (conceptual)
        In Isaac ROS, this uses TensorRT for optimized inference
        """
        # Isaac ROS uses pre-trained models like YOLO, DetectNet, etc.
        # Running on GPU with TensorRT optimization
        pass
```

### Isaac ROS Depth Segmentation

Depth segmentation combines depth information with semantic segmentation:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Point32
from sensor_msgs.msg import PointCloud2, PointField
import numpy as np

class DepthSegmentationProcessor(Node):
    def __init__(self):
        super().__init__('depth_segmentation_processor')

        # Subscribers for RGB and depth images
        self.rgb_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_rect_color',
            self.rgb_callback,
            10
        )

        self.depth_sub = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',
            self.depth_callback,
            10
        )

        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/rgb/camera_info',
            self.camera_info_callback,
            10
        )

        # Publisher for 3D segmented objects
        self.segmented_3d_pub = self.create_publisher(
            PointCloud2,
            '/isaac_ros/segmented_3d',
            10
        )

        self.camera_matrix = None
        self.new_rgb = False
        self.new_depth = False
        self.rgb_image = None
        self.depth_image = None

    def camera_info_callback(self, msg):
        """
        Store camera intrinsic parameters
        """
        self.camera_matrix = np.array(msg.k).reshape(3, 3)

    def rgb_callback(self, msg):
        """
        Store RGB image for segmentation
        """
        self.rgb_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.new_rgb = True
        if self.new_rgb and self.new_depth:
            self.process_segmentation()

    def depth_callback(self, msg):
        """
        Store depth image for 3D reconstruction
        """
        self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')
        self.new_depth = True
        if self.new_rgb and self.new_depth:
            self.process_segmentation()

    def process_segmentation(self):
        """
        Combine RGB segmentation with depth information
        """
        if self.camera_matrix is None:
            return

        # Perform segmentation (Isaac ROS would handle this GPU-accelerated)
        # For each segmented region, compute 3D position using depth and camera parameters
        segmented_3d = self.create_3d_segmented_cloud(
            self.rgb_image, self.depth_image, self.camera_matrix
        )

        self.segmented_3d_pub.publish(segmented_3d)

    def create_3d_segmented_cloud(self, rgb_image, depth_image, camera_matrix):
        """
        Create 3D point cloud with segmentation information
        """
        # Convert 2D segmentation to 3D points using depth and camera matrix
        height, width = depth_image.shape

        # Generate pixel coordinates
        u_coords, v_coords = np.meshgrid(np.arange(width), np.arange(height))
        u_coords = u_coords.flatten()
        v_coords = v_coords.flatten()
        depth_flat = depth_image.flatten()

        # Remove invalid depth values
        valid_mask = (depth_flat > 0) & (depth_flat < 10)  # Filter reasonable depths
        u_valid = u_coords[valid_mask]
        v_valid = v_coords[valid_mask]
        z_valid = depth_flat[valid_mask]

        # Convert to 3D coordinates
        x_3d = (u_valid - camera_matrix[0, 2]) * z_valid / camera_matrix[0, 0]
        y_3d = (v_valid - camera_matrix[1, 2]) * z_valid / camera_matrix[1, 1]

        # Create PointCloud2 message
        points = np.column_stack((x_3d, y_3d, z_valid)).astype(np.float32)

        # In practice, Isaac ROS handles this with GPU acceleration
        return self.create_pointcloud2_msg(points, self.rgb_image.header)
```

### Isaac ROS Stereo DNN

Stereo vision with deep neural networks provides enhanced depth estimation:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from stereo_msgs.msg import DisparityImage
from geometry_msgs.msg import Point32
import numpy as np

class StereoDNNProcessor(Node):
    def __init__(self):
        super().__init__('stereo_dnn_processor')

        # Subscribers for stereo pair
        self.left_sub = self.create_subscription(
            Image,
            '/stereo_camera/left/image_rect',
            self.left_callback,
            10
        )

        self.right_sub = self.create_subscription(
            Image,
            '/stereo_camera/right/image_rect',
            self.right_callback,
            10
        )

        # Publisher for enhanced disparity
        self.disparity_pub = self.create_publisher(
            DisparityImage,
            '/isaac_ros/stereo_dnn/disparity',
            10
        )

        self.left_image = None
        self.right_image = None
        self.images_synced = False

    def left_callback(self, msg):
        """
        Process left camera image
        """
        self.left_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.check_sync()

    def right_callback(self, msg):
        """
        Process right camera image
        """
        self.right_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.check_sync()

    def check_sync(self):
        """
        Check if both images are available for processing
        """
        if self.left_image is not None and self.right_image is not None:
            self.process_stereo_dnn()

    def process_stereo_dnn(self):
        """
        Process stereo pair using DNN for enhanced depth estimation
        """
        # Isaac ROS Stereo DNN combines traditional stereo matching
        # with deep learning for improved accuracy and robustness
        disparity = self.compute_dnn_disparity(self.left_image, self.right_image)

        # Create disparity message
        disp_msg = DisparityImage()
        disp_msg.header = self.left_sub.header  # Use appropriate header
        disp_msg.image = self.cv_bridge.cv2_to_imgmsg(disparity, encoding='32FC1')
        disp_msg.f = self.camera_info.K[0]  # Focal length
        disp_msg.T = 0.1  # Baseline (example value)
        disp_msg.min_disparity = 0.0
        disp_msg.max_disparity = 100.0

        self.disparity_pub.publish(disp_msg)

    def compute_dnn_disparity(self, left_img, right_img):
        """
        Compute disparity using DNN (conceptual - Isaac ROS handles this)
        """
        # Isaac ROS Stereo DNN uses CNNs trained for stereo matching
        # Combines geometric constraints with learned features
        pass
```

## Sensor Fusion Techniques

### Kalman Filtering

Kalman filters provide optimal state estimation by combining multiple sensor measurements:

```python
import numpy as np
from scipy.linalg import block_diag

class ExtendedKalmanFilter:
    def __init__(self, state_dim, measurement_dim):
        # State vector: [x, y, z, vx, vy, vz]
        self.state_dim = state_dim
        self.measurement_dim = measurement_dim

        # State vector [position, velocity]
        self.x = np.zeros(state_dim)

        # Covariance matrix
        self.P = np.eye(state_dim) * 1000  # Initial uncertainty

        # Process noise
        self.Q = np.eye(state_dim) * 0.1

        # Measurement noise
        self.R = np.eye(measurement_dim) * 1.0

    def predict(self, dt):
        """
        Prediction step using motion model
        """
        # State transition model (constant velocity)
        F = np.eye(self.state_dim)
        F[0:3, 3:6] = dt * np.eye(3)  # Position = position + velocity * dt

        # Predict state
        self.x = F @ self.x

        # Predict covariance
        self.P = F @ self.P @ F.T + self.Q

    def update(self, measurement, H_func, R=None):
        """
        Update step with new measurement
        H_func: Jacobian of measurement function
        """
        if R is None:
            R = self.R

        # Measurement Jacobian
        H = H_func(self.x)

        # Innovation
        y = measurement - self.h(self.x)  # Measurement residual

        # Innovation covariance
        S = H @ self.P @ H.T + R

        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)

        # Update state
        self.x = self.x + K @ y

        # Update covariance
        I = np.eye(self.state_dim)
        self.P = (I - K @ H) @ self.P

    def h(self, state):
        """
        Measurement function (nonlinear)
        For position-only measurements: return [x, y, z]
        """
        return state[0:3]  # Return position part of state

def camera_measurement_jacobian(state):
    """
    Jacobian of camera measurement function
    """
    H = np.zeros((3, 6))  # 3 measurements (x,y,z) from 6 state variables
    H[0:3, 0:3] = np.eye(3)  # Direct observation of position
    return H

# Example usage for sensor fusion
def fuse_camera_lidar_ekf():
    """
    Example of fusing camera and LiDAR measurements
    """
    ekf = ExtendedKalmanFilter(state_dim=6, measurement_dim=3)

    # Simulate measurements from different sensors
    camera_pos = np.array([1.0, 2.0, 0.5])
    lidar_pos = np.array([1.05, 1.98, 0.52])

    # Process measurements
    dt = 0.1  # Time step
    ekf.predict(dt)

    # Update with camera measurement
    ekf.update(camera_pos, camera_measurement_jacobian)

    # Update with LiDAR measurement
    ekf.update(lidar_pos, camera_measurement_jacobian)

    return ekf.x  # Return fused state estimate
```

### Particle Filtering

Particle filters are useful for non-linear, non-Gaussian systems:

```python
class ParticleFilter:
    def __init__(self, num_particles, state_dim):
        self.num_particles = num_particles
        self.state_dim = state_dim

        # Initialize particles randomly
        self.particles = np.random.normal(0, 1, (num_particles, state_dim))
        self.weights = np.ones(num_particles) / num_particles

    def predict(self, control_input, process_noise):
        """
        Predict particle states based on motion model
        """
        # Add process noise and motion model
        noise = np.random.normal(0, process_noise, self.particles.shape)
        self.particles += noise

        # Apply motion model based on control input
        # This is simplified - actual model would be more complex
        self.particles[:, 3:6] += control_input * 0.1  # Velocity update
        self.particles[:, 0:3] += self.particles[:, 3:6] * 0.1  # Position update

    def update(self, measurement, measurement_noise):
        """
        Update particle weights based on measurement likelihood
        """
        # Calculate likelihood of each particle given measurement
        for i in range(self.num_particles):
            particle_state = self.particles[i]
            predicted_measurement = self.predict_measurement(particle_state)

            # Calculate likelihood (Gaussian)
            diff = measurement - predicted_measurement
            likelihood = np.exp(-0.5 * diff.T @ diff / (measurement_noise**2))
            self.weights[i] *= likelihood

        # Normalize weights
        self.weights += 1e-300  # Avoid numerical issues
        self.weights /= np.sum(self.weights)

    def resample(self):
        """
        Resample particles based on weights
        """
        # Systematic resampling
        indices = self.systematic_resample()
        self.particles = self.particles[indices]
        self.weights.fill(1.0 / self.num_particles)

    def systematic_resample(self):
        """
        Systematic resampling algorithm
        """
        cumulative_sum = np.cumsum(self.weights)
        start = np.random.uniform(0, 1/self.num_particles)
        indices = []
        i, j = 0, 0
        while i < self.num_particles:
            if start + i / self.num_particles < cumulative_sum[j]:
                indices.append(j)
                i += 1
            else:
                j += 1
        return indices

    def predict_measurement(self, state):
        """
        Predict what measurement should be for given state
        """
        # For position measurement, return position part of state
        return state[0:3]

    def estimate_state(self):
        """
        Estimate current state from particles
        """
        return np.average(self.particles, axis=0, weights=self.weights)
```

## Deep Learning for Perception

### Object Detection Networks

Modern perception systems rely heavily on deep learning for object detection:

```python
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms

class PerceptionNetwork(nn.Module):
    def __init__(self, num_classes=80):
        super(PerceptionNetwork, self).__init__()

        # Use pre-trained backbone (e.g., ResNet, EfficientNet)
        self.backbone = torchvision.models.resnet50(pretrained=True)

        # Remove the final classification layer
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()

        # Detection head
        self.detection_head = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes * 4 + num_classes),  # bbox coords + class probs
        )

    def forward(self, x):
        # Extract features
        features = self.backbone(x)

        # Generate detections
        detections = self.detection_head(features)

        return detections

# Isaac ROS uses TensorRT for optimized inference
def optimize_for_tensorrt(model, input_shape):
    """
    Optimize model for TensorRT inference (conceptual)
    """
    # Isaac ROS automatically handles TensorRT optimization
    # This is done through the Isaac ROS DNN components
    pass
```

### Semantic Segmentation

Semantic segmentation provides pixel-level object classification:

```python
class SemanticSegmentationNet(nn.Module):
    def __init__(self, num_classes=21):  # 21 classes for PASCAL VOC
        super(SemanticSegmentationNet, self).__init__()

        # Encoder (feature extraction)
        self.encoder = torchvision.models.resnet50(pretrained=True)
        self.encoder.fc = nn.Identity()  # Remove classification head

        # Decoder (upsampling to full resolution)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(2048, 512, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(512, 256, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(128, num_classes, kernel_size=1)
        )

    def forward(self, x):
        # Encoder
        features = self.encoder(x)

        # Reshape for decoder (this is simplified)
        features = features.unsqueeze(-1).unsqueeze(-1)  # Add spatial dims

        # Decoder
        segmentation = self.decoder(features)

        return segmentation
```

## Multi-Modal Perception Integration

### Fusion Architecture

A typical multi-modal perception system architecture:

```python
class MultiModalPerceptionSystem(Node):
    def __init__(self):
        super().__init__('multi_modal_perception')

        # Initialize individual perception modules
        self.camera_perception = CameraPerceptionModule()
        self.lidar_perception = LidarPerceptionModule()
        self.radar_perception = RadarPerceptionModule()

        # Sensor fusion module
        self.fusion_module = SensorFusionModule()

        # Publishers for fused results
        self.fused_detections_pub = self.create_publisher(
            Detection3DArray,
            '/perception/fused_detections',
            10
        )

        # Timer for fusion processing
        self.fusion_timer = self.create_timer(0.1, self.perform_fusion)

    def camera_callback(self, msg):
        """
        Process camera data and store for fusion
        """
        camera_detections = self.camera_perception.process(msg)
        self.fusion_module.add_camera_data(camera_detections, msg.header.stamp)

    def lidar_callback(self, msg):
        """
        Process LiDAR data and store for fusion
        """
        lidar_detections = self.lidar_perception.process(msg)
        self.fusion_module.add_lidar_data(lidar_detections, msg.header.stamp)

    def perform_fusion(self):
        """
        Perform sensor fusion when data is synchronized
        """
        # Check if we have synchronized data from multiple sensors
        if self.fusion_module.has_synchronized_data():
            fused_detections = self.fusion_module.fuse_data()

            # Publish fused results
            self.fused_detections_pub.publish(fused_detections)
```

### Synchronization and Timing

Proper synchronization is crucial for multi-modal fusion:

```python
from collections import deque
import threading

class DataSynchronizer:
    def __init__(self, max_queue_size=10, time_tolerance=0.05):
        self.camera_queue = deque(maxlen=max_queue_size)
        self.lidar_queue = deque(maxlen=max_queue_size)
        self.radar_queue = deque(maxlen=max_queue_size)

        self.time_tolerance = time_tolerance  # seconds
        self.lock = threading.Lock()

    def add_camera_data(self, data, timestamp):
        """
        Add camera data with timestamp
        """
        with self.lock:
            self.camera_queue.append((data, timestamp))

    def add_lidar_data(self, data, timestamp):
        """
        Add LiDAR data with timestamp
        """
        with self.lock:
            self.lidar_queue.append((data, timestamp))

    def get_synchronized_data(self):
        """
        Get the best synchronized data from all sensors
        """
        with self.lock:
            if not self.camera_queue or not self.lidar_queue:
                return None, None, None

            # Find closest timestamps across sensors
            best_sync = None
            min_diff = float('inf')

            for cam_data, cam_time in self.camera_queue:
                for lidar_data, lidar_time in self.lidar_queue:
                    time_diff = abs((cam_time - lidar_time).nanoseconds / 1e9)

                    if time_diff < self.time_tolerance and time_diff < min_diff:
                        min_diff = time_diff
                        best_sync = (cam_data, lidar_data, cam_time)

            if best_sync:
                cam_data, lidar_data, timestamp = best_sync
                return cam_data, lidar_data, timestamp
            else:
                return None, None, None
```

## Practical Exercise: Building a Multi-Sensor Perception System

### Exercise Objective
Create a complete multi-sensor perception system that combines camera, LiDAR, and other sensor data for robust object detection and tracking.

### Steps:
1. Set up Isaac ROS perception nodes for different sensor types
2. Implement sensor fusion using appropriate algorithms
3. Create a unified detection and tracking system
4. Test the system with simulated or real sensor data
5. Evaluate the performance improvement from multi-sensor fusion
6. Analyze the system's robustness under different conditions

### Requirements:
- Isaac ROS perception packages installed
- Multi-modal sensor data (simulated or real)
- Working ROS 2 environment
- GPU for accelerated processing
- Evaluation metrics for performance assessment

### Expected Outcome:
A functional multi-modal perception system that demonstrates improved detection accuracy and robustness compared to single-sensor approaches.

## Performance Optimization

### GPU Acceleration Strategies

```python
class GPUPerceptionOptimizer:
    def __init__(self):
        # Use CUDA streams for parallel processing
        self.stream_detection = torch.cuda.Stream()
        self.stream_tracking = torch.cuda.Stream()
        self.stream_fusion = torch.cuda.Stream()

    def process_parallel(self, sensor_data):
        """
        Process different perception tasks in parallel using CUDA streams
        """
        with torch.cuda.stream(self.stream_detection):
            detections = self.run_detection_network(sensor_data['camera'])

        with torch.cuda.stream(self.stream_tracking):
            tracks = self.update_trackers(detections)

        with torch.cuda.stream(self.stream_fusion):
            fused_data = self.fuse_sensor_data(sensor_data)

        # Synchronize all streams
        torch.cuda.synchronize()

        return detections, tracks, fused_data
```

### Memory Management

```python
class MemoryEfficientPerception:
    def __init__(self, max_memory_mb=1000):
        self.max_memory = max_memory_mb * 1024 * 1024  # Convert to bytes
        self.tensor_cache = {}  # Cache for frequently used tensors

    def allocate_tensor(self, shape, dtype):
        """
        Efficiently allocate GPU tensors with caching
        """
        key = (shape, dtype)

        if key in self.tensor_cache:
            # Reuse cached tensor if available
            tensor = self.tensor_cache[key]
        else:
            # Create new tensor and cache it
            tensor = torch.zeros(shape, dtype=dtype, device='cuda')
            self.tensor_cache[key] = tensor

        return tensor
```

## Troubleshooting and Validation

### Common Issues

- **Sensor calibration**: Ensure all sensors are properly calibrated
- **Timing synchronization**: Verify timestamps are properly aligned
- **Coordinate frame alignment**: Check that all sensors use consistent frames
- **Performance bottlenecks**: Profile to identify slow components

### Validation Techniques

- **Ground truth comparison**: Compare against known object positions
- **Cross-validation**: Use different sensor combinations to verify consistency
- **Statistical analysis**: Analyze detection rates, false positives, etc.
- **Real-world testing**: Validate in actual operating environments

## Summary

Perception systems are fundamental to autonomous robotics, combining multiple sensor modalities to create a comprehensive understanding of the environment. Key aspects include:

- **Multi-modal integration**: Combining cameras, LiDAR, radar, and other sensors
- **Deep learning**: Using neural networks for object detection and classification
- **Sensor fusion**: Combining multiple sensor measurements optimally
- **Real-time processing**: Efficient algorithms for real-time operation
- **Robustness**: Handling various environmental conditions and sensor failures

Isaac ROS provides optimized implementations of perception algorithms that leverage GPU acceleration for superior performance, making complex perception systems practical for real-world robotics applications.

## Glossary Terms

- **Perception System**: Collection of sensors and algorithms that enable a robot to understand its environment
- **Sensor Fusion**: Process of combining data from multiple sensors to improve accuracy and robustness
- **Semantic Segmentation**: Pixel-level classification of image content
- **Instance Segmentation**: Identification and segmentation of individual object instances
- **Multi-modal Perception**: Using multiple types of sensors for comprehensive environment understanding
- **TensorRT**: NVIDIA's SDK for optimizing deep learning inference
- **Kalman Filter**: Optimal estimator for linear systems with Gaussian noise
- **Particle Filter**: Sequential Monte Carlo method for non-linear, non-Gaussian systems
- **Data Association**: Process of matching detections to existing tracks
- **Sensor Calibration**: Process of determining sensor parameters for accurate measurements