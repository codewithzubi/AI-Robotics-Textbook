import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  textbookSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'intro',
        'glossary-overview',
        'terminology',
        'cross-references',
        'rag-optimization',
        'accessibility',
        'search-configuration',
        'readability-validation',
        'word-count-verification',
        'quality-assurance',
        'deployment-testing',
        'implementation-summary'
      ],
      link: {
        type: 'doc',
        id: 'intro',
      },
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 Foundations',
      collapsible: true,
      collapsed: false,
      items: [
        'modules/module-1-ros-foundations/index',
        'modules/module-1-ros-foundations/chapter-1-introduction-to-ros',
        'modules/module-1-ros-foundations/chapter-2-nodes-and-topics',
        'modules/module-1-ros-foundations/chapter-3-services-and-parameters',
        'modules/module-1-ros-foundations/chapter-4-urdf-and-robot-modeling',
        'modules/module-1-ros-foundations/chapter-5-ros2-programming',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin Simulation',
      collapsible: true,
      collapsed: true,
      items: [
        'modules/module-2-digital-twin-simulation/index',
        'modules/module-2-digital-twin-simulation/chapter-1-gazebo-simulation',
        'modules/module-2-digital-twin-simulation/chapter-2-unity-robotics',
        'modules/module-2-digital-twin-simulation/chapter-3-sensor-simulation',
        'modules/module-2-digital-twin-simulation/chapter-4-digital-twin-workflows',
        'modules/module-2-digital-twin-simulation/chapter-5-simulation-best-practices',
        'modules/module-2-digital-twin-simulation/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac Robotics AI',
      collapsible: true,
      collapsed: true,
      items: [
        'modules/module-3-nvidia-isaac-ai/index',
        'modules/module-3-nvidia-isaac-ai/chapter-1-isaac-sim-overview',
        'modules/module-3-nvidia-isaac-ai/chapter-2-isaac-ros-components',
        'modules/module-3-nvidia-isaac-ai/chapter-3-vslam-navigation',
        'modules/module-3-nvidia-isaac-ai/chapter-4-perception-systems',
        'modules/module-3-nvidia-isaac-ai/chapter-5-navigation-planning',
        'modules/module-3-nvidia-isaac-ai/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) Systems',
      collapsible: true,
      collapsed: true,
      items: [
        'modules/module-4-vla-systems/index',
        'modules/module-4-vla-systems/chapter-1-vla-introduction',
        'modules/module-4-vla-systems/chapter-2-whisper-integration',
        'modules/module-4-vla-systems/chapter-3-llm-planning',
        'modules/module-4-vla-systems/chapter-4-multimodal-robotics',
        'modules/module-4-vla-systems/chapter-5-humanoid-control',
        'modules/module-4-vla-systems/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      collapsible: true,
      collapsed: true,
      items: [
        'capstone/index',
        'capstone/project-overview',
        'capstone/implementation-guide',
        'capstone/evaluation-criteria',
      ],
    },
  ],
};

export default sidebars;
