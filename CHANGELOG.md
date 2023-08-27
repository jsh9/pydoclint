# Change Log

## [0.3.0] - 2023-08-26

- Improved
  - Relaxed Generator/Iterator checking: stop enforcing the return annotation
    to be Generator if a function yields something
    (https://github.com/jsh9/pydoclint/issues/76)
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
  - Fixed an issue where star arguments (*, *args, \*\*kwargs) were omitted
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.1...0.0.2

## [0.0.1] - 2023-05-15

Initial release
