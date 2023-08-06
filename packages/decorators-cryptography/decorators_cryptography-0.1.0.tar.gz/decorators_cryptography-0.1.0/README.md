# decorators-cryptography

decorators-cryptography is a Python library that provides decorators for encrypting and decrypting passed arguments using the cryptography package.

### Contents:

---

1. [Installing Poetry and running the virtual environment](installing-poetry-and-running-the-virtual-environment)
    1. [Install Poetry](#install-poetry)
    2. [Start virtual environment](#start-virtual-environment)
2. [Install pre-commit hooks](#install-pre-commit-hooks)
    1. [Install pre-commit](#install-pre-commit)
    2. [Install pre-commit hooks](#install-hooks)
3. [Example Usage](example-usage)

## Installing Poetry and running the virtual environment

ℹ️ [Poetry Documentation](https://python-poetry.org/docs/#installation)

### Install Poetry

For Linux, macOS, Windows (WSL):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
For Windows (Powershell):
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

On macOS and Windows, the installation script will prompt you to add the Poetry executable folder to the PATH variable. Do this by running the following command (don't forget to change {USERNAME} to your username):

macOS
```bash
export PATH="/Users/{USERNAME}/.local/bin:$PATH"
```
Windows
```bash
$Env:Path += ";C:\Users\{USERNAME}\AppData\Roaming\Python\Scripts"; setx PATH "$Env:Path"
```

Check installation:
```bash
poetry --version
```

Installing bash completions (optional):
```bash
poetry completions bash >> ~/.bash_completion
```

### Start virtual environment

🔖 [Setting up the Poetry environment for PyCharm](https://www.jetbrains.com/help/pycharm/poetry.html)

Creating a virtual environment:
```bash
poetry env use python3.10
```

Installing dependencies:
```bash
poetry install
```

Launching the shell and activating the virtual environment (from the project folder):
```bash
poetry shell
```

Checking virtual environment activation:
```bash
poetry env list
```

[:arrow_up: Contents](#contents)

---

## Install pre-commit hooks

In order for pre-commit checks to be performed with each commit, you must:
- [Install pre-commit](#install-pre-commit)
- [Install pre-commit hooks](#install-hooks)

### Install pre-commit

The pre-commit module has already been added to the requirements and should be installed automatically with the virtual environment.

You can check the presence of pre-commit with the command (with the virtual environment activated):
```bash
pre-commit --version
# >> pre-commit 2.21.0
```

If this does not happen, then you need to [install pre-commit according to the official instructions](https://pre-commit.com/#install):
* install via brew package manager: `brew install pre-commit`
* installation via poetry: `poetry add pre-commit`
* pip install: `pip install pre-commit`

[:arrow_up: Contents](#contents)

___

### Install hooks

Installing hooks:
```bash
pre-commit install --all
```

In the future, when executing the `git commit` command, the checks listed in the `.pre-commit-config.yaml` file will be performed.

If it is not clear which error is preventing the commit from being executed, you can run the hooks manually with the command:
```bash
pre-commit run --all-files
```

[:arrow_up: Contents](#contents)

___


## Example Usage

To use the decorators provided by decorators-cryptography, follow the examples below.

```python
from decorators_cryptography import encrypt, decrypt

@encrypt(key="encryption_key")
def sensitive_function(arg1, arg2):
    # Your function implementation
    pass

@decrypt(key="decryption_key")
def sensitive_function(arg1, arg2):
    # Your function implementation
    pass
```

[:arrow_up: Contents](#contents)

___
