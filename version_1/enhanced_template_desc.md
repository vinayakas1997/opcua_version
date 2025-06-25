
## Clean Architecture Layers

### 1. Domain Layer (Innermost)
- **Purpose**: Contains enterprise-wide business rules
- **Dependencies**: None (pure business logic)
- **Components**: FINS protocol definitions, abstract interfaces

### 2. Application Layer
- **Purpose**: Contains application-specific business rules
- **Dependencies**: Domain layer only
- **Components**: Use cases that orchestrate domain objects

### 3. Infrastructure Layer
- **Purpose**: Contains implementation details
- **Dependencies**: Domain and Application layers
- **Components**: Concrete implementations of domain interfaces

### 4. Interface Layer (Outermost)
- **Purpose**: Contains controllers, presenters, and external interfaces
- **Dependencies**: All inner layers
- **Components**: CLI, API endpoints, UI components

## Installation

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
