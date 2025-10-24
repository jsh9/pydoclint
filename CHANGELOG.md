# Change Log

## [0.7.4] - 2025-10-24

- Added
  - Validation of invalid config file path
  - Validation of `[tool.pydoclint]` section in the config file
- Removed
  - Python 3.9 support
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.7.3...0.7.4

## [0.7.3] - 2025-09-03

- Fixed
  - Fixed comment handling in type hints to properly ignore inline comments
    when comparing type annotations between function signatures and docstrings
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.7.2...0.7.3

## [0.7.2] - 2025-09-02

- Fixed
  - A bug where false positive arg names are reported in the violation message
- Added
  - Support for checking class attribute default values (numpy and Google
    styles only)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.7.1...0.7.2

## [0.7.1] - 2025-09-02

- Added
  - Support for `--check-arg-default` for Google style
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.7.0...0.7.1

## [0.7.0] - 2025-09-01

- Added
  - A new config option `--check-arg-default` (default: False) to check
    consistency of argument defaults (between docstring and function signature)
- Changed
  - Replace `Prettier` with: [yamlfix](https://github.com/lyz-code/yamlfix),
    [mdformat](https://github.com/hukkin/mdformat), and
    [pretty-format-json](https://github.com/pre-commit/pre-commit-hooks?tab=readme-ov-file#pretty-format-json)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.11...0.7.0

## [0.6.11] - 2025-08-31

- Fixed
  - A bug where short docstring is incorrectly detected
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.10...0.6.11

## [0.6.10] - 2025-08-14

- Changed
  - Migrated from setup.cfg/setup.py to pyproject.toml for modern Python
    packaging
  - Consolidated all package metadata into pyproject.toml [project] section
  - Removed deprecated setup.cfg and setup.py files
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.9...0.6.10

## [0.6.9] - 2025-08-14

- Fixed
  - Fixed output formatting bug where blank lines between files would appear at
    the end when redirecting output to a file instead of between each file
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.8...0.6.9

## [0.6.8] - 2025-08-14

- Changed
  - Enhanced numpy-style docstring detection with pattern-based recognition
  - Added pattern-based detection that looks for section headers with dashes
    (e.g., `Returns\n-------`) before falling back to size-based comparison
- Updated
  - Updated documentation to reflect new detection logic and reformatted to 79
    chars per line
- Added
  - Added comprehensive test coverage for the new numpy-style detection
    functionality
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.7...0.6.8

## [0.6.7] - 2025-05-18

- Changed
  - Reverted the default behavior of `--quiet` to be `False`
- Fixed
  - Fixed a typo in the documentation
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.6...0.6.7

## [0.6.6] - 2025-04-16

- Fixed
  - A bug where double quotes in function signature type hints are not treated
    as interchangeable as double quotes in the docstring
- Changed
  - Changed the default of option `--quiet` from False to True
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.5...0.6.6

## [0.6.5] - 2025-04-03

- Fixed
  - A typo in the default config value of `--ignore-private-args`
  - A bug with checking assert errors when
    `shouldDeclareAssertErrorIfAssertStatementExists` is False
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.4...0.6.5

## [0.6.4] - 2025-03-30

- Fixed
  - A bug with tuple decomposition in docstrings
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.3...0.6.4

## [0.6.3] - 2025-03-30

- Added
  - Added `DOC504` and a config option
    `--should-declare-assert-error-if-assert-statement-exists`. If this option
    is True and a function has an `assert` statement, an `AssertError`
    declaration is required in the docstring. Otherwise `DOC504` is raised.
    (This changes the behavior introduced in v0.6.1.)
  - Added a new config option `--ignore-private-args` (default to `False`)
- Changed
  - Canceled the ignoring of `LN002` violation in flake8 config in tox
  - Fix a typo in maximum line length setting in flake8 config in tox
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.2...0.6.3

## [0.6.2] - 2025-02-17

- Fixed
  - An issue where no error was thrown when the user does not supply a path
  - A bug where `--only-attrs-with-ClassVar-are-treated-as-class-attrs` is not
    properly passed to the visitor in the flake8 mode
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.1...0.6.2

## [0.6.1] - 2025-02-16

- Changed
  - Now if a function as an `assert` statement, an `AssertError` declaration is
    by default required in the docstring's "Asserts" section (if relevant
    config options to check raises/assertions are turned on)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.6.0...0.6.1

## [0.6.0] - 2025-01-13

- Added
  - A new violation code, `DOC003`, to detect docstring style mismatch (when
    docstrings are written in the style different from specified)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.19...0.6.0

## [0.5.19] - 2025-01-12

- Fixed
  - False positive DOC405 and DOC201 when we have bare return statements
    together with `yield` statements
- Added
  - A new config option `--should-document-star-arguments` (if `False`, star
    arguments such as `*args` and `**kwargs` should not be documented in the
    docstring)
  - A pre-commit step to check that "Full diff" is always added in CHANGELOG.md
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.18...0.5.19

## [0.5.18] - 2025-01-12

- Fixed
  - An issue where custom exceptions such as `a.b.c.MyException.from_str`
    cannot be properly parsed and compared
  - A minor wording issue in DOC503 violation message
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.17...0.5.18

## [0.5.17] - 2025-01-12

- Added
  - A new config option `--auto-regenerate-baseline` to automatically
    regenerate the baseline file for every successful _pydoclint_ run
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.16...0.5.17

## [0.5.16] - 2025-01-11

- Added
  - A pre-commit hook for using _pydoclint_ as a flake8 plugin
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.15...0.5.16

## [0.5.15] - 2025-01-10

- Changed
  - Changed to using v0.0.10 of docstring_parser_fork, which now throws a
    `ParseError` when a non-empty docstring section cannot be parsed (in Numpy
    style). This `ParseError` would lead to DOC001.
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.14...0.5.15

## [0.5.14] - 2024-12-26

- Changed
  - Added `DOC002` (syntax error) to handle cases where there are syntax errors
    in the Python file
  - Replaced invisible and zero-width characters with empty strings so that
    Python's AST can correctly parse the files
  - Added end-to-end test (essentially an integration test)
- Fixed
  - A bug in ast.assign
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.13...0.5.14

## [0.5.13] - 2024-12-20

- Fixed
  - Fixed a bug where assigning a dict value (such as `abc['something'] = 123`)
    would result in EdgeCaseError
  - Fixed a bug where non-UTF-8 encoded files would crash _pydoclint_
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.12...0.5.13

## [0.5.12] - 2024-12-15

- Changed
  - Dropped support for Python 3.8
  - Use "modern" type annotation, such as `list` and `str | None`
- Added
  - Added static type checking using `mypy`
  - A new config option,
    `--only-attrs-with-ClassVar-are-treated-as-class-attrs`
  - Ensured support for Python 3.12 and 3.13
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.11...0.5.12

## [0.5.11] - 2024-12-14

- Fixed
  - Fixed a bug where pydoclint uses variable names instead of the exception
    itself (https://github.com/jsh9/pydoclint/issues/175)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.10...0.5.11

## [0.5.10] - 2024-12-07

- Changed
  - Command line message about loading config file is now hidden with config
    option `--quiet`
- Fixed
  - Fixed a bug where assigning a value to an attribute caused pydoclint to
    crash
- Changed
  - Renamed function `unparseAnnotation()` into `unparseNode()`
  - Renamed `EdgeCaseError` into `EdgeCaseError`
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.9...0.5.10

## [0.5.9] - 2024-09-29

- Fixed
  - Fixed an edge case where type annotations are very long
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.8...0.5.9

## [0.5.8] - 2024-09-23

- Fixed
  - Fixed the logic of handling exceptions namespaces (`a.b.c.MyException`)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.7...0.5.8

## [0.5.7] - 2024-09-02

- Added
  - A new violation code, `DOC503`, which checks that exceptions in the
    function body match those in the "Raises" section of the docstring
- Changed
  - Switched from tab to 4 spaces in baseline
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.6...0.5.7

## [0.5.6] - 2024-07-17

- Fixed
  - Fixed a bug where _pydoclint_ treats folders whose names end with `.py` as
    files
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.5...0.5.6

## [0.5.5] - 2024-07-15

- Fixed
  - Fixed a bug where `a = b = c = 1` style cannot be properly parsed
    (https://github.com/jsh9/pydoclint/issues/151)
- Changed
  - Changed the default of `--treat-property-methods-as-class-attributes` to
    `False` to restore backward compatibility
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.4...0.5.5

## [0.5.4] - 2024-07-14

- Added
  - An option `--should-document-private-class-attributes` (if False, private
    class attributes should not appear in the docstring)
  - An option `--treat-property-methods-as-class-attributes` (if True,
    `@property` methods are treated like class attributes and need to be
    documented in the class docstring)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.3...0.5.4

## [0.5.3] - 2024-06-26

- Changed
  - Added DOC604 & 605 test cases
  - Improved DOC605 error message
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.2...0.5.3

## [0.5.2] - 2024-06-26

- Changed
  - Pinned to a higher version (0.0.9) of docstring_parser_fork
  - Relaxed class attribute checking logic
    - When a class has no docstring, no DOC6xx violations will be reported
    - When a class has a short docstring (and
      `--skip-checking-short-docstrings`) is set to `True`, no DOC6xx
      violations will be reported
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.1...0.5.2

## [0.5.1] - 2024-06-24

- Fixed
  - Fixed a bug in unparsing annotations when checking class attributes
  - Fixed a bug in checking class attributes where there are no attributes in
    class def or in docstring
- Changed
  - Used a dedicated "attribute" section for Sphinx-style docstrings
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.5.0...0.5.1

## [0.5.0] - 2024-06-22

- Added
  - Added checks for class attributes
    - This functionality checks class attributes against the "Attributes"
      section of the docstring
    - There is a new config option, `--check-class-attributes` (or `-cca`),
      which defaults to `True`. Therefore, this breaks backward compatibility.
    - To maintain backward compatibility, set `--check-class-attributes` to
      `False`
    - Options like `--check-arg-order`, `--arg-type-hints-in-signature`, and
      `--arg-type-hints-in-docstring` are still effective in checking class
      attributes
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.4.2...0.5.0

## [0.4.2] - 2024-05-29

- Changed
  - Improved the violation message of DOC403 to remind users to add a return
    annotation
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.4.1...0.4.2

## [0.4.1] - 2024-02-17

- Fixed
  - A bug where using double quotes in Literal type (such as `Literal["foo"]`
    could produce a false positive `DOC203` violation.
  - Removed useless argument `--src`
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.4.0...0.4.1

## [0.4.0] - 2024-02-08

- Changed
  - Improved the violation message of DOC105: the arguments with inconsistent
    type hints are now shown in the violation message to make violation
    correction much easier
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.10...0.4.0

## [0.3.10] - 2024-02-07

- Added
  - A new config option `--show-filenames-in-every-violation-message` (or
    `-sfn`), which makes it more convenient to jump to the corresponding line
    in IDEs by clicking on the violation message in the terminal
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.9...0.3.10

## [0.3.9] - 2024-01-16

- Fixed
  - False positive violation `DOC203` when there is no docstring return section
    for methods with `@property` decorator
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.8...0.3.9

## [0.3.8] - 2023-10-20

- Fixed
  - A bug in handling prepended escape characters in docstrings
- Changed
  - Improved documentation
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.7...0.3.8

## [0.3.7] - 2023-10-19

- Changed
  - Improved documentation
  - Disabled parallel mode for pre-commit
    (https://github.com/jsh9/pydoclint/pull/93)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.6...0.3.7

## [0.3.6] - 2023-10-18

- Fixed
  - Updated dependency (docstring_parser_fork) to 0.0.5 to fix issues when
    parsing Google-style return section
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.5...0.3.6

## [0.3.5] - 2023-10-17

- Changed
  - When checking for consistency betwene the docstring arguments and the
    arguments in the function signature, ignore underscore arguments (`_`,
    `__`, `___`, ...) in the arguments in the function signature
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.4...0.3.5

## [0.3.4] - 2023-10-12

- Changed
  - Don't check type hints for DOC103
    (https://github.com/jsh9/pydoclint/pull/86)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.3...0.3.4

## [0.3.3] - 2023-10-01

- Added
  - Added baseline file integration and 2 options:
    1. `--generate-baseline True` Generate baseline content, and write it to a
       file specified from `--baseline` option path.
    1. `--baseline <PATH>` Specify path to file with baseline content.
- Changed
  - For the `--config` option, the default value is now `pyproject.toml`.
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.2...0.3.3

## [0.3.2] - 2023-09-04

- Changed
  - Make `flake8` an optional dependency
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.1...0.3.2

## [0.3.1] - 2023-08-28

- Added
  - Added an option `--require-yield-section-when-yielding-nothing` (defaulting
    to `False`). When it's False, we don't need a "Yields" section when a
    function yields None (https://github.com/jsh9/pydoclint/issues/79)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.3.0...0.3.1

## [0.3.0] - 2023-08-26

- Improved
  - Relaxed Generator/Iterator checking: stop enforcing the return annotation
    to be Generator if a function yields something
    (https://github.com/jsh9/pydoclint/issues/76)
  - Added handling of functions that both return something and yield something
- Changed
  - Used docstring_parser_fork to parse numpy-style docstrings, because the
    official numpydoc doesn't support both Yields and Returns sections in a
    single docstring
- Removed
  - Dependency on numpydoc
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.2.4...0.3.0

## [0.2.4] - 2023-08-24

- Fixed
  - A bug with unparsing yield types
    (https://github.com/jsh9/pydoclint/issues/75#issuecomment-1691398673)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.2.3...0.2.4

## [0.2.3] - 2023-08-24

- Fixed
  - A bug with yields type checking
  - A typo in `DOC403` code logic
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.2.2...0.2.3

## [0.2.2] - 2023-08-22

- Improved

  - Improved handling of escape symbol (`\`) in docstrings
    (https://github.com/jsh9/pydoclint/issues/73)

- Full diff

  - https://github.com/jsh9/pydoclint/compare/0.2.1...0.2.2

## [0.2.1] - 2023-08-21

- Improved

  - Improved handling of backticks or double backticks being used in type hints
    in docstrings

- Full diff

  - https://github.com/jsh9/pydoclint/compare/0.2.0...0.2.1

## [0.2.0] - 2023-08-18

- Added
  - Added checking of yield types (between function signature and the
    docstring's Yields section), as well as a corresponding violation: `DOC404`
  - Added checking of incompatibility between `Generator`/`Iterator` and the
    `yield`/`return` statements, as well as a corresponding violation: `DOC405`
    (https://github.com/jsh9/pydoclint/issues/68)
- Fixed
  - Fixed a bug where raise/return/yield statements in match-case blocks are
    incorrectly identified. (https://github.com/jsh9/pydoclint/issues/63)
- Improved
  - Used a try/catch block to capture potential recursion error, potentially
    due to too complex functions/classes
    (https://github.com/jsh9/pydoclint/issues/65)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.9...0.2.0

## [0.1.9] - 2023-08-18

- Fixed
  - Fixed a bug where union-style return types (such as `int | str`) in
    Google-style docstrings cannot be correctly parsed
    (https://github.com/jsh9/pydoclint/issues/66)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.8...0.1.9

## [0.1.8] - 2023-08-16

- Fixed
  - Fixed a broken URL that used to point to `DOC103` notes
    (https://github.com/jsh9/pydoclint/issues/61)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.7...0.1.8

## [0.1.7] - 2023-08-15

- Fixed
  - Correctly handle potentially unacceptable type hint formats
    (https://github.com/jsh9/pydoclint/issues/59)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.6...0.1.7

## [0.1.6] - 2023-08-13

- Added
  - Added handling of the `NoReturn` type annotation
    (https://github.com/jsh9/pydoclint/issues/55)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.5...0.1.6

## [0.1.5] - 2023-08-12

- Improved
  - Improved algorithm to compare type hints, so that type hints are considered
    equal if their actual meanings are the same.
    (https://github.com/jsh9/pydoclint/issues/56)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.4...0.1.5

## [0.1.4] - 2023-07-23

- Added
  - A documentation site to complement README
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.3...0.1.4

## [0.1.3] - 2023-07-21

- Fixed
  - Pass `--check-return-types` option to flake8 plugin
    (https://github.com/jsh9/pydoclint/pull/52)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.2...0.1.3

## [0.1.2] - 2023-07-20

- Fixed
  - Fixed outdated naming of options `--type-hints-in-docstring` and
    `--type-hints-in-signature` (https://github.com/jsh9/pydoclint/issues/50)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.1...0.1.2

## [0.1.1] - 2023-07-18

- Fixed
  - Fixed incorrect blocking of "sphinx" style in CLI arguments
    (https://github.com/jsh9/pydoclint/issues/49)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.1.0...0.1.1

## [0.1.0] - 2023-07-15

- Added
  - Added support for the
    [Sphinx docstring style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
    (https://github.com/jsh9/pydoclint/issues/43)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.16...0.1.0

## [0.0.16] - 2023-07-14

- Fixed
  - Fixed a bug (https://github.com/jsh9/pydoclint/issues/44) where tuple type
    annotation is incorrectly detected
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.15...0.0.16

## [0.0.15] - 2023-07-10

- Fixed
  - Fixed false positive `DOC402` when `yield` statements are in a block within
    a nested function (https://github.com/jsh9/pydoclint/pull/42)
  - Fixed false positives when `return` and `raise` statements are in a block
    within a nested function (https://github.com/jsh9/pydoclint/pull/42)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.14...0.0.15

## [0.0.14] - 2023-07-05

- Fixed
  - Fixed an issue where quotes in return annotations are not properly handled
    (https://github.com/jsh9/pydoclint/pull/39)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.13...0.0.14

## [0.0.13] - 2023-06-26

- Fixed
  - False positives when checking abstract methods (partially tackles
    https://github.com/jsh9/pydoclint/issues/31)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.12...0.0.13

## [0.0.12] - 2023-06-26

- Fixed
  - False positive of DOC203 when
    `--require-return-section-when-returning-None` is `False`, the docstring
    has no return section, and the return annotation is `None`
    (https://github.com/jsh9/pydoclint/pull/34)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.11...0.0.12

## [0.0.11] - 2023-06-26

- Added
  - A new violation code, DOC203, which is about inconsistency between return
    types in the docstring and in the return annotation
    (https://github.com/jsh9/pydoclint/pull/33)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.10...0.0.11

## [0.0.10] - 2023-06-12

- Fixed
  - Fixed a bug (https://github.com/jsh9/pydoclint/issues/19) in checking type
    hints when the function signature only contains star arguments
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.9...0.0.10

## [0.0.9] - 2023-06-12

- Changed
  - Replaced the `--check-type-hint` option with two new options:
    `--type-hints-in-docstring` and `--type-hints-in-signature`
    (https://github.com/jsh9/pydoclint/issues/19)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.8...0.0.9

## [0.0.8] - 2023-06-06

- Added
  - A command line option `--version` to show the current version of pydoclint
    (https://github.com/jsh9/pydoclint/pull/17)
  - Enabled pydoclint to be used as a pre-commit hook
    (https://github.com/jsh9/pydoclint/pull/18)
- Fixed
  - Encoding issues in Windows (where non-ASCII characters cause issues with
    Windows + pre-commit) (https://github.com/jsh9/pydoclint/pull/21)
  - Stopped using colons (:) in flake8 error messages because they could cause
    issues with tools like "yesqa" (https://github.com/jsh9/pydoclint/pull/22)
- Changed
  - Expanded the logic to identify generator functions
    (https://github.com/jsh9/pydoclint/issues/15)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.7...0.0.8

## [0.0.7] - 2023-06-01

- Fixed
  - Fixed a bug where re-raising an exception was not handled properly
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.6...0.0.7

## [0.0.6] - 2023-05-31

- Fixed
  - A typo in `DOC103` error message that resulted in an invalid URL
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.5...0.0.6

## [0.0.5] - 2023-05-31

- Added
  - A new option to allow no return section in the docstring if the function
    implicitly returns `None` (https://github.com/jsh9/pydoclint/issues/6)
- Changed
  - Made pydoclint options configurable via a config file (both in the native
    mode and in the flake8 plugin mode)
    (https://github.com/jsh9/pydoclint/pull/11)
  - Methods with `@property` as its last decorator no longer need to have a
    return section in the docstring (https://github.com/jsh9/pydoclint/pull/13)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.4...0.0.5

## [0.0.4] - 2023-05-27

- Added
  - A new violation, `DOC001`, for errors in parsing docstrings
    (https://github.com/jsh9/pydoclint/pull/8)
  - A new option to allow `__init__()` methods to have docstring (and when
    users activate this option, check arguments and "Raises" in the docstring
    of `__init__()` instead of in the class docstring)
    (https://github.com/jsh9/pydoclint/pull/7)
- Changed
  - Used AST unparser to unparse type annotation nodes
- Fixed
  - A bug when parsing type annotations such as `Callable[[int], str]`
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.3...0.0.4

## [0.0.3] - 2023-05-18

- Added
  - Added support for
    [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#s3.8.1-comments-in-doc-strings)
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.2...0.0.3

## [0.0.2] - 2023-05-16

- Added
  - New command line options
- Fixed
  - Fixed an issue where star arguments (\*, \*args, \*\*kwargs) were omitted
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.1...0.0.2

## [0.0.1] - 2023-05-15

Initial release
