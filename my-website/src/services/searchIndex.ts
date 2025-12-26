// Service to handle search indexing and searching of book content
import { sidebar } from '../../sidebars';

// Define the structure for indexed content
interface IndexedContent {
  id: string;
  title: string;
  content: string;
  url: string;
  type: 'heading' | 'content' | 'code' | 'glossary';
}

// Global variable to store the search index
let searchIndex: IndexedContent[] = [];
let indexLoaded = false;

// Function to load and build the search index from book content
export const loadSearchIndex = async (): Promise<IndexedContent[]> => {
  if (indexLoaded) {
    return searchIndex;
  }

  try {
    // This would normally be built during the build process, but for now we'll create a comprehensive index
    // representing the actual content of the textbook

    const mockIndex: IndexedContent[] = [
      // Introduction section
      {
        id: 'intro',
        title: 'Introduction to Physical AI & Humanoid Robotics',
        content: 'This textbook covers modern robotics, AI, and humanoid systems. It provides comprehensive coverage of ROS 2, digital twin simulation, NVIDIA Isaac AI, and Vision-Language-Action systems. The book is designed for students and professionals interested in understanding and implementing advanced robotics systems.',
        url: '/docs/intro',
        type: 'heading'
      },

      // Glossary and terminology
      {
        id: 'glossary-overview',
        title: 'Glossary Overview',
        content: 'This section provides definitions for key terms used throughout the textbook. Understanding these terms is essential for grasping the concepts covered in the book.',
        url: '/docs/glossary-overview',
        type: 'heading'
      },
      {
        id: 'terminology',
        title: 'Terminology',
        content: 'Standardized terminology used in robotics and AI. This includes definitions for terms like ROS, URDF, Gazebo, Isaac, VLA, and many others.',
        url: '/docs/terminology',
        type: 'heading'
      },

      // Module 1: ROS 2 Foundations
      {
        id: 'module-1-intro',
        title: 'Module 1: ROS 2 Foundations',
        content: 'ROS 2 (Robot Operating System 2) is the next generation robotics framework. It provides communication between different parts of a robot system, hardware abstraction, device drivers, libraries, and more.',
        url: '/docs/modules/module-1-ros-foundations',
        type: 'heading'
      },
      {
        id: 'chapter-1-introduction-to-ros',
        title: 'Chapter 1: Introduction to ROS',
        content: 'ROS (Robot Operating System) is flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.',
        url: '/docs/modules/module-1-ros-foundations/chapter-1-introduction-to-ros',
        type: 'heading'
      },
      {
        id: 'chapter-2-nodes-and-topics',
        title: 'Chapter 2: Nodes and Topics',
        content: 'Nodes are processes that perform computation. Topics are named buses over which nodes exchange messages. Publishers send messages to topics, and subscribers receive messages from topics. This provides a many-to-many communication mechanism.',
        url: '/docs/modules/module-1-ros-foundations/chapter-2-nodes-and-topics',
        type: 'heading'
      },
      {
        id: 'chapter-3-services-and-parameters',
        title: 'Chapter 3: Services and Parameters',
        content: 'Services provide a request/reply communication pattern. Parameters allow nodes to be configured at runtime. Services are synchronous, unlike the asynchronous nature of topics. Parameters are used for configuration that might change during runtime.',
        url: '/docs/modules/module-1-ros-foundations/chapter-3-services-and-parameters',
        type: 'heading'
      },
      {
        id: 'chapter-4-urdf-and-robot-modeling',
        title: 'Chapter 4: URDF and Robot Modeling',
        content: 'URDF (Unified Robot Description Format) is an XML format for representing a robot model. It describes the robot\'s physical and visual properties, joints, and kinematic chains. URDF is essential for simulation and visualization of robots.',
        url: '/docs/modules/module-1-ros-foundations/chapter-4-urdf-and-robot-modeling',
        type: 'heading'
      },
      {
        id: 'chapter-5-ros2-programming',
        title: 'Chapter 5: ROS 2 Programming',
        content: 'Programming with ROS 2 involves creating nodes, publishers, subscribers, services, and actions. This chapter covers the practical aspects of developing ROS 2 applications using C++ and Python.',
        url: '/docs/modules/module-1-ros-foundations/chapter-5-ros2-programming',
        type: 'heading'
      },

      // Module 2: Digital Twin Simulation
      {
        id: 'module-2-intro',
        title: 'Module 2: Digital Twin Simulation',
        content: 'Digital twin simulation is the process of creating a virtual replica of a physical system. This module covers Gazebo simulation, Unity robotics, sensor simulation, and simulation best practices.',
        url: '/docs/modules/module-2-digital-twin-simulation',
        type: 'heading'
      },
      {
        id: 'chapter-2-1-gazebo-simulation',
        title: 'Chapter 1: Gazebo Simulation',
        content: 'Gazebo is a 3D simulation environment for robotics. It provides realistic physics simulation, high-quality graphics, and interfaces for various robot platforms and sensors. Gazebo is widely used for testing robotics algorithms before deployment on real robots.',
        url: '/docs/modules/module-2-digital-twin-simulation/chapter-1-gazebo-simulation',
        type: 'heading'
      },
      {
        id: 'chapter-2-2-unity-robotics',
        title: 'Chapter 2: Unity Robotics',
        content: 'Unity provides a powerful platform for robotics simulation with its physics engine, rendering capabilities, and asset ecosystem. The Unity Robotics Hub provides tools and packages for robotics simulation and development.',
        url: '/docs/modules/module-2-digital-twin-simulation/chapter-2-unity-robotics',
        type: 'heading'
      },
      {
        id: 'chapter-2-3-sensor-simulation',
        title: 'Chapter 3: Sensor Simulation',
        content: 'Simulating sensors is crucial for developing perception algorithms. This includes cameras, LIDAR, IMU, GPS, and other sensors. Proper sensor simulation allows for testing in various environmental conditions.',
        url: '/docs/modules/module-2-digital-twin-simulation/chapter-3-sensor-simulation',
        type: 'heading'
      },

      // Module 3: NVIDIA Isaac Robotics AI
      {
        id: 'module-3-intro',
        title: 'Module 3: NVIDIA Isaac Robotics AI',
        content: 'NVIDIA Isaac is a robotics platform that combines hardware and software to accelerate AI-powered robotics. It includes Isaac Sim, Isaac ROS, and various perception and navigation capabilities.',
        url: '/docs/modules/module-3-nvidia-isaac-ai',
        type: 'heading'
      },
      {
        id: 'chapter-3-1-isaac-sim-overview',
        title: 'Chapter 1: Isaac Sim Overview',
        content: 'Isaac Sim is NVIDIA\'s robotics simulator based on Omniverse. It provides high-fidelity simulation for training and testing AI-based robotics applications. Isaac Sim integrates with ROS and ROS 2 for seamless development workflows.',
        url: '/docs/modules/module-3-nvidia-isaac-ai/chapter-1-isaac-sim-overview',
        type: 'heading'
      },
      {
        id: 'chapter-3-2-isaac-ros-components',
        title: 'Chapter 2: Isaac ROS Components',
        content: 'Isaac ROS provides accelerated perception and navigation capabilities optimized for NVIDIA hardware. It includes hardware-accelerated packages for SLAM, perception, and navigation that run efficiently on Jetson and other NVIDIA platforms.',
        url: '/docs/modules/module-3-nvidia-isaac-ai/chapter-2-isaac-ros-components',
        type: 'heading'
      },
      {
        id: 'chapter-3-3-vslam-navigation',
        title: 'Chapter 3: Visual SLAM Navigation',
        content: 'Visual SLAM (Simultaneous Localization and Mapping) uses cameras to create maps of the environment while tracking the robot\'s position. This chapter covers ORB-SLAM, RTAB-Map, and other visual SLAM approaches.',
        url: '/docs/modules/module-3-nvidia-isaac-ai/chapter-3-vslam-navigation',
        type: 'heading'
      },

      // Module 4: Vision-Language-Action Systems
      {
        id: 'module-4-intro',
        title: 'Module 4: Vision-Language-Action Systems',
        content: 'Vision-Language-Action systems combine computer vision, natural language processing, and robotic control. These systems enable robots to understand natural language commands and perform complex tasks.',
        url: '/docs/modules/module-4-vla-systems',
        type: 'heading'
      },
      {
        id: 'chapter-4-1-vla-introduction',
        title: 'Chapter 1: VLA Introduction',
        content: 'Vision-Language-Action models represent a new paradigm in robotics where a single model can perceive the environment, understand language commands, and execute appropriate actions. These models enable more natural human-robot interaction.',
        url: '/docs/modules/module-4-vla-systems/chapter-1-vla-introduction',
        type: 'heading'
      },
      {
        id: 'chapter-4-2-whisper-integration',
        title: 'Chapter 2: Whisper Integration',
        content: 'OpenAI\'s Whisper model can be integrated into robotics systems for voice command recognition. This enables natural language interaction with robots in various environments. The integration requires proper audio preprocessing and command parsing.',
        url: '/docs/modules/module-4-vla-systems/chapter-2-whisper-integration',
        type: 'heading'
      },
      {
        id: 'chapter-4-3-llm-planning',
        title: 'Chapter 3: Large Language Model Planning',
        content: 'Large language models can be used for high-level task planning in robotics. They can decompose complex tasks into executable steps and handle natural language instructions. This chapter covers prompt engineering for robotics applications.',
        url: '/docs/modules/module-4-vla-systems/chapter-3-llm-planning',
        type: 'heading'
      },
      {
        id: 'chapter-4-5-humanoid-control',
        title: 'Chapter 5: Humanoid Robot Control',
        content: 'Humanoid robots require sophisticated control systems to maintain balance and perform human-like movements. This involves inverse kinematics, balance control, and gait generation. Advanced control algorithms are needed for stable locomotion.',
        url: '/docs/modules/module-4-vla-systems/chapter-5-humanoid-control',
        type: 'heading'
      },

      // Capstone Project
      {
        id: 'capstone-intro',
        title: 'Capstone Project: Integrated AI Robotics System',
        content: 'The capstone project integrates concepts from all modules to create a complete AI-powered robotic system. Students will design, implement, and test a robotic system that demonstrates the principles learned throughout the textbook.',
        url: '/docs/capstone',
        type: 'heading'
      },

      // Additional content
      {
        id: 'accessibility',
        title: 'Accessibility in Robotics',
        content: 'Designing accessible robotics interfaces and systems that can be used by people with diverse abilities. This includes considerations for visual, auditory, and motor accessibility in robotics applications.',
        url: '/docs/accessibility',
        type: 'heading'
      },
      {
        id: 'search-configuration',
        title: 'Search Functionality Configuration',
        content: 'This document outlines the search functionality configuration implemented in the Physical AI & Humanoid Robotics textbook to enable effective content discovery and navigation.',
        url: '/docs/search-configuration',
        type: 'heading'
      }
    ];

    searchIndex = mockIndex;
    indexLoaded = true;

    return searchIndex;
  } catch (error) {
    console.error('Error loading search index:', error);
    return [];
  }
};

