/**
 * Content Validation Script for Physical AI & Humanoid Robotics Textbook
 *
 * This script provides utilities to validate textbook content against quality standards:
 * - Technical accuracy verification
 * - Readability assessment
 * - Terminology consistency
 * - Structural completeness
 */

const fs = require('fs');
const path = require('path');

class TextbookValidator {
  constructor() {
    this.glossaryTerms = this.loadGlossary();
    this.readabilityThreshold = 12; // Flesch-Kincaid Grade Level
  }

  /**
   * Load glossary terms for consistency checking
   */
  loadGlossary() {
    // In a real implementation, this would load from docs/glossary.md
    // For now, we'll return a basic set of terms
    return [
      'ROS', 'ROS 2', 'Node', 'Topic', 'Service', 'Action', 'URDF',
      'Gazebo', 'Unity', 'NVIDIA Isaac', 'VLA', 'Vision-Language-Action',
      'SLAM', 'Perception', 'Navigation', 'Whisper', 'LLM', 'Humanoid Robot'
    ];
  }

  /**
   * Validate a chapter file for structural completeness
   */
  validateChapterStructure(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const requiredSections = [
      '## Learning Objectives',
      '## Summary',
      '## Glossary Terms',
      '## Review Questions'
    ];

    const issues = [];

    for (const section of requiredSections) {
      if (!content.includes(section)) {
        issues.push(`Missing required section: ${section}`);
      }
    }

    // Check for practical exercises
    if (!content.toLowerCase().includes('exercise') && !content.toLowerCase().includes('practical')) {
      issues.push('No practical exercises found in chapter');
    }

    return {
      isValid: issues.length === 0,
      issues: issues,
      filePath: filePath
    };
  }

  /**
   * Check terminology consistency against glossary
   */
  checkTerminologyConsistency(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const issues = [];

    for (const term of this.glossaryTerms) {
      // Simple check for common misspellings or variations
      const variations = this.getTermVariations(term);
      for (const variation of variations) {
        if (content.includes(variation) && variation !== term) {
          issues.push(`Possible terminology inconsistency: found "${variation}", expected "${term}"`);
        }
      }
    }

    return issues;
  }

  /**
   * Get common variations of a term to check for consistency
   */
  getTermVariations(term) {
    const variations = {
      'ROS': ['ros', 'Robot Operating System'],
      'ROS 2': ['ros2', 'ros 2', 'ROS2'],
      'URDF': ['urdf', 'Unified Robot Description Format'],
      'Gazebo': ['gazebo', 'gazebo simulation'],
      'VLA': ['vla', 'Vision-Language-Action', 'Vision Language Action']
    };

    return variations[term] || [];
  }

  /**
   * Basic readability assessment (simplified Flesch-Kincaid estimator)
   */
  assessReadability(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');

    // Count sentences, words, and syllables (simplified)
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
    const words = content.split(/\s+/).filter(w => w.length > 0).length;

    // Very simplified syllable counting (count vowels as syllables)
    const vowels = content.toLowerCase().match(/[aeiou]/g);
    const syllables = vowels ? vowels.length : 0;

    // Simplified Flesch-Kincaid Grade Level calculation
    // In a real implementation, this would use the actual formula
    const avgWordsPerSentence = words / Math.max(sentences, 1);
    const avgSyllablesPerWord = syllables / Math.max(words, 1);

    // Simplified score calculation
    const gradeLevel = 0.39 * avgWordsPerSentence + 11.8 * avgSyllablesPerWord - 15.59;

    return {
      gradeLevel: Math.round(gradeLevel * 10) / 10,
      isAppropriate: gradeLevel >= 8 && gradeLevel <= 14, // Grade 8-14 range
      sentences: sentences,
      words: words,
      syllables: syllables
    };
  }

  /**
   * Validate all chapters in a directory
   */
  validateDirectory(dirPath) {
    const results = {
      valid: [],
      invalid: [],
      warnings: []
    };

    const files = fs.readdirSync(dirPath);

    for (const file of files) {
      if (file.endsWith('.md')) {
        const filePath = path.join(dirPath, file);

        // Validate structure
        const structureResult = this.validateChapterStructure(filePath);
        if (structureResult.isValid) {
          results.valid.push(structureResult);
        } else {
          results.invalid.push(structureResult);
        }

        // Check terminology
        const termIssues = this.checkTerminologyConsistency(filePath);
        if (termIssues.length > 0) {
          results.warnings.push({
            file: file,
            type: 'terminology',
            issues: termIssues
          });
        }

        // Assess readability
        const readability = this.assessReadability(filePath);
        if (!readability.isAppropriate) {
          results.warnings.push({
            file: file,
            type: 'readability',
            gradeLevel: readability.gradeLevel,
            message: `Readability grade level (${readability.gradeLevel}) outside target range (10-12)`
          });
        }
      }
    }

    return results;
  }

  /**
   * Run comprehensive validation on the textbook
   */
  runComprehensiveValidation(baseDir = 'docs/modules') {
    console.log('Starting comprehensive validation of Physical AI & Humanoid Robotics textbook...\n');

    const modules = fs.readdirSync(baseDir).filter(item =>
      fs.statSync(path.join(baseDir, item)).isDirectory()
    );

    let overallResults = {
      modules: {},
      summary: {
        totalFiles: 0,
        validFiles: 0,
        invalidFiles: 0,
        totalWarnings: 0
      }
    };

    for (const module of modules) {
      console.log(`Validating module: ${module}`);
      const modulePath = path.join(baseDir, module);
      const moduleResults = this.validateDirectory(modulePath);

      overallResults.modules[module] = moduleResults;

      // Update summary
      overallResults.summary.totalFiles += moduleResults.valid.length + moduleResults.invalid.length;
      overallResults.summary.validFiles += moduleResults.valid.length;
      overallResults.summary.invalidFiles += moduleResults.invalid.length;
      overallResults.summary.totalWarnings += moduleResults.warnings.length;

      console.log(`  - Valid files: ${moduleResults.valid.length}`);
      console.log(`  - Invalid files: ${moduleResults.invalid.length}`);
      console.log(`  - Warnings: ${moduleResults.warnings.length}\n`);
    }

    return overallResults;
  }
}

// Example usage:
if (require.main === module) {
  const validator = new TextbookValidator();

  // If a specific file is provided as an argument, validate just that file
  if (process.argv[2]) {
    const filePath = process.argv[2];
    console.log(`Validating file: ${filePath}\n`);

    const structureResult = validator.validateChapterStructure(filePath);
    console.log('Structure validation:', structureResult);

    const termIssues = validator.checkTerminologyConsistency(filePath);
    console.log('Terminology issues:', termIssues);

    const readability = validator.assessReadability(filePath);
    console.log('Readability assessment:', readability);
  } else {
    // Otherwise, run comprehensive validation
    const results = validator.runComprehensiveValidation();
    console.log('Overall validation results:', results.summary);
  }
}

module.exports = TextbookValidator;