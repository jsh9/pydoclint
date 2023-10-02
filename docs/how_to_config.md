# How to configure _pydoclint_

Here is how to configure _pydoclint_.

For detailed explanations of all options, please read this page:
[Configuration options of _pydoclint_](https://jsh9.github.io/pydoclint/config_options.html).

## 1. Specifying options inline

- Native:

  ```bash
  pydoclint --check-arg-order=False <FILE_OR_FOLDER_PATH>
  ```

- Flake8:

  ```bash
  flake8 --check-arg-order=False <FILE_OR_FOLDER_PATH>
  ```

## 2. Specifying options in a configuration file

- Native:

  - In a `.toml` file somewhere in your project folder, add a section like this
    (put in the config that you need):

    ```toml
    [tool.pydoclint]
    style = 'google'
    exclude = '\.git|\.tox|tests/data|some_script\.py'
    require-return-section-when-returning-nothing = true
    ```

  - Then, specify the path of the `.toml` file in your command:

    ```bash
    pydoclint --config=path/to/my/config.toml <FILE_OR_FOLDER_PATH>
    ```

  - Note: the default value for `--config` option is `pyproject.toml` (in the
    root directory of your project) if you do not specify the config file name.

- Flake8:
  - In your flake8 config file (see
    [flake8's official doc](https://flake8.pycqa.org/en/latest/user/configuration.html#configuration-locations)),
    add the config you need under the section `[flake8]`
