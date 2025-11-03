from textwrap import dedent

import pytest

from pydoclint.utils.noqa import collectNoqaCodesByLine, parseNoqaComment


@pytest.mark.parametrize(
    ('comment', 'expected'),
    [
        (
            '# explanation noqa: doc101, DOC202, f401 trailing',
            {'DOC101', 'DOC202'},
        ),
        (
            '# NOQA: DOC105',
            {'DOC105'},
        ),
        (
            '# comment before NOQA : DOC301 extra DOC302',
            {'DOC301', 'DOC302'},
        ),
        (
            '# noqa: F401, W503',
            set(),
        ),
        (
            '# noqa DOC101',
            set(),
        ),
        (
            '# nothing interesting here',
            set(),
        ),
    ],
)
def testParseNoqaComment(comment: str, expected: set[str]) -> None:
    assert parseNoqaComment(comment) == expected


@pytest.mark.parametrize(
    ('src', 'expected'),
    [
        (
            dedent(
                """
                def funcOne():
                    pass  # noqa: DOC101
                def funcTwo():
                    pass  # comment noqa: doc202 extra
                """
            ).strip(),
            {
                2: {'DOC101'},
                4: {'DOC202'},
            },
        ),
        (
            dedent(
                """
                def funcOne():  # NOQA: DOC101, DOC102
                    pass
                def funcTwo():
                    pass  # random text NOQA: DOC201 doc202 trailing
                """
            ).strip(),
            {
                1: {'DOC101', 'DOC102'},
                4: {'DOC201', 'DOC202'},
            },
        ),
    ],
)
def testCollectNoqaCodesByLine(
        src: str, expected: dict[int, set[str]]
) -> None:
    assert collectNoqaCodesByLine(src) == expected
