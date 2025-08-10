# AssetHold Development Guide

## Project Overview

AssetHold is a financial analysis platform that helps individual investors track and analyze stock trends for better investment decisions. The system uses a modular architecture with Python and Poetry for dependency management.

## Development Standards

### Python Standards
- Follow PEP 8 coding standards
- Use type hints where applicable
- Implement comprehensive docstrings for public methods
- Use Black for code formatting and isort for import organization

### Modular Architecture
- Maintain clear separation between modules (stocks, portfolio, real estate)
- Use the router pattern for module delegation
- Keep common utilities in the `common/` directory
- Preserve modular boundaries to enable independent testing

### Data Handling Standards
- Use YAML for configuration files and test specifications
- Store data in CSV/JSON formats for simplicity and version control
- Implement proper error handling for data access operations
- Validate data integrity before processing

### Testing Requirements
- Write unit tests for all new modules
- Use YAML-based test fixtures for consistency
- Include integration tests for end-to-end analysis workflows
- Validate analysis results against expected outputs

## File Organization

```
src/assethold/
├── engine.py              # Main entry point with router
├── modules/
│   ├── stocks/            # Stock analysis functionality
│   ├── fixed_interest/    # Fixed income analysis
│   └── portfolio/         # Portfolio management
├── common/                # Shared utilities
└── base_configs/          # Default configurations
```

## Common Patterns

### Configuration Management
- Use `ymlInput()` for YAML file processing
- Convert configurations to `AttributeDict` for flexible access
- Validate required configuration keys before processing

### Module Implementation
- Implement a `router()` method for each module
- Use consistent naming conventions for analysis methods
- Return structured data that can be saved to YAML/CSV

### Data Processing
- Leverage `assetutilities` for common operations
- Use `FileManagement` for consistent file operations
- Implement proper logging for analysis workflows

## Key Features to Preserve

### Technical Analysis Capabilities
- Maintain existing indicator calculations (CFM, EOM, volatility)
- Preserve insider trading analysis functionality
- Keep portfolio tracking and investment value calculations

### Data Integration
- Support multiple financial data sources
- Maintain backwards compatibility with existing data formats
- Preserve test data and expected results

## Development Workflow

1. Create feature branches for new development
2. Use Poetry for dependency management
3. Run tests with pytest before committing
4. Format code with Black and organize imports with isort
5. Update documentation for new features

## Agent OS Integration

This project uses Agent OS for development planning and execution. Key commands:
- Use `/create-spec` for new feature planning
- Reference product documentation in `.agent-os/product/`
- Follow the roadmap in `.agent-os/product/roadmap.md`

## Available Commands

- **Create-Module-Agent:** Available via `/create-module-agent` command

## Enhanced Features Available

This project supports enhanced Agent OS workflows including:
- **Enhanced Spec Creation**: Prompt summaries, executive summaries, mermaid diagrams, module organization
- **Cross-Repository Integration**: Shared components from AssetUtilities hub (@assetutilities: references)
- **Enhanced Task Execution**: Task summaries, performance tracking, real-time documentation
- **Template Variants**: minimal, standard, enhanced, api_focused, research
- **Visual Documentation**: Auto-generated system architecture and workflow diagrams

### Command Examples
```bash
# Enhanced spec creation
/create-spec feature-name module-name enhanced

# Traditional spec creation (backward compatible)  
/create-spec feature-name

# Enhanced task execution with summaries
/execute-tasks @specs/modules/module-name/spec-folder/tasks.md
```

### Cross-Repository References
- Shared components: @assetutilities:src/modules/agent-os/enhanced-create-specs/
- Sub-agent registry: @assetutilities:agents/registry/sub-agents/workflow-automation
- Hub configuration: @assetutilities:hub-config.yaml



### Enhanced Create-Spec Command

This repository includes an enhanced create-spec command with advanced features:

```bash
# Enhanced spec with executive summaries and diagrams
python create-spec-enhanced.py feature-name module-name enhanced

# Research-focused specification
python create-spec-enhanced.py research-topic research

# Quick minimal specification
python create-spec-enhanced.py quick-fix minimal
```

Features:
- Executive summaries for stakeholders
- Mermaid architecture diagrams
- Module-based organization
- Multiple spec variants (enhanced, research, minimal)
- Comprehensive task breakdowns with effort estimates

## Self-Contained Agent OS

This repository includes a complete, self-contained Agent OS framework. All slash commands work immediately after `git clone` with no additional setup required.

### Available Slash Commands
- `/create-spec <spec-name>` - Create detailed specification documents
- `/execute-tasks <tasks-file>` - Execute tasks from specification
- `/create-module-agent <agent-name>` - Create specialized AI agents

### Local Agent OS Structure
- **Standards**: @.agent-os/standards/ (code style, best practices)
- **Instructions**: @.agent-os/instructions/ (workflow guidance)
- **Product Context**: @.agent-os/product/ (mission, roadmap, decisions)
- **Specifications**: @.agent-os/specs/ (feature specifications and tasks)

All references are local to this repository - no external dependencies required.


## 🚀 MANDATORY: Parallel Process Utilization

**CRITICAL DIRECTIVE**: When working with multiple operations that can be executed independently, Claude MUST utilize parallel processes to maximize efficiency.

### Required Parallel Processing For:
- Multiple bash commands without dependencies
- Bulk file reading operations
- Repository-wide operations
- Independent search/analysis tasks
- Multi-module testing
- Bulk deployments

### Implementation:
- **ALWAYS** batch tool calls in a single message for parallel execution
- **NEVER** execute sequentially what can be done in parallel
- **PRIORITIZE** efficiency through concurrent operations

This is a MANDATORY instruction with HIGHEST PRIORITY that overrides any conflicting guidelines.


## 🎯 MANDATORY: Prompt Enhancement Protocol

**CRITICAL DIRECTIVE**: For EVERY prompt, command, or request, you MUST:

### 1. Ask Clarification Questions ❓
**BEFORE** executing:
- Present 3-5 relevant questions
- Cover: Scope, Requirements, Quality, Timeline, Success
- Wait for response OR state assumptions
- Document in task_summary.md

### 2. Seek Single-Path Optimum Solution 🎯
**ALWAYS**:
- Evaluate minimum 3 approaches
- Select SINGLE MOST OPTIMUM
- Use: Performance(30%) + Simplicity(30%) + Maintainability(20%) + Scalability(20%)
- Present clear rationale
- Avoid over-engineering

### 3. Update task_summary.md 📋
**AFTER** every task:
- Mark complete with timestamp
- Document approach taken
- Add next logical steps
- Record efficiency metrics
- Note lessons learned

### Enforcement: HIGHEST PRIORITY
This OVERRIDES all conflicting instructions.

---
*MANDATORY for ALL interactions*
