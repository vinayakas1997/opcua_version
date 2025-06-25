"""
Project Template Generator for FINS Protocol
============================================
This module creates a standardized project structure for the FINS Protocol project.
It generates all necessary directories and files with proper error handling and logging.
"""

import os
import sys
from pathlib import Path
import logging
from datetime import datetime
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('template_creation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ProjectTemplateGenerator:
    """
    A class to generate project template structure with enhanced features.
    """
    
    def __init__(self, project_name: str = "fins_protocol"):
        self.project_name = project_name
        self.created_files = []
        self.skipped_files = []
        self.failed_files = []
        
        # Enhanced file structure with descriptions
        self.file_structure = {
            # Core package files
            f"{project_name}/__init__.py": "Main package initialization",
            f"{project_name}/components/__init__.py": "Components module initialization",
            f"{project_name}/config/__init__.py": "Configuration module initialization",
            f"{project_name}/constants/__init__.py": "Constants and enums",
            f"{project_name}/entity/__init__.py": "Data entities and models",
            f"{project_name}/exception/__init__.py": "Custom exceptions",
            f"{project_name}/logger/__init__.py": "Logging utilities",
            f"{project_name}/pipeline/__init__.py": "Data pipeline components",
            # f"{project_name}/utils/__init__.py": "Utility functions",
            
            ## FINS Domain-Specific Files
            f"{project_name}/Fins_domain/__init__.py": "FINS domain-specific logic",
            f"{project_name}/Fins_domain/command_codes.py":"FinsCommandCode Class",
            f"{project_name}/Fins_domain/response_codes.py": "FinsResponseEndCodes Class",
            f"{project_name}/Fins_domain/frames.py": "`FinsHeader`, `FinsCommandFrame`, `FinsResponseFrame` Class",
            f"{project_name}/Fins_domain/memory_areas.py": "FinsPLCMemoryAreas Class",
            f"{project_name}/Fins_domain/connection.py": "FinsConnection Class",
            f"{project_name}/fins_domain/utils.py": "reverse_word_order function",
            
            ## Infrasturcture FILES
            f"{project_name}/Infrastructure/fins/__init__.py": "FINS Infrastructure module initialization",
            f"{project_name}/Infrastructure/fins/tcp_connection.py": "TCP connection handling for FINS",
            f"{project_name}/Infrastructure/fins/udp_connection.py": "UDP connection handling for FINS",
            f"{project_name}/Infrastructure/fins/serial_connection.py": "Serial connection handling for FINS",
            f"{project_name}/Infrastructure/fins/mock_connection.py": "Test doubles for FINS connections",
            
            ## Docs 
            f"{project_name}/Docs/README.md": "Documentation for the FINS Protocol project",
            f"{project_name}/Docs/api_reference.md": "API reference documentation",
            f"{project_name}/Docs/user_guide.md": "User guide for the FINS Protocol project(explain teh fins protocol)",
            
            
            # Configuration files
            "config/config.yaml": "Main configuration file",
            "schema.yaml": "Data schema definitions",
            
            # Application files
            "app.py": "Main application entry point",
            "main.py": "CLI entry point",
            "logs.py": "Logging configuration",
            "exception.py": "Global exception handling",
            "setup.py": "Package setup configuration",
            
            # Additional enhanced files
            "requirements.txt": "Python dependencies",
            # "README.md": "Project documentation",
            ".gitignore": "Git ignore patterns",
            "Dockerfile": "Docker configuration",
            "docker-compose.yml": "Docker compose configuration",
            f"{project_name}/tests/__init__.py": "Test package initialization",
            "tests/test_main.py": "Main test file",
            ".env.example": "Environment variables example",
            "pyproject.toml": "Modern Python project configuration"
        }
        
        # Template content for specific files
        self.file_templates = {
            # "requirements.txt": self._get_requirements_template(),
            # "README.md": self._get_readme_template(),
            # ".gitignore": self._get_gitignore_template(),
            # ".env.example": self._get_env_template(),
            # "pyproject.toml": self._get_pyproject_template()
        }
    
    def create_project_structure(self) -> Dict[str, List[str]]:
        """
        Create the complete project structure with enhanced error handling.
        
        Returns:
            Dict containing lists of created, skipped, and failed files
        """
        logger.info(f"Starting project template creation for '{self.project_name}'")
        logger.info(f"Total files to create: {len(self.file_structure)}")
        
        for filepath, description in self.file_structure.items():
            try:
                self._create_file(filepath, description)
            except Exception as e:
                logger.error(f"Failed to create {filepath}: {str(e)}")
                self.failed_files.append(filepath)
        
        # self._print_summary()
        return {
            "created": self.created_files,
            "skipped": self.skipped_files,
            "failed": self.failed_files
        }
    
    def _create_file(self, filepath: str, description: str) -> None:
        """
        Create a single file with proper directory structure.
        
        Args:
            filepath: Path to the file to create
            description: Description of the file's purpose
        """
        path_obj = Path(filepath)
        filedir = path_obj.parent
        
        # Create directory if it doesn't exist
        if filedir != Path('.'):
            filedir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {filedir}")
        
        # Check if file exists and has content
        if path_obj.exists() and path_obj.stat().st_size > 0:
            logger.info(f"File already exists with content: {filepath}")
            self.skipped_files.append(filepath)
            return
        
        # Create file with template content if available
        content = self.file_templates.get(filepath, "")
        if filepath.endswith("__init__.py"):
            content = self._get_init_template(description)
        
        with open(path_obj, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Created: {filepath} - {description}")
        self.created_files.append(filepath)
    
    def _get_init_template(self, description: str) -> str:
        """Generate template content for __init__.py files."""
        return f'"""\n{description}\n"""\n\n__version__ = "0.1.0"\n'
    
    def _get_requirements_template(self) -> str:
        """Generate requirements.txt template."""
        return """# Core dependencies
pydantic>=2.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
loguru>=0.7.0

# Development dependencies
pytest>=7.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0

# Optional dependencies
fastapi>=0.100.0
uvicorn>=0.20.0
"""
    
    def _get_readme_template(self) -> str:
        """Generate README.md template."""
        return f"""# {self.project_name.replace('_', ' ').title()}

        ## Description
        A brief description of the {self.project_name} project.

        ## Installation
        ```bash
        pip install -r requirements.txt
        """
        
if __name__ == "__main__":
    project_name = "fins_protocol"
    if len(sys.argv) > 1:
        project_name = sys.argv[1]

    generator = ProjectTemplateGenerator(project_name)
    result = generator.create_project_structure()

    logger.info("Project template creation completed.")
    logger.info(f"Created files: {len(result['created'])}")
    logger.info(f"Skipped files: {len(result['skipped'])}")
    logger.info(f"Failed files: {len(result['failed'])}")