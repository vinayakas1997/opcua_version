# FINS Protocol Library Architecture v2

## Overview
This project implements a FINS (Factory Interface Network Service) protocol library using Clean Architecture principles, ensuring separation of concerns and testability.

## Directory Structure

```
your_project/
│
├── app/                         # Application-specific logic (use cases)
│   └── use_cases/
│       ├── __init__.py
│       ├── read_values.py       # Read operations from PLC
│       ├── write_values.py      # Write operations to PLC
│       ├── connection_manager.py # Connection lifecycle management
│       └── data_converter.py    # Data type conversions
│
├── domain/                      # Enterprise-wide business rules
│   └── fins/
│       ├── __init__.py
│       ├── command_codes.py     # FINS command definitions
│       ├── connection.py        # Abstract FinsConnection interface
│       ├── frames.py           # Protocol frame structures
│       ├── memory_areas.py     # PLC memory area definitions
│       ├── response_codes.py   # FINS response code mappings
│       ├── utils.py           # Domain utilities (reverse_word_order, etc.)
│       └── exceptions.py      # Domain-specific exceptions
│
├── infrastructure/             # Implementation details & external concerns
│   └── fins/
│       ├── __init__.py
│       ├── tcp_connection.py   # TCP/IP implementation of FinsConnection
│       ├── udp_connection.py   # UDP implementation of FinsConnection
│       ├── mock_connection.py  # Test doubles for development
│       └── serial_connection.py # Serial communication implementation
│
├── interface/                  # Interface adapters (UI, CLI, API)
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py            # CLI entry point
│   │   └── commands.py        # CLI command definitions
│   ├── api/
│   │   ├── __init__.py
│   │   ├── rest_api.py        # REST API endpoints
│   │   └── schemas.py         # API request/response schemas
│   └── config/
│       ├── __init__.py
│       └── settings.py        # Configuration management
│
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_domain/
│   │   │   ├── test_frames.py
│   │   │   ├── test_command_codes.py
│   │   │   └── test_utils.py
│   │   ├── test_app/
│   │   │   ├── test_read_values.py
│   │   │   └── test_write_values.py
│   │   └── test_infrastructure/
│   │       ├── test_tcp_connection.py
│   │       └── test_mock_connection.py
│   ├── integration/
│   │   ├── test_end_to_end.py
│   │   └── test_plc_communication.py
│   └── fixtures/
│       ├── __init__.py
│       └── sample_data.py
│
├── docs/                       # Documentation
│   ├── api.md
│   ├── examples.md
│   └── protocol_reference.md
│
├── examples/                   # Usage examples
│   ├── basic_read_write.py
│   ├── async_operations.py
│   └── configuration_examples.py
│
├── __init__.py
├── pyproject.toml             # Modern Python packaging
├── README.md
└── CHANGELOG.md
```

## Component Migration Map

| Component                                             | Current Location | New Location                          | Notes                                    |
| ----------------------------------------------------- | ---------------- | ------------------------------------- | ---------------------------------------- |
| `FinsCommandCode`                                     | TBD              | `domain/fins/command_codes.py`        | Enum-based command definitions           |
| `FinsResponseEndCode`                                 | TBD              | `domain/fins/response_codes.py`       | Response code mappings and descriptions  |
| `FinsHeader`, `FinsCommandFrame`, `FinsResponseFrame` | TBD              | `domain/fins/frames.py`               | Protocol frame data structures           |
| `FinsPLCMemoryAreas`                                  | TBD              | `domain/fins/memory_areas.py`         | Memory area definitions and validations  |
| `FinsConnection` (Abstract)                           | TBD              | `domain/fins/connection.py`           | Abstract base class/interface            |
| `reverse_word_order`                                  | TBD              | `domain/fins/utils.py`                | Domain utility functions                 |
| TCP Implementation                                    | TBD              | `infrastructure/fins/tcp_connection.py` | Concrete TCP connection implementation   |
| Error Handling                                        | TBD              | `domain/fins/exceptions.py`          | Custom exception hierarchy               |

## Architecture Principles

### 1. Dependency Rule
- Dependencies point inward toward the domain
- Domain layer has no external dependencies
- Infrastructure depends on domain abstractions

### 2. Layer Responsibilities

#### Domain Layer (`domain/`)
- **Pure business logic** - no external dependencies
- **Entities**: Core FINS protocol concepts
- **Value Objects**: Immutable data structures (frames, codes)
- **Domain Services**: Complex business rules
- **Interfaces**: Abstract contracts for external concerns

#### Application Layer (`app/`)
- **Use Cases**: Orchestrate domain objects
- **Application Services**: Coordinate between domain and infrastructure
- **DTOs**: Data transfer objects for use case boundaries

#### Infrastructure Layer (`infrastructure/`)
- **External Concerns**: Network, file system, databases
- **Implementations**: Concrete classes implementing domain interfaces
- **Adapters**: Convert between external formats and domain models

#### Interface Layer (`interface/`)
- **Controllers**: Handle external requests
- **Presenters**: Format responses
- **Configuration**: External configuration management

## Key Improvements in v2

### 1. Enhanced Structure
- Added API interface layer for REST endpoints
- Separated unit and integration tests
- Added documentation and examples directories
- Configuration management centralized

### 2. Better Separation of Concerns
- Domain exceptions isolated
- Utility functions properly categorized
- Multiple connection types supported (TCP, UDP, Serial)

### 3. Testing Strategy
- Unit tests for each layer
- Integration tests for end-to-end scenarios
- Test fixtures for consistent test data
- Mock implementations for development

### 4. Documentation & Examples
- Comprehensive API documentation
- Usage examples for common scenarios
- Protocol reference documentation

### 5. Modern Python Practices
- `pyproject.toml` for packaging
- Type hints throughout
- Async support consideration
- Proper `__init__.py` files for package structure

## Implementation Guidelines

### 1. Start with Domain
1. Define core entities and value objects
2. Create abstract interfaces
3. Implement domain services

### 2. Build Application Layer
1. Define use cases
2. Create application services
3. Establish clear boundaries

### 3. Implement Infrastructure
1. Create concrete implementations
2. Handle external dependencies
3. Implement error handling

### 4. Add Interfaces
1. CLI for basic operations
2. REST API for integration
3. Configuration management

### 5. Comprehensive Testing
1. Unit tests for domain logic
2. Integration tests for full workflows
3. Mock implementations for development

This architecture ensures maintainability, testability, and extensibility while keeping the FINS protocol logic clean and focused.
