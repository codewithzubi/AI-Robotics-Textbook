---
id: 1
title: constitution-update
stage: constitution
date: 2025-12-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, textbook, ai, robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: Textbook — "Physical AI & Humanoid Robotics"

Core principles:
- Technical accuracy aligned with course curriculum (ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA)
- Educational clarity for students of AI, robotics, and computer science
- Modular structure matching Panaversity course outline (Modules 1–4 + Capstone)
- Reusability: content optimized for integration with Claude Code Subagents
- AI-native textbook design (supports RAG, translation, personalization)

Key standards:
- All factual claims must be grounded in robotics, AI, and simulation documentation
- Source verification using official docs (ROS 2, Gazebo, Unity, NVIDIA Isaac, OpenAI, Whisper)
- Writing level: Beginner-friendly but technically precise (Flesch-Kincaid grade 10-12)
- Explanations must include conceptual clarity + real-world examples
- Strict avoidance of hallucination; unverifiable robotics claims not allowed

Content structure requirements:
- Follow Panaversity Physical AI & Humanoid Robotics course flow:
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

Constraints:
- Minimum total content: 25,000–35,000 words
- Each module: at least 5 detailed chapters
- Must be fully compatible with Docusaurus docs format
- No code errors in examples (ROS 2, Python, simulation, VLA workflows)
- Must support future Urdu translation and personalization features

Success criteria:
- Book can be deployed on Docusaurus without structural issues
- RAG chatbot can answer all questions using book content
- All modules align with official course syllabus from Hackathon PDF
- Content is technically correct, verifiable, and logically organized
- Passes internal fact-checking for robotics & AI topics

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with the specified principles and requirements for the "Physical AI & Humanoid Robotics" textbook project. The constitution now includes:

- Core Principles: Technical Accuracy, Educational Clarity, Modular Structure, Reusability, AI-Native Design, and Source Verification
- Content Structure Requirements aligned with the Panaversity course flow
- Development Standards including writing level, verification requirements, and constraints
- Governance section with success criteria

The file is properly formatted with version 1.0.0, ratified and last amended on 2025-12-11.

## Outcome

- ✅ Impact: Created initial constitution for the Physical AI & Humanoid Robotics textbook project
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Can proceed with spec, plan, and task creation based on this constitution
- 🧠 Reflection: Constitution properly reflects the project requirements and can guide future development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All requirements implemented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating feature specifications based on constitution