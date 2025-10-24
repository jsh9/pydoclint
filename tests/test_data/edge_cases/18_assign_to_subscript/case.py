# This comes from the pip repository:
# https://github.com/pypa/pip/blob/3b91f42e461de3f23e9bed46a8c5695435f930fb/src/pip/_internal/cli/cmdoptions.py#L110-L114
# and it was encountered by a user in https://github.com/jsh9/pydoclint/issues/190
#
# It's just supposed to pass without bugs and violations.
# (The previous buggy implementation would raise EdgeCaseError when parsing
# this code.)


class PipOption(Option):
    TYPES = Option.TYPES + ('path', 'package_name')
    TYPE_CHECKER = Option.TYPE_CHECKER.copy()
    TYPE_CHECKER['package_name'] = _package_name_option_check
    TYPE_CHECKER['path'] = _path_option_check
