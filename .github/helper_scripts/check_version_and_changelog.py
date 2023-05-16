import json
import re
import sys

import requests  # type:ignore

try:
    from packaging.version import Version, parse
except ImportError:
    from pip._vendor.packaging.version import Version, parse  # type:ignore


PATTERN = re.compile(r'\[(.*?)\]')
VER_PAT = re.compile(r'^\d\.\d\.\d$')

URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_latest_version_from_PyPI(
        package: str,
        url_pattern: str = URL_PATTERN,
) -> Version:
    """Return version of package on pypi.python.org using json."""
    req = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)

    return version


def should_fail_version_check(
        mode: str,
        local_latest_ver: Version,
        pypi_latest_ver: Version,
) -> bool:
    if mode == 'branch':
        return local_latest_ver < pypi_latest_ver

    if mode == 'main':
        return local_latest_ver <= pypi_latest_ver

    raise RuntimeError('Internal error; please contact the authors')


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else 'branch'

    with open('CHANGELOG.md') as fp:
        lines = fp.readlines()

    if len(lines) == 0:
        print('Empty CHANGELOG.md file')
        return 1

    print('Contents of CHANGELOG.md (up to the latest local version):\n')
    if lines[0] != '# Change Log\n':
        print(f'Unexpected first line in CHANGELOG.md: {lines[0]}')
        return 1

    for line in lines[1:]:
        print(line.rstrip())
        if line.startswith('##'):
            if line == '## [Unreleased]\n':
                continue

            match = PATTERN.search(line)
            version = match.group(1)  # type:ignore
            if not VER_PAT.match(version):
                print(f'Invalid version: {version}')
                return 1

            break

    latest_version_on_PyPI = get_latest_version_from_PyPI('pydoclint')

    if should_fail_version_check(mode, parse(version), latest_version_on_PyPI):
        print(
            f'Newest local version ({version}) must be higher than the'
            f' latest version on PyPI ({latest_version_on_PyPI})'
        )
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
