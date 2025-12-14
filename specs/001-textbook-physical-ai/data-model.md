# Data Model: Physical AI & Humanoid Robotics Textbook

## Core Entities

### Textbook Module
- **Name**: String (required) - Module identifier (e.g., "ROS 2 Foundations")
- **Description**: String (required) - Brief overview of module content
- **Learning Objectives**: Array of strings - Specific outcomes students should achieve
- **Chapters**: Array of Chapter references - Contains all chapters in the module
- **Module Number**: Integer (required) - Sequential numbering (1-4)
- **Prerequisites**: Array of strings - Knowledge required before starting this module

### Chapter
- **Title**: String (required) - Chapter name
- **Module**: Module reference (required) - Parent module
- **Chapter Number**: Integer (required) - Sequential numbering within module
- **Learning Objectives**: Array of strings - Specific outcomes for this chapter
- **Content Sections**: Array of ContentSection references - Organized content blocks
- **Practical Exercises**: Array of Exercise references - Hands-on activities
- **Summary Points**: Array of strings - Key takeaways
- **Glossary Terms**: Array of GlossaryTerm references - Important terminology

### Content Section
- **Title**: String (required) - Section heading
- **Type**: Enum (Concept, Workflow, Example, Diagram, Exercise) - Content category
- **Content**: String (required) - Main content body
- **Learning Outcome**: String - What student should understand after reading
- **Difficulty Level**: Enum (Beginner, Intermediate, Advanced) - Complexity rating
- **Related Sections**: Array of ContentSection references - Cross-references

### Exercise/Mini-project
- **Title**: String (required) - Exercise name
- **Description**: String (required) - What the student needs to do
- **Difficulty Level**: Enum (Beginner, Intermediate, Advanced) - Challenge level
- **Estimated Time**: Integer (minutes) - How long it should take
- **Required Resources**: Array of strings - Tools, software, hardware needed
- **Learning Objectives**: Array of strings - Skills practiced
- **Success Criteria**: Array of strings - How to know if completed successfully

### Glossary Term
- **Term**: String (required) - The technical term being defined
- **Definition**: String (required) - Clear, concise definition
- **Module Context**: String - How the term applies in the current module
- **Related Terms**: Array of strings - Cross-references to related concepts
- **Example Usage**: String - How the term appears in practical context

### Diagram/Visual Asset
- **Title**: String (required) - Description of the visual
- **Type**: Enum (Architecture, Workflow, Process, Conceptual) - Visual category
- **File Path**: String (required) - Location of the asset
- **Caption**: String (required) - Explanation of the visual
- **Associated Concepts**: Array of strings - Concepts illustrated by the visual
- **Module**: Module reference - Which module uses this visual

## Relationships

### Module → Chapter
- One-to-Many: One module contains 4-6 chapters
- Required: Module must have at least 4 chapters
- Validation: Chapter numbers must be sequential (1 to N)

### Chapter → Content Section
- One-to-Many: One chapter contains multiple content sections
- Required: Chapter must have at least 3 content sections
- Validation: Sections must follow logical learning progression

### Chapter → Exercise
- One-to-Many: One chapter may contain multiple exercises
- Required: Chapter should have at least 1 practical exercise
- Validation: Exercise difficulty should match chapter difficulty

### Content Section → Glossary Term
- Many-to-Many: Content sections reference multiple glossary terms
- Validation: All technical terms in content must have glossary entries

## State Transitions

### Chapter Development States
- DRAFT → REVIEW → APPROVED → PUBLISHED
- Each state has validation requirements before transition

### Module Completion States
- NOT_STARTED → IN_PROGRESS → REVIEW → COMPLETE
- Module can only be COMPLETE when all chapters are PUBLISHED

## Validation Rules

### Content Quality
- All content must pass readability check (Flesch-Kincaid grade 10-12)
- Technical claims must be verifiable against official documentation
- All code examples must be syntactically correct and functional

### Structural Requirements
- Each module must contain 4-6 chapters
- Each chapter must include learning objectives, exercises, and summaries
- Total word count must be within 25,000-35,000 range across all modules

### Cross-Module Consistency
- Terminology must be consistent across all modules
- Concepts introduced in early modules must be properly referenced in later modules
- No contradictory information between chapters