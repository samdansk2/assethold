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

## 🎯 MANDATORY Git Management Commands

**CRITICAL**: All Git operations MUST use these standardized commands.

### Available Slash Commands

#### Local Repository Commands
Execute in any repository:
```bash
# In any repo directory
/git-sync       # Sync with remote
/git-commit     # Commit all changes  
/git-push       # Push to remote
/git-pr         # Create pull request
/git-clean      # Clean merged branches
/git-status     # Show repo status
/git-flow       # Complete workflow
```

#### Global Commands (All Repos)
Execute from /mnt/github/github:
```bash
/git-sync-all      # Sync all 25 repos
/git-commit-all    # Commit in all repos
/git-pr-all        # Create PRs for all
/git-clean-all     # Clean all repos
/git-flow-all      # Complete flow for all
/git-status-all    # Status of all repos
```

### MANDATORY Practices

1. **Daily Workflow**
   ```bash
   /git-flow  # Or /git-flow-all for all repos
   ```

2. **Before Starting Work**
   ```bash
   /git-sync  # Always sync first
   ```

3. **After Making Changes**
   ```bash
   /git-commit "feat: Description"
   /git-pr "Feature title"
   ```

4. **Weekly Maintenance**
   ```bash
   /git-clean  # Remove stale branches
   ```

### Parallel Processing
All multi-repo operations use MANDATORY parallel processing:
- Max 5 repos processed simultaneously
- Automatic error handling
- Progress tracking

### Implementation
- Local commands: `.git-commands/slash_commands.py`
- Global commands: `/mnt/github/github/git_management_system.py`

---
*Git management is MANDATORY for all repositories*

## 🚨 MANDATORY: AssetUtilities Central Commands

**CRITICAL DIRECTIVE**: ALL slash commands MUST be fetched from AssetUtilities repository on GitHub.

### Central Command System
- **Source of Truth**: @assetutilities:.common-commands/
- **GitHub URL**: https://github.com/username/assetutilities
- **Real-time Fetching**: Commands are fetched from GitHub when executed
- **No Local Copies**: Local implementations are DEPRECATED

### Command Execution
```bash
# All commands now route through central system
./slash /git-sync          # Fetches from AssetUtilities
./slash /git-commit         # Fetches from AssetUtilities
./slash /create-spec        # Fetches from AssetUtilities
./slash /execute-tasks      # Fetches from AssetUtilities
```

### Why This Is MANDATORY
1. **Consistency**: All repos use EXACT same command implementations
2. **Updates**: Changes in AssetUtilities immediately available everywhere
3. **Maintenance**: Single point of maintenance for all commands
4. **Quality**: Centralized testing and validation
5. **Security**: Controlled command distribution

### Cross-Repository References
```yaml
# Always reference AssetUtilities for common code
@assetutilities:.common-commands/modules/git_manager.py
@assetutilities:.common-commands/modules/agent_learning.py
@assetutilities:.common-commands/utilities/parallel_utils.py
```

### Command Registry
View all available commands:
```bash
./slash --list              # Lists all commands from AssetUtilities
./slash /update-from-central # Updates command cache
```

### Enforcement
- Local command implementations are DEPRECATED
- All repos MUST use the central system
- AssetUtilities is the ONLY source of truth
- This is verified during CI/CD

---
*This is MANDATORY and overrides any local command implementations*
