your_project/
│
├── app/                         # Application-specific logic (use cases)
│   └── use_cases/
│       ├── read_values.py
│       └── write_values.py
│
├── domain/                      # Enterprise-wide business rules
│   └── fins/
│       ├── command_codes.py
│       ├── connection.py        # Abstract class FinsConnection
│       ├── frames.py            # FinsHeader, FinsCommandFrame, etc.
│       ├── memory_areas.py
│       └── response_codes.py
│
├── infrastructure/             # Implementation details
│   └── fins/
│       ├── tcp_connection.py    # Your concrete subclass of FinsConnection
│       └── mock_connection.py   # For testing/mocking
│
├── interface/                  # Interface adapters (UI, CLI, API)
│   └── cli/
│       └── main.py
│
├── tests/                      # Unit and integration tests
│   └── test_fins/
│       ├── test_frames.py
│       ├── test_connection.py
│       └── test_use_cases.py
│
├── __init__.py
└── pyproject.toml / setup.py


| Component                                             | Move To                                       |
| ----------------------------------------------------- | --------------------------------------------- |
| `FinsCommandCode`                                     | `domain/fins/command_codes.py`                |
| `FinsResponseEndCode`                                 | `domain/fins/response_codes.py`               |
| `FinsHeader`, `FinsCommandFrame`, `FinsResponseFrame` | `domain/fins/frames.py`                       |
| `FinsPLCMemoryAreas`                                  | `domain/fins/memory_areas.py`                 |
| `FinsConnection`                                      | `domain/fins/connection.py`                   |
| `reverse_word_order`                                  | `domain/fins/utils.py` or same as `frames.py` |
