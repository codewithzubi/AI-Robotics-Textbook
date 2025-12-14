<!-- SYNC IMPACT REPORT
Version change: N/A → 1.0.0
List of modified principles: N/A (initial constitution)
Added sections: All principles and sections (initial constitution)
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/commands/*.md: ⚠ pending
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics textbook Constitution

## Core Principles

### Technical Accuracy
Technical accuracy aligned with course curriculum (ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA)

### Educational Clarity
Educational clarity for students of AI, robotics, and computer science

### Modular Structure
Modular structure matching Panaversity course outline (Modules 1–4 + Capstone)

### Reusability
Reusability: content optimized for integration with Claude Code Subagents

### AI-Native Design
AI-native textbook design (supports RAG, translation, personalization)

### Source Verification
All factual claims must be grounded in robotics, AI, and simulation documentation; Source verification using official docs (ROS 2, Gazebo, Unity, NVIDIA Isaac, OpenAI, Whisper)

## Content Structure Requirements

Follow Panaversity Physical AI & Humanoid Robotics course flow:
  * Module 1: ROS 2 (Nodes, Topics, Services, URDF, rclpy)
  * Module 2: Digital Twin Simulation (Gazebo, Unity, sensors)
  * Module 3: NVIDIA Isaac (Sim, Isaac ROS, VSLAM, navigation)
  * Module 4: VLA systems (Whisper, LLM planning, multimodal robotics)
  * Capstone: Autonomous Humanoid Robot project
- Include learning outcomes for all modules
- Include diagrams, examples, definitions, and step-by-step workflows

RAG & AI integration standards:
- Chapters must be structured for optimal vector retrieval
- Sentences clear and chunk-friendly (no long paragraphs)
- Embed metadata for Qdrant-compatible semantic chunks
- Maintain consistent terminology for ROS, simulation, and VLA concepts

## Development Standards

Writing level: Beginner-friendly but technically precise (Flesch-Kincaid grade 10-12)
Explanations must include conceptual clarity + real-world examples
Strict avoidance of hallucination; unverifiable robotics claims not allowed

Constraints:
- Minimum total content: 25,000–35,000 words
- Each module: at least 5 detailed chapters
- Must be fully compatible with Docusaurus docs format
- No code errors in examples (ROS 2, Python, simulation, VLA workflows)
- Must support future Urdu translation and personalization features

## Governance

All content must align with official course syllabus from Hackathon PDF
Content is technically correct, verifiable, and logically organized
Passes internal fact-checking for robotics & AI topics
Success criteria:
- Book can be deployed on Docusaurus without structural issues
- RAG chatbot can answer all questions using book content
- All modules align with official course syllabus from Hackathon PDF

**Version**: 1.0.0 | **Ratified**
: 2025-12-11 | **Last Amended**: 2025-12-11