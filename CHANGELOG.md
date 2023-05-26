# Change Log

## Unreleased

- Added
  - A new option to allow `__init__()` methods to have docstring (and when
    users activate this option, check arguments and "Raises" in the docstring
    of `__init__()` instead of in the class docstring)
- Changed
  - Used AST unparser to unparse type annotation nodes
- Fixed
  - A bug when parsing type annotations such as `Callable[[int], str]`

## [0.0.3] - 2023-05-18

- Added
  - Added support for
    [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#s3.8.1-comments-in-doc-strings)
- Full changelog
  - https://github.com/jsh9/pydoclint/compare/0.0.2...0.0.3

## [0.0.2] - 2023-05-16

- Added
  - New command line options
- Fixed
  - Fixed an issue where star arguments (*, *args, \*\*kwargs) were omitted
- Full changelog
  - https://github.com/jsh9/pydoclint/compare/0.0.1...0.0.2

## [0.0.1] - 2023-05-15

Initial release
