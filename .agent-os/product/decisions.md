# AssetHold Technical Decisions

## Architecture Decisions

### Modular Engine Design
**Decision**: Implemented a central engine with module-specific routers
**Rationale**: Enables easy extension of analysis capabilities while maintaining consistent configuration and data handling patterns
**Implementation**: `engine.py` serves as the main entry point, delegating to module routers (stocks, portfolio, etc.)

### YAML-based Configuration
**Decision**: Use YAML files for all configuration and test specifications
**Rationale**: Human-readable, version-controllable, and flexible for complex nested configurations
**Implementation**: `ymlInput` utility handles YAML parsing with `AttributeDict` for dynamic access

### Poetry for Dependency Management
**Decision**: Chose Poetry over pip/requirements.txt
**Rationale**: Better dependency resolution, lock files for reproducible builds, and integrated packaging
**Current State**: Minimal dependencies in pyproject.toml, room for growth

### Custom Utility Library
**Decision**: Separate `assetutilities` library for common functionality
**Rationale**: Reusable components across multiple projects, cleaner separation of concerns
**Implementation**: Local development dependency with utilities for data handling, file management

## Data Management Decisions

### File-based Data Storage
**Decision**: Use local files (CSV, JSON) for data persistence
**Rationale**: Simple deployment, no database dependencies, easy backup and version control
**Trade-offs**: Limited scalability but appropriate for current user base

### Multiple Data Source Strategy
**Decision**: Support multiple financial data providers
**Rationale**: Reduces dependency on single provider, enables data validation through comparison
**Implementation**: Abstracted data access through common interfaces

## Development Process Decisions

### Comprehensive Testing Strategy
**Decision**: Extensive test suite with YAML-based test fixtures
**Rationale**: Financial calculations require high accuracy, test fixtures enable easy test case management
**Implementation**: Separate test modules mirroring source structure

### Legacy Code Preservation
**Decision**: Keep legacy Flask application in codebase
**Rationale**: Preserve working web interface while developing new architecture
**Location**: `src/assethold/legacy_code/`

## Feature Implementation Decisions

### Technical Analysis Focus
**Decision**: Prioritize technical indicators over fundamental analysis
**Rationale**: Aligns with target user needs for trend-based investment decisions
**Current State**: Multiple indicators implemented (CFM, EOM, volatility, strength)

### Insider Trading Analysis
**Decision**: Comprehensive insider trading tracking and analysis
**Rationale**: Valuable signal for individual investors, differentiates from basic charting tools
**Implementation**: Timeline, relation-based, and volume analysis

### Real Estate Module Inclusion
**Decision**: Include real estate analysis alongside stock analysis
**Rationale**: Supports holistic investment approach for target users
**Scope**: Commercial and residential property analysis tools

## Future Architecture Considerations

### Scalability Preparation
- Modular design enables easy addition of new analysis types
- Router pattern supports performance optimization through caching
- Configuration system can adapt to more complex requirements

### Integration Readiness
- Clean module boundaries enable API development
- Data abstractions support multiple storage backends
- Testing framework scales with feature additions

### Performance Optimization
- File-based storage allows for caching strategies
- Modular architecture enables selective loading
- YAML configuration supports performance tuning parameters