// Function to search the content index with better relevance scoring
export const searchContent = async (query: string): Promise<IndexedContent[]> => {
  if (!indexLoaded) {
    await loadSearchIndex();
  }

  if (!query.trim()) {
    return [];
  }

  const queryLower = query.toLowerCase();
  const searchTerms = queryLower.split(/\s+/).filter(term => term.length > 0);

  // Calculate relevance score for each item
  const scoredResults = searchIndex.map(item => {
    let score = 0;
    const titleLower = item.title.toLowerCase();
    const contentLower = item.content.toLowerCase();

    // Score based on title matches (higher weight)
    for (const term of searchTerms) {
      if (titleLower.includes(term)) {
        score += 10; // Higher weight for title matches
      }
      // Count occurrences in title
      const titleMatches = (titleLower.match(new RegExp(term, 'g')) || []).length;
      score += titleMatches * 5;
    }

    // Score based on content matches (lower weight)
    for (const term of searchTerms) {
      if (contentLower.includes(term)) {
        score += 1; // Lower weight for content matches
      }
      // Count occurrences in content
      const contentMatches = (contentLower.match(new RegExp(term, 'g')) || []).length;
      score += contentMatches * 0.5;
    }

    return { item, score };
  });

  // Sort by score in descending order and return the items
  return scoredResults
    .filter(result => result.score > 0)
    .sort((a, b) => b.score - a.score)
    .map(result => result.item);
};

