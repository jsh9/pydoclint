# AGENTS.md

This file provides guidance to AI coding assistants when working with code in
this repository.

## 1. pydoclint Project Conventions

### 1.1. Code Style

- Use camelCase for function and variable names (not snake_case)

### 1.2. Branch Naming

- Format: `yyyy-mm-dd-What-this-branch-does`

### 1.3. Commit Messages & PR Titles

- Use action verbs (imperative mood), not past tense
- Good: "Add feature", "Fix bug"
- Bad: "Added feature", "Fixed bug"

## 2. Development Commands

### 2.1. Testing

- `pytest --tb=long .` - Run all tests with detailed traceback
- `tox` - Run full test suite across multiple Python versions
- `tox -e py311` - Run tests on specific Python version (py39, py310, py311,
  py312, py313)

### 2.2. Code Quality

- `mypy pydoclint/` - Type checking
- `muff format --diff --config=muff.toml pydoclint tests` - Format checking
  (use `--diff` to avoid accidental formatting)
- `flake8 .` - Basic linting
- `pydoclint --config=pyproject.toml .` - Self-check using pydoclint
- `pre-commit run -a` - Run all pre-commit hooks

### 2.3. Specialized Tox Commands

- `tox -e mypy` - Type checking only
- `tox -e muff` - Format checking only
- `tox -e check-self` - Run pydoclint on itself
- `tox -e flake8-basic` - Basic flake8 checks
- `tox -e flake8-misc` - Additional flake8 plugins
- `tox -e flake8-docstrings` - Docstring style checks
- `tox -e pre-commit` - Pre-commit hooks (skips muff formatter)

### 2.4. Running a Single Test

Use pytest with specific test file or test function:

```bash
pytest tests/test_main.py
pytest tests/test_main.py::test_function_name
```

## 3. Architecture Overview

Pydoclint is a Python docstring linter that checks docstring sections against
function signatures. The core architecture consists of:

### 3.1. Main Components

- **main.py**: CLI entry point using Click, handles command-line options and
  orchestrates linting
- **visitor.py**: AST visitor that traverses Python code and applies docstring
  checks
- **flake8_entry.py**: Plugin interface for flake8 integration
- **parse_config.py**: Configuration parsing from pyproject.toml and other
  sources
- **baseline.py**: Baseline functionality for gradual adoption

### 3.2. Utils Package Structure

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

### 3.3. Supported Docstring Styles

- **Numpy**: numpydoc format
- **Google**: Google-style docstrings
- **Sphinx**: Sphinx/reStructuredText format

### 3.4. Key Features

- Fast AST-based analysis (thousands of times faster than darglint)
- Supports type hint checking against docstring parameter types
- Class attribute documentation checking
- Baseline mode for gradual adoption in existing codebases
- Both standalone CLI and flake8 plugin modes
- Native CLI supports inline suppression via `# noqa: DOCxxx` (see
  `--native-mode-noqa-location` for placement options)

### 3.5. Test Structure

- `tests/data/` contains test cases organized by docstring style (google,
  numpy, sphinx, edge_cases)
- `tests/test_data/noqa/` contains end-to-end fixtures by style for native
  suppression behaviour
- Tests use real Python files with expected violations rather than string-based
  tests

## 4. Coding style

1. When writing tests, use pytest.parametrized. Use "flat" test functions
   instead of using classes.
2. Use camelCase in this repo
3. Add type hints wherever possible
