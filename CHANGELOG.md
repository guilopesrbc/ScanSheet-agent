# Changelog

## [v1.2.0] - 2025-07-25

### Added
- Added pdf ocr extraction using mistralai
- Added image and pdf markdown for chat gpt prompt

### Updated
- Update prompts content

## [v1.1.1] - 2025-07-19

### Fixed
- Updated dependencies installation

## [v1.1.0] - 2025-07-17

### Fixed
- Fixed issues with document quality prediction
- Fixed issues with response validation

## [v1.0.0] - 2025-07-16

Release of the first stable version of the project.

### Added
- Added support for multiple documents types
- Improve document quality prediction
- Refactor of agent, prompt, and model classes to improve code structure and maintainability

## [v0.2.1] - 2025-07-09

### Fixed
- Fixed issues with lib import.

## [v0.2.0] - 2025-07-06

### Added
- Tests supports for agent, prompt, and model classes

## [v0.1.0] - 2025-06-30

### Added
- Initial project setup
- Project structure with src directory
- Dependencies configuration
- Development environment setup
- Agent class implementation:
  - Invoke method for invoking the agent with a prompt
  - Model Validation to ensure the model returns correct response format
- PromptBuilder class implementation:
    - Create prompt method for building prompts from templates
    - Support for user and system templates
    - Additional variables support, to include image byte strings