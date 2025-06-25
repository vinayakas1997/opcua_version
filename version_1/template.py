"""
FINS Protocol Clean Architecture Template Generator
=================================================
This module creates a Clean Architecture project structure for the FINS Protocol project
based on the architecture defined in architecture.md.

Clean Architecture Layers:
- Domain: Enterprise business rules (innermost layer)
- Application: Use cases and application business rules
- Infrastructure: External interfaces and frameworks
- Interface: Controllers, presenters, and gateways
"""

import os
import sys
from pathlib import Path
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fins_template_creation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class FinsCleanArchitectureGenerator:
    """
    Generates FINS Protocol project structure following Clean Architecture principles.
    """
    
    def __init__(self, project_name: str = "your_project"):
        self.project_name = project_name
        self.created_files = []
        self.skipped_files = []
        self.failed_files = []
        
        # Clean Architecture structure based on architecture.md
        self.architecture_structure = {
            # Root level files
            f"{project_name}/__init__.py": "Main package initialization",
            "pyproject.toml": "Modern Python project configuration",
            "setup.py": "Legacy setup configuration",
            "README.md": "Project documentation",
            "requirements.txt": "Python dependencies",
            ".gitignore": "Git ignore patterns",
            ".env.example": "Environment variables template",
            
            # APPLICATION LAYER - Use cases and application business rules
            f"{project_name}/app/__init__.py": "Application layer initialization",
            f"{project_name}/app/use_cases/__init__.py": "Use cases module",
            f"{project_name}/app/use_cases/read_values.py": "Read PLC values use case",
            f"{project_name}/app/use_cases/write_values.py": "Write PLC values use case",
            
            # DOMAIN LAYER - Enterprise business rules (core business logic)
            f"{project_name}/domain/__init__.py": "Domain layer initialization",
            f"{project_name}/domain/fins/__init__.py": "FINS domain module",
            f"{project_name}/domain/fins/command_codes.py": "FINS command codes enumeration",
            f"{project_name}/domain/fins/connection.py": "Abstract FINS connection interface",
            f"{project_name}/domain/fins/frames.py": "FINS protocol frames and headers",
            f"{project_name}/domain/fins/memory_areas.py": "PLC memory areas definitions",
            f"{project_name}/domain/fins/response_codes.py": "FINS response codes enumeration",
            f"{project_name}/domain/fins/utils.py": "FINS utility functions",
            
            # INFRASTRUCTURE LAYER - External interfaces and frameworks
            f"{project_name}/infrastructure/__init__.py": "Infrastructure layer initialization",
            f"{project_name}/infrastructure/fins/__init__.py": "FINS infrastructure module",
            f"{project_name}/infrastructure/fins/tcp_connection.py": "TCP implementation of FINS connection",
            f"{project_name}/infrastructure/fins/mock_connection.py": "Mock FINS connection for testing",
            
            # INTERFACE LAYER - Controllers, CLI, API adapters
            f"{project_name}/interface/__init__.py": "Interface layer initialization",
            f"{project_name}/interface/cli/__init__.py": "CLI interface module",
            f"{project_name}/interface/cli/main.py": "CLI main entry point",
            
            # TESTS - Comprehensive testing structure
            f"{project_name}/tests/__init__.py": "Tests package initialization",
            f"{project_name}/tests/test_fins/__init__.py": "FINS tests module",
            f"{project_name}/tests/test_fins/test_frames.py": "FINS frames unit tests",
            f"{project_name}/tests/test_fins/test_connection.py": "FINS connection tests",
            f"{project_name}/tests/test_use_cases.py": "Use cases integration tests",
            f"{project_name}/tests/conftest.py": "Pytest configuration and fixtures",
        }
        
        # File templates with actual implementation content
        self.file_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize all file templates with appropriate content."""
        return {
            # Configuration files
            "pyproject.toml": self._get_pyproject_template(),
            "setup.py": self._get_setup_template(),
            "requirements.txt": self._get_requirements_template(),
            "README.md": self._get_readme_template(),
            ".gitignore": self._get_gitignore_template(),
            ".env.example": self._get_env_template(),
            
            # Domain layer templates
            f"{self.project_name}/domain/fins/command_codes.py": self._get_command_codes_template(),
            f"{self.project_name}/domain/fins/response_codes.py": self._get_response_codes_template(),
            f"{self.project_name}/domain/fins/memory_areas.py": self._get_memory_areas_template(),
            f"{self.project_name}/domain/fins/frames.py": self._get_frames_template(),
            f"{self.project_name}/domain/fins/connection.py": self._get_connection_template(),
            f"{self.project_name}/domain/fins/utils.py": self._get_utils_template(),
            
            # Application layer templates
            f"{self.project_name}/app/use_cases/read_values.py": self._get_read_use_case_template(),
            f"{self.project_name}/app/use_cases/write_values.py": self._get_write_use_case_template(),
            
            # Infrastructure layer templates
            f"{self.project_name}/infrastructure/fins/tcp_connection.py": self._get_tcp_connection_template(),
            f"{self.project_name}/infrastructure/fins/mock_connection.py": self._get_mock_connection_template(),
            
            # Interface layer templates
            f"{self.project_name}/interface/cli/main.py": self._get_cli_main_template(),
            
            # Test templates
            f"{self.project_name}/tests/conftest.py": self._get_conftest_template(),
            f"{self.project_name}/tests/test_fins/test_frames.py": self._get_test_frames_template(),
            f"{self.project_name}/tests/test_fins/test_connection.py": self._get_test_connection_template(),
            f"{self.project_name}/tests/test_use_cases.py": self._get_test_use_cases_template(),
        }
    
    def create_project_structure(self) -> Dict[str, List[str]]:
        """Create the complete Clean Architecture project structure."""
        logger.info("=" * 60)
        logger.info("FINS PROTOCOL CLEAN ARCHITECTURE TEMPLATE GENERATOR")
        logger.info("=" * 60)
        logger.info(f"Project: {self.project_name}")
        logger.info(f"Architecture: Clean Architecture (Domain-Driven Design)")
        logger.info(f"Total files to create: {len(self.architecture_structure)}")
        logger.info("=" * 60)
        
        # Create files organized by layer
        self._create_layer_files("🏗️  ROOT LEVEL", [f for f in self.architecture_structure.keys() if not f.startswith(self.project_name)])
        self._create_layer_files("🎯 DOMAIN LAYER", [f for f in self.architecture_structure.keys() if "/domain/" in f])
        self._create_layer_files("⚙️  APPLICATION LAYER", [f for f in self.architecture_structure.keys() if "/app/" in f])
        self._create_layer_files("🔌 INFRASTRUCTURE LAYER", [f for f in self.architecture_structure.keys() if "/infrastructure/" in f])
        self._create_layer_files("🖥️  INTERFACE LAYER", [f for f in self.architecture_structure.keys() if "/interface/" in f])
        self._create_layer_files("🧪 TESTS", [f for f in self.architecture_structure.keys() if "/tests/" in f])
        
        self._print_summary()
        self._print_architecture_explanation()
        
        return {
            "created": self.created_files,
            "skipped": self.skipped_files,
            "failed": self.failed_files
        }
    
    def _create_layer_files(self, layer_name: str, files: List[str]) -> None:
        """Create files for a specific architecture layer."""
        if not files:
            return
            
        logger.info(f"\n{layer_name}")
        logger.info("-" * len(layer_name))
        
        for filepath in files:
            try:
                description = self.architecture_structure[filepath]
                self._create_file(filepath, description)
            except Exception as e:
                logger.error(f"Failed to create {filepath}: {str(e)}")
                self.failed_files.append(filepath)
    
    def _create_file(self, filepath: str, description: str) -> None:
        """Create a single file with appropriate content."""
        path_obj = Path(filepath)
        filedir = path_obj.parent
        
        # Create directory structure
        if filedir != Path('.'):
            filedir.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists with content
        if path_obj.exists() and path_obj.stat().st_size > 0:
            logger.info(f"  ⏭️  {filepath} (already exists)")
            self.skipped_files.append(filepath)
            return
        
        # Get content for the file
        content = self.file_templates.get(filepath, "")
        if filepath.endswith("__init__.py") and not content:
            content = self._get_init_template(description)
        
        # Write file
        with open(path_obj, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"  ✅ {filepath}")
        self.created_files.append(filepath)
    
    def _get_init_template(self, description: str) -> str:
        """Generate __init__.py template."""
        return f'"""\n{description}\n"""\n\n__version__ = "0.1.0"\n'
    
    # Configuration Templates
    def _get_pyproject_template(self) -> str:
        return f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{self.project_name.replace('_', '-')}"
version = "0.1.0"
description = "FINS Protocol implementation following Clean Architecture"
authors = [{{name = "Your Name", email = "your.email@example.com"}}]
license = {{text = "MIT"}}
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "pydantic>=2.0.0",
    "typing-extensions>=4.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "coverage>=7.0.0",
]

[project.scripts]
fins-cli = "{self.project_name}.interface.cli.main:main"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["{self.project_name}/tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
"""

    def _get_requirements_template(self) -> str:
        return """# Core dependencies
pydantic>=2.0.0
typing-extensions>=4.0.0

# Development dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
coverage>=7.0.0

# Optional dependencies for CLI
click>=8.0.0
rich>=13.0.0
"""

    def _get_readme_template(self) -> str:
        return f"""# {self.project_name.replace('_', ' ').title()}

A Clean Architecture implementation of the FINS (Factory Interface Network Service) protocol for communicating with Omron PLCs.

## Architecture Overview

This project follows Clean Architecture principles with clear separation of concerns:

