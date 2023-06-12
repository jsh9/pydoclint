# Change Log

## [0.0.9] - 2023-06-12

- Changed
  - Replaced the `--check-type-hint` option with two new options:
    `--type-hints-in-docstring` and `--type-hints-in-signature`
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.8...0.0.9

## [0.0.8] - 2023-06-06

- Added
  - A command line option `--version` to show the current version of pydoclint
  - Enabled pydoclint to be used as a pre-commit hook
- Fixed
  - Encoding issues in Windows (where non-ASCII characters cause issues with
    Windows + pre-commit)
  - Stopped using colons (:) in flake8 error messages because they could cause
    issues with tools like "yesqa"
- Changed
  - Expanded the logic to identify generator functions
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
    implicitly returns `None`
- Changed
  - Made pydoclint options configurable via a config file (both in the native
    mode and in the flake8 plugin mode)
  - Methods with `@property` as its last decorator no longer need to have a
    return section in the docstring
- Full diff
  - https://github.com/jsh9/pydoclint/compare/0.0.4...0.0.5

## [0.0.4] - 2023-05-27

- Added
  - A new violation, `DOC001`, for errors in parsing docstrings
  - A new option to allow `__init__()` methods to have docstring (and when
    users activate this option, check arguments and "Raises" in the docstring
    of `__init__()` instead of in the class docstring)
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
