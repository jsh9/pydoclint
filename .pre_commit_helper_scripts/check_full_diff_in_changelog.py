import sys

from markdown_it import MarkdownIt


def parseChangelog(filePath: str) -> tuple[bool, list[str]]:
    """
    Parses the changelog file and ensures each version section has "Full diff".

    Parameters
    ----------
    filePath : str
        Path to the CHANGELOG.md file.

    Returns
    -------
    bool
        True if all sections include a "Full diff", False otherwise.
    list[str]
        A list of version headers missing the "Full diff" section.
    """
    with open(filePath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the Markdown content
    md = MarkdownIt()
    tokens = md.parse(content)

    versionHeaders = []
    missingFullDiff = []

    # Iterate through parsed tokens to find version sections
    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and token.tag == 'h2':
            # Extract version header text
            header = tokens[i + 1].content
            if header.startswith('[') and ' - ' in header:
                versionHeaders.append((header, i))

    # Check each version section for "Full diff"
    for idx, (header, startIdx) in enumerate(versionHeaders):
        if header.startswith('[0.0.1]'):
            # The initial version shouldn't have a "Full diff" section.
            continue

        endIdx = (
            versionHeaders[idx + 1][1]
            if idx + 1 < len(versionHeaders)
            else len(tokens)
        )
        sectionTokens = tokens[startIdx:endIdx]

        # Check for "Full diff" in section content
        if not any(
            token.type == 'inline' and 'Full diff' in token.content
            for token in sectionTokens
        ):
            missingFullDiff.append(header)

    return len(missingFullDiff) == 0, missingFullDiff


if __name__ == '__main__':
    filePath = 'CHANGELOG.md'
    isValid, missingSections = parseChangelog(filePath)

    if isValid:
        print("All sections include a 'Full diff' section.")
        sys.exit(0)

    print("The following sections are missing a 'Full diff':")
    for section in missingSections:
        print(section)

    sys.exit(1)
