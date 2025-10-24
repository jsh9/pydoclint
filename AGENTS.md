# AGENTS.md

This file provides guidance to AI coding assistants when working with code in
this repository.

## pydoclint Project Conventions

### Code Style

- Use camelCase for function and variable names (not snake_case)

### Branch Naming

- Format: `yyyy-mm-dd-What-this-branch-does`

### Commit Messages & PR Titles

- Use action verbs (imperative mood), not past tense
- Good: "Add feature", "Fix bug"
- Bad: "Added feature", "Fixed bug"

## Development Commands

### Testing

- `pytest --tb=long .` - Run all tests with detailed traceback
- `tox` - Run full test suite across multiple Python versions
- `tox -e py311` - Run tests on specific Python version (py39, py310, py311,
  py312, py313)

### Code Quality

- `mypy pydoclint/` - Type checking
- `muff format --diff --config=muff.toml pydoclint tests` - Format checking
  (use `--diff` to avoid accidental formatting)
- `flake8 .` - Basic linting
- `pydoclint --config=pyproject.toml .` - Self-check using pydoclint
- `pre-commit run -a` - Run all pre-commit hooks

### Specialized Tox Commands

- `tox -e mypy` - Type checking only
- `tox -e muff` - Format checking only
- `tox -e check-self` - Run pydoclint on itself
- `tox -e flake8-basic` - Basic flake8 checks
- `tox -e flake8-misc` - Additional flake8 plugins
- `tox -e flake8-docstrings` - Docstring style checks
- `tox -e pre-commit` - Pre-commit hooks (skips muff formatter)

### Running a Single Test

Use pytest with specific test file or test function:

```bash
pytest tests/test_main.py
pytest tests/test_main.py::test_function_name
```

## Architecture Overview

Pydoclint is a Python docstring linter that checks docstring sections against
function signatures. The core architecture consists of:

### Main Components

- **main.py**: CLI entry point using Click, handles command-line options and
  orchestrates linting
- **visitor.py**: AST visitor that traverses Python code and applies docstring
  checks
- **flake8_entry.py**: Plugin interface for flake8 integration
- **parse_config.py**: Configuration parsing from pyproject.toml and other
  sources
- **baseline.py**: Baseline functionality for gradual adoption

### Utils Package Structure

- **arg.py/argList.py**: Function argument representation and handling
- **doc.py**: Docstring parsing and representation
- **return_arg.py/yield_arg.py**: Return/yield argument handling
- **violation.py**: Violation representation and reporting
- **astTypes.py**: AST type definitions and utilities
- **generic.py**: Common utility functions
- **method_type.py**: Method type detection (regular, static, class, property)
- **parse_docstring.py**: Core docstring parsing for numpy/google/sphinx styles
- **return_yield_raise.py**: Analysis of return/yield/raise statements in
  function bodies
- **visitor_helper.py**: Helper functions for the main visitor

### Supported Docstring Styles

- **Numpy**: numpydoc format
- **Google**: Google-style docstrings
- **Sphinx**: Sphinx/reStructuredText format

### Key Features

- Fast AST-based analysis (thousands of times faster than darglint)
- Supports type hint checking against docstring parameter types
- Class attribute documentation checking
- Baseline mode for gradual adoption in existing codebases
- Both standalone CLI and flake8 plugin modes

### Test Structure

- `tests/data/` contains test cases organized by docstring style (google,
  numpy, sphinx, edge_cases)
- Tests use real Python files with expected violations rather than string-based
  tests
