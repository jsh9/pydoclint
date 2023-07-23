"""Copy `README.md` into `docs/index.md` at every pre-commit runs"""

with open('README.md', encoding='UTF-8') as fp:
    lines = fp.readlines()

with open('docs/index.md', 'w', encoding='UTF-8') as fp:
    fp.writelines(lines)
