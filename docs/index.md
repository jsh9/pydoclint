# pydoclint

A Python docstring linter to check whether a docstring's sections (arguments,
returns, raises, ...) match the function signature or function implementation.

It runs really fast. In fact, it is at least ~1,475 times faster than
[darglint](https://github.com/terrencepreilly/darglint) (or its maintained fork
[darglint2](https://github.com/akaihola/darglint2)).

Here is a comparison of linting time on some famous Python projects:

|                                                              | pydoclint | darglint                          |
| ------------------------------------------------------------ | --------- | --------------------------------- |
| [numpy](https://github.com/numpy/numpy)                      | 2.0 sec   | 49 min 9 sec (1,475x slower)      |
| [scikit-learn](https://github.com/scikit-learn/scikit-learn) | 2.4 sec   | 3 hr 5 min 33 sec (4,639x slower) |

Currently, _pydoclint_ supports three docstring styles:

- The [numpy stlyle](https://numpydoc.readthedocs.io/en/latest/format.html)
- The
  [Google style](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html)
- The
  [Sphinx style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
