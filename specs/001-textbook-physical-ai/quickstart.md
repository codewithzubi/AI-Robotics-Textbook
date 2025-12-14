# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Getting Started

This guide will help you begin working with the Physical AI & Humanoid Robotics textbook project. The textbook is structured as a Docusaurus-based documentation site with 4 core modules.

## Prerequisites

- Node.js (v16 or higher)
- Git
- Basic understanding of Markdown
- Access to ROS 2, Gazebo, Unity, and NVIDIA Isaac documentation

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies
```bash
cd my-website
npm install
```

### 3. Start Local Development Server
```bash
npm start
```
This will start a local development server at `http://localhost:3000`

## Textbook Structure

### Modules Overview
The textbook is organized into 4 core modules:

1. **Module 1: ROS 2 Foundations** - Core ROS 2 concepts, nodes, topics, services, URDF
2. **Module 2: Digital Twin Simulation** - Gazebo and Unity simulation environments
3. **Module 3: NVIDIA Isaac Robotics AI** - Isaac Sim, perception, navigation
4. **Module 4: Vision-Language-Action (VLA) Systems** - Multimodal robotics, LLM integration

### Content Format
All content is written in Docusaurus-compatible Markdown with the following structure per chapter:
- Learning objectives
- Concept explanations with real-world examples
- Step-by-step workflows
- Diagrams and visual aids
- Practical exercises
- Chapter summary
- Glossary terms

## Writing Guidelines

### Technical Accuracy
- Verify all technical claims against official documentation
- Use official terminology consistently
- Include working code examples where appropriate

### Educational Clarity
- Write at Flesch-Kincaid grade 10-12 level
- Use analogies and step-by-step breakdowns for complex concepts
- Include practical exercises to reinforce learning

### RAG Optimization
- Write concise, chunk-friendly sentences
- Use clear headings and subheadings
- Maintain consistent terminology across modules

## Building and Deployment

### Build for Production
```bash
npm run build
```

### Preview Build
```bash
npm run serve
```

## Quality Assurance

### Content Validation
- Run automated checks for technical accuracy
- Verify all links and cross-references
- Ensure consistent terminology usage
- Validate readability metrics

### Review Process
1. Self-review content for technical accuracy
2. Peer review for educational clarity
3. Cross-module consistency check
4. Final validation against official documentation