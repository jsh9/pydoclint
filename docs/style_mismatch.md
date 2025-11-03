# More about docstring style mismatch (`DOC003`)

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [1. How does _pydoclint_ detect the style of a docstring?](#1-how-does-pydoclint-detect-the-style-of-a-docstring)
  - [1.1. Keyword heuristics for each style](#11-keyword-heuristics-for-each-style)
  - [1.2. Handling ambiguous or missing matches](#12-handling-ambiguous-or-missing-matches)
  - [1.3. What happens after a mismatch is detected?](#13-what-happens-after-a-mismatch-is-detected)
- [2. How accurate is this detection heuristic?](#2-how-accurate-is-this-detection-heuristic)
- [3. Can I turn this off?](#3-can-i-turn-this-off)
- [4. Is it much slower to parse a docstring with the heuristics?](#4-is-it-much-slower-to-parse-a-docstring-with-the-heuristics)
- [5. What violation code is associated with style mismatch?](#5-what-violation-code-is-associated-with-style-mismatch)
- [6. How to fix this violation code?](#6-how-to-fix-this-violation-code)

______________________________________________________________________

<!--TOC-->

This violation code warns you when _pydoclint_ thinks that the docstring is
written in a different style than the style you specified via the `--style`
config option.

## 1. How does _pydoclint_ detect the style of a docstring?

_pydoclint_ detects the style of a docstring with this procedure:

### 1.1. Keyword heuristics for each style

We now rely on lightweight heuristics that look for style-specific keywords at
the indentation level where the docstring begins:

- **NumPy**: section headers followed by dashed underlines (for example,
  `Returns` + `-------`), using a curated list of keywords.
- **Google**: top-level section headers such as `Args:`, `Returns:`, `Yields:`,
  `Raises:`, `Examples:`, or `Notes:` with matching indentation.
- **Sphinx/reST**: top-level field lists such as `:param`, `:type`, `:raises`,
  `:return:`, `:rtype:`, `:yield:`, or `:ytype:`.

Each helper only considers keywords that start at the same indentation level as
the opening triple quotes to avoid counting inline roles or nested blocks.

### 1.2. Handling ambiguous or missing matches

- **Exactly one match** We parse the docstring using the detected style. If it
  differs from the configured style, DOC003 is emitted. Google parse failures
  are also treated as style mismatches because malformed Google sections almost
  always indicate another style.
- **No matches** We assume the docstring uses the configured style and skip
  style mismatch warnings entirely.
- **Multiple matches** The docstring appears to mix styles (for example, Google
  `Args:` plus Sphinx `:param` directives), so we emit DOC003 for every
  configured style.

### 1.3. What happens after a mismatch is detected?

When DOC003 is triggered we still return the docstring parsed in the configured
style, but we suppress many follow-up checks that would otherwise generate
cascading false positives (argument type-hint expectations, return/yield/raise
consistency, etc.). This keeps the feedback focused on resolving the style
mismatch first.

## 2. How accurate is this detection heuristic?

The authors of _pydoclint_ have manually tested this heuristic in 8
repositories written in all 3 styles (numpy, Google, and Sphinx), and have
found this heuristic to be satisfactory:

- Accuracy: 100%
- Precision: 100%
- Recall: 100%

However, we admit that 8 is too small a sample size to be statistically
representative. If you encounter any false positives or false negatives, please
don't hesitate to file an issue
[here](https://github.com/jsh9/pydoclint/issues).

## 3. Can I turn this off?

Actually, this style mismatch detection feature is by default _off_.

You can turn this feature on by setting `--check-style-mismatch` (or `-csm`) to
`True` (or `--check-style-mismatch=True`).

## 4. Is it much slower to parse a docstring with the heuristics?

No. The new detection flow usually parses at most one style per docstring, but
even when we fall back to the configured style the cost is still negligible.
For reference, benchmarking large code bases (as of 2025/01/12) shows the
overhead of style detection is only a few percent:

|                              | numpy | scikit-learn | Bokeh | Airflow |
| ---------------------------- | ----- | ------------ | ----- | ------- |
| Number of .py files          | 581   | 929          | 1196  | 5004    |
| Run time with 1 style [sec]  | 1.84  | 2.68         | 0.77  | 5.50    |
| Run time with 3 styles [sec] | 1.91  | 2.79         | 0.78  | 5.77    |
| Additional run time [sec]    | 0.07  | 0.11         | 0.01  | 0.07    |
| Relative additional run time | 4%    | 4%           | 1%    | 5%      |

## 5. What violation code is associated with style mismatch?

`DOC003`: "Docstring style mismatch".

## 6. How to fix this violation code?

You are suggested to check if the docstring style is consistent with what you
specified via the `--style` config option. If not, please rewrite your
docstring, or specify the correct style via `--style`.

Also, please note that specifying an incorrect docstring style may mask other
violations. So after you fix the docstring style, you may need to fix other
"new" (previously hidden) violations.
