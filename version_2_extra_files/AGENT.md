# AGENT.md - OMRON FINS Protocol Library

## Commands
- **Run main script**: `python main.py`
- **Run single test**: `python -m pytest path/to/test_file.py::test_function_name` (if pytest is available)
- **Type check**: `python -m mypy OMRON_FINS_PROTOCOL/` (if mypy is available)

## Architecture
- **Main entry**: `main.py` - demonstration script for FINS UDP connection
- **Core protocol**: `OMRON_FINS_PROTOCOL/` - main package containing FINS implementation
  - `Infrastructure/fins/` - UDP connection implementation (`udp_connection.py`)
  - `Fins_domain/` - Core protocol logic (frames, addresses, commands, errors)
  - `components/` - Data conversion utilities (`conversion.py`)
  - `exception/` - Custom exception handling
  - `logger/` - Logging utilities
  - `tests/` - Test files (currently minimal)

## Code Style
- **Imports**: Absolute imports from `OMRON_FINS_PROTOCOL` package
- **Error handling**: Custom FINS error classes, connection errors raised with descriptive messages
- **Naming**: snake_case for functions/variables, PascalCase for classes, ALL_CAPS for constants
- **Docstrings**: Google-style docstrings with Args/Returns sections
- **Type hints**: Use typing module (`Optional`, `Tuple`, `Union`, `bytes`, `str`, `int`)
- **Context managers**: Implement `__enter__`/`__exit__` for connection classes
- **Memory addresses**: Support string format parsing (e.g., 'D1000', '100.05' for CIO bits)