// Define structure for search suggestions with more details
export interface SearchSuggestion {
  title: string;
  contentPreview: string;
  url: string;
}

// Function to get suggestions based on query with better relevance
export const getSuggestions = async (query: string): Promise<string[]> => {
  if (!query.trim()) {
    return [];
  }

  const results = await searchContent(query);

  // Return titles of matching content as suggestions, with the most relevant first
  return results.slice(0, 5).map(item => item.title);
};

// Function to get detailed suggestions with content preview
export const getDetailedSuggestions = async (query: string): Promise<SearchSuggestion[]> => {
  if (!query.trim()) {
    return [];
  }

  const results = await searchContent(query);

  // Return detailed suggestions with content preview
  return results.slice(0, 5).map(item => ({
    title: item.title,
    contentPreview: item.content.length > 100 ? item.content.substring(0, 100) + '...' : item.content,
    url: item.url
  }));
};

// Function to get content by URL for direct navigation
export const getContentByUrl = async (url: string): Promise<IndexedContent | undefined> => {
  if (!indexLoaded) {
    await loadSearchIndex();
  }

  return searchIndex.find(item => item.url === url);
};

// Function to get content by ID for navigation
export const getContentById = async (id: string): Promise<IndexedContent | undefined> => {
  if (!indexLoaded) {
    await loadSearchIndex();
  }

  return searchIndex.find(item => item.id === id);
};