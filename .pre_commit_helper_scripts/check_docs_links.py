"""
Check that the documentation has no orphan pages and no broken links.

This script checks that:

1. Every page in ``docs/`` (except ``index.md``) is linked from ``README.md``
2. Every link to the documentation site (``https://jsh9.github.io/pydoclint``)
   in ``README.md``, ``docs/``, and the ``pydoclint`` package points to an
   existing page and an existing anchor
3. Every in-page link (such as ``[text](#anchor)``) in a Markdown file points
   to an existing anchor
4. Every page is listed in ``docs/llms.txt``
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SITE_URL_PATTERN = re.compile(
    r'https?://jsh9\.github\.io/pydoclint'
    r'(?P<path>/[\w./-]*)?(?:#(?P<fragment>[\w-]+))?'
)
MARKDOWN_LINK_PATTERN = re.compile(r'\]\((?P<target>[^)\s]+)\)')
EXPLICIT_ANCHOR_PATTERN = re.compile(r'<a\s+(?:id|name)="(?P<anchor>[^"]+)"')
HEADING_PATTERN = re.compile(r'^#{1,6}\s+(?P<text>.+?)\s*$')
FENCE_PATTERN = re.compile(r'^\s*(```|~~~)')


@dataclass(frozen=True)
class Reference:
    """A link found in a source file, with where it was found."""

    location: str
    target: str


def slugifyHeading(text: str) -> str:
    """
    Convert a Markdown heading into a GitHub-style anchor.

    Parameters
    ----------
    text : str
        The heading text, without the leading ``#`` characters.

    Returns
    -------
    str
        The anchor, such as ``28---baseline`` for ``28. `--baseline```.
    """
    text = re.sub(r'<[^>]+>', '', text)  # HTML tags
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)  # links, images
    plainParts: list[str] = []
    for index, part in enumerate(text.split('`')):
        if index % 2 == 1:  # inside a code span: keep the content as is
            plainParts.append(part)
        else:  # outside code spans: drop emphasis markers
            part = part.replace('*', '')
            part = re.sub(r'(?<!\w)_+|_+(?!\w)', '', part)
            plainParts.append(part)

    slug = ''.join(plainParts).strip().lower()
    slug = re.sub(r'[^\w\- ]', '', slug)
    return slug.replace(' ', '-')


def iterNonFencedLines(text: str) -> list[tuple[int, str]]:
    """
    List the lines of a Markdown file that are outside fenced code blocks.

    Parameters
    ----------
    text : str
        The content of the Markdown file.

    Returns
    -------
    list[tuple[int, str]]
        The 1-based line numbers and contents of the lines.
    """
    lines: list[tuple[int, str]] = []
    inFence = False
    for lineNum, line in enumerate(text.splitlines(), start=1):
        if FENCE_PATTERN.match(line):
            inFence = not inFence
            continue

        if not inFence:
            lines.append((lineNum, line))

    return lines


def collectAnchors(markdownFile: Path) -> set[str]:
    """
    Collect all anchors that a Markdown file defines.

    Parameters
    ----------
    markdownFile : Path
        The Markdown file.

    Returns
    -------
    set[str]
        The anchors generated from headings, plus explicit anchors such as ``<a
        id="baseline"></a>``.
    """
    anchors: set[str] = set()
    slugCounts: dict[str, int] = {}
    text = markdownFile.read_text(encoding='UTF-8')
    for _, line in iterNonFencedLines(text):
        headingMatch = HEADING_PATTERN.match(line)
        if headingMatch:
            slug = slugifyHeading(headingMatch.group('text'))
            count = slugCounts.get(slug, 0)
            anchors.add(slug if count == 0 else f'{slug}-{count}')
            slugCounts[slug] = count + 1

        for anchorMatch in EXPLICIT_ANCHOR_PATTERN.finditer(line):
            anchors.add(anchorMatch.group('anchor'))

    return anchors


def collectMarkdownReferences(
        markdownFile: Path,
        root: Path,
) -> list[Reference]:
    """
    Collect site URLs and in-page links from a Markdown or text file.

    Parameters
    ----------
    markdownFile : Path
        The Markdown (or plain text) file.
    root : Path
        The repository root, used to display relative file paths.

    Returns
    -------
    list[Reference]
        The links found in the file. In-page links start with ``#``.
    """
    references: list[Reference] = []
    relativePath = markdownFile.relative_to(root)
    text = markdownFile.read_text(encoding='UTF-8')
    for lineNum, line in iterNonFencedLines(text):
        location = f'{relativePath}:{lineNum}'
        for urlMatch in SITE_URL_PATTERN.finditer(line):
            references.append(Reference(location, urlMatch.group(0)))

        for linkMatch in MARKDOWN_LINK_PATTERN.finditer(line):
            target = linkMatch.group('target')
            if target.startswith('#'):
                references.append(Reference(location, target))

    return references


def collectPythonReferences(pythonFile: Path, root: Path) -> list[Reference]:
    """
    Collect site URLs from the string literals of a Python file.

    Parameters
    ----------
    pythonFile : Path
        The Python file.
    root : Path
        The repository root, used to display relative file paths.

    Returns
    -------
    list[Reference]
        The site URLs found in the file. Implicitly concatenated string
        literals are joined by the parser, so URLs split across several
        literals are found too.
    """
    references: list[Reference] = []
    relativePath = pythonFile.relative_to(root)
    tree = ast.parse(pythonFile.read_text(encoding='UTF-8'))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for urlMatch in SITE_URL_PATTERN.finditer(node.value):
                references.append(
                    Reference(
                        f'{relativePath}:{node.lineno}', urlMatch.group(0)
                    )
                )

    return references


def resolveSiteUrl(url: str, docsDir: Path) -> tuple[Path, str | None]:
    """
    Map a documentation site URL to its source file and anchor.

    Parameters
    ----------
    url : str
        The URL, such as
        ``https://jsh9.github.io/pydoclint/config_options.html#baseline``.
    docsDir : Path
        The ``docs/`` folder.

    Returns
    -------
    tuple[Path, str | None]
        The source file (which may not exist) and the anchor (if any).
    """
    urlMatch = SITE_URL_PATTERN.fullmatch(url)
    assert urlMatch is not None
    name = (urlMatch.group('path') or '').strip('/').rstrip('.')
    if name in {'', 'index.html'}:
        sourceFile = docsDir / 'index.md'
    elif name.endswith('.html'):
        sourceFile = docsDir / f'{name.removesuffix(".html")}.md'
    else:
        sourceFile = docsDir / name

    return sourceFile, urlMatch.group('fragment')


def checkDocs(root: Path) -> list[str]:
    """
    Check the documentation for orphan pages and broken links.

    Parameters
    ----------
    root : Path
        The repository root.

    Returns
    -------
    list[str]
        The problems found. An empty list means that everything is fine.
    """
    docsDir = root / 'docs'
    readme = root / 'README.md'
    llmsTxt = docsDir / 'llms.txt'
    pages = sorted(p for p in docsDir.glob('*.md') if p.name != 'index.md')
    problems: list[str] = []
    anchorCache: dict[Path, set[str]] = {}

    def getAnchors(markdownFile: Path) -> set[str]:
        if markdownFile not in anchorCache:
            anchorCache[markdownFile] = collectAnchors(markdownFile)

        return anchorCache[markdownFile]

    markdownSources = [readme, *sorted(docsDir.glob('*.md'))]
    referencesBySource: dict[Path, list[Reference]] = {
        source: collectMarkdownReferences(source, root)
        for source in markdownSources
    }
    if llmsTxt.exists():
        referencesBySource[llmsTxt] = collectMarkdownReferences(llmsTxt, root)
    else:
        problems.append('docs/llms.txt: file not found')

    for pythonFile in sorted((root / 'pydoclint').rglob('*.py')):
        referencesBySource[pythonFile] = collectPythonReferences(
            pythonFile, root
        )

    linkedPagesBySource: dict[Path, set[Path]] = {}
    for source, references in referencesBySource.items():
        linkedPages = linkedPagesBySource.setdefault(source, set())
        for reference in references:
            if reference.target.startswith('#'):  # in-page link
                if reference.target[1:] not in getAnchors(source):
                    problems.append(
                        f'{reference.location}: anchor not found:'
                        f' {reference.target}'
                    )

                continue

            sourceFile, fragment = resolveSiteUrl(reference.target, docsDir)
            if not sourceFile.exists():
                problems.append(
                    f'{reference.location}: page not found: {reference.target}'
                )
                continue

            linkedPages.add(sourceFile)
            if (
                fragment is not None
                and sourceFile.suffix == '.md'
                and fragment not in getAnchors(sourceFile)
            ):
                problems.append(
                    f'{reference.location}: anchor not found:'
                    f' {reference.target}'
                )

    for page in pages:
        if page not in linkedPagesBySource[readme]:
            problems.append(
                f'README.md: orphan page (not linked from README.md):'
                f' docs/{page.name}'
            )

        if llmsTxt.exists() and page not in linkedPagesBySource[llmsTxt]:
            problems.append(
                f'docs/llms.txt: page not listed: docs/{page.name}'
            )

    return problems


def main(argv: list[str] | None = None) -> int:
    """
    Run the checks and print the problems found.

    Parameters
    ----------
    argv : list[str] | None, default=None
        The command line arguments. If ``None``, use ``sys.argv[1:]``.

    Returns
    -------
    int
        The exit code: 0 if no problems are found, 1 otherwise.
    """
    parser = argparse.ArgumentParser(
        description='Check the docs for orphan pages and broken links.'
    )
    parser.add_argument(
        '--root',
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help='The repository root (default: the root of this repository)',
    )
    args = parser.parse_args(argv)
    problems = checkDocs(args.root.resolve())
    for problem in problems:
        print(problem)

    if problems:
        print(f'\nFound {len(problems)} documentation link problem(s).')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
